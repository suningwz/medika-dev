# -*- coding: utf-8 -*-

# import odoo.exceptions
from odoo import models, fields, api, _

class InvoiceDetail(models.Model):
    _inherit = 'eclaim.invoice.detail'

    # batch_id = fields.Many2one('eclaim.batch', string='Batch No')    
