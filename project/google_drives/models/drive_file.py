# -*- coding: utf-8 -*-

from odoo import _, api, fields, models

# https://developers.google.com/drive/api/v3/reference/files


class DriveFile(models.Model):
    _description = 'Drive Files'
    _name = 'drive.file'

    name = fields.Char("Name", required=True)
    code = fields.Char("Code")
    file_id = fields.Char("File ID", required=True, readonly=True)
    is_dir = fields.Boolean("Is Directory", related='type_id.is_dir')
    drive_id = fields.Many2one('google.drive.account', 'Google Drive')
    parent_file_id = fields.Char("Parent File ID", readonly=True)
    parent_id = fields.Many2one(
        'drive.file', 'Parent', readonly=True, domain=[('is_dir', '=', True)])
    child_ids = fields.One2many(
        'drive.file', 'parent_id', string="Children Files")
    type_id = fields.Many2one('drive.file.type', 'Type')
    tag_ids = fields.Many2many(
        'drive.tag', 'file_tag_rel', 'file_id', 'tag_id', string="Tags")
    description = fields.Text("Description")

    shared = fields.Boolean("Shared?")
    web_content_link = fields.Char("Web Content Link")
    web_view_link = fields.Char("Web View Link")

    @api.model
    def create(self, vals):
        parent_file_id = vals.get('parent_file_id', None)
        if parent_file_id:
            parent = self.get_file(parent_file_id)
            if parent:
                vals['parent_id'] = parent.id
        res = super(DriveFile, self).create(vals)
        return res

    @api.model
    def get_file(self, code):
        if not code:
            return None
        file = self.search([('file_id', '=', code)], limit=1)
        return file or None

    @api.multi
    def get_parent(self):
        self.ensure_one()
        if not self.parent_file_id:
            return None
        parent = self.get_file(self.parent_file_id)
        return parent or None

    @api.multi
    def set_parent(self):
        for rec in self:
            parent = rec.get_parent()
            if not parent:
                continue
            rec.parent_id = parent.id
