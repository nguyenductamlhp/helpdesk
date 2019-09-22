# -*- encoding: utf-8 -*-
# Copyright (C) 2018 Nguyen Duc Tam <nguyenductamlhp@gmail.com>

from datetime import datetime, timedelta

from odoo import api, fields, models
from odoo.exceptions import Warning
from odoo.exceptions import Warning
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT


class HostelInvoiceExpense(models.Model):
    _name = 'hostel.invoice.expense'

    def default_responsible(self):
        if self.invoice_id:
            import pdb; pdb.set_trace()
            return self.invoice_id.participant_ids
        return None

    invoice_id = fields.Many2one('hostel.invoice', 'Invoice', required=True)
    product_id = fields.Many2one('product.template', string="Product")
    quantity = fields.Integer('Quantity', default=1)
    unit_price = fields.Float("Unit Price")
    total = fields.Float("Total", compute='compute_total', store=True)
    owner_id = fields.Many2one('res.partner', 'Paid By')
    buy_date = fields.Date('Buy Date', default=datetime.now().date())
    note = fields.Text('Note')

    room_id = fields.Many2one('hostel.room', related="invoice_id.room_id")
    responsible_ids = fields.Many2many(
        'hostel.invoice.participant', string="Responsible", required=True,
        default=lambda self: self.default_responsible())
    sum_factor = fields.Float(
        'Sum factor', compute='compute_sum_factor')
    item_ids = fields.One2many('hostel.invoice.expense.item', 'expense_id')


    @api.onchange('invoice_id')
    def onchange_reponsible(self):
        self.responsible_ids = self.invoice_id and self.invoice_id.participant_ids

    @api.depends('quantity', 'unit_price')
    def compute_total(self):
        for line in self:
            line.total = line.quantity * line.unit_price

    @api.depends('responsible_ids', 'responsible_ids.factor')
    def compute_sum_factor(self):
        for rec in self:
            rec.sum_factor = sum([p.factor for p in rec.responsible_ids])

    @api.multi
    def generate_payment_line(self):
        """
        Generate related payment line
        """
        payment_line_env = self.env['hostel.invoice.payment.line']
        payment_env = self.env['hostel.invoice.payment']

        for line in self:
            npartners = len(line.responsible_ids)
            template_line_vals = {
                'invoice_line_id': line.id,
                'amount': line.total / npartners,
            }
            for partner in line.responsible_ids:
                payment = payment_env.search([
                    ('partner_id', '=', partner.id),
                    ('invoice_id', '=', line.invoice_id.id)
                ], limit=1)

                line_vals = template_line_vals.copy()
                line_vals.update({
                    'payment_id': payment.id
                })
                if partner == line.owner_id:
                    line_vals.update({
                        'state': 'paid'
                    })
                payment_line_env.create(line_vals)

    def compute_expense_granular(self):
        """
        Expense Granular
        """
        self.ensure_one()
        total = 0
        invoice = self.invoice_id
        start = datetime.strptime(invoice.date_from, DEFAULT_SERVER_DATE_FORMAT)
        end = datetime.strptime(invoice.date_to, DEFAULT_SERVER_DATE_FORMAT)
        delta = (end - start).days + 1
        for day in range(delta):
            process_date = start + timedelta(days=day)
            participants = self.get_participants(process_date)
            total += len(participants & self.responsible_ids)
        return total / delta

    # @api.multi
    # def compute_cost_granular(self):
    #     '''
    #     '''
    #     for rec in self:
    #         # foreacch day from start to end of month
    #         total = 0
    #         invoice = rec.invoice_id
    #         start = datetime.strptime(invoice.date_from, DEFAULT_SERVER_DATE_FORMAT)
    #         end = datetime.strptime(invoice.date_to, DEFAULT_SERVER_DATE_FORMAT)
    #         delta = (end - start).days + 1
    #         for day in range(delta):
    #             process_date = start + timedelta(days=day)
    #             participants = invoice.get_participants(process_date)
    #             total += len(participants & rec.responsible_ids)
    #         rec.cost_granular = rec.total / total
