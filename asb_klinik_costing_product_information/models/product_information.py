# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import date, datetime
    
class ProductInformation(models.Model):
    _name = 'costing.product.information'
    _description = 'Product Information'
    
    name = fields.Char(string='Name')
    description = fields.Char(string='Description')
    start_from = fields.Date(string='Start From')
    start_to = fields.Date(string='Start To')
    attachment = fields.Binary(string='Attachment')
    archive = fields.Boolean(string='Archive')
    state = fields.Selection([
        ('active', 'Active'),
        ('inactive', 'Inactive')
    ], string='Status', default='inactive')

    @api.onchange('start_from','start_to')
    def _onchange_start_from(self):
        for rec in self:
            if rec.start_from and rec.start_to:
                if rec.start_from <= date.today() and date.today() <= rec.start_to:
                    rec.status = 'active'
                else:
                    rec.status = 'inactive'

    def action_archive(self):
        self.write({'archive': True})

    def action_unarchive(self):
        self.write({'archive': False})