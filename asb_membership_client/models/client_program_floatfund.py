# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from datetime import date

class ClientProgramFloatfund(models.Model):
    _name = 'client.program.floatfund'
    _description = 'Client Program Floatfund'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
    
    name = fields.Char(string='Description', tracking=True)
    program_id = fields.Many2one('client.program', string='Program', tracking=True)
    amount = fields.Float(string='Amount', tracking=True)
    company_id = fields.Many2one('res.company', 'Company', default=lambda self: self.env.user.company_id.id, index=1, tracking=True)
    currency_id = fields.Many2one(related="program_id.currency_id", tracking=True)
    created_date = fields.Date(string='Created Date', default=lambda self: fields.datetime.now(), required=True, tracking=True)
    created_by = fields.Many2one('res.users', string='Created By', default=lambda self: self.env.user.id, required=True, tracking=True)
