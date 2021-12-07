# -*- coding: utf-8 -*-

from odoo import models, fields, api

class CallRecord(models.Model):
    _inherit = 'call.record'
    
    source_id = fields.Many2one('helpline.source', string='Source')

class CallRecordLines(models.Model):
    _inherit = 'call.record.lines'

    source_id = fields.Many2one('helpline.source', string='Source')
