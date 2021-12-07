# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from datetime import datetime, date



class FacilityCategory(models.Model):
    _name = 'facility.category'
    _description = 'Facility Category'
    
    name = fields.Char(string='Facility Category')