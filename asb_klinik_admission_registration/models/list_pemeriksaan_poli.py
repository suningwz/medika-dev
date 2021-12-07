from odoo import _, api, fields, models

class ListPemeriksaanPoli(models.Model):
    _name               = 'list.pemeriksaan.poli'
    _description        = 'List Pemeriksaan Poli'
    
    poli_unit_id        = fields.Many2one( 'master.poli.unit', 
                                           string = 'Poli / Unit')
    
    status              = fields.Char(string  = 'Status Pemeriksaan',
                                      store   = True)
    