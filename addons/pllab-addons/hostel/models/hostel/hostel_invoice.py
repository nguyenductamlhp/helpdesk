# -*- encoding: utf-8 -*-
# Copyright (C) 2018 Nguyen Duc Tam <nguyenductamlhp@gmail.com>

from datetime import datetime, timedelta
import time

from odoo import api, fields, models
from odoo.exceptions import Warning
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT


class HostelInvoice(models.Model):
    _name = 'hostel.invoice'

    name = fields.Char('Reference', compute='_compute_invoice_name')
    room_id = fields.Many2one('hostel.room', 'Room', required=True)
    date_from = fields.Date(
        'From', required=True, default=lambda *a: time.strftime('%Y-%m-01'))
    date_to = fields.Date('To', required=True)
    invoice_date = fields.Date('Invoice Date')
    invoice_expense_ids = fields.One2many(
        'hostel.invoice.expense', 'invoice_id', 'Invoice Expenses',
        track_visibility='onchange' )
    participant_ids = fields.One2many(
        'hostel.invoice.participant', 'invoice_id', 'Participants',
        track_visibility='onchange')
    payment_ids = fields.One2many(
        'hostel.invoice.payment', 'invoice_id', 'Payments',
        track_visibility='onchange' )
    total_days = fields.Integer(
        'Total Days', compute='compute_total_days', store=True)
    total_factor = fields.Float(
        compute='compute_total_factor', store=True)

    responsible_ids = fields.Many2many('res.partner', string="Responsible")
    state = fields.Selection(
        [
            ('draft', 'Draft'),
            ('validate', 'Validate'),
            ('done', 'Done'),
            ('cancel', 'Cancel')
        ],
        string='State',
        default='draft',
        required=True,
        track_visibility='onchange')

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

    @api.depends('participant_ids', 'participant_ids.factor')
    def compute_total_factor(self):
        for rec in self:
            rec.total_factor = sum([p.factor for p in rec.participant_ids])

    @api.multi
    def generate_payment(self):
        """
        Generate related payment. One partn er one payment
        """
        payment_env = self.env['hostel.invoice.payment']
        expense_env = self.env['hostel.invoice.expense']
        expense_item_env = self.env['hostel.invoice.expense.item']

        for invoice in self:
            invoice.payment_ids.unlink()
            for partner in invoice.responsible_ids:
                expense_items = expense_item_env.search([
                    ('invoice_id', '=', invoice.id),
                    ('owner_id', '=', partner.id)])
                expenses = expense_env.search([
                    ('invoice_id', '=', invoice.id),
                    ('owner_id', '=', partner.id)])

                payment_vals = {
                    'invoice_id': invoice.id,
                    'partner_id': partner.id,
                    'total': sum([item.amount for item in expense_items]),
                    'paid': sum([expense.total for expense in expenses]),
                }
                payment = payment_env.create(payment_vals)

    @api.multi
    def action_allocate_expense(self):
        ExpenseItem = self.env['hostel.invoice.expense.item']
        for invoice in self:
            for expense in invoice.invoice_expense_ids:
                expense.item_ids.unlink()

                sum_factor = expense.sum_factor
                for part in expense.responsible_ids:
                    rate = part.factor / sum_factor
                    ExpenseItem.create({
                        'expense_id': expense.id,
                        'owner_id': part.partner_id.id,
                        'amount': rate * expense.total
                    })

    @api.multi
    def action_cancel(self):
        """Chnage state to confirm and generate payment (lines)
        """
        for invoice in self:
            invoice.state = 'cancel'

    @api.multi
    def reset_to_draft(self):
        for invoice in self:
            invoice.state = 'draft'

    @api.multi
    def action_done(self):
        for invoice in self:
            invoice.state = 'done'

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
        process_date = datetime.strptime(day, DEFAULT_SERVER_DATETIME_FORMAT).date()
        participants = Participant.search([
            ('invoice_id', '=', self.id),
            ('start', '<=', process_date),
            ('end', '>=', process_date)])
        return participants.mapped('partner_id')

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