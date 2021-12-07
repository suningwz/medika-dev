# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class GuaranteeLetter(models.Model):
    _inherit = 'guarantee.letter'

    def action_member_limit(self):
        for rec in self:
            rec.member_id.refresh_benefit()
            res = self.env['ir.actions.act_window']._for_xml_id('asb_membership_member_limit.action_gl_member_benefit_limit')
            res['domain'] = [('member_id', '=', rec.member_id.id)]
            return res