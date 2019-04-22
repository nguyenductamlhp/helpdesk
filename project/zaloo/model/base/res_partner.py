# -*- encoding: utf-8 -*-
# Copyright (C) 2018 Nguyen Duc Tam <nguyenductamlhp@gmail.com>

from odoo import fields, models, api, _


class ResPartner(models.Model):
    _inherit = 'res.partner'

    zalo = fields.Char(string='Zalo')