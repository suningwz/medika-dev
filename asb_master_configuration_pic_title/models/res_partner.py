from odoo import _, api, fields, models

class ResPartner(models.Model):
    _inherit        = 'res.partner'
    _description    = 'Res Partner'
    
    client_title_id = fields.Many2one('pic.title', string = 'PIC Title', domain = [('type', '=', 'client')])
    