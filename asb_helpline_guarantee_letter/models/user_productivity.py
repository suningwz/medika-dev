from odoo import models, fields, api


class UserProductivity(models.Model):
    _inherit = 'user.productivity'
    _description = 'User Productivity'
    
    letter_id = fields.Many2one('guarantee.letter', string='Letter ID')