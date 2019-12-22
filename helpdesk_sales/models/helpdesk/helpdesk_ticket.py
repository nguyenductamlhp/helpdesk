# -*- coding: utf-8 -*-
from odoo import _, api, fields, models, tools


class HelpdeskTicket(models.Model):

    _inherit = 'helpdesk.ticket'

    estimation = fields.Float('Workload Estimation')
    sale_order_id = fields.Many2one('sale.order', "Sale Order")
