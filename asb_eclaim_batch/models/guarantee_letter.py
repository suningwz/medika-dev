# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class GuaranteeLetter(models.Model):
    _inherit = 'guarantee.letter'

    batch_id = fields.Many2one('eclaim.batch', string='Batch No')
    batch_approve = fields.Boolean(string='Batch Approved')
    receive_date = fields.Date(string='Receive Date')

    def open_gl(self):
        view_id = self.env.ref('asb_helpline_guarantee_letter.guarantee_letter_view_form').id
        return {
            'name': 'Claim Analyst',
            'view_type': 'form',
            'view_mode': 'tree',
            'views': [(view_id, 'form')],
            'res_model': 'guarantee.letter',
            'view_id': view_id,
            'type': 'ir.actions.act_window',
            'res_id': self.id,
            'target': 'new',
            'context': "{'create': False}",
        }
