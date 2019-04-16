# -*- encoding: utf-8 -*-
# Copyright (C) 2018 Nguyen Duc Tam <nguyenductamlhp@gmail.com>

from odoo import fields, models, api, _


class WebsiteSupportTicketStage(models.Model):
    _name = 'website.support.ticket.stage'

    name = fields.Char(
        string='Name', required=True, readonly=False, help='Name of Stage')
    sequence = fields.Char(
        string='Sequence', required=False, readonly=False)
