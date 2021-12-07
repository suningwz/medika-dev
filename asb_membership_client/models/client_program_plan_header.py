# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from datetime import date

class ProgramPlanHeader(models.Model):
    _name = 'program.plan.header'
    _description = 'Program Plan Header'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
    _rec_name = 'benefit_category_id'
    
    benefit_category_id = fields.Many2one('benefit.master', string='Header Name', ondelete='restrict')
    plan_id = fields.Many2one('client.program.plan', string='Plan Name', tracking=True)
    program_id = fields.Many2one('client.program', related="plan_id.program_id", string='Program', tracking=True)
    annual_limit = fields.Float(string='Annual Limit', tracking=True)
    daily_limit = fields.Float(string='Daily Limit', tracking=True)
    deductible = fields.Float(string='Deductible', tracking=True)
    coinsurance = fields.Float(string='Co-Insurance', tracking=True)
    coshare = fields.Float(string='Co-Payment', tracking=True)
    company_id = fields.Many2one('res.company', 'Company', default=lambda self: self.env.user.company_id.id, index=1, tracking=True)
    currency_id = fields.Many2one('res.currency', 'Currency', default=lambda self: self.env.user.company_id.currency_id.id, required=True, tracking=True)
    detail_line = fields.One2many('header.detail', 'header_id', string='Header Detail')
    created_date = fields.Date(string='Created Date', default=lambda self: fields.datetime.now(), required=True, tracking=True)
    created_by = fields.Many2one('res.users', string='Created By', default=lambda self: self.env.user.id, required=True, tracking=True)
    deductible_period = fields.Selection([
        ('onetime', 'One Time'),
        ('annual', 'Per Tahun'),
        ('visit', 'Per Visit'),
    ], string='Deductible Period')
    limit_selection = fields.Selection([
        ('individu', 'Individual'),
        ('family', 'Family'),
    ], string='Limit Option', tracking=True, ondelete='cascade')
    # is_editable = fields.Boolean(string="Is editable", compute="_compute_is_editable", readonly=True, default=True)
    is_editable = fields.Boolean(related='program_id.is_editable')

    # def _compute_is_editable(self):
    #     for rec in self:
    #         if rec.program_id:
    #             if rec.program_id.state in ("enabled", "disabled"):
    #                 rec.is_editable = False
    #         else:
    #             rec.is_editable = True

    @api.onchange('currency_id')
    def _onchange_currency_id(self):
        for rec in self:
            for line in rec.detail_line:
                line.currency_id = rec.currency_id

    @api.onchange('benefit_category_id')
    def _onchange_benefit_category_id(self):
        detail_lines = [(5, 0, 0)]
        benefit_category_id = self.env['benefit.benefit'].search([('master_id', '=', self.benefit_category_id.id)])
        for line in benefit_category_id:
            vals = {
                'benefit_id': line.id
            }
            detail_lines.append((0, 0, vals))
        self.detail_line = detail_lines
