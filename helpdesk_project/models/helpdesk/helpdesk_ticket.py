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

    @api.model
    def create(self, vals):
        res = super(HelpdeskTicket, self).create(vals)
        res.set_default_channel_data()
        return res

    @api.multi
    def set_default_channel_data(self):
        '''
        When ticket is created, set default team and assignee from channel
        '''
        for ticket in self:
            if not ticket.channel_id:
                continue
            ticket.write({
                'team_id': ticket.channel_id.default_team_id and \
                    ticket.channel_id.default_team_id.id,
                'user_id': ticket.channel_id.default_assignee_id and \
                    ticket.channel_id.default_assignee_id.id or None
            })
