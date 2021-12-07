# -*- coding: utf-8 -*-

from odoo import models, fields, api


class HelplineSupportingEmbassy(models.Model):
    _name = 'helpline.supporting.embassy'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
    _description = 'Helpline Supporting Embassy'
    
    name = fields.Char(string='Embassy', tracking=True, required=True, )
    address = fields.Char(string='Address', trecking=True, required=True, )
    telp = fields.Char(string='Telp', tracking=True, required=True, )
    fax = fields.Char(string='Fax', tracking=True, required=True, )
    email = fields.Char(string='Email/Web', tracking=True, required=True, )