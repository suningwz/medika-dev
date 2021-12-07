from odoo import _, api, fields, models

class MasterPricelist(models.Model):
    _name                   = 'master.pricelist'
    _description            = 'Master Pricelist'
    _order                  = 'perusahaan_id'
    _inherit                = ['mail.thread', 'mail.activity.mixin']
    
    name                    = fields.Char( string  = 'Nama Perusahaan',
                                           related = 'perusahaan_id.name')
    
    perusahaan_id           = fields.Many2one( 'res.partner', 
                                                string   = 'Perusahaan', 
                                                domain   = [('is_company', '=', True), '|', '&', ('is_perusahaan', '=', True), ('status_perusahaan', '=', 'approved'), '&', ('client', '=', True), ('client_state', '=', 'enabled')], 
                                                required = True,
                                                ondelete = 'restrict', 
                                                tracking = True)
    
    examination_list_line   = fields.One2many( 'master.tindakan.layanan.line', 
                                               'pricelist_id', 
                                               string = 'Examination List Line')
    
    product_line            = fields.One2many( 'master.alat.obat.line', 
                                               'pricelist_id', 
                                               string = 'Alat Kesehatan dan Obat Line')
    
    master_tindakan_ids     = fields.Many2many( 'product.product', 
                                                compute = '_compute_master_tindakan')
    
    product_ids             = fields.Many2many( 'product.product', 
                                                compute = '_compute_product_ids')
    
    examination_list_count  = fields.Integer( string    = 'Jumlah Examination List',  
                                              copy      = False,
                                              compute   = '_compute_examination_list_count')
    
    product_count           = fields.Integer( string    = 'Jumlah Product',  
                                              copy      = False,
                                              compute   = '_compute_product_count')
    
    is_pricelist            = fields.Boolean(   string  = 'Pricelist',
                                                default = False)
    
    perusahaan_ids          = fields.Many2many( 'res.partner', 
                                                compute = '_compute_perusahaan_ids')
    
    # Menghitung Jumlah Examination List yang mendapatkan Harga Khusus
    def _compute_examination_list_count(self):
        for rec in self:
            read_examination_list_ids  = self.env['master.tindakan.layanan.line'].search([]).filtered(lambda r: rec.id in r.pricelist_id.ids)
            rec.examination_list_count = len(read_examination_list_ids.ids)
        
    # Menghitung Jumlah Obat dan Alat Kesehatan yang mendapatkan Harga Khusus   
    def _compute_product_count(self):
        for rec in self:
            read_product_ids  = self.env['master.alat.obat.line'].search([]).filtered(lambda r: rec.id in r.pricelist_id.ids)
            rec.product_count = len(read_product_ids.ids)
    
    # Digunakan untuk Filter Examination List agar tidak ada Duplicate
    @api.depends('examination_list_line.master_tindakan_id')
    def _compute_master_tindakan(self):
        for data in self:
            domain = [('is_service', '=', True)]
            if data.examination_list_line:
                domain += [('id', 'not in', [line.master_tindakan_id.id for line in data.examination_list_line])]
            data.master_tindakan_ids = self.env['product.product'].search(domain)
    
    # Digunakan untuk Filter Alat Kesehatan dan Obat agar tidak ada Duplicate
    @api.depends('product_line.master_alat_obat_id')
    def _compute_product_ids(self):
        for data in self:
            domain = [('jenis_persediaan', 'in', ['obat', 'alkes'])]
            if data.product_line:
                domain += [('id', 'not in', [line.master_alat_obat_id.id for line in data.product_line])]
            data.product_ids = self.env['product.product'].search(domain)
    
    # Memastikan tidak adanya Double Data Perusahaan pada Pembuatan Pricelist
    @api.depends('is_pricelist')
    def _compute_perusahaan_ids(self):
        for data in self:
            master_pricelist_ids    = self.search([]).perusahaan_id.ids
            domain                  = [('is_company', '=', True), '|', '&', ('is_perusahaan', '=', True), ('status_perusahaan', '=', 'approved'), '&', ('client', '=', True), ('client_state', '=', 'enabled')]
            
            if data.is_pricelist:
                domain += [('id', 'not in', master_pricelist_ids)]
                
            data.perusahaan_ids = self.env['res.partner'].search(domain)

class MasterTindakanLayananLine(models.Model):
    _inherit                = 'master.tindakan.layanan.line'
    _description            = 'Master Tindakan Layanan Line'
    
    pricelist_id            = fields.Many2one( 'master.pricelist', 
                                                string   = 'Pricelist',
                                                ondelete = 'cascade')
    
class MasterAlatObatLine(models.Model):
    _inherit            = 'master.alat.obat.line'
    _description        = 'Master Alat Kesehatan & Obat Line'
    
    pricelist_id        = fields.Many2one( 'master.pricelist', 
                                            string   = 'Pricelist',
                                            ondelete = 'cascade')