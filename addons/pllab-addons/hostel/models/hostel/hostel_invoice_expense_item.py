# -*- encoding: utf-8 -*-
# Copyright (C) 2018 Nguyen Duc Tam <nguyenductamlhp@gmail.com>

from datetime import datetime

from odoo import api, fields, models
from odoo.exceptions import Warning


class HostelInvoiceExpenseItem(models.Model):
    _name = 'hostel.invoice.expense.item'

    expense_id = fields.Many2one('hostel.invoice.expense', 'Expense')
    invoice_id = fields.Many2one(
        'hostel.invoice', related='expense_id.invoice_id')
    room_id = fields.Many2one('hostel.room', related="invoice_id.room_id")
    product_id = fields.Many2one('product.template', related='expense_id.product_id')
    amount = fields.Float("Amount", )
    owner_id = fields.Many2one('res.partner', 'Owner')
