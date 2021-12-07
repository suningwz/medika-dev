# -*- coding: utf-8 -*-

from odoo import models, fields, api


class HelplineSupportingAssistance(models.Model):
    _name = 'helpline.supporting.assistance'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
    _description = 'Helpline Supporting Assistnca'
    
    name = fields.Char(string='Company', tracking=True, required=True, )
    assistance_type = fields.Char(string='Type', trecking=True, required=True, )
    country = fields.Char(string='Country', tracking=True, required=True, )
    mobile = fields.Char(string='Mobile', tracking=True, required=True, )
    email = fields.Char(string='Email', tracking=True, required=True, )