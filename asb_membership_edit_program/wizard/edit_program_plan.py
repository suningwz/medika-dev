from odoo import models, fields, api
from datetime import date

class ProgramPlanHeader(models.Model):
    _inherit = 'program.plan.header'
    _description = 'Program Plan Header'

    def action_edit_wizard(self):
        pass

    def action_edit_header(self):
        detail_lines = []
        existing_detail = []
        for rec in self:
            for detail in rec.detail_line:
                vals_detail_line = {
                    'temp_id' : detail._origin.id,
                    'plan_id': rec.plan_id.id,
                    'header_id' : rec._origin.id,
                    'benefit_id' : detail.benefit_id.id,
                    'cover' : detail.cover,
                    'cover' : detail.cover,
                    'max_per_visit' : detail.max_per_visit,
                    'max_day_per_year' : detail.max_day_per_year,
                    'max_per_day' : detail.max_per_day,
                    'inner_limit' : detail.inner_limit,
                    'per_day_limit' : detail.per_day_limit,
                    'currency_id' : detail.currency_id.id,
                    'created_by' : detail.created_by.id,
                    'created_date' : detail.created_date,
                }
                detail_lines.append((0, 0, vals_detail_line))
                existing_detail.append(detail._origin.id)
        return {
                'name': "Edit Header",
                'type': 'ir.actions.act_window',
                'res_model': 'edit.program.plan.header',
                'view_mode': 'form',
                'target': 'new',
                'context': {
                    'default_edit_header': True,
                    'default_header_id': self._origin.id,
                    'default_program_id': self.program_id.id,
                    'default_plan_id': self.plan_id.id,
                    'default_benefit_category_id': self.benefit_category_id.id,
                    'default_annual_limit': self.annual_limit,
                    'default_daily_limit': self.daily_limit,
                    'default_deductible': self.deductible,
                    'default_deductible_period': self.deductible_period,
                    'default_limit_selection': self.limit_selection,
                    'default_coinsurance': self.coinsurance,
                    'default_coshare': self.coshare,
                    'default_company_id': self.company_id.id,
                    'default_currency_id': self.currency_id.id,
                    'default_created_by': self.created_by.id,
                    'default_created_date': self.created_date,
                    'default_detail_line': detail_lines,
                    'default_existing_detail': existing_detail,
                    'default_is_editable': False,
                }
            }

