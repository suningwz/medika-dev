# -*- coding: utf-8 -*-

# import odoo.exceptions
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime

class UserProductivity(models.Model):
    _name = 'user.productivity'
    _description = 'User Productivity'
    
    name = fields.Char(string='Description')   
    user_id = fields.Many2one('res.users', string='User')
    eclaim_category = fields.Selection([
        ('ip', 'IP'),
        ('op', 'OP'),
        ('de', 'DE'),
        ('eg', 'EG'),
        ('ma', 'MA'),
        ('mcu', 'MCU'),
        ('ot', 'OT'),
    ], string='Category', tracking=True)
    department = fields.Selection([
        ('eclaim', 'E-Claim')
    ], string='Department')
    point = fields.Integer(string='Point')