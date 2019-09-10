# -*- encoding: utf-8 -*-
# Copyright (C) 2018 Nguyen Duc Tam <nguyenductamlhp@gmail.com>

from datetime import datetime
import time

from odoo import api, fields, models
from odoo.exceptions import Warning


class HostelInvoice(models.Model):
    _name = 'hostel.invoice'

    name = fields.Char('Reference', compute='_compute_invoice_name')
    room_id = fields.Many2one('hostel.room', 'Room', required=True)
    date_from = fields.Date(
        'Form', required=True, default=lambda *a: time.strftime('%Y-%m-01'))
    date_to = fields.Date('To', required=True)
    invoice_date = fields.Date('Invoice Date')
    invoice_line_ids = fields.One2many('hostel.invoice.line', 'invoice_id', 'Invoice Lines')
    participant_ids = fields.One2many('hostel.invoice.participant', 'invoice_id', 'Participants')
    payment_ids = fields.One2many('hostel.invoice.payment', 'invoice_id', 'Payments')

    responsible_ids = fields.Many2many('res.partner', string="Responsible")
    state = fields.Selection(
        [
            ('draft', 'Draft'),
            ('confirm', 'Confirm'),
            ('validate', 'Validate'),
            ('cancel', 'Cancel')
        ],
        string='State',
        default='draft',
        required=True)

    @api.onchange('room_id')
    def onchange_reponsible(self):
        if not self.room_id:
            return
        self.responsible_ids = self.room_id and self.room_id.member_ids

    @api.depends('room_id', 'invoice_date')
    def _compute_invoice_name(self):
        for rec in self:
            if not all([rec.room_id, rec.date_from, rec.date_to]):
                continue
            rec.name = '%s (%s - %s)' % (
                rec.room_id.name, rec.date_from, rec.date_to)

    @api.multi
    def generate_payment(self):
        """
        Generate related payment. One partn er one payment
        """
        payment_env = self.env['hostel.invoice.payment']

        for invoice in self:
            for partner in invoice.responsible_ids:
                payment_vals = {
                    'invoice_id': invoice.id,
                    'partner_id': partner.id
                }
                payment = payment_env.create(payment_vals)

    @api.multi
    def action_confirm(self):
        """Chnage state to confirm and generate payment (lines)
        """
        for invoice in self:
            invoice.generate_payment()
            for line in invoice.invoice_line_ids:
                line.generate_payment_line()
            invoice.state = 'confirm'

    @api.multi
    def reset_to_draft(self):
        for invoice in self:
            for payment in invoice.payment_ids:
                payment.unlink()
            invoice.state = 'draft'

    @api.multi
    def action_validate(self):
        """Change state to validate
        """
        for invoice in self:
            invoice.state = 'validate'
