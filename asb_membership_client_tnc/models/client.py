# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class Client(models.Model):
    _inherit = 'res.partner'
    
    def action_get_terms_condition_attachment_view(self):
        res = self.env['ir.actions.act_window']._for_xml_id('asb_membership_client_tnc.action_client_terms_condition_attachment')
        res['domain'] = [('res_model', '=', 'res.partner'), ('res_id', 'in', self.ids)]
        res['context'] = {'default_res_model': 'res.partner', 'default_res_id': self.id}
        return res

class Ticketing(models.Model):
    _inherit = 'call.record'
        
    def action_get_client_terms_condition_attachment_view(self):
        res = self.env['ir.actions.act_window']._for_xml_id('asb_membership_client_tnc.action_client_terms_condition_attachment')
        res['domain'] = [('res_model', '=', 'res.partner'), ('res_id', 'in', self.client_id.ids)]
        res['context'] = {'default_res_model': 'res.partner', 'default_res_id': self.client_id.id}
        return res