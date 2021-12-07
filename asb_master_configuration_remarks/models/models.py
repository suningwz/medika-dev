# -*- coding: utf-8 -*-

from odoo import models, fields, api

class MasterRemarks(models.Model):
    _name = 'master.remarks'
    _description = 'Master Remarks'
    
    name = fields.Char(string='Remarks', store=True,)