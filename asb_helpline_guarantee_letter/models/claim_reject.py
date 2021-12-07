from odoo import models, fields, api, _

class ClaimRejectReason(models.Model):
    _name = 'claim.reject.reason'
    _description = 'Claim Reject Reason'
    
    name = fields.Char(string='Reject Reason')
    comment = fields.Char(string='Comment')