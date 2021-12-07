from odoo import _, api, fields, models

class MasterDokumen(models.Model):
    _inherit            = 'master.dokumen'
    _description        = 'Master Dokumen'
    
    #Relasi ke Faskes
    nama_faskes                 = fields.Char( string   = 'Nama Fas. Kesehatan', 
                                               related  = 'faskes_id.nama_faskes',
                                               tracking = True)
    
    kode_faskes                 = fields.Char( string   = 'Kode Fas. Kesehatan', 
                                               related  = 'faskes_id.name',
                                               tracking = True)
    
    poli_unit_ids               = fields.Many2many( string      = 'Poli / Unit', 
                                                    related     = 'faskes_id.poli_unit_ids',
                                                    tracking    = True)
    
    penaggung_jawab_id          = fields.Many2one(  string      = 'Penanggung Jawab', 
                                                    related     = 'faskes_id.penanggung_jawab_id',
                                                    tracking    = True)
    
    state_id                = fields.Many2one( 'res.country.state', 
                                               string   = 'State', 
                                               ondelete = 'restrict', 
                                               domain   = "[('country_id', '=', country_id)]", 
                                               related  = 'faskes_id.state_id',
                                               tracking = True)
    
    country_id              = fields.Many2one( 'res.country', 
                                               string   = 'Country', 
                                               ondelete = 'restrict', 
                                               related  = 'faskes_id.country_id',
                                               tracking = True)
    
    city_id                 = fields.Many2one( 'res.state.city', 'Kabupaten', 
                                               domain   = "[('state_id', '=', state_id)]",
                                               ondelete = 'restrict',
                                               related  = 'faskes_id.city_id',
                                               tracking = True)
    
    kecamatan_id            = fields.Many2one( 'res.city.kecamatan', 'Kecamatan', 
                                               domain   = [('city_id', '=', 'city_id')],
                                               ondelete = 'restrict',
                                               related  = 'faskes_id.kecamatan_id',
                                               tracking = True)
    
    kelurahan_id            = fields.Many2one( 'res.kecamatan.kelurahan', 'Kelurahan', 
                                               domain   = "[('kecamatan_id','=',kecamatan_id)]",
                                               ondelete = 'restrict',
                                               related  = 'faskes_id.kelurahan_id',
                                               tracking = True)
    
    street                  = fields.Char( related  = 'faskes_id.street',
                                           tracking = True)
    
    street2                 = fields.Char( related  = 'faskes_id.street2',
                                           tracking = True)
    
    zip                     = fields.Char( change_default = True, 
                                           related  = 'faskes_id.zip',
                                           tracking = True)
    
    city                    = fields.Char( related  = 'faskes_id.city',
                                           tracking = True)