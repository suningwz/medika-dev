from odoo import _, api, fields, models

class MasterTindakanLayananLine(models.Model):
    _name           = 'master.tindakan.layanan.line'
    _description    = 'Master Tindakan Layanan Line'
    
    master_tindakan_id      = fields.Many2one( 'product.product', 
                                                string   = 'Examination List',
                                                required = True,
                                                tracking = True)
    
    poli_unit_id            = fields.Many2one( 'master.poli.unit', 
                                             string  = 'Poli / Unit', 
                                             related = 'master_tindakan_id.poli_unit_id', 
                                             store   = True)
    
    list_price              = fields.Float( string  = 'Harga (Rp)', 
                                            digits  = (10,2), 
                                            related = 'master_tindakan_id.list_price', 
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
    
    # Mendapakan Nilai Margin ketika Harga Khusus diisi
    @api.onchange('harga_khusus')
    def compute_harga_khusus(self):
        for rec in self: rec.margin = rec.list_price - rec.harga_khusus if rec.harga_khusus else 0
                
    