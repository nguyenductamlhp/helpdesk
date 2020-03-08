from odoo import _, api, fields, models, tools


class HelpdeskTicket(models.Model):

    _inherit = 'helpdesk.ticket'

    task_ids = fields.One2many(
        'project.task', 'helpdesk_ticket_id',
        string="Tasks", track_visibility='onchange')
    project_id = fields.Many2one(
        'project.project', string='Project', track_visibility='onchange')

    @api.multi
    def create_project_task(self):
        """
        Create new project task and link to helpdesk ticket
        """
        Task = self.env['project.task']
        for ticket in self:
            Task.create({
                'project_id': ticket.project_id and ticket.project_id.id,
                'user_id': ticket.user_id and ticket.user_id.id,
                'helpdesk_ticket_id': ticket.id,
                'name': ticket.name,
                'description': ticket.description,
                'partner_id': ticket.partner_id and ticket.partner_id.id,
                'planned_hours': ticket.estimation
            })
