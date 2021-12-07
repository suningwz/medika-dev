# -*- coding: utf-8 -*-

from odoo import models, fields, api


class HelplineSupportingAmbulanceRental(models.Model):
    _name = 'helpline.supporting.ambulance.rental'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
    _description = 'Helpline Supporting Ambulance Rental'
    
    name = fields.Char(string='Ambulance Company', tracking=True, required=True, )
    remarks = fields.Char(string='Remarks', tracking=True, required=True, )
    ambulance_rental_from = fields.Char(string='From', trecking=True, required=True, )
    ambulance_rental_to = fields.Char(string='To', tracking=True, required=True, )