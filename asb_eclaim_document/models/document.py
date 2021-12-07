# -*- coding: utf-8 -*-

# import odoo.exceptions
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class EclaimDocument(models.Model):
    _name = 'eclaim.document'
    _description = 'Eclaim Document'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
    _rec_name = 'receipt_number'
    
    receipt_number = fields.Char(string='Receipt Number', tracking=True)
    document_from = fields.Char(string='From', tracking=True)
    to = fields.Selection([
        ('eclaim', 'E-Claim'),
        ('mas', 'MAS'),
    ], string='To', tracking=True)
    item_type_id = fields.Many2one('eclaim.item.type', string='Item Type', tracking=True)
    item_id = fields.Many2one('eclaim.item', string='Item', tracking=True)
    quantity = fields.Integer(string='Quantity', tracking=True)
    expedition = fields.Char(string='Expedition', tracking=True)
    courier = fields.Char(string='Courier Name', tracking=True)
    invoice_number = fields.Char(string='Invoice Number', tracking=True)
    date = fields.Datetime(string='Created Date', default=lambda self: fields.datetime.now(), tracking=True)
    notes = fields.Char(string='Notes', tracking=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submit', 'Submitted'),
        ('receive', 'Received'),
    ], string='Status', default='draft', tracking=True)

    def action_submit(self):
        return self.write({'state': 'submit'})