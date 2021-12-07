# -*- coding: utf-8 -*-

# import odoo.exceptions
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class Ticketing(models.Model):
    _name = 'call.record'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
    _description = 'Ticketing'
    _rec_name = 'number_ticket'

    number_ticket = fields.Char(string='Number Ticket', tracking=True)
    caller_name = fields.Char(string='Caller Name', required=True, tracking=True)
    phone_number = fields.Char(string='Phone Number', tracking=True)
    patient_phone = fields.Char(string='Patient Phone', tracking=True)
    email = fields.Char(string='Email', tracking=True)
    provider_id = fields.Many2one('res.partner', string='Provider Name', domain=[('provider','=',True),('provider_type','=','provider')], tracking=True)
    member = fields.Boolean(string='Member', default=True, tracking=True)
    card_number_id = fields.Many2one('card.number', string='Card Number', tracking=True)
    member_name = fields.Char(string='Name', tracking=True)
    member_id = fields.Many2one('res.partner', string='Member Name', domain=[('member','=',True)], ondelete='restrict')
    client_id = fields.Many2one('res.partner', string='Client Name', domain=[('client','=',True)], tracking=True)
    client_branch_id = fields.Many2one('client.branch', string='Branch Name', domain=lambda self: [('client_id', '=', self.client_id)], tracking=True)
    relationship = fields.Selection([
        ('E', 'Employee'),
        ('S', 'Spouse'),
        ('C', 'Child'),
    ], string='Relationship', tracking=True)
    nik = fields.Char(string='NIK / Parent Name ', tracking=True)
    job_position = fields.Char(string='Job Position', tracking=True)
    issued_id = fields.Many2one('issued.issued', string='Issue', required=True, tracking=True)
    issued_status = fields.Selection([
        ('key', 'value')
    ], string=' Status')
    created_date = fields.Datetime(string='Created Date', default=lambda self: fields.datetime.now(), required=True, tracking=True)
    created_by = fields.Many2one('res.users', string='Created By', default=lambda self: self.env.user.id, required=True, tracking=True)
    source_id = fields.Many2one('helpline.source', string='Source',required=True, tracking=True)
    provider_check = fields.Selection([
        ('client', 'Client\'s Provider'),
        ('not_client', 'Not Client\'s Provider'),
    ], string='Provider Check', default='not_client')
    state = fields.Selection([
        ('open', 'Open'),
        ('close', 'Closed'),
    ], string='Status', default="open", tracking=True)
    caller_status = fields.Selection([
        ('provider', 'Provider'),
        ('peserta', 'Peserta'),
        ('pic_rs', 'PIC RS'),
        ('pic_perusahaan', 'PIC Perusahaan'),
        ('lainnya', 'Lainnya'),
    ], string='Caller Status', required=True, tracking=True)
    assign_to = fields.Selection([
        ('center', 'Medical Center'),
        ('onsite', 'Medical On-site'),
        ('evacuation', 'Medical Evacuation'),
        ('administration', 'Medical Administration Service'),
        ('training', 'Medical Training'),
        ('hospital', 'Medical Hospital Management'),
    ], string='Assign to', tracking=True, required="1")
    classification_member = fields.Selection(related='member_id.classification_member', string='Classification Member')
    call_record_line = fields.One2many('call.record.lines', 'call_id', string='Call Record')
    call_record_history_ids = fields.Many2many('call.record.lines', string='Ticket History')
    created_by = fields.Many2one('res.users', string='Created By', default=lambda self: self.env.user.id, required=True, tracking=True)

    def action_process(self):
        return self.write({'state': 'process'})

    def action_close(self):
        return self.write({'state': 'close'})
    


    @api.onchange('card_number_id')
    def _onchange_card_number_id(self):
        if self.card_number_id:
            member = self.env['res.partner'].search([('card_number','=',self.card_number_id.name),('member','=',True)])
            self.member_id = member
            self.client_id = member.member_client_id
            parent = self.env['res.partner'].search([('suffix_id.name','=','A'),('member_number','=',self.member_id.member_number)])
            self.nik = self.member_id.nik + " / " + parent.name
            self.relationship = self.member_id.relationship
            self.classification_member = self.member_id.classification_member
            self.client_branch_id = self.member_id.client_branch_id


    @api.onchange('member_id')
    def _onchange_member_id(self):
        if self.member and self.member_id:
            if self.card_number_id.name != self.member_id.card_number or not self.card_number_id:
                card_number = self.env['card.number'].search([('name','=',self.member_id.card_number)])
                self.card_number_id = card_number
            self.member_name = self.member_id.name

    @api.model
    def create(self, vals):
        vals['number_ticket'] = self.env['ir.sequence'].next_by_code('call.record')
        res = super(Ticketing, self).create(vals)
        if not self.call_record_line:
            ticket_record = res.env['call.record.lines'].create({
            'name': res.caller_name, 
            'caller_status_selection': res.caller_status, 
            'phone_number': res.phone_number, 
            'email': res.email, 
            'source_id': res.source_id.id, 
            'issued_id': res.issued_id.id,
            })
            res.call_record_line = [(4,ticket_record.id)]
        if res.member_id:
            ticket = self.env['call.record'].search([('member_id','=',res.member_id.id)])
            for rec in ticket.call_record_line:
                if rec not in res.call_record_history_ids:
                    res.call_record_history_ids = [(4,rec.id)]
        return res

    def call_record_history_button(self):
        if not self.member or not self.member_id:
            raise ValidationError (_("Member field is false"))
        action = self.env['ir.actions.act_window']._for_xml_id('asb_helpline_call_record.call_record_history_action_window')
        action['domain'] = [('member_id','=',self.member_id.id)]
        return action

    def call_record_dependent_button(self):
        action = self.env['ir.actions.act_window']._for_xml_id('asb_membership_member.member_relation_action')
        action['domain'] = [('member','=',True),('nik','=',self.member_id.nik)]
        action['context'] = {'default_member': True}
        return action

    def call_record_claim_button(self):
        pass

    @api.onchange('provider_id','client_id')
    def _onchange_provider_id(self):
        if self.provider_id and self.client_id:
            provider_ids = self.client_id.client_provider_ids
            provider = self.env['res.partner'].search([('id','=',self.provider_id.id)])
            if provider in provider_ids:
                self.provider_check = 'client'
            else:
                self.provider_check = 'not_client'
    
    @api.model
    def retrieve_call_record_dashboard(self):
        self.check_access_rights('read')
        call_in = self.search_count([('state', '=', 'open'),('source_id.name','=','Call In')])
        call_out = self.search_count([('state', '=', 'open'),('source_id.name','=','Call Out')])
        email_in = self.search_count([('state', '=', 'open'),('source_id.name', '=', 'Email In')])
        email_out = self.search_count([('state', '=', 'open'),('source_id.name', '=', 'Email Out')])
        whatsapp = self.search_count([('state', '=', 'open'),('source_id.name', '=', 'Whatsapp')])
        eclient = self.search_count([('state', '=', 'open'),('source_id.name', '=', 'E-Client')])
        others = self.search_count([('state', '=', 'open'),'|',('source_id','=',False),('source_id.name','not in',['Whatsapp','Call In','Call Out','Email In','Email Out'])])
        open_ticket = self.search_count([('state', '=', 'open')])
        close_ticket = self.search_count([('state', '=', 'close')])
        res = {
            "total_caller_in": 0,
            "total_caller_out": 0,
            "total_email_in": 0,
            "total_email_out": 0,
            "total_whatsapp": 0,
            "total_others": 0,
            "total_open": 0,
            "total_close": 0,
        }
        res['total_caller_in'] = call_in
        res['total_caller_out'] = call_out
        res['total_email_in'] = email_in
        res['total_email_out'] = email_out
        res['total_whatsapp'] = whatsapp
        res['total_eclient'] = eclient
        res['total_others'] = others
        res['total_open'] = open_ticket
        res['total_close'] = close_ticket
        return res

    @api.model
    def check_condition_show_dialog(self, record_id, data_changed):
        if data_changed.get('provider_id') and data_changed.get('member_id'):
            member = self.env['res.partner'].search([('id','=',data_changed['member_id'])])
            provider_ids = member.member_client_id.client_provider_ids
            provider = self.env['res.partner'].search([('id','=',data_changed['provider_id'])])
            if provider not in provider_ids:
                return True
        else:
            return False

    def write(self, vals):
        res = super(Ticketing, self).write(vals)
        # add record to call.record field call_record_history_ids on create
        if self.member_id:
            ticket = self.env['call.record'].search([('member_id','=',self.member_id.id)])
            for rec in ticket.call_record_line:
                if rec not in self.call_record_history_ids:
                    self.call_record_history_ids = [(4,rec.id)]
        return res

    @api.onchange('member')
    def _onchange_member(self):
        for rec in self:
            rec.member_id = False
            rec.nik = False
            rec.relationship = False
            rec.card_number_id = False
            rec.client_id = False
            rec.job_position = False

            client_domain = []

            if not rec.member:
                client_domain = self.env['res.partner'].search(['|',('client','=',True),('is_perusahaan','=',True)])
                return {
                    'domain' : {
                        'client_id' : [('id','in',client_domain.ids)]
                    }
                }

