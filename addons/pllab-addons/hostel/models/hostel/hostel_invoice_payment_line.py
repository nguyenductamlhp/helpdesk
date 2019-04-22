# -*- encoding: utf-8 -*-
# Copyright (C) 2018 Nguyen Duc Tam <nguyenductamlhp@gmail.com>

from datetime import datetime

from odoo import api, fields, models
from odoo.exceptions import Warning


class HostelInvoicePaymentLine(models.Model):
    _name = 'hostel.invoice.payment.line'

    payment_id = fields.Many2one('hostel.invoice.payment', 'payment', required=True)
    invoice_line_id = fields.Many2one('hostel.invoice.line', 'Invoice Line')
    product_id = fields.Many2one('product.template', related='invoice_line_id.product_id')
    quantity = fields.Integer('Quantity', related='invoice_line_id.quantity')
    unit_price = fields.Float("Unit Price", related='invoice_line_id.unit_price')
    total = fields.Float("Unit Price", related='invoice_line_id.total')
    amount = fields.Float("Amount", compute='compute_amount', store=True)
    partner_id = fields.Many2one('res.partner', related='payment_id.partner_id')
    state = fields.Selection(
        [
            ('open', 'Open'),
            ('paid', 'Paid')
        ],
        string='State',
        default='open')

    @api.depends('invoice_line_id')
    def compute_amount(self):
        for line in self:
            if not line.invoice_line_id:
                continue
            total = line.invoice_line_id.total
            number = len(line.invoice_line_id.responsible_ids)
            line.amount = total / number
