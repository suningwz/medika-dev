from odoo import _, api, fields, models
import math, re

class ProductTemplate(models.Model):
    _inherit            = 'product.template'
    _description        = 'Product Template'
    
    @api.model
    def _get_default_direct_cost(self):
        direct_cost     = 0.0
        cost            = self.env['master.cost.allocation'].search([], limit=1)
        for data in cost:
            direct_cost = data.direct_cost_allocation
        return direct_cost
    
    @api.model
    def _get_default_fixed_cost(self):
        fixed_cost      = 0.0
        cost            = self.env['master.cost.allocation'].search([], limit=1)
        for data in cost:
            fixed_cost  = data.fixed_cost_allocation
        return fixed_cost
    
    @api.model
    def _get_default_profit_margin(self):
        profit_margin   = 0.0
        cost            = self.env['master.cost.allocation'].search([], limit=1)
        for data in cost:
            profit_margin  = data.profit_margin_allocation
        return profit_margin
    
    direct_cost                 = fields.Float( string   = 'Direct Cost (%)', 
                                                default  = _get_default_direct_cost,
                                                readonly = True,
                                                tracking = True)
    
    fixed_cost                  = fields.Float( string   = 'Fixed Cost (%)', 
                                                default  = _get_default_fixed_cost,
                                                readonly = True,
                                                tracking = True)
    
    profit_margin               = fields.Float( string   = 'Profit Margin (%)', 
                                                default  = _get_default_profit_margin,
                                                readonly = True,
                                                tracking = True)
    
    kode_lis                    = fields.Char( string   = 'Kode LIS',
                                               tracking = True,
                                               copy     = False,
                                               index    = True)
    
    kode_sap                    = fields.Char( string   = 'Kode SAP',
                                               tracking = True,
                                               copy     = False,
                                               index    = True)
    
    status                      = fields.Char( compute  = '_get_status')
    
    active                      = fields.Boolean( default = True)
    
    pengaturan_jasa             = fields.Boolean( string  = 'Pengaturan Jasa', 
                                                  default = False)
    
    semua_unit                  = fields.Boolean( string = 'Pilih Semua Poli')
    
    kategori_produk_id          = fields.Many2one( 'master.kategori.produk', 
                                                    string   = 'Kategori Produk',
                                                    tracking = True)
    
    sub_kategori_produk_id      = fields.Many2one( 'master.sub.kategori.product', 
                                                    string   = 'Sub Kategori Produk',
                                                    tracking = True)
    
    poli_unit_id                = fields.Many2one(  'master.poli.unit', 
                                                    string  = 'Default Poli / Unit', 
                                                    store   = True,
                                                    domain  = [('kategori', 'in', ['poli', 'penunjang'])])
    
    poli_unit_ids               = fields.Many2many( 'master.poli.unit', 
                                                    string  = 'Poli / Unit',
                                                    store   = True,
                                                    domain  = [('kategori', 'in', ['poli', 'penunjang'])])
    
    master_dokter_line          = fields.One2many(  'master.dokter.line', 
                                                    'product_tmpl_id', 
                                                    string   = 'Master Dokter Line')
    
    master_perawat_line         = fields.One2many(  'master.perawat.line', 
                                                    'product_tmpl_id', 
                                                    string   = 'Master Perawat Line')
    
    master_obat_line            = fields.One2many(  'master.obat.line', 
                                                    'product_tmpl_id', 
                                                    string   = 'Master Obat Line')
    
    master_alat_kesehatan_line  = fields.One2many(  'master.alat.kesehatan.line', 
                                                    'product_tmpl_id', 
                                                    string   = 'Master Alat Kesehatan Line')
    
    master_jasa_line            = fields.One2many(  'master.jasa.line', 
                                                    'product_tmpl_id', 
                                                    string   = 'Master Jasa Line')
    
    master_dokter_ids           = fields.Many2many( 'res.partner', 
                                                    compute = '_compute_dokter_ids')
    
    master_perawat_ids          = fields.Many2many( 'res.partner', 
                                                    compute = '_compute_perawat_ids')
    
    master_obat_ids              = fields.Many2many( 'product.product', 
                                                    compute = '_compute_obat_ids')
    
    master_alat_kesehatan_ids   = fields.Many2many( 'product.product', 
                                                    compute = '_compute_alkes_ids')
    
    master_jasa_ids             = fields.Many2many( 'product.product', 
                                                    compute = '_compute_jasa_ids')
    
    master_sub_kategori_ids     = fields.Many2many( 'master.sub.kategori.product', 
                                                    compute = '_compute_sub_kategori_ids')
    
    total_beban_langsung    = fields.Float( string  = 'Total Beban Langsung', 
                                            digits  = (10,2), 
                                            compute = '_compute_total_beban_langsung', 
                                            store   = True)
    
    alokasi_beban_tetap     = fields.Float( string  = 'Alokasi Beban Tetap', 
                                            digits  = (10,2), 
                                            compute = '_compute_alokasi_beban_tetap', 
                                            store   = True)
    
    total_beban_pokok       = fields.Float( string  = 'Total Beban Pokok', 
                                            digits  = (10,2), 
                                            compute = '_compute_total_beban_pokok', 
                                            store   = True)
    
    profit_margin_rupiah    = fields.Float( string  = 'Profit Margin (Rp)', 
                                            digits  = (10,2), 
                                            compute = '_compute_profit_margin_rupiah', 
                                            store   = True)
    
    harga_jual_minimum      = fields.Float( string  = 'Harga Jual Minimum', 
                                            digits  = (10,2), 
                                            compute = '_compute_harga_jual_minimum', 
                                            store   = True)
    
    total_nominal_dokter    = fields.Float(compute = '_compute_total_nominal_dokter')
    total_nominal_perawat   = fields.Float(compute = '_compute_total_nominal_perawat')
    total_nominal_obat      = fields.Float(compute = '_compute_total_nominal_obat')
    total_nominal_alkes     = fields.Float(compute = '_compute_total_nominal_alkes')
    total_nominal_jasa      = fields.Float(compute = '_compute_total_nominal_jasa')
    is_laboratorium         = fields.Boolean(string = 'Laboratorium', default = False, Store = True)
    
    @api.onchange('poli_unit_id', 'kategori_produk_id')
    def _onchange_poli_unit_id(self):
        for rec in self:
            if rec.poli_unit_id:
                if re.search('Labora', str(rec.poli_unit_id.nama_poli_unit), re.IGNORECASE):
                    rec.is_laboratorium = True
            if rec.kategori_produk_id:
                if re.search('Labora', str(rec.kategori_produk_id.kategori_produk), re.IGNORECASE):
                    rec.is_laboratorium = True
    
    # Digunakan untuk Memilih Semua Poli yang tersedia ke Tindakan / Layanan
    @api.onchange('semua_unit')
    def pilih_semua_unit(self):
        poli_unit_ids = self.env['master.poli.unit'].search([('kategori', 'in', ['poli', 'penunjang'])])
        for rec in self: rec.poli_unit_ids = [(6, 0, [data.id for data in poli_unit_ids])] if rec.semua_unit else [(5, 0, 0)]
    
    # Memasukkan Default Poli yang dipilih ke Poli Unit IDS
    @api.onchange('poli_unit_id')
    def pilih_unit(self):
        for rec in self: rec.poli_unit_ids = [(6, 0, [rec.poli_unit_id.id])] if rec.poli_unit_id else [(5, 0, 0)]
    
    # Memberikan Flags Aktif
    @api.depends('active')
    def _get_status(self):
        for rec in self: rec.status = "Aktif" if rec.active else "Tidak Aktif"
    
    # Digunakan untuk melakukan Filter Data Dokter berdasarkan Poli Unit dan Dokter agar tidak Duplicate
    @api.depends('poli_unit_id', 'poli_unit_ids', 'master_dokter_line.partner_id')
    def _compute_dokter_ids(self):
        for data in self:
            domain_dokter   = [('is_dokter','=',True)]
            data_poli_unit  = []
            
            if data.poli_unit_id:
                data_poli_unit.append(data.poli_unit_id.id)
            if data.poli_unit_ids:
                data_poli_unit += [rec for rec in data.poli_unit_ids.ids if rec not in data_poli_unit]
            if data_poli_unit:
                domain_dokter += [('poli_unit_id', 'in', data_poli_unit)]
            if data.master_dokter_line:
                domain_dokter += [('id', 'not in', [line.partner_id.id for line in data.master_dokter_line])]
                
            data.master_dokter_ids = self.env['res.partner'].search(domain_dokter)
    
    # Digunakan untuk melakukan Filter Data Perawat berdasarkan Poli Unit dan Perawat agar tidak Duplicate
    @api.depends('poli_unit_id', 'poli_unit_ids', 'master_perawat_line.partner_id')
    def _compute_perawat_ids(self):
        for data in self:
            domain_perawat  = [('is_perawat','=',True)]
            data_poli_unit  = []
            
            if data.poli_unit_id:
                data_poli_unit.append(data.poli_unit_id.id)
            if data.poli_unit_ids:
                data_poli_unit += [rec for rec in data.poli_unit_ids.ids if rec not in data_poli_unit]
            if data_poli_unit:
                domain_perawat += [('poli_unit_id', 'in', data_poli_unit)]
            if data.master_perawat_line:
                domain_perawat += [('id', 'not in', [line.partner_id.id for line in data.master_perawat_line])]
                
            data.master_perawat_ids = self.env['res.partner'].search(domain_perawat)
    
    # Digunakan untuk Filter Data Obat yang sudah dipilih agar tidak Duplicate
    @api.depends('master_obat_line.product_id')
    def _compute_obat_ids(self):
        for data in self:
            domain_product   = [('jenis_persediaan', '=', 'obat')]
            
            if data.master_obat_line:
                domain_product += [('id', 'not in', [line.product_id.id for line in data.master_obat_line])]
                
            data.master_obat_ids = self.env['product.product'].search(domain_product)
    
    # Digunakan untuk Filter Data Alat Kesehatan yang sudah dipilih agar tidak Duplicate
    @api.depends('master_alat_kesehatan_line.product_id')
    def _compute_alkes_ids(self):
        for data in self:
            domain_product   = [('jenis_persediaan', '=', 'alkes')]
            
            if data.master_alat_kesehatan_line:
                domain_product += [('id', 'not in', [line.product_id.id for line in data.master_alat_kesehatan_line])]
                
            data.master_alat_kesehatan_ids = self.env['product.product'].search(domain_product)
    
    # Digunakan untuk Filter Data Jasa yang sudah dipilih agar tidak Duplicate
    @api.depends('master_jasa_line.product_id')
    def _compute_jasa_ids(self):
        for data in self:
            domain_product   = [('is_jasa', '=', True)]
            
            if data.master_jasa_line:
                domain_product += [('id', 'not in', [line.product_id.id for line in data.master_jasa_line])]
                
            data.master_jasa_ids = self.env['product.product'].search(domain_product)
            
    @api.depends('kategori_produk_id')
    def _compute_sub_kategori_ids(self):
        for data in self:
            domain_product   = []
            
            if data.kategori_produk_id:
                domain_product += [('kategori_produk_id', '=', data.kategori_produk_id.id)]
                
            data.master_sub_kategori_ids = self.env['master.sub.kategori.product'].search(domain_product)
    
    # Mendapatkan Harga Jasa Dokter berdasarkan Jenis Tindakan
    @api.depends('master_dokter_line.persentase', 'list_price')
    def _compute_total_nominal_dokter(self):
        for rec in self:
            nominal = total_nominal_dokter = 0.0
            for data in rec.master_dokter_line:
                if data.persentase > 0.0:
                    nominal             = (data.persentase * rec.list_price) / 100
                    data.nominal        = nominal
                if data.jenis_tindakan == 'mcu':
                    total_nominal_dokter += data.nominal
            rec.total_nominal_dokter    = total_nominal_dokter

    # Mendapatkan Harga Jasa Perawat berdasarkan Jenis Tindakan
    @api.depends('master_perawat_line.persentase', 'list_price')
    def _compute_total_nominal_perawat(self):
        for rec in self:
            nominal = total_nominal_perawat = 0.0
            for data in rec.master_perawat_line:
                if data.persentase > 0.0:
                    nominal             = (data.persentase * rec.list_price) / 100
                    data.nominal        = nominal
                if data.jenis_tindakan == 'mcu':
                    total_nominal_perawat += data.nominal
            rec.total_nominal_perawat    = total_nominal_perawat
    
    # Menghitung Subtotal dari Obat
    @api.depends('master_obat_line.subtotal')
    def _compute_total_nominal_obat(self):
        for rec in self:
            rec.total_nominal_obat      = sum(rec.master_obat_line.mapped('subtotal'))
    
    # Menghitung Subtotal dari Alat Kesehatan
    @api.depends('master_alat_kesehatan_line.subtotal')
    def _compute_total_nominal_alkes(self):
        for rec in self:
            rec.total_nominal_alkes      = sum(rec.master_alat_kesehatan_line.mapped('subtotal'))
    
    # Menghitung Subtotal dari Jasa
    @api.depends('master_jasa_line.subtotal')
    def _compute_total_nominal_jasa(self):
        for rec in self:
            rec.total_nominal_jasa      = sum(rec.master_jasa_line.mapped('subtotal'))
    
    # Mendapatkan Total Beban Langsung
    @api.depends('total_nominal_dokter', 'total_nominal_perawat', 'total_nominal_obat', 'total_nominal_alkes', 'total_nominal_jasa')
    def _compute_total_beban_langsung(self):
        for rec in self:
            rec.total_beban_langsung = rec.total_nominal_dokter + rec.total_nominal_perawat + rec.total_nominal_obat + rec.total_nominal_alkes + rec.total_nominal_jasa
    
    # Mendapatkan Alokasi Beban Tetap
    @api.depends('total_beban_langsung', 'direct_cost', 'fixed_cost')
    def _compute_alokasi_beban_tetap(self):
        for rec in self:
            rec.direct_cost         = 1.0 if rec.direct_cost == 0.0 else rec.direct_cost
            rec.alokasi_beban_tetap = (rec.total_beban_langsung / rec.direct_cost) * rec.fixed_cost
    
    # Mendapatkan Total Beban Pokok
    @api.depends('total_beban_langsung', 'alokasi_beban_tetap')
    def _compute_total_beban_pokok(self):
        for rec in self:
            rec.total_beban_pokok      = rec.total_beban_langsung + rec.alokasi_beban_tetap
    
    # Mendapatkan Profit Margin Rupiah
    @api.depends('total_beban_pokok', 'profit_margin')
    def _compute_profit_margin_rupiah(self):
        for rec in self:
            rec.profit_margin_rupiah   = rec.total_beban_pokok * rec.profit_margin
    
    # Mendapatkan Harga Jual Minimum dari Tindakan / Layanan
    @api.depends('total_beban_pokok', 'profit_margin_rupiah')
    def _compute_harga_jual_minimum(self):
        for rec in self:
            rec.harga_jual_minimum     = rec.total_beban_pokok + rec.profit_margin_rupiah
    
