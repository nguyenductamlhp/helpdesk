# -*- coding: utf-8 -*-

from odoo import models, fields, api

class HelpdeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'

    parent_id = fields.Many2one('helpdesk.ticket', 'Parent')
    child_ids = fields.One2many(
        'helpdesk.ticket', 'parent_id', 'Children Tickets')
