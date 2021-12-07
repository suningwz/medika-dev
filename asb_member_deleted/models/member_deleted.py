from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from datetime import date, datetime

class MemberDeleted(models.Model):
    _name = 'member.deleted'
    _description = 'Member Deleted'

    name = fields.Char(string='Name')
    nik = fields.Char(string='Employee ID (NIK)' )
    card_number = fields.Char(string='Card Number' )
    member_number = fields.Char(string='Member Number' )
    suffix_id = fields.Many2one('suffix.id', string='Suffix ID' )
    policy_number = fields.Char(string='Policy Number' )

    join_date = fields.Date(string='Join Date' , )
    start_date = fields.Date(string='Start Date' , )
    end_date = fields.Date(string='End Date' , )
    effective_date_member = fields.Date(string='Effective Date' , )
    end_policy_date = fields.Date(string='End Policy Date' , )

    #Page Work Information
    member_client_id = fields.Many2one('res.partner', string='Company ID', domain=[('client','=',True)] )
    client_branch_id = fields.Many2one('client.branch', string='Client Branch', tracking=True)
    division = fields.Char(string='Division' )
    division_id = fields.Char(string='Division ID' )
    employment_status = fields.Selection([
        ('A', 'Active'),
        ('H', 'Hold'),
        ('T', 'Terminate'),
    ], string='Employment Status' )
    salary = fields.Float(string='Salary' )

    #Page Private Information
    country_id = fields.Many2one('res.country', string='Country', ondelete='restrict' )
    state_id = fields.Many2one('res.country.state', "State", domain="[('country_id','=',country_id)]")
    city_id = fields.Many2one('res.state.city', 'Kabupaten', domain="[('state_id','=',state_id)]")
    kecamatan_id = fields.Many2one('res.city.kecamatan', 'Kecamatan', domain=[('city_id', '=', 'city_id')])
    kelurahan_id = fields.Many2one('res.kecamatan.kelurahan', 'Kelurahan', domain="[('kecamatan_id','=',kecamatan_id)]")
    street = fields.Char(string='Street' )
    street2 = fields.Char(string='Street2' )
    zip = fields.Char(change_default=True )
    mobile = fields.Char(string='Mobile')
    email = fields.Char('Email')
    tlp_office = fields.Char(string='Telephone (Office)' )
    tlp_residence = fields.Char(string='Telephone (Resident)' )
    identification_no = fields.Char(string='Identification No' )
    passport_no = fields.Char(string='Passport No' )
    passport_country = fields.Char(string='Passport Country')
    passport_country2 = fields.Many2one('res.country',string='Passport Country' )
    gender = fields.Selection([
        ('M', 'Male'),
        ('F', 'Female'),
    ], string='Gender' )
    birth_date = fields.Date(string='Date of Birth')
    marital_status = fields.Selection([
        ('S', 'Single'),
        ('M', 'Married'),
        ('D', 'Divorced'),
    ], string='Marital Status' )
    relationship = fields.Selection([
        ('E', 'Employee'),
        ('S', 'Supouse'),
        ('C', 'Child'),
    ], string='Relationship' )
    language = fields.Selection([
        ('M', 'Malayan '),
        ('E', 'English'),
        ('C', 'Chinese'),
        ('I', 'Indian'),
        ('O', 'Others'),
    ], string='Language')

    #bank account
    bank_id = fields.Many2one('bank.master', string='Bank')
    bank_account = fields.Char(string='Bank Account' )
    bank_branch = fields.Char(string='Bank Branch' )
    account_name = fields.Char(string='Account Name' )
    swift_code = fields.Char(string='SWIFT code' )


    #Page Member Information
    record_type = fields.Selection([
        ('P', 'Principal'),
        ('D', 'Dependent'),
    ], string='Record Type' )
    payor_id = fields.Char(string='Payor ID')
    rule_bpjs = fields.Selection([
        ('Y', 'Yes'),
        ('N', 'No'),
    ], string='Rule BPJS' )
    bpjs_number = fields.Char(string='BPJS Number' )
    bpjs_classes_room = fields.Selection([
        ('1', 'Kelas Rawat 1'),
        ('2', 'Kelas Rawat 2'),
        ('3', 'Kelas Rawat 3'),
    ], string='BPJS Classes Room' )
    name_faskes_fktp = fields.Char(string='Name Faskes FKTP' )
    classification_member = fields.Selection([
        ('0', 'Reguler'),
        ('1', 'VIP/VVIP'),
    ], string='Classification Member' )
    pre_existing = fields.Char(string='Pre Existing' )
    remarks = fields.Char(string='Remarks' , size=400 )
    endorsement_date = fields.Date(string='Endorsement Date')
    member_since = fields.Date(string='Member Since')
    policy_status = fields.Selection([
        ('A', 'Active'),
        ('N', 'Non Active'),
    ], string='Policy Status' )
    member_suspend = fields.Selection([
        ('Y', 'Yes'),
        ('N', 'No'),
    ], string='Member Suspend' )
    renewal_activation_date = fields.Date(string='Renewal Activation Date')
    internal_use = fields.Char(string='Internal Use' )
    option_mode = fields.Char(string='Option Mode' )

    #Page Benefit Information
    ip = fields.Char(string='IP' )
    op = fields.Char(string='OP' )
    de = fields.Char(string='DE' )
    eg = fields.Char(string='EG' )
    ma = fields.Char(string='MA' )
    mcu = fields.Char(string='MCU' )
    ot = fields.Char(string='OT' )

    #Page Plan Information
    program_id = fields.Many2one('client.program', string='Program')
    program_plan_id = fields.Many2one('client.program.plan', string='Program Plan')
    get_program_id_domain = fields.Many2many('client.program')    
    get_program_plan_id_domain = fields.Many2many('client.program.plan')
    # plan_information_line = fields.One2many('plan.information', 'partner_id', string='Plan Information')
    program_plan_header_line = fields.Many2many('program.plan.header', string='Program Plan Header', compute='_compute_get_program_plan_line')
    
    @api.depends('program_plan_id')
    def _compute_get_program_plan_line(self):
        program_plan_header_lines = [(5,0,0)]
        for line in self.program_plan_id.header_line:
            program_plan_header_lines.append((4,line.id))
        self.program_plan_header_line = program_plan_header_lines
    