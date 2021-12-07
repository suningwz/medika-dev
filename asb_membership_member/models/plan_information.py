# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from datetime import date
from odoo.exceptions import UserError

class PlanInformation(models.Model):
    _name = 'plan.information'
    _description = 'Plan Information'

    partner_id = fields.Many2one('res.partner', string='Member')
    
    program_plan_id = fields.Many2one('client.program.plan', string='Plan Name')
    benefit_id = fields.Many2one('benefit.benefit', string='Detail Name')
    
    header_id = fields.Many2one('program.plan.header', string='Header Name')
    annual_limit = fields.Float(related='header_id.annual_limit')
    daily_limit = fields.Float(related='header_id.daily_limit')
    deductible = fields.Float(related='header_id.deductible')
    coinsurance = fields.Float(related='header_id.coinsurance')
    coshare = fields.Float(related='header_id.coshare')
    
    cover = fields.Boolean(string='Cover')
    max_per_visit = fields.Float(string='Max Per Visit' )
    max_day_per_year = fields.Integer(string='Max Day Per Year' )
    max_per_day = fields.Integer(string='Max Per Day' )
    inner_limit = fields.Float(string='Inner Limit' )
    per_day_limit = fields.Float(string='Per Day limit' )