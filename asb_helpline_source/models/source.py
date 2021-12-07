# -*- coding: utf-8 -*-

from odoo import models, fields, api


class HelplineSource(models.Model):
    _name = 'helpline.source'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
    _description = 'Helpline Source'
    
    name = fields.Char(string='Name')
