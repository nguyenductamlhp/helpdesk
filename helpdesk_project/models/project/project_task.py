# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Project_task(models.Model):
    _inherit = 'project.task'

    helpdesk_ticket_id = fields.Many2one(
        'helpdesk.ticket', help='Link to helpdesk ticket if exist')
