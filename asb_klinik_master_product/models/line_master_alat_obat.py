from odoo import _, api, fields, models

class MasterAlatObatLine(models.Model):
    _name           = 'master.alat.obat.line'
    _description    = 'Master Alat Kesehatan & Obat Line'
    
    master_alat_obat_id     = fields.Many2one( 'product.product', 
                                                string   = 'Product',
                                                required = True,
                                                tracking = True)
    
    jenis_persediaan        = fields.Selection( related     = 'master_alat_obat_id.jenis_persediaan', 
                                                store       = True,  
                                                string      = 'Jenis Persediaan')
    
    list_price              = fields.Float( string  = 'Harga (Rp)', 
                                            digits  = (10,2), 
                                            related = 'master_alat_obat_id.list_price', 
                                            store   = True)
    
    margin                  = fields.Float( string  = 'Margin (Rp)', 
                                            digits  = (10,2), 
                                            store   = True)
    
    harga_khusus            = fields.Float( string  = 'Harga Khusus (Rp)', 
                                            digits  = (10,2), 
                                            store   = True)
    
    # Mendapatkan Harga Khusus ketika Margin diisi
    @api.onchange('margin')
    def compute_margin(self):
        for rec in self: rec.harga_khusus = rec.list_price - rec.margin if rec.margin else 0
    
    # Mendapatkan Nilai Margin ketika Harga Khusus diisi
    @api.onchange('harga_khusus')
    def compute_harga_khusus(self):
        for rec in self: rec.margin = rec.list_price - rec.harga_khusus if rec.harga_khusus else 0