# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class CallRecord(models.Model):
    _inherit = 'call.record'

    def action_member_limit(self):
        for rec in self:
            rec.member_id.ticketing_member_limit()
            res = self.env['ir.actions.act_window']._for_xml_id('asb_membership_member_limit.action_call_record_member_benefit_limit')
            res['domain'] = [('member_id', '=', rec.member_id.id)]
            res['target'] = 'main'
            return res