class MasterDokterLine(models.Model):
    _inherit            = 'master.dokter.line'
    _description        = 'Master Dokter Line'
    
    product_tmpl_id     = fields.Many2one( 'product.template', 
                                            string   = 'Product Template',
                                            ondelete = 'cascade')
    
class MasterPerawatLine(models.Model):
    _inherit            = 'master.perawat.line'
    _description        = 'Master Perawat Line'
    
    product_tmpl_id     = fields.Many2one( 'product.template', 
                                            string   = 'Product Template',
                                            ondelete = 'cascade')
    
class MasterObatLine(models.Model):
    _inherit            = 'master.obat.line'
    _description        = 'Master Obat Line'
    
    product_tmpl_id     = fields.Many2one( 'product.template', 
                                            string   = 'Product Template',
                                            ondelete = 'cascade')

class MasterAlatKesehatanLine(models.Model):
    _inherit            = 'master.alat.kesehatan.line'
    _description        = 'Master Alat Kesehatan Line'
    
    product_tmpl_id     = fields.Many2one( 'product.template', 
                                            string   = 'Product Template',
                                            ondelete = 'cascade')

class MasterJasaLine(models.Model):
    _inherit            = 'master.jasa.line'
    _description        = 'Master Jasa Line'
    
    product_tmpl_id     = fields.Many2one( 'product.template', 
                                            string   = 'Product Template',
                                            ondelete = 'cascade')
    
    
    
    
    