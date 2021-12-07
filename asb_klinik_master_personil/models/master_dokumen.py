from odoo import _, api, fields, models

class MasterDokumen(models.Model):
    _inherit            = 'master.dokumen'
    _description        = 'Master Dokumen'
    
    #Relasi ke Partner
    display_name                = fields.Char( string   = 'Nama Personil',
                                               related  = 'partner_id.display_name')
    
    kode_personil               = fields.Char( string   = 'Kode Personil', 
                                               related  = 'partner_id.kode',
                                               tracking = True)
    
    unit_kerja                  = fields.Selection( string      = 'Unit Kerja', 
                                                    related     = 'partner_id.unit_kerja',
                                                    tracking    = True)
    
    jenis_kelamin               = fields.Selection( string      = 'Jenis Kelamin',
                                                    related     = 'partner_id.jenis_kelamin',
                                                    tracking    = True)
    
    poli_unit_id                = fields.Many2one( string   = 'Poli / Unit', 
                                                   related  = 'partner_id.poli_unit_id',
                                                   tracking = True)
    
    master_ketenagaan_id        = fields.Many2one( string   = 'Bidang Ketenagaan', 
                                                   related  = 'partner_id.master_ketenagaan_id',
                                                   tracking = True)
    
    faskes_ids                  = fields.Many2many( string   = 'Fasilitas Kesehatan', 
                                                    related  = 'partner_id.faskes_ids',
                                                    tracking = True)
    