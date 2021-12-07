from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'
    _description = 'Res Partner'

    claim_history_count = fields.Integer(compute='_compute_claim_history_count', string='Claim History', store=True,)

    def _compute_claim_history_count(self):
        for record in self:
            record.claim_history_count = self.env['guarantee.letter'].search_count([('provider_id', '=', record.id), ('service_type', '=', 'cashless')])

    def claim_history(self):
        res = self.env['ir.actions.act_window']._for_xml_id('asb_helpline_guarantee_letter.guarantee_letter_action_window')
        res['domain'] = [('provider_id', '=', self.id), ('service_type', '=', 'cashless')]
        res['context'] = {'create': False, 'edit': False, 'delete': False}
        return res
