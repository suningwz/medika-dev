from odoo import _, api, fields, models

class ResPartner(models.Model):
    _inherit            = 'res.partner'
    _description        = 'Res Partner'
    
    master_ketenagaan_id = fields.Many2one( 'master.ketenagaan', 
                                            string   = 'Bidang Ketenagaan',
                                            tracking = True)
    