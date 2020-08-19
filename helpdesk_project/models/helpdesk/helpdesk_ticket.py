from odoo import _, api, fields, models, tools
from odoo.exceptions import Warning


class HelpdeskTicket(models.Model):

    _inherit = 'helpdesk.ticket'

    task_ids = fields.One2many(
        'project.task', 'helpdesk_ticket_id',
        string="Tasks", track_visibility='onchange')
    count_task = fields.Integer(
        'Number of Tasks', compute='_compute_no_of_task', store=True)
    project_id = fields.Many2one(
        'project.project', string='Project', track_visibility='onchange')
    project_name = fields.Char('Project Name', related='project_id.name')

    @api.depends('task_ids')
    def _compute_no_of_task(self):
        for ticket in self:
            ticket.count_task = len(ticket.task_ids)

    @api.multi
    def create_project_task(self):
        """
        Create new project task and link to helpdesk ticket
        """
        Task = self.env['project.task']
        for ticket in self:
            if not ticket.project_id:
                raise Warning("Missing ticket's project")
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

    @api.multi
    def action_related_tasks(self):
        self.ensure_one()
        action = self.env.ref('project.project_task_action_sub_task').read()[0]
        ctx = self.env.context.copy()
        ctx.update({
            'default_project_id' :  self.project_id.id,
            'default_partner_id' : self.partner_id.id,
            'default_helpdesk_ticket_id': self.id,
            'default_planned_hours': self.estimation,
            'search_default_project_id': self.env.context.get('project_id', self.project_id.id),
        })
        action['context'] = ctx
        action['domain'] = [('id', 'in', self.task_ids.ids)]
        return action

