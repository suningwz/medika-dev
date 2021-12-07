from odoo import models, fields, api, _

class ClaimPrimarySurgery(models.Model):
    _name = 'claim.primary.surgery'
    _description = 'Claim Primary Surgery'
    
    name = fields.Char(string='Name')

class ClaimSecondarySurgery(models.Model):
    _name = 'claim.secondary.surgery'
    _description = 'Claim Secondary Surgery'
    
    name = fields.Char(string='Name')
