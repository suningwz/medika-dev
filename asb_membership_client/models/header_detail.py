# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from datetime import date

class HeaderDetail(models.Model):
    _name = 'header.detail'
    _description = 'Header Detail'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
    _rec_name = 'benefit_id'
    
    header_id = fields.Many2one('program.plan.header', string='Header', tracking=True)
    program_id = fields.Many2one('client.program', related="header_id.program_id", string='Program', tracking=True)
    plan_id = fields.Many2one('client.program.plan', related="header_id.plan_id", string='Plan Name', tracking=True)
    benefit_category_id = fields.Many2one('benefit.master', string='Header Name', ondelete='restrict')
    benefit_id = fields.Many2one('benefit.benefit', string='Detail Name')
    cover = fields.Boolean(string='Cover', tracking=True)
    max_per_day = fields.Integer(string='Max Per Day', tracking=True)
    max_day_per_year = fields.Integer(string='Max Day Per Year', tracking=True)
    max_per_visit = fields.Float(string='Max Per Visit', tracking=True)
    inner_limit = fields.Float(string='Inner Limit', tracking=True)
    per_day_limit = fields.Float(string='Per Day limit', tracking=True)
    company_id = fields.Many2one('res.company', 'Company', default=lambda self: self.env.user.company_id.id, index=1, tracking=True)
    currency_id = fields.Many2one(related='header_id.currency_id')
    created_date = fields.Date(string='Created Date', default=lambda self: fields.datetime.now(), required=True, tracking=True)
    created_by = fields.Many2one('res.users', string='Created By', default=lambda self: self.env.user.id, required=True, tracking=True)
    get_benefit_id_domain = fields.Many2many('benefit.benefit', compute='_compute_get_benefit_id_domain', string='Benefit Domain')

    @api.depends('header_id')
    def _compute_get_benefit_id_domain(self):
        for rec in self:
            if rec.header_id.benefit_category_id:
                rec.get_benefit_id_domain = self.env['benefit.benefit'].search([('master_id', '=', rec.header_id.benefit_category_id.id)])
            if not rec.header_id.benefit_category_id:
                rec.get_benefit_id_domain = self.env['benefit.benefit'].search([('master_id', '=', rec.header_id.benefit_category_id.id)])

