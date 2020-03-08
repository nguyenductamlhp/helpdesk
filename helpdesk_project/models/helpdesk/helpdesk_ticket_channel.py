from odoo import _, api, fields, models, tools


class HelpdeskTicketChannel(models.Model):

    _inherit = 'helpdesk.ticket.channel'

    default_team_id = fields.Many2one(
        'helpdesk.ticket.team', string='Default Team')
    default_assignee_id = fields.Many2one(
        'res.users', string='Default Assignee')
