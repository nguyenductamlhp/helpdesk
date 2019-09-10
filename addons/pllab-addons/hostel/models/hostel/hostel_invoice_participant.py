
# -*- encoding: utf-8 -*-
# Copyright (C) 2018 Nguyen Duc Tam <nguyenductamlhp@gmail.com>

from odoo import fields, models, api, _


class HostelInvoiceParticipant(models.Model):
    _name = 'hostel.invoice.participant'

    invoice_id = fields.Many2one(
        'hostel.invoice', string='Invoice', required=True, help='Invoice')
    partner_id = fields.Many2one(
        'res.partner', string='Partner', required=True)
    start = fields.Date(
        string='Start', required=True, help='Start',
        default=lambda self: self.invoice_id and self.invoice_id.date_from)
    end = fields.Date(
        string='End', required=True, help='End',
        default=lambda self: self.invoice_id and self.invoice_id.date_to)
    responsible_ids = fields.Many2many(
        'res.partner', string="Responsible",
        related='invoice_id.responsible_ids')