class ClientProgramPlan(models.Model):
    _inherit = 'client.program.plan'
    _description = 'Client Program Plan'

    def refresh(self):
        pass

    def action_edit_wizard(self):
        header_lines = []
        existing_header = []
        existing_program_plan_line = []
        all_detail_lines = []
        program_plan_lines = []
        for rec in self:
            for line in rec.header_line:
                detail_lines = []
                for detail in line.detail_line:
                    vals_detail_line = {
                        'temp_id' : detail._origin.id,
                        'plan_id': line.plan_id.id,
                        'header_id' : line._origin.id,
                        'benefit_id' : detail.benefit_id.id,
                        'cover' : detail.cover,
                        'cover' : detail.cover,
                        'max_per_visit' : detail.max_per_visit,
                        'max_day_per_year' : detail.max_day_per_year,
                        'max_per_day' : detail.max_per_day,
                        'inner_limit' : detail.inner_limit,
                        'per_day_limit' : detail.per_day_limit,
                        'currency_id' : detail.currency_id.id,
                        'created_by' : detail.created_by.id,
                        'created_date' : detail.created_date,
                    }
                    # detail_lines.append((0, 0, vals_detail_line))
                    all_detail_lines.append((0, 0, vals_detail_line))
                vals_header_line = {
                    'temp_id' : line._origin.id,
                    'benefit_category_id' : line.benefit_category_id.id,
                    'plan_id': line.plan_id.id,
                    'program_id': line.program_id.id,
                    'annual_limit': line.annual_limit,
                    'daily_limit': line.daily_limit,
                    'deductible': line.deductible,
                    'deductible_period': line.deductible_period,
                    'limit_selection': line.limit_selection,
                    'coinsurance': line.coinsurance,
                    'coshare': line.coshare,
                    'company_id': line.company_id.id,
                    'currency_id': line.currency_id.id,
                    'created_date': line.created_date,
                    'created_by': line.created_by.id,
                    # 'detail_line': [],
                }
                header_lines.append((0, 0, vals_header_line))
                existing_header.append((line._origin.id))
            for line in rec.program_plan_lines:
                vals_program_plan = {
                    'temp_id' : line._origin.id,
                    'benefit_category_id' : line.benefit_category_id.id,
                    'benefit_id' : line.benefit_id.id,
                    'remarks' : line.remarks,
                    'edit_program_id' : line.program_plan_id.id,
                }
                program_plan_lines.append((0, 0, vals_program_plan))
                existing_program_plan_line.append((line._origin.id))
        return {
                'name': "Edit Plan",
                'type': 'ir.actions.act_window',
                'res_model': 'edit.program.plan',
                'view_mode': 'form',
                'target': 'new',
                'context': {
                    'default_program_id': self.program_id.id,
                    'default_program_plan_id': self._origin.id,
                    'default_entity': self.entity,
                    'default_name': self.name,
                    'default_service': self.service,
                    'default_fullcover': self.fullcover,
                    'default_created_date': self.created_date,
                    'default_created_by': self.created_by.id,
                    'default_program_plan_lines': program_plan_lines,
                    'default_header_line': header_lines,
                    'default_temp_detail_line': all_detail_lines,
                    'default_existing_header': existing_header,
                    'default_existing_program_plan_line': existing_program_plan_line,
                }
            }

    def action_add_header(self):
        return {
                'name': "Add Header",
                'type': 'ir.actions.act_window',
                'res_model': 'edit.program.plan.header',
                'view_mode': 'form',
                'target': 'new',
                'context': {
                    'default_plan_id': self._origin.id,
                    'default_program_id': self.program_id.id,
                }
            }

