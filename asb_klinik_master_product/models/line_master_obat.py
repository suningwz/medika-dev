from odoo import _, api, fields, models

class MasterObatLine(models.Model):
    _name           = 'master.obat.line'
    _description    = 'Master Obat Line'
    
    product_id              = fields.Many2one( 'product.product', 
                                               string   = 'Nama Obat',
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
    
    # Perhitungan Subtotal untuk Obat di Tindakan / Layanan
    @api.depends('quantity','unit_price')
    def _compute_subtotal(self):
        for rec in self:
            rec.subtotal = rec.quantity * rec.unit_price