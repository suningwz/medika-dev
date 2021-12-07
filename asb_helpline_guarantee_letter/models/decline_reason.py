from odoo import models, fields, api, _

class DeclineReason(models.Model):
    _name = 'decline.reason'
    _description = 'Decline Reason'
    
    name = fields.Char(string='Decline Reason')