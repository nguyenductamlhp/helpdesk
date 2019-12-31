# -*- coding: utf-8 -*-
from odoo import _, api, fields, models, tools


class HelpdeskTicket(models.Model):

    _inherit = 'helpdesk.ticket'

    estimation = fields.Float('Workload Estimation')
    sale_order_id = fields.Many2one('sale.order', "Sale Order")

    def create_sale_order(self):
        self.ensure_one()
        return {
            'name':_("Create New Sale Order"),
            'view_mode': 'form',
            'view_type': 'form',
            'res_model': 'sale.order',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': {
                'default_partner_id': self.partner_id and self.partner_id.id}
        }