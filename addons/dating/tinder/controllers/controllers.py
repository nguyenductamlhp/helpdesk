# -*- coding: utf-8 -*-
from odoo import http

# class Tinder(http.Controller):
#     @http.route('/tinder/tinder/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/tinder/tinder/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('tinder.listing', {
#             'root': '/tinder/tinder',
#             'objects': http.request.env['tinder.tinder'].search([]),
#         })

#     @http.route('/tinder/tinder/objects/<model("tinder.tinder"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('tinder.object', {
#             'object': obj
#         })