from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class GuaranteeLetter(models.Model):
    _inherit = 'guarantee.letter'
    _description = 'Guarantee Letter'

    def decline_reason_wizard(self):
        return {
            'name': "Decline",
            'type': 'ir.actions.act_window',
            'res_model': 'decline.reason.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_guarantee_letter_id': self.id,
                'default_decline_reason_id': self.decline_reason_id.id,
            }
        }
