# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from datetime import date


class ClientProgram(models.Model):
    _name = 'client.program'
    _description = 'Client Program'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']

    client_branch_id = fields.Many2one('client.branch', string='Client Branch', tracking=True)
    name = fields.Char(string='Program Name', tracking=True)
    claim_by = fields.Selection([
        ('client', 'Client'),
        ('medika', 'Medika Plaza'),
    ], string='Claim Paid by', tracking=True, required=True, )
    floatfund = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No'),
    ], string='Using Floatfund', tracking=True, required=True, )
    floatfund_warning = fields.Float(string='Warning Percentage', tracking=True)
    company_id = fields.Many2one('res.company', 'Company', default=lambda self: self.env.user.company_id.id, index=1, tracking=True)
    currency_id = fields.Many2one('res.currency', 'Currency', default=lambda self: self.env.user.company_id.currency_id.id, required=True, tracking=True)
    basic_floatfund = fields.Float(string='Basic Floatfund', tracking=True)

    # @api.onchange('floatfund_line')
    # def _onchange_floatfund_line(self):
    #     self.basic_floatfund = sum(line.amount for line in self.floatfund_line)

    @api.depends('floatfund_line')
    def _compute_basic_floatfund(self):
        if self.floatfund_line:
            self.basic_floatfund = sum(line.amount for line in self.floatfund_line)
        else:
            self.basic_floatfund = 0

    used_floatfund = fields.Float(string='Used Floatfund', tracking=True, readonly=True)
    remaining_floatfund = fields.Float(compute='_compute_remaining_floatfund', string='Remaining Floatfund', tracking=True, store=True)

    @api.depends('floatfund_total','used_floatfund')
    def _compute_remaining_floatfund(self):
        for rec in self:
            if rec.floatfund_total:
                rec.remaining_floatfund = rec.floatfund_total - rec.used_floatfund
            else:
                rec.remaining_floatfund = 0

    start_date = fields.Date(string='Effective Date', tracking=True)
    end_date = fields.Date(string='Expiry Date', tracking=True)
    created_date = fields.Date(string='Created Date', default=lambda self: fields.datetime.now(), required=True, tracking=True)
    created_by = fields.Many2one('res.users', string='Created By', default=lambda self: self.env.user.id, required=True, tracking=True)
    program_plan_count = fields.Integer(compute='_compute_program_plan_count', string='Member')
    program_floatfund_count = fields.Integer(compute='_compute_program_floatfund_count', string='Member')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('enabled', 'Enabled'),
        ('disabled', 'Disabled'),
    ], string='Status', default='draft', tracking=True)
    is_editable = fields.Boolean(string="Is editable", compute="_compute_is_editable", readonly=True, default=True)

    floatfund_line = fields.One2many('client.program.floatfund', 'program_id', string='Floatfund')
    plan_line = fields.One2many('client.program.plan', 'program_id', string='Plan')
    floatfund_warning_tree = fields.Char(compute='_compute_floatfund_warning_tree', string='Warning Percentage', default="0 %", tracking=True)
    floatfund_total = fields.Float(compute='_compute_floatfund_total', string='Total Amount', store=True)
    
    @api.depends('floatfund_line')
    def _compute_floatfund_total(self):
        for rec in self:
            rec.floatfund_total = sum(line.amount for line in self.floatfund_line)
                
    @api.depends('floatfund_warning')
    def _compute_floatfund_warning_tree(self):
        for rec in self:
            if rec.floatfund_warning:
                rec.floatfund_warning_tree = _("%s %%") % (rec.floatfund_warning)
            else:
                rec.floatfund_warning_tree = "0 %"

    def _compute_is_editable(self):
        for rec in self:
            if rec.state in ("enabled", "disabled"):
                rec.is_editable = False
            else:
                rec.is_editable = True

    def _compute_program_plan_count(self):
        for record in self:
            record.program_plan_count = self.env['client.program.plan'].search_count([('program_id', '=', self.id)])

    def _compute_program_floatfund_count(self):
        for record in self:
            record.program_floatfund_count = self.env['client.program.floatfund'].search_count([('program_id', '=', self.id)])

    def enable(self):
        for rec in self:
            rec.state = 'enabled'

    def disable(self):
        for rec in self:
            rec.state = 'disabled'

    def draft(self):
        for rec in self:
            rec.state = 'draft'

    @api.model
    def create(self, vals):
        vals['state'] = 'enabled'
        return super(ClientProgram, self).create(vals)
