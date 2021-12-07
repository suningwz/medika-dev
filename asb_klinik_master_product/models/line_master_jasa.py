from odoo import _, api, fields, models

class MasterJasaLine(models.Model):
    _name           = 'master.jasa.line'
    _description    = 'Master Jasa Line'
    
    product_id              = fields.Many2one( 'product.product', 
                                               string   = 'Nama Jasa',
                                               required = True)
    
    quantity                = fields.Integer( string   = 'Qty', 
                                              default  = 1,
                                              store    = True,
                                              readonly = True)
    
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

    # Perhitungan Subtotal untuk Jasa di Tindakan / Layanan
    @api.depends('quantity','unit_price')
    def _compute_subtotal(self):
        for rec in self:
            rec.subtotal = rec.quantity * rec.unit_price