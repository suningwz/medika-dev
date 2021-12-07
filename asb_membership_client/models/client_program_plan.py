# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from datetime import date


class ClientProgramPlan(models.Model):
    _name = 'client.program.plan'
    _description = 'Client Program Plan'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Plan Name', tracking=True)
    program_id = fields.Many2one('client.program', string='Program', tracking=True)
    service = fields.Selection([
        ('reimburse', 'Reimbursement'),
        ('cashless', 'Cashless'),
        ('both', 'Both'),
    ], string='Service Type', tracking=True)
    fullcover = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No'),
    ], string='Fullcover', tracking=True)
    created_date = fields.Date(string='Created Date', default=lambda self: fields.datetime.now(), required=True, tracking=True)
    created_by = fields.Many2one('res.users', string='Created By', default=lambda self: self.env.user.id, required=True, tracking=True)
    entity = fields.Char(string='Entity', tracking=True)
    plan_header_count = fields.Integer(compute='_compute_plan_header_count', string='Member')
    program_plan_lines = fields.One2many('program.plan.line', 'program_plan_id', string='')

    def _compute_plan_header_count(self):
        for record in self:
            record.plan_header_count = self.env['program.plan.header'].search_count([('plan_id', '=', self.id)])

    is_editable = fields.Boolean(string="Is editable", compute="_compute_is_editable", readonly=True, default=True)

    def _compute_is_editable(self):
        for rec in self:
            if rec.program_id:
                if rec.program_id.state in ("enabled", "disabled"):
                    rec.is_editable = False
                else:
                    rec.is_editable = True
            else:
                rec.is_editable = True

    header_line = fields.One2many('program.plan.header', 'plan_id', string='Header')

    def copy(self, default=None):
        new_header = []
        default = dict(default or {})
        default.update(name=_('%s (copy)') % (self.name))
        new_plan = super(ClientProgramPlan, self).copy(default=default)
        for line in self.header_line:
            header_copy = line.copy(default=None)
            new_detail = []
            for detail in line.detail_line:
                detail_copy = detail.copy(default=None)
                new_detail.append((4, detail_copy.id))
            header_copy.detail_line = new_detail
            new_header.append((4, header_copy.id))
        new_plan.header_line = new_header
        return new_plan

    program = fields.Char(compute='_compute_program', string='Program')

    @api.depends('program_id')
    def _compute_program(self):
        for rec in self:
            rec.program = rec.program_id.name


class ProgramPlanLine(models.Model):
    _name = 'program.plan.line'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
    _description = 'Program Plan Line'

    benefit_category_id = fields.Many2one('benefit.master', string='Category', required=True, tracking=True)
    benefit_id = fields.Many2one('benefit.benefit', string='Benefit Name', required=True, tracking=True)
    remarks = fields.Char(string='Remarks', size=400, required=True, tracking=True)
    program_plan_id = fields.Many2one('client.program.plan', string='Client Program Plan')
    get_benefit_id_domain = fields.Many2many('benefit.benefit', compute='_compute_get_benefit_id_domain', string='Benefit Domain')

    @api.onchange('benefit_category_id')
    def _onchange_benefit_category_id(self):
        for rec in self:
            rec.benefit_id = False
            rec.remarks = False

    @api.depends('benefit_category_id')
    def _compute_get_benefit_id_domain(self):
        for rec in self:
            if rec.benefit_category_id:
                rec.get_benefit_id_domain = self.env['benefit.benefit'].search([('master_id', '=', rec.benefit_category_id.id)])
            if not rec.benefit_category_id:
                rec.get_benefit_id_domain = self.env['benefit.benefit'].search([('master_id', '=', rec.benefit_category_id.id)])
