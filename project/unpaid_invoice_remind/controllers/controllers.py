# -*- coding: utf-8 -*-
from odoo import http

# class UnpaidInvoiceRemind(http.Controller):
#     @http.route('/unpaid_invoice_remind/unpaid_invoice_remind/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/unpaid_invoice_remind/unpaid_invoice_remind/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('unpaid_invoice_remind.listing', {
#             'root': '/unpaid_invoice_remind/unpaid_invoice_remind',
#             'objects': http.request.env['unpaid_invoice_remind.unpaid_invoice_remind'].search([]),
#         })

#     @http.route('/unpaid_invoice_remind/unpaid_invoice_remind/objects/<model("unpaid_invoice_remind.unpaid_invoice_remind"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('unpaid_invoice_remind.object', {
#             'object': obj
#         })