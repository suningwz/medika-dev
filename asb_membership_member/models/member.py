# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from datetime import date
from odoo.exceptions import UserError, ValidationError


class Partner(models.Model):
    _inherit = 'res.partner'

    def _compute_history_count(self):
        for record in self:
            record.history_count = self.env['member.history'].search_count([('member_id', '=', self.id)])

    def _compute_member_relation_count(self):
        for record in self:
            record.member_relation_count = self.env['res.partner'].search_count([('nik', '=', self.nik)])

    member = fields.Boolean(string='Member')
    history_count = fields.Integer(compute='_compute_history_count', string='History')
    member_claim_count = fields.Integer(string='Claim')
    member_relation_count = fields.Integer(string='Relation', compute='_compute_member_relation_count')
    member_annual_limit_count = fields.Integer(string='Annual Limit')
    member_inner_limit_count = fields.Integer(string='Inner Limit')

    nik = fields.Char(string='Employee ID (NIK)',)
    card_number = fields.Char(string='Card Number')
    member_number = fields.Char(string='Member Number')
    suffix_id = fields.Many2one('suffix.id', string='Suffix ID')
    policy_number = fields.Char(string='Policy Number')

    join_date = fields.Date(string='Join Date', )
    start_date = fields.Date(string='Start Date', )
    end_date = fields.Date(string='End Date', )
    effective_date_member = fields.Date(string='Effective Date', )
    end_policy_date = fields.Date(string='End Policy Date', )

    # Page Work Information
    member_client_id = fields.Many2one('res.partner', string='Client Name', domain=[('client', '=', True)])
    division = fields.Char(string='Division')
    division_id = fields.Char(string='Division ID')
    employment_status = fields.Selection([
        ('A', 'Active'),
        ('H', 'Hold'),
        ('T', 'Terminate'),
    ], string='Employment Status', compute='_compute_employment_status')
    salary = fields.Float(string='Salary')

    # Page Private Information
    tlp_office = fields.Char(string='Telephone (Office)')
    tlp_residence = fields.Char(string='Telephone (Resident)')
    identification_no = fields.Char(string='Identification No')
    passport_no = fields.Char(string='Passport No')
    passport_country = fields.Char(string='Passport Country')
    passport_country2 = fields.Many2one('res.country', string='Passport Country')
    gender = fields.Selection([
        ('M', 'Male'),
        ('F', 'Female'),
    ], string='Gender')
    birth_date = fields.Date(string='Date of Birth', )
    marital_status = fields.Selection([
        ('S', 'Single'),
        ('M', 'Married'),
        ('D', 'Divorced'),
    ], string='Marital Status')
    relationship = fields.Selection([
        ('E', 'Employee'),
        ('S', 'Spouse'),
        ('C', 'Child'),
    ], string='Relationship')
    language = fields.Selection([
        ('M', 'Malayan '),
        ('E', 'English'),
        ('C', 'Chinese'),
        ('I', 'Indian'),
        ('O', 'Others'),
    ], string='Language')

    # Page Member Information
    employee_name = fields.Char(compute='_compute_employee_name', string='Employee Name')

    @api.depends('member_number')
    def _compute_employee_name(self):
        for rec in self:
            parent = self.env['res.partner'].search([('suffix_id.name', '=', 'A'), ('member_number', '=', rec.member_number)])
            rec.employee_name = parent.name

    record_type = fields.Selection([
        ('P', 'Principal'),
        ('D', 'Dependent'),
    ], string='Record Type')
    payor_id = fields.Char(string='Payor ID')
    rule_bpjs = fields.Selection([
        ('Y', 'Yes'),
        ('N', 'No'),
    ], string='Rule BPJS')
    bpjs_number = fields.Char(string='BPJS Number')
    bpjs_classes_room = fields.Selection([
        ('1', 'Kelas Rawat 1'),
        ('2', 'Kelas Rawat 2'),
        ('3', 'Kelas Rawat 3'),
    ], string='BPJS Classes Room')
    name_faskes_fktp = fields.Char(string='Name Faskes FKTP')
    classification_member = fields.Selection([
        ('0', 'Reguler'),
        ('1', 'VIP/VVIP'),
    ], string='Classification Member')
    pre_existing = fields.Char(string='Pre Existing')
    remarks = fields.Char(string='Remarks', size=400)
    endorsement_date = fields.Date(string='Endorsement Date', )
    member_since = fields.Date(string='Member Since', )
    policy_status = fields.Selection([
        ('A', 'Active'),
        ('N', 'Non Active'),
    ], string='Policy Status', compute='_compute_policy_status')
    member_suspend = fields.Selection([
        ('Y', 'Yes'),
        ('N', 'No'),
    ], string='Member Suspend')
    renewal_activation_date = fields.Date(string='Renewal Activation Date', )
    internal_use = fields.Char(string='Internal Use')
    option_mode = fields.Char(string='Option Mode')

    # Page Benefit Information
    ip = fields.Char(string='IP')
    op = fields.Char(string='OP')
    de = fields.Char(string='DE')
    eg = fields.Char(string='EG')
    ma = fields.Char(string='MA')
    mcu = fields.Char(string='MCU')
    ot = fields.Char(string='OT')

    # Page Plan Information
    program_id = fields.Many2one('client.program', string='Program')
    program_plan_id = fields.Many2one('client.program.plan', string='Program Plan')
    get_program_id_domain = fields.Many2many('client.program', compute='_compute_get_program_id_domain')
    get_program_plan_id_domain = fields.Many2many('client.program.plan')
    plan_information_line = fields.One2many('plan.information', 'partner_id', string='Plan Information')
    program_plan_header_line = fields.Many2many('program.plan.header', string='Program Plan Header', compute='_compute_get_program_plan_line')

    get_domain_client_branch_ids = fields.Many2many('client.branch', compute='_compute_get_domain_client_branch_ids', string='Domain')

    record_mode = fields.Integer(string='Record Mode')
    request_date = fields.Date(string='Request Date')
    print_card_date = fields.Date(string='Print Card Date')

    @api.onchange('effective_date_member', 'end_date')
    def _onchange_date(self):
        for rec in self:
            if rec.effective_date_member and rec.end_date:
                x = (rec.end_date - rec.effective_date_member).days
                if x < 0:
                    return {
                        'warning': {'title': 'Error!', 'message': 'End Date referenced before Effective Date!'},
                        'value': {'end_date': None, }
                    }
                else:
                    active = (date.today() - rec.effective_date_member).days
                    terminate = (rec.end_date - date.today()).days
                    if active < 0:
                        rec.employment_status = 'H'
                    elif active >= 0 and terminate >= 0:
                        rec.employment_status = 'A'
                    else:
                        rec.employment_status = 'T'
            else:
                rec.employment_status = False

    @api.depends('effective_date_member', 'end_date')
    def _compute_employment_status(self):
        for rec in self:
            if rec.effective_date_member and rec.end_date:
                x = (rec.end_date - rec.effective_date_member).days
                if x < 0:
                    return {
                        'warning': {'title': 'Error!', 'message': 'End Date referenced before Effective Date!'},
                        'value': {'end_date': None, }
                    }
                else:
                    active = (date.today() - rec.effective_date_member).days
                    terminate = (rec.end_date - date.today()).days
                    if active < 0:
                        rec.employment_status = 'H'
                    elif active >= 0 and terminate >= 0:
                        rec.employment_status = 'A'
                    else:
                        rec.employment_status = 'T'
            else:
                rec.employment_status = False

    @api.model
    def update_employment_status(self):
        current_date = date.today()
        for rec in self:
            rec.search([('effective_date_member', '>', current_date)]).write({'employment_status': 'H'})
            rec.search([('effective_date_member', '<=', current_date), ('end_date', '>=', current_date)]).write({'employment_status': 'A'})
            rec.search([('effective_date_member', '<', current_date), ('end_date', '<', current_date)]).write({'employment_status': 'T'})

    def write(self, vals):
        res = super().write(vals)
        for rec in self:
            if rec.member_number:
                employee = self.env['res.partner'].search([('member_number', '=', rec.member_number), ('relationship', '=', 'E')])
                family = self.env['res.partner'].search([('member_number', '=', rec.member_number), ('relationship', '!=', 'E')])
                for line in family:
                    if line.nik != employee.nik:
                        line.nik = employee.nik
                    if line.bank_id != employee.bank_id:
                        line.bank_id = employee.bank_id.id
                    if line.swift_code != employee.swift_code:
                        line.swift_code = employee.swift_code
                    if line.account_name != employee.account_name:
                        line.account_name = employee.account_name
                    if line.bank_account != employee.bank_account:
                        line.bank_account = employee.bank_account
                    if line.bank_branch != employee.bank_branch:
                        line.bank_branch = employee.bank_branch
                    # if line.member_client_id != employee.member_client_id:
                    #     line.member_client_id = employee.member_client_id.id
                    # if line.client_branch_id != employee.client_branch_id:
                    #     line.client_branch_id = employee.client_branch_id.id
                    if line.division != employee.division:
                        line.division = employee.division
                    if line.division_id != employee.division_id:
                        line.division_id = employee.division_id
                    if line.salary != employee.salary:
                        line.salary = employee.salary

        return res

    @api.onchange('client_branch_id')
    def _onchange_client_branch_id(self):
        self.program_id = False
        if self.member_number:
            sequence = str(self.member_number).split("-")
            self.member_number = sequence[0] + '-' + str(self.client_branch_id.id) + '-' + sequence[2]

    @api.depends('member_client_id')
    def _compute_get_domain_client_branch_ids(self):
        for rec in self:
            rec.get_domain_client_branch_ids = self.env['client.branch'].search([('client_id', '=', rec.member_client_id.id)])

    @api.onchange('member_client_id')
    def _onchange_member_client_id(self):
        self.program_id = False
        self.client_branch_id = False
        if self.member_number:
            sequence = str(self.member_number).split("-")
            self.member_number = str(self.member_client_id.id) + '-' + str(self.client_branch_id.id) + '-' + sequence[2]

    @api.onchange('program_plan_id')
    def _onchange_program_plan_id(self):
        for rec in self:
            plan_information_lines = [(5, 0, 0)]
            detail_line = self.env['header.detail'].search([('plan_id', '=', rec.program_plan_id.id)])
            for line in detail_line:
                vals = {
                    'program_plan_id': line.plan_id.id,
                    'benefit_id': line.benefit_id.id,
                    'header_id': line.header_id.id,
                    'cover': line.cover,
                    'max_per_visit': line.max_per_visit,
                    'max_day_per_year': line.max_day_per_year,
                    'max_per_day': line.max_per_day,
                    'inner_limit': line.inner_limit,
                    'per_day_limit': line.per_day_limit,
                }
                plan_information_lines.append((0, 0, vals))
            self.plan_information_line = plan_information_lines

    @api.depends('program_plan_id')
    def _compute_get_program_plan_line(self):
        program_plan_header_lines = [(5, 0, 0)]
        for line in self.program_plan_id.header_line:
            program_plan_header_lines.append((4, line.id))
        self.program_plan_header_line = program_plan_header_lines

    @api.depends('program_id')
    def _compute_get_program_id_domain(self):
        for rec in self:
            rec.get_program_id_domain = self.env['client.program'].search([('client_branch_id', '=', rec.client_branch_id.id)])

    @api.onchange('program_id')
    def _onchange_program_id(self):
        for rec in self:
            rec.get_program_plan_id_domain = self.env['client.program.plan'].search([('program_id', '=', rec.program_id.id)])
            rec.program_plan_id = False

    @api.model
    def create(self, vals):
        result = super(Partner, self).create(vals)
        for rec in result:
            if rec.member:
                nik = self.env["res.partner"].search([('nik', '=', rec.nik)])
                employee = self.env["res.partner"].search([('nik', '=', rec.nik), ('relationship', '=', 'E')])
                if employee:
                    if len(nik) > 1:
                        rec.member_number = employee.member_number
                        rec.bank_id = employee.bank_id.id
                        rec.swift_code = employee.swift_code
                        rec.account_name = employee.account_name
                        rec.bank_account = employee.bank_account
                        rec.bank_branch = employee.bank_branch
                        rec.member_client_id = employee.member_client_id.id
                        rec.client_branch_id = employee.client_branch_id.id
                        rec.division = employee.division
                        rec.division_id = employee.division_id
                        rec.salary = employee.salary
                    else:
                        rec.member_number = str(rec.member_client_id.id) + '-' + str(rec.client_branch_id.id) + '-' + self.env['ir.sequence'].next_by_code('member.number.sequence')
                else:
                    raise UserError("Create data with Relationship 'Employee' first!")
            return result

    @api.onchange('join_date')
    def _onchange_join_date(self):
        for rec in self:
            if rec.start_date == False:
                rec.start_date = rec.join_date
            if rec.effective_date_member == False:
                rec.effective_date_member = rec.join_date

    @api.onchange('end_date')
    def _onchange_end_date(self):
        for rec in self:
            if rec.end_policy_date == False:
                rec.end_policy_date = rec.end_date

    @api.onchange('policy_number')
    def _onchange_policy_number(self):
        for rec in self:
            if rec.policy_number:
                if not rec.policy_number.isdigit():
                    return {
                        'warning': {'title': 'Error!', 'message': 'Policy Number cannot contain characters (digits only)'},
                        'value': {'policy_number': None, }
                    }

    @api.onchange('card_number')
    def _onchange_card_number(self):
        for rec in self:
            if rec.card_number:
                if not rec.card_number.isdigit():
                    return {
                        'warning': {'title': 'Error!', 'message': 'Card Number cannot contain characters (digits only)'},
                        'value': {'card_number': None, }
                    }

    def print_card_member(self):
        num_id = self.member_client_id.id
        name = '%s Card Member' % num_id
        name_action = self.env['ir.actions.report'].sudo().search([('name', '=', name)])
        return name_action.report_action(self)

    @api.constrains('relationship')
    def check_relationship(self):
        if self.member:
            for rec in self:
                res = self.env["res.partner"].search([('nik', '=', rec.nik), ('relationship', '=', 'E')])
                if len(res) > 1:
                    raise ValidationError(_("You cannot create more than 1 Relationship of type 'Employee' in one NIK"))

    @api.constrains('suffix_id')
    def check_suffix_id(self):
        if self.member:
            for rec in self:
                res = self.env["res.partner"].search([('nik', '=', rec.nik), ('suffix_id', '=', rec.suffix_id.id)])
                if len(res) > 1:
                    raise ValidationError(_("You cannot create the same Suffix ID in one NIK!"))

    @api.constrains('card_number')
    def check_card_number(self):
        if self.member:
            for rec in self:
                res = self.env["res.partner"].search([('nik', '=', rec.nik), ('card_number', '=', rec.card_number)])
                if len(res) > 1:
                    raise ValidationError(_("You cannot create the same Card Number in one NIK!"))

    @api.constrains('record_type')
    def check_card_number(self):
        if self.member:
            for rec in self:
                res = self.env["res.partner"].search([('nik', '=', rec.nik), ('record_type', '=', 'P')])
                if len(res) > 1:
                    raise ValidationError(_("You cannot create the same Record Type of type 'Principal' in one NIK!"))

    @api.depends('employment_status')
    def _compute_policy_status(self):
        for rec in self:
            if rec.employment_status:
                if rec.employment_status != 'T':
                    rec.policy_status = 'A'
                else:
                    rec.policy_status = 'N'
            else:
                rec.policy_status = False

    def member_relation(self):
        res = self.env['ir.actions.act_window']._for_xml_id('asb_membership_member.member_relation_action')
        res['domain'] = [('member', '=', True), ('nik', '=', self.nik)]
        res['context'] = {'default_member': True}
        return res

    def action_send_card(self):
        for rec in self:
            if not rec.member:
                raise ValidationError(_("This function only for member!"))
            template_id = self.env.ref('asb_membership_member.card_member_email_template').id
            template = self.env['mail.template'].browse(template_id)
            template.send_mail(rec.id, force_send=True)
