# -*- coding: utf-8 -*-
import re
from odoo import models, fields, api, _
from datetime import date, datetime
from odoo.exceptions import UserError, ValidationError

import qrcode
import base64
from io import BytesIO

class HistoryJoin(models.Model):
    _name = 'history.join'
    _description = 'History Join'
    
    partner_id = fields.Many2one('res.partner', string='Provider', ondelete='cascade')
    provider_join_date = fields.Date(string='Provider Join Date')

    provider_join_date_month = fields.Char(compute='_compute_provider_join_date_month', string='Provider Join Date Month', store=True,)
    
    @api.depends('provider_join_date')
    def _compute_provider_join_date_month(self):
        self.provider_join_date_month = False
        for rec in self:
            if rec.provider_join_date:
                rec.provider_join_date_month = rec.provider_join_date.month
    
    provider_join_date_year = fields.Char(compute='_compute_provider_join_date_year', string='Provider Join Date Year', store=True,)
    
    @api.depends('provider_join_date')
    def _compute_provider_join_date_year(self):
        self.provider_join_date_year = False
        for rec in self:
            if rec.provider_join_date:
                rec.provider_join_date_year = rec.provider_join_date.year
    
        
