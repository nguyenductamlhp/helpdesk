# -*- encoding: utf-8 -*-
# Copyright (C) 2018 Nguyen Duc Tam <nguyenductamlhp@gmail.com>

from odoo import fields, models, api, _


class WebsiteSupportTicketStage(models.Model):
    _name = 'website.support.ticket.stage'

    name = fields.Char(
        string='Name', required=True, readonly=False, help='Name of Stage')
    state_ids = fields.Many2one(
        string='States', required=False, readonly=False)
    sequence = fields.Char(
        string='Sequence', required=False, readonly=False)
