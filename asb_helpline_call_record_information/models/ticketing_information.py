# -*- coding: utf-8 -*-

# import odoo.exceptions
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class CallRecord(models.Model):
    _inherit = 'call.record'
    _description = 'Call Record'
    
    def action_information(self):
        action = self.env['ir.actions.act_window']._for_xml_id('asb_helpline_call_record_information.action_ticketing_information')
        action['context'] = {'default_call_id': self.id}
        return action

class TicketingInformation(models.TransientModel):
    _name = 'ticketing.information'
    _description = 'Ticketing Information'
    _rec_name = 'call_id'
    
    call_id = fields.Many2one('call.record', string='Ticketing')
    information = fields.Selection([
        ('provider', 'Provider'),
        ('product', 'Product Information'),
        ('package', 'Package MCU In House'),
        ('diagnosa', 'Diagnosa'),
        ('ambulance_rental', 'Ambulance Rental'),
        ('ambulance_rs', 'Ambulance RS'),
        ('assistance', 'Assistance'),
        ('eap', 'EAP'),
        ('embassy', 'Embassy'),
        ('specialist', 'Specialist'),
        ('benefit', 'Benefit'),
    ], string='Information', default='provider')
    provider_ids = fields.Many2many('res.partner', string='Provider')

    @api.onchange('information')
    def _onchange_information(self):
        data = []
        if self.information == 'provider':
            provider_ids = self.env['res.partner'].search([('provider','=',True)])
            for provider in provider_ids:
                data.append((4,provider.id))
            self.provider_ids = data

    def provider_information(self):
        client = self.env['res.partner'].search([('id','=',self.call_id.member_id.member_client_id.id)])
        action = self.env['ir.actions.act_window']._for_xml_id('asb_helpline_call_record_information.action_ticketing_information_provider')
        action['domain'] = [('provider','=',True),('id','in',client.client_provider_ids.ids)]
        return action

    def open_information(self):
        client = self.env['res.partner'].search([('id','=',self.call_id.member_id.member_client_id.id)])

        if not self.information:
            raise ValidationError(_("Information to show is not selected"))

        if self.information == 'provider':
            action = self.env['ir.actions.act_window']._for_xml_id('asb_helpline_call_record_information.action_ticketing_information_provider')
            # action['domain'] = [('provider','=',True),('id','in',client.client_provider_ids.ids)]
        
        if self.information == 'product':
            action = self.env['ir.actions.act_window']._for_xml_id('asb_helpline_call_record_information.action_ticketing_information_product')
            action['domain'] = [('archive','=',False)]
        
        if self.information == 'package':
            action = self.env['ir.actions.act_window']._for_xml_id('asb_helpline_call_record_information.action_ticketing_information_package_mcu')
            action['domain'] = [('in_house','=',True)]
        
        if self.information == 'diagnosa':
            action = self.env['ir.actions.act_window']._for_xml_id('asb_helpline_call_record_information.action_ticketing_information_diagnosa')
        
        if self.information == 'ambulance_rental':
            action = self.env['ir.actions.act_window']._for_xml_id('asb_helpline_call_record_information.action_ticketing_information_ambulance_rental')
        
        if self.information == 'ambulance_rs':
            action = self.env['ir.actions.act_window']._for_xml_id('asb_helpline_call_record_information.action_ticketing_information_ambulance_rs')
        
        if self.information == 'assistance':
            action = self.env['ir.actions.act_window']._for_xml_id('asb_helpline_call_record_information.action_ticketing_information_eap')
        
        if self.information == 'eap':
            action = self.env['ir.actions.act_window']._for_xml_id('asb_helpline_call_record_information.action_ticketing_information_eap')
        
        if self.information == 'embassy':
            action = self.env['ir.actions.act_window']._for_xml_id('asb_helpline_call_record_information.action_ticketing_information_embassy')
        
        if self.information == 'specialist':
            action = self.env['ir.actions.act_window']._for_xml_id('asb_helpline_call_record_information.action_ticketing_information_specialist')
        
        if self.information == 'benefit':
            action = self.env['ir.actions.act_window']._for_xml_id('asb_helpline_call_record_information.action_ticketing_information_benefit')
            benefit_domain = []
            detail_domain = self.env['header.detail'].search([('header_id','in',self.call_id.member_id.program_plan_id.header_line.ids)])
            for benefit in detail_domain:
                    benefit_domain.append(benefit.benefit_id.id)
            action['domain'] = [('id','in', benefit_domain)]

        return action