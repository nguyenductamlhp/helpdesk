
# -*- encoding: utf-8 -*-
# Copyright (C) 2018 Nguyen Duc Tam <nguyenductamlhp@gmail.com>

from odoo import fields, models, api, _


class HostelInvoiceParticipant(models.Model):
    _name = 'hostel.invoice.participant'

    def _get_default_start(self):
        if self.invoice_id:
            return self.invoice_id.date_from
        return None

    invoice_id = fields.Many2one(
        'hostel.invoice', string='Invoice', required=True, readonly=True)
    partner_id = fields.Many2one(
        'res.partner', string='Partner', required=True)
    start = fields.Date(
        string='Start', required=True, help='Start',
        default=lambda self: self._get_default_start())
    end = fields.Date(
        string='End', required=True, help='End',
        default=lambda self: self.invoice_id and self.invoice_id.date_to)
    responsible_ids = fields.Many2many(
        'res.partner', string="Responsible",
        related='invoice_id.responsible_ids')
