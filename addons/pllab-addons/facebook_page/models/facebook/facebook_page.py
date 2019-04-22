# -*- encoding: utf-8 -*-
# Copyright (C) 2018 Nguyen Duc Tam <nguyenductamlhp@gmail.com>

import urllib.request
from urllib.request import urlopen
from datetime import datetime
from github import Github

from odoo import api, fields, models
from odoo.exceptions import Warning


class FacebookPage(models.Model):
    _name = 'facebook.page'

    name = fields.Char('Page Name', required=True)
    page_id = fields.Char('Page ID', required=True)
    page_url = fields.Char(
        'Page Url', compute='compute_page_url')
    owner_id = fields.Many2one('res.partner', 'Owner')
    description = fields.Text('Description')
    active = fields.Boolean('Active', default=True)

    _sql_constraints = [
         ('unique_page_id', 'unique (page_id)','This page already existed!')]

    def compute_page_url(self):
        url = 'https://github.com/%s/%s/milestone/%s'
        for rec in self:
            rec.page_url = 'page_url'
