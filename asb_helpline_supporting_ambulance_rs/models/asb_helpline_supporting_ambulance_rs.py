# -*- coding: utf-8 -*-

from odoo import models, fields, api


class HelplineSupportingAmbulanceRs(models.Model):
    _name = 'helpline.supporting.ambulance.rs'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
    _description = 'Helpline Supporting Ambulance Rs'
    
    name = fields.Char(string='Hospital Name', tracking=True, required=True, )
    address = fields.Char(string='Address', tracking=True, required=True, )
    city = fields.Char(string='City', trecking=True, required=True, )
    contact = fields.Char(string='Contact', tracking=True, required=True, )