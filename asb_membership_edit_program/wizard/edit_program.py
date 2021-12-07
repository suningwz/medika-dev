from odoo import models, fields, api
from datetime import date


class ClientProgram(models.Model):
    _inherit = 'client.program'
    _description = 'Client Program'

    def refresh(self):
        pass

    def action_edit_wizard(self):
        floatfund_lines = []
        plan_lines = []
        existing_floatfund = []
        existing_plan = []
        for rec in self:
            for line in rec.floatfund_line:
                vals_floatfund = {
                    'temp_id': line._origin.id,
                    'name': line.name,
                    'amount': line.amount,
                    'company_id': line.company_id.id,
                    'currency_id': line.currency_id.id,
                    'created_date': line.created_date,
                    'created_by': line.created_by.id,
                }
                floatfund_lines.append((0, 0, vals_floatfund))
                existing_floatfund.append(line._origin.id)
            for line in rec.plan_line:
                vals_plan = {
                    'temp_id': line._origin.id,
                    'program_id': self._origin.id,
                    'entity': line.entity,
                    'name': line.name,
                    'service': line.service,
                    'fullcover': line.fullcover,
                    'created_date': line.created_date,
                    'created_by': line.created_by.id,
                }
                plan_lines.append((0, 0, vals_plan))
                existing_plan.append(line._origin.id)
        return {
            'name': "Edit Program",
            'type': 'ir.actions.act_window',
            'res_model': 'edit.program',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                    'default_name': self.name,
                    'default_program_id': self._origin.id,
                    'default_client_branch_id': self.client_branch_id.id,
                    'default_claim_by': self.claim_by,
                    'default_floatfund': self.floatfund,
                    'default_floatfund_warning': self.floatfund_warning,
                    'default_company_id': self.company_id.id,
                    'default_currency_id': self.currency_id.id,
                    'default_basic_floatfund': self.basic_floatfund,
                    'default_remaining_floatfund': self.remaining_floatfund,
                    'default_used_floatfund': self.used_floatfund,
                    'default_start_date': self.start_date,
                    'default_end_date': self.end_date,
                    'default_created_by': self.created_by.id,
                    'default_created_date': self.created_date,
                    'default_floatfund_line': floatfund_lines,
                    'default_plan_line': plan_lines,
                    'default_existing_plan': existing_plan,
                    'default_existing_floatfund': existing_floatfund,
            }
        }


class EditFloatfund(models.TransientModel):
    _name = 'edit.floatfund'
    _description = 'Edit Floatfund'

    temp_id = fields.Integer(string='Line ID')
    name = fields.Char(string='Description')
    edit_program_id = fields.Many2one('edit.program', string='Program', ondelete='cascade')
    amount = fields.Float(string='Amount')
    company_id = fields.Many2one('res.company', 'Company', default=lambda self: self.env.user.company_id.id, index=1)
    currency_id = fields.Many2one(related="edit_program_id.currency_id")
    created_date = fields.Date(string='Created Date', default=lambda self: fields.datetime.now(), required=True )
    created_by = fields.Many2one('res.users', string='Created By', default=lambda self: self.env.user.id, required=True )


class EditPlan(models.TransientModel):
    _name = 'edit.plan'
    _description = 'Edit Plan'

    temp_id = fields.Integer(string='Line ID')
    name = fields.Char(string='Plan Name')
    edit_program_id = fields.Many2one('edit.program', string='Edit Program')
    program_id = fields.Many2one('client.program', string='Program')
    service = fields.Selection([
        ('reimburse', 'Reimbursement'),
        ('cashless', 'Cashless'),
        ('both', 'Both'),
    ], string='Service Type')
    fullcover = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No'),
    ], string='Fullcover')
    created_date = fields.Date(string='Created Date', default=lambda self: fields.datetime.now(), required=True )
    created_by = fields.Many2one('res.users', string='Created By', default=lambda self: self.env.user.id, required=True )
    entity = fields.Char(string='Entity')
    # program_plan_lines = fields.One2many('program.plan.line', 'program_plan_id', string='')

    # header_line = fields.One2many('program.plan.header', 'plan_id', string='Header')


