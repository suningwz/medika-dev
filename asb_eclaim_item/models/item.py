# -*- coding: utf-8 -*-

# import odoo.exceptions
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class EclaimItemType(models.Model):
    _name = 'eclaim.item.type'
    _description = 'Eclaim Item Type'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
    
    name = fields.Char(string='Item Type')
    description = fields.Char(string='Description')

class EclaimItem(models.Model):
    _name = 'eclaim.item'
    _description = 'Eclaim Item'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
    
    name = fields.Char(string='Item')
    description = fields.Char(string='Description')
    item_type_id = fields.Many2one('eclaim.item.type', string='Item Type')