class EditProgramPlan(models.TransientModel):
    _name = 'edit.program.plan'
    _description = 'Edit Program Plan'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']

    
    name = fields.Char(string='Plan Name' )
    program_id = fields.Many2one('client.program', string='Program' )
    program_plan_id = fields.Many2one('client.program.plan', string='Program' )
    service = fields.Selection([
        ('reimburse', 'Reimbursement'),
        ('cashless', 'Cashless'),
        ('both', 'Both'),
    ], string='Service Type' )
    fullcover = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No'),
    ], string='Fullcover' )
    created_date = fields.Date(string='Created Date')
    created_by = fields.Many2one('res.users', string='Created By')
    entity = fields.Char(string='Entity' )
    plan_header_count = fields.Integer(compute='_compute_plan_header_count', string='Member')
    program_plan_lines = fields.One2many('edit.program.plan.line', 'edit_program_id', string='')
    existing_program_plan_line = fields.Many2many('program.plan.line', string='Existing EDC')
    program_plan_line_count = fields.Integer(compute='_compute_program_plan_line_count', string='Total Program Plan')
    existing_header = fields.Many2many('program.plan.header', string='Existing Header')
    header_line_count = fields.Integer(string='Header Count')

    @api.depends('program_plan_lines')
    def _compute_program_plan_line_count(self):
        for rec in self:
            rec.program_plan_line_count = len(rec.program_plan_lines)

    def _compute_plan_header_count(self):
        for record in self:
            record.plan_header_count = self.env['program.plan.header'].search_count([('plan_id', '=', self.id)])

    @api.onchange('header_line')
    def _onchange_header_line(self):
        self.header_line_count = len(self.header_line)
    
    header_line = fields.One2many('edit.program.plan.header', 'edit_plan_id', string='Header')
    temp_detail_line = fields.One2many('edit.header.detail', 'edit_plan_id', string='Header')

    def save_program(self):
        # program_plan_lines = [(5, 0, 0)]
        program_plan_lines = []
        update_program_plan_line = []
        header_lines = []
        update_header_line = []
        for rec in self:
            for line in rec.program_plan_lines:
                update_program_plan_line.append(line.temp_id)
                vals_program_plan = {
                    'benefit_category_id' : line.benefit_category_id.id,
                    'benefit_id' : line.benefit_id.id,
                    'remarks' : line.remarks,
                    'program_plan_id' : line.edit_program_id.id,
                }
                if line.temp_id:
                    program_plan_lines.append((1, line.temp_id, vals_program_plan))
                    program_plan_lines.append((4, line.temp_id))
                else:
                    program_plan_lines.append((0, 0, vals_program_plan))
                # program_plan_lines.append((0, 0, vals_program_plan))
            for line in rec.header_line:
                update_header_line.append(line.temp_id)
                vals_header_line = {
                    'benefit_category_id' : line.benefit_category_id.id,
                    'plan_id': line.plan_id.id,
                    'program_id': line.program_id.id,
                    'annual_limit': line.annual_limit,
                    'daily_limit': line.daily_limit,
                    'deductible': line.deductible,
                    'deductible_period': line.deductible_period,
                    'limit_selection': line.limit_selection,
                    'coinsurance': line.coinsurance,
                    'coshare': line.coshare,
                    'company_id': line.company_id.id,
                    'currency_id': line.currency_id.id,
                    'created_date': line.created_date,
                    'created_by': line.created_by.id,
                    # 'detail_line': line.detail_line.id,
                }
                if line.temp_id:
                    header_lines.append((1, line.temp_id, vals_header_line))
                    header_lines.append((4, line.temp_id))
                else:
                    header_lines.append((0, 0, vals_header_line))
            for delete in rec.existing_header:
                if delete.id not in update_header_line:
                    header_lines.append((2, delete.id))
            if rec.header_line_count == 0:
                    header_lines = [(5, 0, 0)]
            for delete in rec.existing_program_plan_line:
                if delete.id not in update_program_plan_line:
                    program_plan_lines.append((2, delete.id))
            if rec.program_plan_line_count == 0:
                    program_plan_lines = [(5, 0, 0)]
        for rec in self.program_plan_id:
            rec.name = self.name
            rec.program_id = self.program_id.id
            rec.service = self.service
            rec.fullcover = self.fullcover
            rec.entity = self.entity
            # rec.plan_header_count = self.plan_header_count
            rec.created_by = self.created_by.id
            rec.created_date = self.created_date
            rec.program_plan_lines = program_plan_lines
            # if self.program_plan_line_count == 0:
            #     rec.program_plan_lines.unlink()
            # else:
            #     rec.program_plan_lines = program_plan_lines
            rec.header_line = header_lines
                
class EditProgramPlanLine(models.TransientModel):
    _name = 'edit.program.plan.line'
    _description = 'Edit Program Plan Line'

    temp_id = fields.Integer(string='Line ID')
    benefit_category_id = fields.Many2one('benefit.master', string='Category', required=True )
    benefit_id = fields.Many2one('benefit.benefit', string='Benefit Name', required=True )
    remarks = fields.Char(string='Remarks', size=400, required=True )
    edit_program_id = fields.Many2one('edit.program.plan', string='Edit Program Plan')
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


