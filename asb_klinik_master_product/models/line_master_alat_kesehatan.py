from odoo import _, api, fields, models

class MasterAlatKesehatanLine(models.Model):
    _name           = 'master.alat.kesehatan.line'
    _description    = 'Master Alat Kesehatan Line'
    
    product_id              = fields.Many2one( 'product.product', 
                                               string   = 'Nama Alat Kesehatan',
                                               required = True)
    
    quantity                = fields.Float( string   = 'Qty', 
                                            digits   = (2,2))
    
    unit_price              = fields.Float( string   = 'Harga', 
                                            digits   = (10,2), 
                                            readonly = True, 
                                            store    = True,
                                            related  = 'product_id.standard_price')
    
    subtotal                = fields.Float( string   = 'Subtotal', 
                                            digits   = (10,2), 
                                            store    = True,
                                            compute  = '_compute_subtotal', 
                                            readonly = True)
    
    # Perhitungan Subtotal untuk Alat Kesehatan di Tindakan / Layanan
    @api.depends('quantity','unit_price')
    def _compute_subtotal(self):
        for rec in self:
            rec.subtotal = rec.quantity * rec.unit_price