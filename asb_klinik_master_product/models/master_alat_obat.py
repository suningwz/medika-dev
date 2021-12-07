from odoo import _, api, fields, models
import math

class ProductTemplate(models.Model):
    _inherit                = 'product.template'
    _description            = 'Product Template'
    
    @api.model
    def _get_default_profit_margin_product(self):
        cost = self.env['master.cost.allocation'].search([], limit=1)
        for data in cost: 
            profit_margin_product = data.profit_margin_product if data.profit_margin_product else 0
            return profit_margin_product
    
    @api.model
    def _get_default_ppn_product(self):
        cost = self.env['master.cost.allocation'].search([], limit=1)
        for data in cost: 
            ppn_product = data.ppn_product if data.ppn_product else 0
            return ppn_product
    
    profit_margin_product       = fields.Float( string   = 'Profit Margin (%)', 
                                                default  = _get_default_profit_margin_product,
                                                store    = True,
                                                readonly = True,
                                                tracking = True)
    
    ppn_product                 = fields.Float(  string   = 'PPn Product (%)', 
                                                 default  = _get_default_ppn_product,
                                                 store    = True,
                                                 readonly = True,
                                                 tracking = True)
    
    type                        = fields.Selection( string  = 'Product Type')
    
    bentuk_persediaan_id        = fields.Many2one( 'master.bentuk.persediaan', 
                                                   string = 'Bentuk Persediaan')
    
    is_alat_obat                = fields.Boolean( string  = 'Alat Kesehatan & Obat', 
                                                  default = False)
    
    is_jasa                     = fields.Boolean( string  = 'Jasa',
                                                  default = False)
    
    is_service                  = fields.Boolean( string  = 'Service',
                                                  default = False)
    
    is_product                  = fields.Boolean( string  = 'Product Klinik',
                                                  default = False)
    
    nama_generik                = fields.Char(  string      = 'Nama Generik',
                                                tracking    = True)
    
    kelompok_obat               = fields.Selection( [
                                                        ('generik', 'Obat Generik'),
                                                        ('nongenerik', 'Obat Non Generik'),
                                                        ('lainnya', 'Lainnya'),
                                                    ],  string   = 'Kelompok Obat',
                                                        tracking = True)
    
    golongan_obat               = fields.Selection( [
                                                        ('narkotika', 'Narkotika'), 
                                                        ('biasa', 'Obat Biasa'), 
                                                        ('keras', 'Obat Keras'),
                                                        ('psikotropika', 'Psikotropika'),
                                                        ('lainnya', 'Lainnya'),   
                                                    ],  string   = 'Golongan Obat',
                                                        tracking = True)

    jenis_persediaan            = fields.Selection( [
                                                        ('obat', 'Obat'),
                                                        ('alkes', 'Alat Kesehatan'),
                                                    ],  string   = 'Jenis Persediaan',
                                                        tracking = True)
    
    company_id                  = fields.Many2one( 'res.company', 'Company',
                                                    default = lambda self: self.env.user.company_id.id, 
                                                    index   = 1)
    
    harga_jual_product          = fields.Float( string  = 'Harga Jual Minimum', 
                                                digits  = (10,2), 
                                                store   = True,
                                                compute = '_compute_harga_jual_product')
    
    harga_jual_product_fix      = fields.Float( string  = 'Harga Jual Product', 
                                                digits  = (10,2),  
                                                store   = True,
                                                compute = '_compute_harga_jual_product_fix')
    
    # Mengaktifkan Warning ketika Pemilihan Tipe Produk : Service di Alat Kesehatan atau Obat
    @api.onchange('type')
    def _onchange_show_data(self):
        for rec in self:
            if rec.type == 'service' and rec.is_alat_obat:
                rec.type = 'product'
                return{ 'warning':{
                    'title': "Invalid Product",
                    'message': "Tipe Product yang dipilih tidak Relevan pada Menu ini"
                }}
    
    # Menghitung Harga Jual Minimum dari Obat dan Alat Kesehatan
    @api.depends('standard_price', 'profit_margin_product', 'ppn_product')
    def _compute_harga_jual_product(self):
        for rec in self:
            harga_jual_product_fix      = rec.standard_price + (rec.standard_price * rec.profit_margin_product)
            rec.harga_jual_product      = harga_jual_product_fix + (harga_jual_product_fix * rec.ppn_product)
    
    # Menghitung Harga Jual Fix dari Obat dan Alat Kesehatan
    @api.depends('harga_jual_product', 'is_alat_obat')
    def _compute_harga_jual_product_fix(self):
        for rec in self:
            if rec.is_alat_obat:
                rec.harga_jual_product_fix      = round((math.ceil(rec.harga_jual_product) + 50), -2)
                rec.list_price                  = rec.harga_jual_product_fix