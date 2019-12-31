# -*- coding: utf-8 -*-
from odoo import _, api, fields, models, tools


class SaleOrder(models.Model):

    _inherit = 'sale.order'

    @api.model
    @tools.ormcache("self")
    def _selection_ref_item_id(self):
        models = self.env["ir.model"].search([])
        return [(r.model, r.name) for r in models]

    source_id = fields.Reference(
        string="Referenced item",
        selection="_selection_ref_item_id")
