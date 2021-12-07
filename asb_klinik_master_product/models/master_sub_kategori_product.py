from odoo import _, api, fields, models

class MasterSubKategoriProduct(models.Model):
    _name           = 'master.sub.kategori.product'
    _description    = 'Master Sub Kategori Product'
    
    name                    = fields.Char(string   = 'Sub - Kategori Produk',
                                          required = True)
    
    kategori_produk_id      = fields.Many2one( 'master.kategori.produk', 
                                                string   = 'Kategori Produk',
                                                required = True)
    