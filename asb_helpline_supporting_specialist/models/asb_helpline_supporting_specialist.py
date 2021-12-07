# -*- coding: utf-8 -*-

from odoo import models, fields, api


class HelplineSupportingSpecialist(models.Model):
    _name = 'helpline.supporting.specialist'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
    _description = 'Helpline Supporting Specialist'
    
    name = fields.Char(string='Name', tracking=True, required=True, )
    position = fields.Char(string='Position', trecking=True, required=True, )
    contact = fields.Char(string='Contact Person', tracking=True, required=True, )