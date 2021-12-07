# -*- coding: utf-8 -*-

from odoo import models, fields, api


class IssuedIssued(models.Model):
    _name = 'issued.issued'
    _description = 'Issued Issued'
    
    name = fields.Char(string='Name')