class EditProgramPlanHeader(models.TransientModel):
    _name = 'edit.program.plan.header'
    _description = 'Edit Program Plan Header'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
    _rec_name = 'benefit_category_id'
    
    header_id = fields.Many2one('program.plan.header', string='Header')
    temp_id = fields.Integer(string='Line ID')
    benefit_category_id = fields.Many2one('benefit.master', string='Header Name')
    edit_plan_id = fields.Many2one('edit.program.plan', string='Edit Plan' )
    plan_id = fields.Many2one('client.program.plan', string='Plan Name' )
    program_id = fields.Many2one('client.program', string='Program' )
    annual_limit = fields.Float(string='Annual Limit' )
    daily_limit = fields.Float(string='Daily Limit' )
    deductible = fields.Float(string='Deductible' )
    coinsurance = fields.Float(string='Co-Insurance' )
    coshare = fields.Float(string='Co-Payment' )
    company_id = fields.Many2one('res.company', 'Company', default=lambda self: self.env.user.company_id.id, index=1 )
    currency_id = fields.Many2one('res.currency', 'Currency', default=lambda self: self.env.user.company_id.currency_id.id, required=True )
    detail_line = fields.One2many('edit.header.detail', 'edit_header_id', string='Header Detail')
    created_date = fields.Date(string='Created Date', default=lambda self: fields.datetime.now(), required=True )
    created_by = fields.Many2one('res.users', string='Created By', default=lambda self: self.env.user.id, required=True )
    edit_header = fields.Boolean(string='Edit Header', default=False)
    detail_line_count = fields.Integer(string='detail_line_count')
    existing_detail = fields.Many2many('header.detail', string='Existing')
    is_editable = fields.Boolean(string='editable')
    deductible_period = fields.Selection([
        ('onetime', 'One Time'),
        ('annual', 'Per Tahun'),
        ('visit', 'Per Visit'),
    ], string='Deductible Period')
    limit_selection = fields.Selection([
        ('individu', 'Individual'),
        ('family', 'Family'),
    ], string='Limit Option', tracking=True, ondelete='cascade')

    @api.onchange('currency_id')
    def _onchange_currency_id(self):
        for rec in self:
            for line in rec.detail_line:
                line.currency_id = rec.currency_id

    onchange_count = fields.Integer(string='Count')
    @api.onchange('benefit_category_id')
    def _onchange_benefit_category_id(self):
        detail_lines = [(5, 0, 0)]
        self.onchange_count += 1
        if self.onchange_count > 1:
            benefit_category_id = self.env['benefit.benefit'].search([('master_id', '=', self.benefit_category_id.id)])
            for line in benefit_category_id:
                vals = {
                    'benefit_id': line.id
                }
                detail_lines.append((0, 0, vals))
            self.detail_line = detail_lines

    @api.onchange('detail_line')
    def _onchange_detail_line(self):
        for rec in self:
            rec.detail_line_count = len(rec.detail_line)
    
    def save_plan_header(self):
        detail_lines = []
        header_lines = []
        for rec in self:
            for detail in rec.detail_line:
                vals_detail_line = {
                    'plan_id': rec.plan_id.id,
                    # 'header_id' : line._origin.id,
                    'benefit_id' : detail.benefit_id.id,
                    'cover' : detail.cover,
                    'cover' : detail.cover,
                    'max_per_visit' : detail.max_per_visit,
                    'max_day_per_year' : detail.max_day_per_year,
                    'max_per_day' : detail.max_per_day,
                    'inner_limit' : detail.inner_limit,
                    'per_day_limit' : detail.per_day_limit,
                    'currency_id' : detail.currency_id.id,
                    'created_by' : detail.created_by.id,
                    'created_date' : detail.created_date,
                }
                detail_lines.append((0, 0, vals_detail_line))
            vals_header_line = {
                'benefit_category_id' : rec.benefit_category_id.id,
                'plan_id': rec.plan_id.id,
                'program_id': rec.program_id.id,
                'annual_limit': rec.annual_limit,
                'daily_limit': rec.daily_limit,
                'deductible': rec.deductible,
                'deductible_period': rec.deductible_period,
                'limit_selection': rec.limit_selection,
                'coinsurance': rec.coinsurance,
                'coshare': rec.coshare,
                'company_id': rec.company_id.id,
                'currency_id': rec.currency_id.id,
                'created_date': rec.created_date,
                'created_by': rec.created_by.id,
                'detail_line': detail_lines,
            }
            header_lines.append((0, 0, vals_header_line))
        rec.plan_id.header_line = header_lines
    
    def save_header(self):
        detail_lines = []
        update_line = []
        for rec in self:
            for detail in rec.detail_line:
                update_line.append(detail.temp_id)
                vals_detail_line = {
                    'plan_id': rec.plan_id.id,
                    'header_id' : detail.header_id,
                    'benefit_id' : detail.benefit_id.id,
                    'cover' : detail.cover,
                    'cover' : detail.cover,
                    'max_per_visit' : detail.max_per_visit,
                    'max_day_per_year' : detail.max_day_per_year,
                    'max_per_day' : detail.max_per_day,
                    'inner_limit' : detail.inner_limit,
                    'per_day_limit' : detail.per_day_limit,
                    'currency_id' : detail.currency_id.id,
                    'created_by' : detail.created_by.id,
                    'created_date' : detail.created_date,
                }
                if detail.temp_id:
                    detail_lines.append((1, detail.temp_id, vals_detail_line))
                    detail_lines.append((4, detail.temp_id, vals_detail_line))
                else:
                    detail_lines.append((0, 0, vals_detail_line))
            for delete in rec.existing_detail:
                if delete.id not in update_line:
                    detail_lines.append((2, delete.id))
            if rec.detail_line_count == 0:
                    detail_lines = [(5, 0, 0)]
        for header in rec.header_id:
            header.benefit_category_id = rec.benefit_category_id.id
            header.plan_id = rec.plan_id.id
            header.program_id = rec.program_id.id
            header.annual_limit = rec.annual_limit
            header.daily_limit = rec.daily_limit
            header.deductible = rec.deductible
            header.deductible_period = rec.deductible_period
            header.limit_selection = rec.limit_selection
            header.coinsurance = rec.coinsurance
            header.coshare = rec.coshare
            header.company_id = rec.company_id.id
            header.currency_id = rec.currency_id.id
            header.detail_line = detail_lines

