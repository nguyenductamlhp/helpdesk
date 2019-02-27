# -*- coding: utf-8 -*-

import os
import errno
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from odoo import _, api, fields, models
from odoo.exceptions import Warning
from odoo.tools import safe_eval

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

def get_current_directory():
    return '/tmp/google_drives' + '/'

FOLDER_TYPE = 'application/vnd.google-apps.folder'
DEFAULT_SETTING_DIR = get_current_directory()

SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']


class GoogleDriveAccount(models.Model):
    _description = 'Google Drive'
    _name = 'google.drive.account'

    name = fields.Char("Drive Name", required=True)
    username = fields.Char("Username", required=True)

    url = fields.Char("URL")
    client_secrets = fields.Text("Client Secrets")
    token_path = fields.Char(
        string="Token Path", compute='compute_credentials_path', store=True)
    credential_path = fields.Char(
        string="Credential Path", compute='compute_credentials_path', store=True)
    credential = fields.Text("Credential")
    description = fields.Text("Description")
    file_ids = fields.One2many(
        'drive.file', 'drive_id', string="Files")
    max_query_file = fields.Integer("Max query", default=1000)

    @api.depends('username')
    @api.multi
    def compute_credentials_path(self):
        for drive in self:
            if not drive.username:
                continue
            drive.token_path = DEFAULT_SETTING_DIR + drive.username + '/token.pickle'
            drive.credential_path = DEFAULT_SETTING_DIR + drive.username + '/credentials.json'
            # create fiel
            os.makedirs(os.path.dirname(drive.token_path), exist_ok=True)
            os.makedirs(os.path.dirname(drive.credential_path), exist_ok=True)

    @api.constrains('credential')
    def generate_credential_file(self):
        for drive in self:
            if not drive.credential_path or not drive.credential:
                continue
            os.makedirs(os.path.dirname(drive.credential_path), exist_ok=True)
            with open(drive.credential_path, 'w') as file:
                file.write(drive.credential)

    @api.multi
    def get_credential(self):
        self.ensure_one()
        creds = None
        token_path = self.token_path
        credential_path = self.credential_path

        if os.path.exists(token_path):
            with open(token_path, 'rb') as token:
                creds = pickle.load(token)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if os.path.isfile(credential_path):
                    flow = InstalledAppFlow.from_client_secrets_file(
                        credential_path, SCOPES)
                    creds = flow.run_local_server()
                else:
                    creds = None
            # Save the credentials for the next run
            with open(token_path, 'wb') as token:
                pickle.dump(creds, token)
        return creds

    @api.multi
    def get_service(self):
        self.ensure_one()
        creds = self.get_credential()
        if creds:
            service = build('drive', 'v3', credentials=creds)
            return service
        return None

    @api.multi
    def sync_drive_files(self):
        file_env = self.env['drive.file']
        file_type_env = self.env['drive.file.type']
        for rec in self:
            service = rec.get_service()
            if not service:
                raise Warning("Authenticate fail for %s" % rec.name)
                continue
            # Call the Drive v3 API
            # mimeType='application/vnd.google-apps.folder'
            results = service.files().list(
                q="trashed=false",
                pageSize=rec.max_query_file,
                fields="nextPageToken, files(id, name, parents, mimeType, description, webViewLink, webContentLink, shared)"
            ).execute()

            items = results.get('files', [])
            for item in items:
                mime_type = item.get('mimeType', None)
                file_type = file_type_env.get_file_type(mime_type)
                code = item.get('id', None)
                parent_code = item.get('parents', None)
                if not code:
                    continue
                file = file_env.get_file(code)
                if not file:
                    file_env.create({
                        'drive_id': rec.id,
                        'file_id': code,
                        'name': item.get('name', 'unknown'),
                        'parent_file_id': parent_code and parent_code[0] or None,
                        'description': item.get('description'),
                        'type_id': file_type and file_type.id or None,
                        'web_content_link': item.get('webContentLink'),
                        'web_view_link': item.get('webViewLink'),
                    })

    @api.multi
    def set_file_parents(self):
        for rec in self:
            if not rec.file_ids:
                continue
            rec.file_ids.set_parent()
