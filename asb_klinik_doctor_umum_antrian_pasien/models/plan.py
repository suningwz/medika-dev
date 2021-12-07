# -*- coding: utf-8 -*-
from odoo import api, fields, models, exceptions, _
from odoo.exceptions import UserError, ValidationError

class MasterPlan(models.Model):
    _name           = 'master.plan'
    _description    = 'Master Plan'
    
    name            = fields.Char(string = 'Plan')