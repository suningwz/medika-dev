from odoo import _, api, fields, models

class ResPartner(models.Model):
    _inherit            = 'res.partner'
    _description        = 'Res Partner'
    
    poli_unit_id        = fields.Many2one( 'master.poli.unit', 
                                           string   = 'Poli Unit',
                                           tracking = True)
    