# -*- coding: utf-8 -*-

# import odoo.exceptions
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import date

class EclaimInvoiceDetail(models.Model):
    _name = 'eclaim.invoice.detail'
    _description = 'Invoice Detail'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']

    # batch_number = fields.Char(string='Batch Number')
    # claim_charge = fields.Char(string='Claim Charge')
    # claim_approve = fields.Char(string='Claim Approve')
    # advanced_payment = fields.Float(string='Advanced Payment')    
    # claim_status = fields.Char(string='Claim Status')    
    # excess_charge = fields.Float(string='Excess Charge')    
    # claim_paid = fields.Float(string='Claim Paid')
    # receive_date = fields.Date(string='Receive Date')
    # admission_date = fields.Date(string='Admission Date')
    # discharge_date = fields.Date(string='Discharge Date')
    # created_time = fields.Datetime(string='Created Time')
    # provider_id = fields.Many2one('res.partner', string='Provider', domain=[('provider','=',True)])
    # diagnosa1_id = fields.Many2one('diagnosis.diagnosis', string='Diagnosa 1')
    # diagnosa2_id = fields.Many2one('diagnosis.diagnosis', string='Diagnosa 2')
    # diagnosa3_id = fields.Many2one('diagnosis.diagnosis', string='Diagnosa 3')
    # diagnosa4_id = fields.Many2one('diagnosis.diagnosis', string='Diagnosa 4')
    # total_charge = fields.Float(string='Total Charge')
    # created_date = fields.Date(string='Created Date', default=lambda self: fields.date.today(), required=True, tracking=True)
    # currency_id = fields.Many2one('res.currency', 'Currency', default=lambda self: self.env.user.company_id.currency_id.id, required=True, tracking=True)
    # billing_no = fields.Char(string='Billing No')
    # eclaim_id = fields.Many2one('eclaim.eclaim', string='Claim Number')
    # # case_id = fields.Many2one('case.monitoring', string='Case Number')
    # # client_id = fields.Many2one(related='case_id.client_id')
    # client_id = fields.Many2one('res.partner', string='Client')
    # member_name = fields.Char(string='Member Name')
    # # item_line = fields.One2many('invoice.detail.item', 'invoice_detail_id', string='Item')
    # # final_gl_line = fields.One2many('final.gl', 'invoice_detail_id', string='Claim Analyst')
    # # claim_analyst_line = fields.One2many('final.gl', 'invoice_detail_id', string='Claim Analyst')
    # client_type = fields.Selection([
    #     ('member', 'Member'),
    #     ('non_member', 'Nonmember'),
    # ], string='Client Type')
    # claim_type = fields.Selection([
    #     ('cashless', 'Cashless'),
    #     ('reimburse', 'Reimburse'),
    # ], string='Claim Type')
    # payment = fields.Selection([
    #     ('provider', 'Provider'),
    #     ('member', 'Member'),
    # ], string='Payment to')

    # @api.onchange('case_id')
    # def _onchange_case_id(self):
    #     for rec in self:
    #         if rec.case_id.member:
    #             rec.client_type = 'member'
    #         else:
    #             rec.client_type = 'non_member'
    #         rec.claim_type = rec.case_id.letter_id.service_type
    #         rec.member_name = rec.case_id.name
    #         rec.admission_date = rec.case_id.letter_id.admission_date
    #         rec.discharge_date = rec.case_id.letter_id.discharge_date
    #         rec.provider_id = rec.case_id.provider_id.id
    #         rec.created_time = rec.case_id.created_date

    #         final_gl_lines = []
    #         for line in rec.case_id.letter_id.final_gl_line:
    #             final_gl_lines.append((4,line.id))
    #         rec.final_gl_line = final_gl_lines

    
    def action_get_attachment_view(self):
        res = self.env['ir.actions.act_window']._for_xml_id('asb_eclaim_eclaim.action_attachment_eclaim')
        res['domain'] = [('res_model', '=', 'eclaim.eclaim'), ('res_id', 'in', self.ids)]
        res['context'] = {'default_res_model': 'eclaim.eclaim', 'default_res_id': self.id}
        return res

    def action_claim_benefit_check(self):
        pass

    def action_validate(self):
        pass

class InvoiceDetailItem(models.Model):
    _name = 'invoice.detail.item'
    _description = 'Invoice Detail Item'

# class FinalGl(models.Model):
#     _inherit = 'final.gl'

#     invoice_detail_id = fields.Many2one('eclaim.invoice.detail', string='Invoice Detail ID')    