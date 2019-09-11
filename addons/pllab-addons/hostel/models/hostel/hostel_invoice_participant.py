
# -*- encoding: utf-8 -*-
# Copyright (C) 2018 Nguyen Duc Tam <nguyenductamlhp@gmail.com>

from odoo import fields, models, api, _
from odoo.exceptions import Warning


class HostelInvoiceParticipant(models.Model):
    _name = 'hostel.invoice.participant'

    def _get_default_start(self):
        if self.invoice_id:
            return self.invoice_id.date_from
        return None

    invoice_id = fields.Many2one(
        'hostel.invoice', string='Invoice', required=True, readonly=True)
    partner_id = fields.Many2one(
        'res.partner', string='Partner', required=True)
    start = fields.Date(
        string='Start', required=True, help='Start',
        default=lambda self: self._get_default_start())
    end = fields.Date(
        string='End', required=True, help='End',
        default=lambda self: self.invoice_id and self.invoice_id.date_to)
    responsible_ids = fields.Many2many(
        'res.partner', string="Responsible",
        related='invoice_id.responsible_ids')

    @api.constrains('invoice_id', 'partner_id', 'start', 'end')
    def _constrains_not_duplicate_participant(self):
        Participant = self.env['hostel.invoice.participant']
        for rec in self:
            participants = Participant.search([
                ('id', '!=', self.id),
                ('invoice_id', '=', rec.id),
                '|',
                ('start', '>=', rec.end),
                ('end', '<=', rec.start)], limit=1)
            if participants:
                raise Warning('Can not overlap participant!')
