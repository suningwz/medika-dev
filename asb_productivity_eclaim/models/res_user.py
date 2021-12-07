# -*- coding: utf-8 -*-

# import odoo.exceptions
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime

class ResUsers(models.Model):
    _inherit = 'res.users'
    _description = 'Res Users'

    user_productivity_line = fields.One2many('user.productivity', 'user_id', string='User Productivity')