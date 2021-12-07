from odoo import _, api, fields, models

class MasterPoliUnit(models.Model):
    _name                   = 'master.poli.unit'
    _description            = 'Master Poli Unit'
    _parent_name            = 'parent_id'
    _parent_store           = True
    _rec_name               = 'nama_poli_unit'
    _order                  = 'name'
    _inherit                = ['mail.thread', 'mail.activity.mixin']
    
    parent_path             = fields.Char(  index   = True, 
                                            copy    = False)
    
    parent_id               = fields.Many2one(  'master.poli.unit', 
                                                string      = 'Parent Poli / Unit', 
                                                index       = True, 
                                                copy        = False, 
                                                ondelete    = 'cascade')
    
    child_id                = fields.One2many(  'master.poli.unit', 
                                                'parent_id', 
                                                string  = 'Child Poli / Unit',
                                                copy    = False)
    
    name                    = fields.Char(  string      = 'Kode Poli / Unit',
                                            default     = '-',
                                            readonly    = True, 
                                            copy        = False)
    
    nama_poli_unit          = fields.Char(  string      = 'Nama Unit / Poli', 
                                            required    = True,
                                            index       = True, 
                                            tracking    = True)
    
    color                   = fields.Integer( string    = 'Pilih Warna Unit / Poli',
                                              copy      = False,
                                              tracking  = True)
    
    kategori                = fields.Selection([
                                                    ('poli', 'Poli'),
                                                    ('unit', 'Unit'),
                                                    ('penunjang', 'Penunjang'),
                                                ],  string   = 'Kategori', 
                                                    default  = 'poli',
                                                    required = True,
                                                    tracking = True)
    
    tenaga_medis_count      = fields.Integer( string    = '# Tenaga Kerja',  
                                              copy      = False,
                                              compute   = '_compute_tenaga_medis_count')
    
    # Sequence untuk Poli Unit
    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('master.poli.unit.sequence')
        return super(MasterPoliUnit, self).create(vals)
    
    # Untuk Fungsi Duplicate
    def copy(self, default = {}):
        default['nama_poli_unit'] = "{} (Copy)".format(self.nama_poli_unit)
        res     = super(MasterPoliUnit, self).copy(default = default)
        return res
    
    # Name Get untuk Poli Unit
    def name_get(self):
        res = []
        for rec in self: res.append((rec.id, '%s' % (rec.nama_poli_unit)))
        return res
    
    # Compute Tenaga Medis dari Poli Terkait
    def _compute_tenaga_medis_count(self):
        for rec in self:
            read_partner_ids = self.env['res.partner'].search([]).filtered(lambda r: rec.id in r.poli_unit_id.ids)
            rec.tenaga_medis_count = len(read_partner_ids.ids)