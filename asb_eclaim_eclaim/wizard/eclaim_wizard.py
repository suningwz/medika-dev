# -*- coding: utf-8 -*-

# import odoo.exceptions
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class EclaimInvoiceWizard(models.Model):
    _name = 'eclaim.invoice.wizard'
    _description = 'Eclaim Invoice Wizard'
    
    # name = fields.Char(string='Add Invoice Detail')
    # case_ids = fields.Many2many('case.monitoring', string='Case Number',)
    # provider_id = fields.Many2one('res.partner', string='Provider')
    # eclaim_id = fields.Many2one('eclaim.eclaim', string='E-Claim')
    # case_domain_ids = fields.Many2many('res.partner', compute='_compute_case_domain_ids', string='Case Monitoring Domain')
    
    # @api.depends('provider_id')
    # def _compute_case_domain_ids(self):
    #     if self.provider_id:
    #         self.case_domain_ids = self.provider_id
    #     else:
    #         self.case_domain_ids = self.env['res.partner'].search([('provider','=',True)])
    
    # @api.onchange('eclaim_id')
    # def _onchange_eclaim_id(self):
    #     if self.eclaim_id.provider_id:
    #         self.provider_id = self.eclaim_id.provider_id 

    # def add_invoice_detail(self):
    #     lines = []
    #     member = 'non_member'
    #     for case in self.case_ids:
    #         if case.member:
    #             member = 'member'
    #         vals = {
    #             'case_id' : case.id,
    #             'member_name' : case.name,
    #             'client_type' : member,
    #             'claim_type' : case.letter_id.service_type,
    #         }
    #         lines.append((0, 0, vals))
    #     self.eclaim_id.invoice_detail_line = lines