class EditHeaderDetail(models.TransientModel):
    _name = 'edit.header.detail'
    _description = 'Edit Header Detail'
    _rec_name = 'benefit_id'
    
    edit_plan_id = fields.Many2one('edit.program.plan', string='Edit Plan' )
    temp_id = fields.Integer(string='Line ID')
    edit_header_id = fields.Many2one('edit.program.plan.header', string='Edit' )
    header_id = fields.Many2one('program.plan.header', string='Header' )
    program_id = fields.Many2one('edit.program', related="edit_header_id.program_id", string='Program' )
    plan_id = fields.Many2one('edit.program.plan', related="edit_header_id.plan_id", string='Plan Name' )
    benefit_category_id = fields.Many2one('benefit.master', string='Header Name')
    benefit_id = fields.Many2one('benefit.benefit', string='Detail Name')
    cover = fields.Boolean(string='Cover' )
    max_per_day = fields.Integer(string='Max Per Day' )
    max_day_per_year = fields.Integer(string='Max Day Per Year' )
    max_per_visit = fields.Float(string='Max Per Visit' )
    inner_limit = fields.Float(string='Inner Limit' )
    per_day_limit = fields.Float(string='Per Day limit' )
    company_id = fields.Many2one('res.company', 'Company', default=lambda self: self.env.user.company_id.id, index=1 )
    currency_id = fields.Many2one(related='edit_header_id.currency_id')
    created_date = fields.Date(string='Created Date', default=lambda self: fields.datetime.now(), required=True )
    created_by = fields.Many2one('res.users', string='Created By', default=lambda self: self.env.user.id, required=True )
    get_benefit_id_domain = fields.Many2many('benefit.benefit', compute='_compute_get_benefit_id_domain', string='Benefit Domain')

    @api.depends('edit_header_id')
    def _compute_get_benefit_id_domain(self):
        for rec in self:
            if rec.edit_header_id.benefit_category_id:
                rec.get_benefit_id_domain = self.env['benefit.benefit'].search([('master_id', '=', self.edit_header_id.benefit_category_id.id)])
            if not rec.edit_header_id.benefit_category_id:
                rec.get_benefit_id_domain = self.env['benefit.benefit'].search([('master_id', '=', self.edit_header_id.benefit_category_id.id)])

