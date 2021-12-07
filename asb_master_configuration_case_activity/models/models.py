# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProviderActivity(models.Model):
    _name = 'provider.activity'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
    _description = 'Provider Activity'
    
    name = fields.Char(string='Provider Case Activity', tracking=True)