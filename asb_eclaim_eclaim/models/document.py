# -*- coding: utf-8 -*-

# import odoo.exceptions
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import date, datetime, timedelta
class EclaimDocument(models.Model):
    _inherit = 'eclaim.document'
    _description = 'Eclaim Document'
    

    def action_submit(self):
        for rec in self:
            rec.write({'state': 'submit'})
            receive_date = rec.date
            if receive_date.time().hour >= 9:
                receive_date += timedelta(days=1)
                receive_date = receive_date.replace(hour=1, minute=0, second=0)
            if receive_date.isoweekday() == 6:
                receive_date += timedelta(days=2)
            elif receive_date.isoweekday() == 7:
                receive_date += timedelta(days=1)
            eclaim_vals = {
                'document_id' : rec._origin.id,
                'receipt_number' : rec.receipt_number,
                'document_from' : rec.document_from,
                'to' : rec.to,
                'case_quantity' : rec.quantity,
                'invoice_number' : rec.invoice_number,
                'date' : receive_date,
                'notes' : rec.notes,
                'document_status' : rec.state,
            }
            eclaim = self.env['eclaim.eclaim'].create(eclaim_vals)