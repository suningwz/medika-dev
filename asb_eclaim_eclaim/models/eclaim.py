# -*- coding: utf-8 -*-

# import odoo.exceptions
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import date


class EclaimEclaim(models.Model):
    _name = 'eclaim.eclaim'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
    _description = 'Eclaim'
    _rec_name = 'receipt_number'

    receipt_number = fields.Char(string='Receipt Number')
    document_id = fields.Many2one('eclaim.document', string='Document')
    document_from = fields.Char(string='From')
    to = fields.Selection([
        ('eclaim', 'E-Claim'),
        ('mas', 'MAS'),
    ], string='To')
    case_quantity = fields.Integer(string='Case Quantity')
    invoice_number = fields.Char(string='Invoice Number')
    date = fields.Datetime(string='Date')
    notes = fields.Char(string='Notes')
    letter_ids = fields.Many2many('guarantee.letter', string='Claim Analyst')
    provider_id = fields.Many2one('res.partner', string='Provider', domain=[('provider', '=', True)])
    client_id = fields.Many2one('res.partner', string='Client', domain=[('client', '=', True),('is_perusahaan', '=', True)])
    upload_scans_ids = fields.Many2many('ir.attachment', string='Upload Scans')
    upload_date = fields.Date(string='Upload Date')
    receive_date = fields.Date(string='Receive Date')
    document_status = fields.Selection([
        ('draft', 'Draft'),
        ('submit', 'Submitted'),
        ('receive', 'Received'),
    ], string='Document Status')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('scan', 'Scanned'),
        ('batch', 'Batched'),
    ], string='Claim Status', default='draft')
    claim_type = fields.Selection([
        ('cashless', 'Cashless'),
        ('reimburse', 'Reimbursement'),
    ], string='Claim Type')

    def action_receive(self):
        for rec in self:
            rec.receive_date = date.today()
            rec.document_id.write({'state': 'receive'})
            rec.write({'document_status': 'receive'})

    def action_scan(self):
        for rec in self:
            attachment = self.env['ir.attachment'].search([('res_model', '=', 'eclaim.eclaim'), ('res_id', 'in', self.ids)])
            if not rec.letter_ids:
                raise ValidationError(_("Invoice detail is empty"))
            for line in rec.letter_ids:
                if not line.attachment_ids:
                    raise ValidationError(_("Scan not uploaded for %s") % line.claim_number)
            rec.write({'state': 'scan'})

    def action_batch(self):
        pass

    def action_get_attachment_view(self):
        res = self.env['ir.actions.act_window']._for_xml_id('asb_eclaim_eclaim.action_attachment_eclaim')
        res['domain'] = [('res_model', '=', 'eclaim.eclaim'), ('res_id', 'in', self.ids)]
        res['context'] = {'default_res_model': 'eclaim.eclaim', 'default_res_id': self.id}
        return res

    @api.onchange('claim_type', 'provider_id', 'client_id')
    def _onchange_claim_type(self):
        if self.claim_type == 'reimburse':
            self.provider_id = False
        if self.claim_type == 'cashless':
            self.client_id = False

        if self.provider_id:
            provider_domain = self.provider_id
            return {
                'domain' : {
                    'letter_ids' : [('provider_id','in',provider_domain.ids),('service_type','=',self.claim_type),('claim_status','=','release')]
                }
            }

        if self.client_id:
            client_domain = self.client_id
            return {
                'domain' : {
                    'letter_ids' : [('client_id','in',client_domain.ids),('service_type','=',self.claim_type),('claim_status','=','release')]
                }
            }
