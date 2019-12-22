# -*- coding: utf-8 -*-
from odoo import http

# class HelpdeskProject(http.Controller):
#     @http.route('/helpdesk_project/helpdesk_project/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/helpdesk_project/helpdesk_project/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('helpdesk_project.listing', {
#             'root': '/helpdesk_project/helpdesk_project',
#             'objects': http.request.env['helpdesk_project.helpdesk_project'].search([]),
#         })

#     @http.route('/helpdesk_project/helpdesk_project/objects/<model("helpdesk_project.helpdesk_project"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('helpdesk_project.object', {
#             'object': obj
#         })