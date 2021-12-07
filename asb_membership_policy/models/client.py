# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class ResPartner(models.Model):
    _inherit = 'res.partner'
    _description = 'Res Partner'

    def _compute_policy_count(self):
        for record in self:
            record.policy_count = self.env['policy.policy'].search_count([('client_id', '=', record.id)])
    
    policy_id = fields.Many2one('policy.policy', string='Policy')
    policy_count = fields.Integer(compute='_compute_policy_count', string='Policy')

