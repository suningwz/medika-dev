from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class RejectReasonWizard(models.TransientModel):
    _name = 'reject.reason.wizard'
    _description = 'reject Reason Wizard'

    guarantee_letter_id = fields.Many2one('guarantee.letter', string='GL')
    claim_reject_id = fields.Many2one('claim.reject.reason', string='Reject Reason')

    def button_reject(self):
        for rec in self:
            rec.guarantee_letter_id.claim_status = 'reject'
            rec.guarantee_letter_id.claim_reject_id = rec.claim_reject_id.id
