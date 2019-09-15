
# -*- encoding: utf-8 -*-
# Copyright (C) 2018 Nguyen Duc Tam <nguyenductamlhp@gmail.com>
from datetime import datetime, timedelta

from odoo import fields, models, api, _
from odoo.exceptions import Warning
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT


class HostelInvoiceParticipant(models.Model):
    _name = 'hostel.invoice.participant'

    invoice_id = fields.Many2one(
        'hostel.invoice', string='Invoice', required=True, readonly=True)
    partner_id = fields.Many2one(
        'res.partner', string='Partner', required=True)
    start = fields.Date(
        string='Start', required=True, help='Start')
    end = fields.Date(
        string='End', required=True, help='End',
        default=lambda self: self.invoice_id and self.invoice_id.date_to)
    factor = fields.Float('Factor', compute='compute_factor', store=True)
    responsible_ids = fields.Many2many(
        'res.partner', string="Responsible",
        related='invoice_id.responsible_ids')

    @api.constrains('invoice_id', 'partner_id', 'start', 'end')
    def _constrains_not_duplicate_participant(self):
        Participant = self.env['hostel.invoice.participant']
        for rec in self:
            participants = Participant.search([
                ('id', '!=', self.id),
                ('invoice_id', '=', rec.id),
                '|',
                ('start', '>=', rec.end),
                ('end', '<=', rec.start)], limit=1)
            if participants:
                raise Warning('Can not overlap participant!')

    @api.depends('invoice_id', 'start', 'end')
    def compute_factor(self):
        for rec in self:
            if not all([rec.start, rec.end, rec.invoice_id]):
                continue
            start = datetime.strptime(rec.start, DEFAULT_SERVER_DATE_FORMAT)
            end = datetime.strptime(rec.end, DEFAULT_SERVER_DATE_FORMAT)
            delta = (end - start).days + 1
            rec.factor = delta / rec.invoice_id.total_days
