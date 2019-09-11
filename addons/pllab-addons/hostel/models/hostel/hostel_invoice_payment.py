# -*- encoding: utf-8 -*-
# Copyright (C) 2018 Nguyen Duc Tam <nguyenductamlhp@gmail.com>

from datetime import datetime

from odoo import api, fields, models
from odoo.exceptions import Warning


class HostelInvoicePayment(models.Model):
    _name = 'hostel.invoice.payment'

    name = fields.Char('Reference')
    invoice_id = fields.Many2one('hostel.invoice', 'Invoice', required=True)
    payment_date = fields.Date('Payment Date')
    # payment_line_ids = fields.One2many(
    #     'hostel.invoice.payment.line', 'payment_id', 'Payment Lines')
    partner_id = fields.Many2one('res.partner', 'Partner')
    state = fields.Selection(
        [
            ('open', 'Open'),
            ('paid', 'Paid')
        ],
        string='State',
        default='open')
    total = fields.Float('Total to Pay', compute='compute_payment_amount')
    paid = fields.Float('Paid', compute='compute_payment_amount')
    remain = fields.Float('Remain', compute='compute_payment_amount')

    # @api.depends('payment_line_ids', 'payment_line_ids.state',
    #     'payment_line_ids.amount')
    # def compute_payment_amount(self):
    #     for payment in self:
    #         paid = 0
    #         remain = 0
    #         for line in payment.payment_line_ids:
    #             if line.state == 'open':
    #                 remain += line.amount
    #             elif line.state == 'paid':
    #                 paid += line.amount
    #         payment.paid = paid
    #         payment.remain = remain
    #         payment.total = payment.paid + payment.remain
