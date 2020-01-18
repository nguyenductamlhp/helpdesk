# -*- coding: utf-8 -*-
from odoo import _, api, fields, models, tools


class HelpdeskTicket(models.Model):

    _inherit = 'helpdesk.ticket'

    active = fields.Boolean('Active', default=True)

    @api.constrains('stage_id')
    def constrains_tocket_stage(self):
        '''
        '''
        for ticket in self:
            stage = ticket.stage_id or None
            if not stage:
                continue
            if stage.closed:
                ticket.active = False
            else:
                ticket.active = True
