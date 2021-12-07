from odoo import _, api, fields, models
import math

class MasterSampling(models.Model):
    _name                   = 'master.sampling'
    _description            = 'Master Sampling'
    _inherit                = ['mail.thread', 'mail.activity.mixin']
    
    name                    = fields.Char(  string   = 'Nama Sampling',
                                            required = True)
    
    master_action_ids       = fields.Many2many( 'product.product', 
                                                string = 'Nama Tindakan')
    
    is_sampling             = fields.Boolean(   string  = 'Sampling',
                                                default = False)
    
    alat_kesehatan_line     = fields.One2many(  'master.alat.kesehatan.line', 
                                                'master_sampling_id', 
                                                string   = 'Alat Kesehatan')
    
    currency_id             = fields.Many2one( 'res.currency', 'Currency',
                                                default  = lambda self: self.env.company.currency_id.id,
                                                readonly = True,
                                                store    = True)
    
    total_cost              = fields.Float( string  = 'Total Cost', 
                                            digits  = (10,2),
                                            compute = '_compute_total_cost',
                                            store   = True)

    alat_kesehatan_ids      = fields.Many2many( 'product.product', 
                                                compute = '_compute_alat_kesehatan_ids')
    
    master_tindakan_ids     = fields.Many2many( 'product.product', 
                                                compute = '_compute_master_tindakan_ids')
    
    # Menghitung Subtotal dari Alat kesehatan
    @api.depends('alat_kesehatan_line.subtotal')
    def _compute_total_cost(self):
        for rec in self:
            total_fixed_cost    = round((math.ceil(sum(rec.alat_kesehatan_line.mapped('subtotal'))) + 50), -2)
            rec.total_cost      = total_fixed_cost
    
    # Digunakan untuk Filter Alat Kesehatan agar tidak ada Duplicate Data
    @api.depends('alat_kesehatan_line.product_id')
    def _compute_alat_kesehatan_ids(self):
        for data in self:
            domain_product       = [('jenis_persediaan', '=', 'alkes')]
            
            if data.alat_kesehatan_line:
                domain_product += [('id', 'not in', [line.product_id.id for line in data.alat_kesehatan_line])]
                
            data.alat_kesehatan_ids = self.env['product.product'].search(domain_product)
    
    # Digunakan untuk menghilangkan Tindakan / Layanan yang sudah memiliki Sampling dari Daftar
    @api.depends('is_sampling')
    def _compute_master_tindakan_ids(self):
        for data in self:
            master_sampling_ids     = self.search([]).master_action_ids.ids
            domain                  = [('is_service', '=', True)]
            
            if data.is_sampling:
                domain += [('id', 'not in', master_sampling_ids)]
                
            data.master_tindakan_ids = self.env['product.product'].search(domain)

class MasterAlatKesehatanLine(models.Model):
    _inherit                = 'master.alat.kesehatan.line'
    _description            = 'Master Alat Kesehatan Line'
    
    master_sampling_id      = fields.Many2one( 'master.sampling', 
                                                string   = 'Sampling',
                                                ondelete = 'cascade')