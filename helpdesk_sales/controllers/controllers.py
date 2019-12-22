# -*- coding: utf-8 -*-
from odoo import http

# class HelpdeskSales(http.Controller):
#     @http.route('/helpdesk_sales/helpdesk_sales/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/helpdesk_sales/helpdesk_sales/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('helpdesk_sales.listing', {
#             'root': '/helpdesk_sales/helpdesk_sales',
#             'objects': http.request.env['helpdesk_sales.helpdesk_sales'].search([]),
#         })

#     @http.route('/helpdesk_sales/helpdesk_sales/objects/<model("helpdesk_sales.helpdesk_sales"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('helpdesk_sales.object', {
#             'object': obj
#         })