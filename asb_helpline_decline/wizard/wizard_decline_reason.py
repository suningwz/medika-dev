from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class DeclineReasonWizard(models.TransientModel):
    _name = 'decline.reason.wizard'
    _description = 'Decline Reason Wizard'

    guarantee_letter_id = fields.Many2one('guarantee.letter', string='GL')
    decline_reason_id = fields.Many2one('decline.reason', string='Decline Reason')

    def button_decline(self):
        for rec in self.guarantee_letter_id:
            rec.claim_status = 'decline'
            rec.case_status = 'decline'
            rec.decline_reason_id = self.decline_reason_id.id
