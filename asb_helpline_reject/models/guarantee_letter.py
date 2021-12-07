from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class GuaranteeLetter(models.Model):
    _inherit = 'guarantee.letter'
    _description = 'Guarantee Letter'

    def reject_reason_wizard(self):
        return {
            'name': "Reject",
            'type': 'ir.actions.act_window',
            'res_model': 'reject.reason.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_guarantee_letter_id': self.id,
                'default_claim_reject_id': self.claim_reject_id.id,
            }
        }
