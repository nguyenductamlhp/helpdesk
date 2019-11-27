from odoo import _, api, fields, models, tools


class HelpdeskTicket(models.Model):

    _inherit = 'helpdesk.ticket'

    task_ids = fields.One2many(
        'project.task', 'helpdesk_ticket_id',
        string="Tasks")
    project_id = fields.Many2one(
        'project.project', string='Project')
