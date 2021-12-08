# -*- coding: utf-8 -*-
import re
from odoo import models, fields, api, _
from datetime import date, datetime
from odoo.exceptions import UserError, ValidationError

import qrcode
import base64
from io import BytesIO


class HistoryFinished(models.Model):
    _name = 'history.finished'
    _description = 'History Finished'

    partner_id = fields.Many2one('res.partner', string='Provider', ondelete='cascade')
    provider_finished_date = fields.Date(string='Provider Finished Date')

    provider_finished_date_month = fields.Char(compute='_compute_provider_finished_date_month', string='Provider Finished Date Month', store=True,)

    @api.depends('provider_finished_date')
    def _compute_provider_finished_date_month(self):
        self.provider_finished_date_month = False
        for rec in self:
            if rec.provider_finished_date:
                rec.provider_finished_date_month = rec.provider_finished_date.month

    provider_finished_date_year = fields.Char(compute='_compute_provider_finished_date_year', string='Provider Finished Date Year', store=True,)

    @api.depends('provider_finished_date')
    def _compute_provider_finished_date_year(self):
        self.provider_finished_date_year = False
        for rec in self:
            if rec.provider_finished_date:
                rec.provider_finished_date_year = rec.provider_finished_date.year
