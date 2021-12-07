# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import date, timedelta
from odoo.exceptions import ValidationError

class PreAdmission(models.Model):
    _name = 'pre.admission'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
    _description = 'Preadmission'

    name = fields.Char(string='Name')
    preadmission_number = fields.Char(string='Preadmission Number')
    call_id = fields.Many2one('call.record', string='Call id')
    card_number_id = fields.Many2one('card.number', string='Card Number')
    member_id = fields.Many2one('res.partner', string='Member Name', domain=[('member','=',True)])
    member = fields.Boolean(string='Member', default=True)
    client_id = fields.Many2one('res.partner', string='Client Name', domain=[('client','=',True)])
    provider_id = fields.Many2one('res.partner', string='Provider Name', domain=[('provider','=',True)])
    receive_date = fields.Date(string='Receive Date', default=lambda self: fields.datetime.now())
    admission_date = fields.Date(string='Admission Date')
    remarks = fields.Char(string='Remarks')
    created_date = fields.Datetime(string='Created Date', default=lambda self: fields.datetime.now(), required=True, tracking=True)
    created_by = fields.Many2one('res.users', string='Created By', default=lambda self: self.env.user.id, required=True, tracking=True)

    header_id = fields.Many2one('program.plan.header', string='Services')
    header_domain_ids = fields.Many2many('program.plan.header', compute='_compute_header_domain_ids', string='Service Domain')
    
    @api.depends('member_id')
    def _compute_header_domain_ids(self):
        if self.member_id:
            self.header_domain_ids = self.member_id.program_plan_id.header_line
        else:
            self.header_domain_ids = []


    # services = fields.Selection([
    #     ('inpatient', 'Inpatient Service'),
    #     ('outpatient', 'Outpatient Service'),
    #     ('maternity', 'Maternity Service'),
    #     ('dental', 'Dental Service'),
    #     ('optical', 'Optical Service'),
    #     ('specialist', 'Specialist Doctor Service'),
    #     ('pre_inpatient', 'Pre Inpatient Service'),
    #     ('post_inpatient', 'Post Inpatient Service'),
    #     ('medical_checkup', 'Medical Check Up Service'),
    #     ('pre_post_inpatient', 'Pre & Post Inpatient  Service'),
    #     ('surgery', 'Surgery Service'),
    #     ('layanan_khusus', 'Layanan Khusus - Miscellanous'),
    #     ('rider', 'Rider'),
    # ], string='Services')
    state = fields.Selection([
        ('pending', 'Pending'),
        ('process', 'On process'),
        ('close', 'Closed'),
    ], string='Issued Status', default="pending")
    service_type = fields.Selection([
        ('cashless', 'Cashless'),
        ('reimburse', 'Reimburse'),
    ], string='Type')

    @api.model
    def retrieve_preadmission_dashboard(self):
        self.check_access_rights('read')
        # preadmission_case = self.search_count([('admission_date','=',date.today() - timedelta(days=1)),])
        preadmission_case = self.search_count([('admission_date','=',fields.Date.today() + timedelta(days=1)),])
        preadmission_process = self.search_count([('state', '=', 'process')])
        preadmission_pending = self.search_count([('state', '=', 'pending')])
        preadmission_done = self.search_count([('state', '=', 'done')])
        res = {
            "total_preadmission_case": 0,
            "total_preadmission_process": 0,
            "total_preadmission_pending": 0,
            "total_preadmission_done": 0,
        }
        res['total_preadmission_case'] = preadmission_case
        res['total_preadmission_process'] = preadmission_process
        res['total_preadmission_pending'] = preadmission_pending
        res['total_preadmission_done'] = preadmission_done
        return res

    @api.onchange('card_number_id')
    def _onchange_card_number_id(self):
        if self.card_number_id:
            member = self.env['res.partner'].search([('card_number','=',self.card_number_id.name),('member','=',True)])
            self.member_id = member
            self.client_id = member.member_client_id
        
    @api.onchange('member_id')
    def _onchange_member(self):
        if self.member and self.member_id:
            if self.card_number_id.name != self.member_id.card_number or not self.card_number_id:
                card_number = self.env['card.number'].search([('name','=',self.member_id.card_number)])
                self.card_number_id = card_number
            self.name = self.member_id.name

    def action_process(self):
        return self.write({'state': 'process'})

    def action_done(self):
        return self.write({'state': 'done'})

    def action_close(self):
        return self.write({'state': 'close'})


    @api.model
    def create(self, vals):
        vals['preadmission_number'] = self.env['ir.sequence'].next_by_code(
            'pre.admission')
        return super(PreAdmission, self).create(vals)