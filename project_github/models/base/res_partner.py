# -*- encoding: utf-8 -*-
# Copyright (C) 2018 Nguyen Duc Tam <nguyenductamlhp@gmail.com>


from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    github_login = fields.Char('Github Username')
    github_password = fields.Char('Github Password')
