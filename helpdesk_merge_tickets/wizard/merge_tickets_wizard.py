# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import Warning


class MergeTicketsWizard(models.TransientModel):
    """Merge multiple tickets"""
    _name = "merge.tickets.wizard"

    name = fields.Char(string='Title', required=True)
    description = fields.Text(required=True)
    user_id = fields.Many2one(
        'res.users',
        string='Assigned user',)
    user_ids = fields.Many2many(
        comodel_name='res.users',
        related='team_id.user_ids',
        string='Users')
    partner_id = fields.Many2one('res.partner')
    tag_ids = fields.Many2many('helpdesk.ticket.tag')
    company_id = fields.Many2one(
        'res.company',
        string="Company",
        default=lambda self: self.env['res.company']._company_default_get(
            'helpdesk.ticket')
    )
    channel_id = fields.Many2one(
        'helpdesk.ticket.channel',
        string='Channel',
        help='Channel indicates where the source of a ticket'
             'comes from (it could be a phone call, an email...)',
    )
    category_id = fields.Many2one(
        'helpdesk.ticket.category', string='Category')
    team_id = fields.Many2one('helpdesk.ticket.team')
    attachment_ids = fields.One2many(
        'ir.attachment', 'res_id',
        domain=[('res_model', '=', 'helpdesk.ticket')],
        string="Media Attachments")
    child_ids = fields.Many2many('helpdesk.ticket')

    @api.onchange('create_uid')
    def onchange_create_uid(self):
        '''
        Set default data and add live domain
        '''
        ctx = self.env.context

        active_model = ctx.get('active_model', None)
        active_ids = ctx.get('active_ids', [])

        if not active_model or not active_ids or \
                active_model != 'helpdesk.ticket':
            return

        HelpdeskTicket = self.env['helpdesk.ticket']
        tickets = HelpdeskTicket.search([('id', 'in', active_ids)])
        if not tickets:
            return

        data = {
            'name': ' - '.join([ticket.name for ticket in tickets]),
            'description': '\n'.join(
                [ticket.description for ticket in tickets]),
            'team_id': tickets.mapped('team_id.id'),
            'user_id': tickets.mapped('user_id.id'),
            'user_ids': tickets.mapped('user_ids.id'),
            'category_id': tickets.mapped('category_id.id'),
            'partner_id': tickets.mapped('partner_id.id'),
            'channel_id': tickets.mapped('channel_id.id'),
            'tag_ids': tickets.mapped('tag_ids.id'),
            'attachment_ids': tickets.mapped('attachment_ids.id'),
            'child_ids': tickets and tickets.ids or [],
        }

        default_vals = {}
        default_domain = {}
        # Set default data
        for field, value in data.items():
            default_domain[field] = [('id', 'in', value)]
            if isinstance(self._fields[field], (fields.Many2one)):
                if len(value) == 1:
                    self[field] = value[0]
            elif isinstance(self._fields[field], (fields.Many2many, fields.One2many)):
                self[field] = [(6, 0, value)]
            else:
                self[field] = value
        return {
            'domain': default_domain,
        }

    @api.multi
    def btn_create_ticket(self):
        '''
        Create merged tickets from selected
        '''
        self.ensure_one()
        context = self.env.context
        rec = self

        HelpdeskTicket = self.env['helpdesk.ticket']
        add_fields = ['name', 'description', 'team_id', 'user_id', 'user_ids',
            'category_id', 'partner_id', 'channel_id', 'tag_ids', 'child_ids']

        vals = {}
        for field in add_fields:
            if not rec[field]:
                continue
            if isinstance(self._fields[field], (fields.Many2one)):
                vals[field] = rec[field].id
            elif isinstance(
                    self._fields[field],
                    (fields.Many2many, fields.One2many)):
                vals[field] = [(6, 0, rec[field].ids)]
            else:
                vals[field] = rec[field]

        new_ticket = HelpdeskTicket.create(vals)

        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form,tree',
            'res_model': context['active_model'],
            'target': 'current',
            'context': context,
            'res_id': new_ticket.id,
            'domain': [('id', '=', new_ticket.id)],
        }
