# -*- coding: utf-8 -*-

import logging
from datetime import datetime

from odoo import models, fields, api

class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.model
    def scheduler_send_email_late_paiding_invoice(self):
        today = datetime.now().date()
        unpaids =self.search([
            ('type','=','out_invoice'),
            ('state', '=', 'open'),
            ('date_due', '>=', str(today))])
        unpaids.send_email_late_paiding_invoice()

    @api.multi
    def send_email_late_paiding_invoice(self):
        mail_template = self.env.ref(
            'unpaid_invoice_remind.late_paiding_invoice_remind',
            raise_if_not_found=False)
        if not mail_template:
            logging.info("Email template not found")
            return False
        for invoice in self:
            mail_template.send_mail(
                invoice.id, force_send=True, raise_exception=False)
        return True
