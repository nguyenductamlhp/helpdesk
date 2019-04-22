# -*- encoding: utf-8 -*-
# Copyright (C) 2018 Nguyen Duc Tam <nguyenductamlhp@gmail.com>

from datetime import datetime

from odoo import api, fields, models
from odoo.exceptions import Warning


class HostelRoom(models.Model):
    _name = 'hostel.room'

    name = fields.Char('Hostel Name', required=True)
    address = fields.Char('Address', required=True)
    user_id = fields.Many2one('res.partner', 'Owner')
    member_ids = fields.Many2many('res.partner', string="Member")
    description = fields.Text('Description')
    active = fields.Boolean('Active', default=True)
