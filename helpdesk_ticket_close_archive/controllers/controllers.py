# -*- coding: utf-8 -*-
from odoo import http

# class HelpdeskTicketCloseArchive(http.Controller):
#     @http.route('/helpdesk_ticket_close_archive/helpdesk_ticket_close_archive/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/helpdesk_ticket_close_archive/helpdesk_ticket_close_archive/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('helpdesk_ticket_close_archive.listing', {
#             'root': '/helpdesk_ticket_close_archive/helpdesk_ticket_close_archive',
#             'objects': http.request.env['helpdesk_ticket_close_archive.helpdesk_ticket_close_archive'].search([]),
#         })

#     @http.route('/helpdesk_ticket_close_archive/helpdesk_ticket_close_archive/objects/<model("helpdesk_ticket_close_archive.helpdesk_ticket_close_archive"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('helpdesk_ticket_close_archive.object', {
#             'object': obj
#         })