class EditProgram(models.TransientModel):
    _name = 'edit.program'
    _description = 'Edit Program'

    name = fields.Char(string='Program')
    program_id = fields.Many2one('client.program', string='Program')

    client_branch_id = fields.Many2one('client.branch', string='Client Branch')
    name = fields.Char(string='Program Name')
    claim_by = fields.Selection([
        ('client', 'Client'),
        ('medika', 'Medika Plaza'),
    ], string='Claim Paid by')
    floatfund = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No'),
    ], string='Using Floatfund')
    floatfund_warning = fields.Float(string='Warning Percentage')
    company_id = fields.Many2one('res.company', 'Company', default=lambda self: self.env.user.company_id.id, index=1)
    currency_id = fields.Many2one('res.currency', 'Currency', default=lambda self: self.env.user.company_id.currency_id.id, required=True)
    basic_floatfund = fields.Float(string='Basic Floatfund', store=True)

    remaining_floatfund = fields.Float(compute='_compute_remaining_floatfund', string='Remaining Floatfund', tracking=True, store=True)

    @api.depends('basic_floatfund')
    def _compute_remaining_floatfund(self):
        for rec in self:
            if rec.floatfund_total:
                rec.remaining_floatfund = rec.floatfund_total - rec.used_floatfund
            else:
                rec.remaining_floatfund = 0

    used_floatfund = fields.Float(string='Used Floatfund', readonly=True)
    start_date = fields.Date(string='Effective Date')
    end_date = fields.Date(string='Expiry Date')
    created_date = fields.Date(string='Created Date')
    created_by = fields.Many2one('res.users', string='Created By')
    # program_plan_count = fields.Integer(compute='_compute_program_plan_count', string='Member')
    # program_floatfund_count = fields.Integer(compute='_compute_program_floatfund_count', string='Member')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('enabled', 'Enabled'),
        ('disabled', 'Disabled'),
    ], string='Status', default='draft')

    existing_floatfund = fields.Many2many('client.program.floatfund', string='Existing Plan')
    floatfund_line = fields.One2many('edit.floatfund', 'edit_program_id', string='Floatfund', ondelete='cascade')
    floatfund_line_count = fields.Integer(string='Floatfund Count')
    floatfund_total = fields.Float(compute='_compute_floatfund_total', string='Total Amount')
    
    @api.depends('floatfund_line')
    def _compute_floatfund_total(self):
        for rec in self:
            rec.floatfund_total = sum(line.amount for line in self.floatfund_line)
                
    @api.onchange('floatfund_line')
    def _onchange_floatfund_line(self):
        # self.basic_floatfund = sum(line.amount for line in self.floatfund_line)
        self.floatfund_line_count = len(self.floatfund_line)
        for rec in self:
            rec.remaining_floatfund = rec.floatfund_total - rec.used_floatfund

    existing_plan = fields.Many2many('client.program.plan', string='Existing Plan')
    plan_line = fields.One2many('edit.plan', 'edit_program_id', string='Plan')
    plan_line_count = fields.Integer(string='plan Count')

    @api.onchange('plan_line')
    def _onchange_plan_line(self):
        self.plan_line_count = len(self.plan_line)

    # @api.depends('floatfund_line')
    # def _compute_basic_floatfund(self):
    #     if self.floatfund_line:
    #         self.basic_floatfund = sum(line.amount for line in self.floatfund_line)
    #     else:
    #         self.basic_floatfund = 0

    def save_program(self):
        floatfund_lines = []
        plan_lines = []
        update_plan = []
        update_floatfund = []
        for rec in self:
            for line in rec.floatfund_line:
                update_floatfund.append(line.temp_id)
                vals_floatfund = {
                    'name': line.name,
                    'amount': line.amount,
                    'company_id': line.company_id.id,
                    'currency_id': line.currency_id.id,
                    'created_date': line.created_date,
                    'created_by': line.created_by.id,
                }
                if line.temp_id:
                    floatfund_lines.append((1, line.temp_id, vals_floatfund))
                    floatfund_lines.append((4, line.temp_id))
                else:
                    floatfund_lines.append((0, 0, vals_floatfund))
            for line in rec.plan_line:
                update_plan.append(line.temp_id)
                vals_plan = {
                    # 'program_id' : line.program_id.id,
                    'entity': line.entity,
                    'name': line.name,
                    'service': line.service,
                    'fullcover': line.fullcover,
                    'created_date': line.created_date,
                    'created_by': line.created_by.id,
                }
                if line.temp_id:
                    plan_lines.append((1, line.temp_id, vals_plan))
                    plan_lines.append((4, line.temp_id))
                else:
                    plan_lines.append((0, 0, vals_plan))
        for delete in rec.existing_floatfund:
            if delete.id not in update_floatfund:
                floatfund_lines.append((2, delete.id))
        for delete in rec.existing_plan:
            if delete.id not in update_plan:
                plan_lines.append((2, delete.id))
        if self.plan_line_count == 0:
            plan_lines = [(5, 0, 0)]
        if self.floatfund_line_count == 0:
            floatfund_lines = [(5, 0, 0)]
        # if self.plan_line_count == 0:
        #     plan_lines = [(5, 0, 0)]
        for rec in self.program_id:
            rec.name = self.name
            rec.client_branch_id = self.client_branch_id.id
            rec.claim_by = self.claim_by
            rec.floatfund = self.floatfund
            rec.floatfund_warning = self.floatfund_warning
            rec.company_id = self.company_id.id
            rec.currency_id = self.currency_id.id
            rec.basic_floatfund = self.basic_floatfund
            rec.remaining_floatfund = self.remaining_floatfund
            rec.used_floatfund = self.used_floatfund
            rec.start_date = self.start_date
            rec.end_date = self.end_date
            rec.floatfund_line = floatfund_lines
            rec.plan_line = plan_lines
