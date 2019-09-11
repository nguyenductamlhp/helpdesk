# -*- encoding: utf-8 -*-
# Copyright (C) 2018 Nguyen Duc Tam <nguyenductamlhp@gmail.com>

from datetime import datetime, timedelta
import time

from odoo import api, fields, models
from odoo.exceptions import Warning
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT


class HostelInvoice(models.Model):
    _name = 'hostel.invoice'

    name = fields.Char('Reference', compute='_compute_invoice_name')
    room_id = fields.Many2one('hostel.room', 'Room', required=True)
    date_from = fields.Date(
        'Form', required=True, default=lambda *a: time.strftime('%Y-%m-01'))
    date_to = fields.Date('To', required=True)
    invoice_date = fields.Date('Invoice Date')
    invoice_expense_ids = fields.One2many('hostel.invoice.expense', 'invoice_id', 'Invoice Expenses')
    participant_ids = fields.One2many('hostel.invoice.participant', 'invoice_id', 'Participants')
    payment_ids = fields.One2many('hostel.invoice.payment', 'invoice_id', 'Payments')
    total_days = fields.Integer(
        'Total Days', compute='compute_total_days', store=True)

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
            for line in invoice.invoice_expense_ids:
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

    def get_participants(self, day):
        """
        Return participants of invoice on date
        """
        self.ensure_one()
        Participant = self.env['hostel.invoice.participant']
        day = str(day)
        process_date = datetime.strptime(day, DEFAULT_SERVER_DATET_FORMAT)
        participants = Participant.search([
            ('invoice_id', '=', self.id),
            ('start', '<=', process_date),
            ('end', '>=', process_date)])
        return participants

    # def compute_participant_data(self):
    #     self.ensure_one()
    #     data = {}
    #     start = datetime.strptime(self.date_from, DEFAULT_SERVER_DATE_FORMAT)
    #     end = datetime.strptime(self.date_to, DEFAULT_SERVER_DATE_FORMAT)
    #     delta = (end - start).days + 1
    #     for day in range(delta):
    #         process_date = start + timedelta(days=day)
    #         participants = self.get_participants(process_date)
    #         data[process_date] =

    @api.depends('date_from', 'date_to')
    def compute_total_days(self):
        for rec in self:
            start = datetime.strptime(rec.date_from, DEFAULT_SERVER_DATE_FORMAT)
            end = datetime.strptime(rec.date_to, DEFAULT_SERVER_DATE_FORMAT)
            rec.total_days = (end - start).days + 1