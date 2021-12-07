from odoo import _, api, fields, models

class MasterKategoriProduk(models.Model):
    _name                   = 'master.kategori.produk'
    _description            = 'Kategori Produk'
    _parent_name            = "parent_id"
    _parent_store           = True
    _rec_name               = 'kategori_produk'
    _order                  = 'name'
    _inherit                = ['mail.thread', 'mail.activity.mixin']
    
    parent_id               = fields.Many2one( 'master.kategori.produk', 
                                               string   = 'Parent Kategori Produk', 
                                               index    = True, 
                                               ondelete = 'cascade')
    
    parent_path             = fields.Char(index = True)
    
    child_id                = fields.One2many( 'master.kategori.produk', 
                                               'parent_id', 
                                               string   = 'Kategori Produk')
    
    name                    = fields.Char( string   = 'Kode Kategori Produk', 
                                           readonly = True, 
                                           default  = 'New',
                                           copy     = False)
    
    kategori_produk         = fields.Char( string   = 'Kategori Produk', 
                                           required = True,
                                           tracking = True)
    
    product_count           = fields.Integer( string    ='# Product', 
                                              compute   = '_compute_product_count', 
                                              copy      = False)
    
    # Name Get untuk Kategori Product
    def name_get(self):
        res = []
        for rec in self: res.append((rec.id, '%s' % (rec.kategori_produk)))
        return res
    
    # Sequence untuk Kategori Product
    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('master.kategori.produk.sequence')
        return super(MasterKategoriProduk, self).create(vals)

    # Menghitung Jumlah Tindakan / Layanan dari Kategori terkait
    def _compute_product_count(self):
        for rec in self:
            read_product_ids  = self.env['master.tindakan.layanan'].search([]).filtered(lambda r: rec.id in r.kategori_produk_id.ids)
            rec.product_count = len(read_product_ids.ids)