# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from datetime import datetime, date


class PicTitle(models.Model):
    _name = 'pic.title'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
    _description = 'Pic Title'

    name = fields.Char(string='PIC Title', tracking=True)
    type = fields.Selection([
        ('provider', 'Provider'),
        ('client', 'Client')
    ], string='Type', tracking=True)
