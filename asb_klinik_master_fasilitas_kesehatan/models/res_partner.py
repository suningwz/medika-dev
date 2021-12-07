from odoo import _, api, fields, models

class ResPartner(models.Model):
    _inherit        = 'res.partner'
    _description    = 'Res Partner'
    
    faskes_ids      = fields.Many2many( 'master.fasilitas.kesehatan', 
                                        string   = 'Fasilitas Kesehatan',
                                        tracking = True)
    