class TicketRecord(models.Model):
    _name = 'call.record.lines'
    _description = 'Call Record Lines'
    
    name = fields.Char(string='Caller Name', required="1")
    call_id = fields.Many2one('call.record', string='Call ID')
    caller_status = fields.Char(string='Caller Status')
    caller_status_selection = fields.Selection([
        ('provider', 'Provider'),
        ('peserta', 'Peserta'),
        ('pic_rs', 'PIC RS'),
        ('pic_perusahaan', 'PIC Perusahaan'),
        ('lainnya', 'Lainnya'),
    ], string='Caller Status', required=True, tracking=True)
    email = fields.Char(string='Email')
    phone_number = fields.Char(string='Phone Number')
    provider_id = fields.Many2one('res.partner', string='Provider')
    issued_id = fields.Many2one('issued.issued', string='Issue')
    description = fields.Char(string='Description')
    created_date = fields.Datetime(string='Created Date', default=lambda self: fields.datetime.now(), required=True, tracking=True)
    created_by = fields.Many2one('res.users', string='Created By', default=lambda self: self.env.user.id, required=True, tracking=True)
    interval = fields.Float(string='Interval')
    source_id = fields.Many2one('helpline.source', string='Source')
    source = fields.Selection([
        ('call_in', 'Call In'),
        ('call_out', 'Call Out'),
        ('email_in', 'Email In'),
        ('email_out', 'Email Out'),
        ('whatsapp', 'Whatsapp'),
    ], string='Source')
    issued_status = fields.Selection([
        ('key', 'value')
    ], string='Issued Status')

    @api.model
    def create(self, vals):
        res = super(TicketRecord, self).create(vals)
        # add record to call.record field call_record_history_ids on create
        if res.call_id.member_id:
            ticket = self.env['call.record'].search([('member_id','=',res.call_id.member_id.id)])
            for rec in ticket:
                rec.call_record_history_ids = [(4,res.id)]
        return res

class HelplineSource(models.Model):
    _name = 'helpline.source'
    _description = 'Helpline Source'
    
    name = fields.Char(string='Name')
