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
    partner_id = fields.Many2one('res.partner', 'Partner')
    total = fields.Float('Total to Pay')
    paid = fields.Float('Paid')
    remain = fields.Float('Remain', compute='compute_remain_amount')

    @api.depends('total', 'paid')
    def compute_remain_amount(self):
        for payment in self:
            payment.remain = payment.total - payment.paid
