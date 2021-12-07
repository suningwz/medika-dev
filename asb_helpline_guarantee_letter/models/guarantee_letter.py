from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import date, timedelta


class GuaranteeLetter(models.Model):
    _name = 'guarantee.letter'
    _description = 'Guarantee Letter'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
    _rec_name = 'gl_number'

    helping_id = fields.Char(string='Helping ID')

    @api.onchange('helping_id')
    def _onchange_helping_id(self):
        for rec in self:
            if not rec.helping_id:
                rec.helping_id = rec.id

    claim_number = fields.Char(string='Claim Number', tracking=True)
    gl_number = fields.Char(string='GL Number', default='-', tracking=True)
    claim_status = fields.Selection([
        ('open', 'Open'),
        ('discharge', 'Discharge Completed'),
        ('release', 'Guarantee Release'),
        ('verified', 'Verified'),
        ('completed', 'Completed'),
        ('approved', 'Approved'),
        ('paid', 'Paid'),
        ('decline', 'Declined'),
        ('reject', 'Rejected'),
    ], string='Claim Status', default="open", tracking=True)
    case_status = fields.Selection([
        ('open', 'Open'),
        ('initial', 'Initial Guarantee Release'),
        ('process', 'Case Monitoring Process'),
        ('close', 'Case Monitoring Close'),
        ('submit', 'Final Guarantee Submitted'),
        ('approved', 'Final Guarantee Approved'),
        ('discharge', 'Discharge Completed'),
        ('decline', 'Declined'),
    ], string='Case Status', default="open", tracking=True)
    service_type = fields.Selection([
        ('cashless', 'Cashless'),
        ('reimburse', 'Reimbursement'),
    ], string='Claim Type', default='cashless')
    claim_category = fields.Many2one('benefit.master', string='Claim Category', tracking=True)
    claim_reject_id = fields.Many2one('claim.reject.reason', string='Reason for claim rejection', tracking=True)
    decline_reason_id = fields.Many2one('decline.reason', string='Decline Reason', tracking=True)
    claim_source = fields.Selection([
        ('eclaim', 'E-Claim'),
        ('portal', 'Hospital Portal'),
        ('edc', 'EDC'),
    ], string='Claim Source', default='eclaim')
    created_by = fields.Many2one('res.users', string='Created By', default=lambda self: self.env.user.id, required=True, tracking=True)
    created_date = fields.Datetime(string='Created Date', default=lambda self: fields.datetime.now(), required=True, tracking=True)
    claim_due_date = fields.Integer(compute='_compute_claim_due_date', string='Claim Expired (Int)', store=True)
    claim_due_days = fields.Char(string='Claim Expired')

    @api.depends('client_id')
    def _compute_claim_due_date(self):
        for rec in self:
            if rec.client_id.claim_expiry_length and rec.admission_date:
                due_date = rec.admission_date + timedelta(days=rec.client_id.claim_expiry_length)
                difference = date.today() - due_date
                rec.claim_due_date = difference.days
                rec.claim_due_days = '%s' % rec.claim_due_date
                if rec.claim_due_date > 0:
                    rec.claim_due_days = '+%s' % rec.claim_due_date
            else:
                rec.claim_due_date = False

    name = fields.Char(string='Name', required="1", tracking=True)
    card_number_id = fields.Many2one('card.number', string='Card Number', tracking=True)
    member_id = fields.Many2one('res.partner', string='Member Name', domain=[('member', '=', True)])
    member = fields.Boolean(string='Member', default="True")
    member_number = fields.Char(string='Member Number', tracking=True)
    suffix_id = fields.Many2one('suffix.id', string='Suffix ID', tracking=True)
    dob = fields.Date(string='Date of Birth', tracking=True)
    nik = fields.Char(string='NIK / Parent Name', tracking=True)
    client_id = fields.Many2one('res.partner', string='Client Name', domain=[('client', '=', True)], tracking=True)
    client_branch_id = fields.Many2one('client.branch', string='Branch Name', domain=lambda self: [('client_id', '=', self.client_id)], tracking=True)
    provider_id = fields.Many2one('res.partner', string='Provider Name', domain=[('provider', '=', True), ('provider_type', '=', 'provider')], tracking=True)
    provider_check = fields.Selection([
        ('provider', 'Client\'s Provider'),
        ('not_provider', 'Not Client\'s Provider'),
    ], string='Provider Check', compute='_compute_provider_check')
    program_id = fields.Many2one('client.program', string='Program', tracking=True)
    plan_id = fields.Many2one('client.program.plan', string='Plan', tracking=True)
    policy_number = fields.Char(string='Policy Number')

    @api.depends('provider_id', 'client_id')
    def _compute_provider_check(self):
        for rec in self:
            rec.provider_check = False
            if rec.provider_id and rec.client_id:
                provider_ids = rec.client_id.client_provider_ids
                provider = rec.env['res.partner'].search([('id', '=', rec.provider_id.id)])
                if provider in provider_ids:
                    rec.provider_check = 'provider'
                else:
                    rec.provider_check = 'not_provider'

    join_date = fields.Date(string='Join Date', tracking=True)
    start_date = fields.Date(string='Start Date', tracking=True)
    end_date = fields.Date(string='End Date', tracking=True)
    effective_date_member = fields.Date(string='Effective Date', tracking=True)
    end_policy_date = fields.Date(string='End Policy Date', tracking=True)
    lodgement_status = fields.Selection([
        ('ok', 'Received OK'),
        ('doctor', 'Need contact treating doctor'),
        ('hospital', 'Need contact hospital'),
        ('hrd', 'Need contact HRD'),
        ('facility', 'Need contact facility (apotik, klinik)'),
    ], string='Lodgement Status', tracking=True)
    primary_surgery_id = fields.Many2one('claim.primary.surgery', string='Primary Surgery', tracking=True)
    secondary_surgery_id = fields.Many2one('claim.secondary.surgery', string='Secondary Surgery', tracking=True)
    internal_comment = fields.Char(string='Internal Comment', tracking=True)
    comment_statement = fields.Char(string='Comment Statement', tracking=True)
    number_of_item = fields.Integer(compute='_compute_number_of_item', string='Number of Item')
    checker_flagging = fields.Boolean(string='Checker', tracking=True)
    approval_payment = fields.Selection([
        ('exgratia', 'Ex Gratia'),
        ('exclusion', 'Exclusion'),
        ('hrd', 'Approval by HRD'),
    ], string='Approval Payment', tracking=True)
    approved_by = fields.Many2one('res.users', string='Created By', tracking=True)
    approval_date = fields.Date(string='Approval Date', tracking=True)

    @api.onchange('checker_flagging')
    def _onchange_checker_flagging(self):
        for rec in self:
            if rec.checker_flagging == True:
                rec.approved_by = self.env.user.id
                rec.approval_date = date.today()

                already_exist = False
                user = self.env.user
                for productivity in user.user_productivity_line:
                    if productivity.letter_id.id == rec._origin.id and name == 'Checker':
                        already_exist = True
                if not already_exist:
                    user.user_productivity_line.create({
                        'name' : 'Checker',
                        'user_id' : user.id,
                        'eclaim_category' : rec.benefit_master_id.category,
                        'letter_id' : rec._origin.id,
                        'point' : 1,
                    })

    @api.depends('final_gl_line')
    def _compute_number_of_item(self):
        for rec in self:
            rec.number_of_item = len(rec.final_gl_line)

    doctor_name = fields.Char(string='Doctor Name', tracking=True)
    policy_status = fields.Selection([
        ('A', 'Active'),
        ('N', 'Non Active'),
    ], string='Policy Status', tracking=True)
    marital_status = fields.Selection([
        ('S', 'Single'),
        ('M', 'Married'),
        ('D', 'Divorced'),
    ], string='Marital Status', tracking=True)
    relationship = fields.Selection([
        ('E', 'Employee'),
        ('S', 'Supouse'),
        ('C', 'Child'),
    ], string='Relationship', tracking=True)
    doctor_diagnosis = fields.Char(string='Doctor Diagnosis', tracking=True)
    benefit = fields.Char(string='Package Remarks', tracking=True)
    admission_date = fields.Date(string='Admission Date', tracking=True)
    up = fields.Char(string='UP', tracking=True)
    benefit_master_id = fields.Many2one('benefit.master', string='Claim Category', tracking=True)
    category = fields.Selection([
        ('ip', 'IP'),
        ('op', 'OP'),
        ('de', 'DE'),
        ('eg', 'EG'),
        ('ma', 'MA'),
        ('mcu', 'MCU'),
        ('ot', 'OT'),
    ], string='Category')
    diagnosa1_id = fields.Many2one('diagnosis.diagnosis', string='Diagnosa 1', tracking=True)
    diagnosa2_id = fields.Many2one('diagnosis.diagnosis', string='Diagnosa 2', tracking=True)
    diagnosa3_id = fields.Many2one('diagnosis.diagnosis', string='Diagnosa 3', tracking=True)
    diagnosa4_id = fields.Many2one('diagnosis.diagnosis', string='Diagnosa 4', tracking=True)
    claim_received_currency_id = fields.Many2one('res.currency', 'Currency', default=lambda self: self.env.user.company_id.currency_id.id, required=True, tracking=True)
    claim_paid_currency_id = fields.Many2one('res.currency', 'Currency', default=lambda self: self.env.user.company_id.currency_id.id, required=True, tracking=True)
    claim_received_rate = fields.Float(string='Claim Received Rate', default=1, tracking=True)
    claim_paid_rate = fields.Float(string='Claim Paid Rate', default=1, tracking=True)
    attachment_ids = fields.Many2many('ir.attachment', string='Scan', tracking=True)

    diagnosa1_check = fields.Selection([
        ('exclusion', 'Exclusion')
    ], string='Diagnosa 1 Exclusion Check')

    @api.onchange('diagnosa1_id')
    def _onchange_diagnosa1_id(self):
        if self.diagnosa1_id and self.client_id:
            exclusion_ids = self.client_id.diagnosis_ids
            if self.diagnosa1_id in exclusion_ids:
                self.diagnosa1_check = 'exclusion'
            else:
                self.diagnosa1_check = False

    diagnosa2_check = fields.Selection([
        ('exclusion', 'Exclusion')
    ], string='Diagnosa 2 Exclusion Check')

    @api.onchange('diagnosa2_id')
    def _onchange_diagnosa2_id(self):
        if self.diagnosa2_id and self.client_id:
            exclusion_ids = self.client_id.diagnosis_ids
            if self.diagnosa2_id in exclusion_ids:
                self.diagnosa2_check = 'exclusion'
            else:
                self.diagnosa2_check = False

    diagnosa3_check = fields.Selection([
        ('exclusion', 'Exclusion')
    ], string='Diagnosa 3 Exclusion Check')

    @api.onchange('diagnosa3_id')
    def _onchange_diagnosa3_id(self):
        if self.diagnosa3_id and self.client_id:
            exclusion_ids = self.client_id.diagnosis_ids
            if self.diagnosa3_id in exclusion_ids:
                self.diagnosa3_check = 'exclusion'
            else:
                self.diagnosa3_check = False

    diagnosa4_check = fields.Selection([
        ('exclusion', 'Exclusion')
    ], string='Diagnosa 4 Exclusion Check')

    @api.onchange('diagnosa4_id')
    def _onchange_diagnosa4_id(self):
        if self.diagnosa4_id and self.client_id:
            exclusion_ids = self.client_id.diagnosis_ids
            if self.diagnosa4_id in exclusion_ids:
                self.diagnosa4_check = 'exclusion'
            else:
                self.diagnosa4_check = False

    @api.onchange('diagnosa1_id', 'diagnosa2_id', 'diagnosa3_id', 'diagnosa4_id',)
    def _onchange_diagnosa_id(self):
        for rec in self:
            rec.diagnosis_ids = []
            if rec.diagnosa1_id:
                rec.diagnosis_ids += rec.diagnosa1_id
            if rec.diagnosa2_id:
                rec.diagnosis_ids += rec.diagnosa2_id
            if rec.diagnosa3_id:
                rec.diagnosis_ids += rec.diagnosa3_id
            if rec.diagnosa4_id:
                rec.diagnosis_ids += rec.diagnosa4_id

    @api.onchange('header_id')
    def _onchange_header_id_to_service(self):
        for rec in self:
            if rec.header_id:
                rec.benefit_master_id = rec.header_id.benefit_category_id
            else:
                rec.benefit_master_id = False

    @api.onchange('benefit_master_id')
    def _onchange_benefit_master_id(self):
        for rec in self:
            rec.category = rec.benefit_master_id.category

    header_id = fields.Many2one('program.plan.header', string='Claim Category (Member)')
    get_header_ids = fields.Many2many('program.plan.header', string='Service Domain')
    # preadmission_id = fields.Many2one('pre.admission', string='Preadmision ID')
    call_id = fields.Many2one('call.record', string='Call Record ID')
    preadmission = fields.Boolean(string='Preadmission Check')

    @api.onchange('header_id', 'benefit_master_id')
    def _onchange_header_id(self):
        for rec in self:
            for line in self.final_gl_line:
                line.get_detail_ids = self.env['header.detail'].search([('header_id', '=', rec.header_id.id)])
                line.get_benefit_ids = self.env['benefit.benefit'].search([('master_id', '=', rec.benefit_master_id.id)])

    @api.onchange('discharge_date')
    def _onchange_discharge_date(self):
        for rec in self:
            if rec.discharge_date:
                if rec.discharge_date < rec.admission_date:
                    raise ValidationError(_("Discharge date can not be earlier than admission date"))

    medical_record = fields.Char(string='Medical Record')
    discharge_date = fields.Date(string='Discharge Date')
    gl_date = fields.Date(string='Date of GL', default=lambda self: fields.datetime.now(), required=True, tracking=True)
    pic = fields.Char(string='PIC')
    remarks = fields.Char(string='Remarks')
    diagnosis_ids = fields.Many2many('diagnosis.diagnosis', string='Diagnosis')
    final_gl_line = fields.One2many('final.gl', 'letter_id', string='Final GL', ondelete='cascade')
    final_gl = fields.Boolean(string='Final GL')
    initial_gl = fields.Boolean(string='Initial GL')
    gender = fields.Selection([
        ('M', 'Male'),
        ('F', 'Female'),
    ], string='Gender')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submit', 'Submitted'),
        ('receive', 'Received'),
    ], string='Status', default="draft")
    company_id = fields.Many2one('res.company', 'Company', default=lambda self: self.env.user.company_id.id, index=1, tracking=True)

    def action_decline(self):
        return self.write({'claim_status': 'decline'})

    def action_reject(self):
        return self.write({'claim_status': 'decline'})

    def action_approve(self):
        return self.write({'claim_status': 'approved'})

    def action_complete(self):
        return self.write({'claim_status': 'completed'})

    def action_set_verified(self):
        return self.write({'claim_status': 'verified'})

    def action_initial_gl(self):
        for rec in self:
            if not rec.practitioner_id:
                raise ValidationError(_("Required field Practitioner Name is empty"))
            if not rec.admission_date:
                raise ValidationError(_("Required field Admission Date is empty"))
            if rec.gl_number == '-':
                rec.generate_gl_number()
            rec.case_status = 'initial'
        return self.write({'initial_gl': True})
    
    def action_process_case(self):
        return self.write({'case_status': 'process'})
    
    def action_close_case(self):
        return self.write({'case_status': 'close'})
    
    def action_submit_case(self):
        for rec in self:
            if not rec.practitioner_id:
                raise ValidationError(_("Required field Practitioner Name is required"))
            if not rec.admission_date:
                raise ValidationError(_("Required field Admission Date is required"))
            if not rec.discharge_date:
                raise ValidationError(_("Required field Discharge Date is required"))
            if not rec.final_gl_line:
                raise ValidationError(_("Claim Item is empty"))
        return self.write({
            'final_gl': True,
            'case_status': 'submit',
            })

    def action_final_gl(self):
        for rec in self:
            rec.case_status = 'approved'
            if not rec.gl_number:
                rec.generate_gl_number()
        return self.write({'final_gl': True})
    
    def action_discharge_case(self):
        return self.write({
            'case_status': 'discharge',
            'claim_status': 'release',
            })
    
    def action_revise_case(self):
        return self.write({'case_status': 'close'})

    def action_print_initial_gl(self):
        action_name = str(self.client_id.id) + ' initial GL'
        name_action = self.env['ir.actions.report'].sudo().search([('name', '=', action_name)])
        return name_action.report_action(self)

    def action_print_final_gl(self):
        for rec in self:
            if not rec.medical_record:
                raise ValidationError(_("Required field Medical Record is empty"))
            if not rec.discharge_date:
                raise ValidationError(_("Required field Discharge Date is empty"))
        action_name = str(self.client_id.id) + ' final GL'
        name_action = self.env['ir.actions.report'].sudo().search([('name', '=', action_name)])
        return name_action.report_action(self)

    @api.onchange('member')
    def _onchange_member(self):
        for rec in self:
            rec.member_id = False
            rec.header_id = False

    @api.onchange('member_id')
    def _onchange_member_id(self):
        if self.member and self.member_id:
            parent = self.env['res.partner'].search([('suffix_id.name', '=', 'A'), ('member_number', '=', self.member_id.member_number)])
            if parent:
                self.nik = self.member_id.nik + " / " + parent.name
            else:
                self.nik = self.member_id.nik
            if self.card_number_id.name != self.member_id.card_number or not self.card_number_id:
                card_number = self.env['card.number'].search([('name', '=', self.member_id.card_number)])
                self.card_number_id = card_number
            self.name = self.member_id.name
            self.client_id = self.member_id.member_client_id
            self.client_branch_id = self.member_id.client_branch_id
            self.program_id = self.member_id.program_id
            self.plan_id = self.member_id.program_plan_id
            self.member_number = self.member_id.member_number
            self.gender = self.member_id.gender
            self.dob = self.member_id.birth_date
            self.relationship = self.member_id.relationship
            self.suffix_id = self.member_id.suffix_id
            self.marital_status = self.member_id.marital_status
            self.policy_number = self.member_id.policy_number
            self.join_date = self.member_id.join_date
            self.start_date = self.member_id.start_date
            self.effective_date_member = self.member_id.effective_date_member
            self.end_date = self.member_id.end_date
            self.end_policy_date = self.member_id.end_policy_date
            self.policy_status = self.member_id.policy_status

    @api.onchange('card_number_id')
    def _onchange_card_number_id(self):
        if self.card_number_id:
            member = self.env['res.partner'].search([('card_number', '=', self.card_number_id.name), ('member', '=', True)])
            self.member_id = member

    @api.model
    def create(self, vals):
        vals['claim_number'] = self.env['ir.sequence'].next_by_code(
            'guarantee.letter.claim.number')
        return super(GuaranteeLetter, self).create(vals)

    def generate_gl_number(self):
        for rec in self:
            if rec.member:
                value = rec.benefit_master_id.category
                rec.gl_number = 'GL/' + dict(self.env['benefit.master']._fields['category'].selection)[value] + self.env['ir.sequence'].next_by_code('guarantee.letter.gl.number')
            if not rec.member:
                rec.gl_number = 'GLNM/' + dict(self.env['benefit.master']._fields['category'].selection)[value] + self.env['ir.sequence'].next_by_code('guarantee.letter.gl.number')

    final_gl_benefit = fields.Char(string='Benefit')
    final_gl_max_per_visit = fields.Float(string='Max Per Visit')
    final_gl_max_day_per_year = fields.Integer(string='Max Day Per Year')

    preadmission_state = fields.Selection([
        ('open', 'Open'),
        ('close', 'Closed'),
    ], string='Status')

    @api.model
    def retrieve_preadmission_dashboard(self):
        self.check_access_rights('read')
        # preadmission_case = self.search_count([('admission_date','=',date.today() - timedelta(days=1)),])
        preadmission_case = self.search_count([('admission_date', '=', fields.Date.today() + timedelta(days=1)), ('preadmission', '=', True)])
        preadmission_open = self.search_count([('preadmission_state', '=', 'open'), ('preadmission', '=', True)])
        preadmission_close = self.search_count([('preadmission_state', '=', 'close'), ('preadmission', '=', True)])
        res = {
            "total_preadmission_case": 0,
            "total_preadmission_open": 0,
            "total_preadmission_close": 0,
        }
        res['total_preadmission_case'] = preadmission_case
        res['total_preadmission_open'] = preadmission_open
        res['total_preadmission_close'] = preadmission_close
        return res

    @api.model
    def retrieve_guarantee_letter_dashboard(self):
        self.check_access_rights('read')
        maternity = self.search_count([('benefit_master_id.category', 'in', ['ip', 'ma'])])
        need_follow_up = self.search_count([('daily_fu', '=', False), ('claim_status', '!=', 'open')])
        followed_up = self.search_count([('daily_fu', '=', True), ('claim_status', '!=', 'open')])
        res = {
            "total_maternity": 0,
            "total_need_follow_up": 0,
            "total_followed_up": 0,
        }
        res['total_maternity'] = maternity
        res['total_need_follow_up'] = need_follow_up
        res['total_followed_up'] = followed_up
        return res

    def action_process_preadmission(self):
        return self.write({'preadmission_state': 'process'})

    def action_close_preadmission(self):
        for rec in self:
            if not rec.benefit_master_id:
                raise ValidationError("Claim Category is required to process preadmission")
        return self.write({'preadmission_state': 'close'})

    def case_history(self):
        for rec in self:
            res = self.env['ir.actions.act_window']._for_xml_id('asb_helpline_guarantee_letter.gl_case_history_smart_button')
            res['domain'] = [('member_id', '=', rec.member_id.id)]
            res['target'] = 'main'
            return res

    def guarantee_letter_relation_smart_button(self):
        action = self.env['ir.actions.act_window']._for_xml_id('asb_membership_member.member_relation_action')
        action['domain'] = [('member', '=', True), ('nik', '=', self.member_id.nik)]
        action['context'] = {'default_member': True}
        action['target'] = 'main'

        return action

    def action_get_attachment_view(self):
        for rec in self:
            if rec.attachment_ids:
                for scan in rec.attachment_ids:
                    scan.res_id = rec._origin.id
        res = self.env['ir.actions.act_window']._for_xml_id('asb_helpline_guarantee_letter.action_attachment_guarantee_letter')
        res['domain'] = [('res_model', '=', 'guarantee.letter'), ('res_id', 'in', self.ids)]
        res['context'] = {'default_res_model': 'guarantee.letter', 'default_res_id': self.id}
        res['target'] = 'main'
        return res

    currency_id = fields.Many2one('res.currency', 'Currency', default=lambda self: self.env.user.company_id.currency_id.id, required=True, tracking=True)
    amount_excess = fields.Float(compute='_compute_amount', string='Total Excess')
    amount_cover = fields.Float(compute='_compute_amount', string='Total Cover')
    amount_deductible = fields.Float(compute='_compute_amount', string='Total Deductible')
    amount_total = fields.Float(compute='_compute_amount', string='Total Amount')
    amount_approved = fields.Float(compute='_compute_amount', string='Total Approved')
    received_claim = fields.Float(string='Received Provider Claim')
    amount_difference = fields.Float(compute='_compute_amount_difference', string='Difference')

    @api.depends('received_claim', 'amount_total')
    def _compute_amount_difference(self):
        for rec in self:
            rec.amount_difference = abs(rec.received_claim - rec.amount_total)

    @api.depends(
        'final_gl_line.real_excess_amount',
        'final_gl_line.real_cover_amount',
        'final_gl_line.deductible_amount',
    )
    def _compute_amount(self):
        for rec in self:
            total_excess = 0
            total_cover = 0
            total_deductible = 0
            total_amount = 0
            total_approved = 0

            for line in rec.final_gl_line:
                total_excess += line.real_excess_amount
                total_cover += line.real_cover_amount
                total_amount += line.total_amount
                total_approved += line.approved_amount
                if line.deductible_amount > 0:
                    total_deductible += line.cover_amount - line.real_cover_amount

            rec.amount_excess = total_excess
            rec.amount_cover = total_cover
            rec.amount_total = total_amount
            rec.amount_approved = total_approved
            rec.amount_deductible = total_deductible

    def confirm_send_email(self):
        return {
            'name': "Send Email",
            'type': 'ir.actions.act_window',
            'res_model': 'confirm.send.email',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_guarantee_letter_id': self.id}
        }

    daily_fu = fields.Boolean(string='Daily Follow Up')

    def update_daily_fu(self):
        letter = self.env['guarantee.letter'].search([])
        for rec in letter:
            rec.daily_fu = False
    
    def lmi(self):
        return self.env.ref('asb_helpline_guarantee_letter.action_report_lmi').report_action(self)

    practitioner_id = fields.Many2one('helpline.master.practitioner', string='Practitioner Name', tracking=True)