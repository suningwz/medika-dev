from odoo import models, fields, api


class Member(models.Model):
    _inherit = 'res.partner'

    def case_history(self):
        for rec in self:
            res = self.env['ir.actions.act_window']._for_xml_id('asb_helpline_guarantee_letter.gl_case_history_smart_button')
            res['domain'] = [('member_id', '=', rec._origin.id)]
            res['target'] = 'main'
            return res
