from odoo import _, api, fields, models

class MasterKetenagaan(models.Model):
    _name                       = 'master.ketenagaan'
    _description                = 'Master Ketenagaan'
    _parent_name                = 'parent_id'
    _parent_store               = True
    _rec_name                   = 'bidang_ketenagaan'
    _order                      = 'kode_ketenagaan'
    _inherit                    = ['mail.thread', 'mail.activity.mixin']
    
    parent_path                 = fields.Char( index = True)
    
    parent_id                   = fields.Many2one( 'master.ketenagaan', 
                                                   string   = 'Parent Master Ketenagaan', 
                                                   index    = True, 
                                                   ondelete = 'cascade')
    
    child_id                    = fields.One2many( 'master.ketenagaan', 
                                                   'parent_id', 
                                                   string   = 'Child Master Ketenagaan')
    
    bidang_ketenagaan           = fields.Char( string   = 'Bidang Ketenagaan', 
                                               required = True,
                                               tracking = True)
    
    kode_ketenagaan             = fields.Char( string   = 'Kode Ketenagaan', 
                                               copy     = False, 
                                               default  = "-", 
                                               readonly = True)
    
    title_ketanagaan            = fields.Char( string   = 'Title Ketenagaan',
                                               tracking = True)
    
    unit_kerja                  = fields.Selection( [
                                                ('dokter', 'Dokter'),
                                                ('perawat', 'Perawat'),
                                                ('nonmedis', 'Tenaga Non-Medis'),
                                            ],  string   = 'Unit Kerja', 
                                                default  = 'dokter',
                                                required = True,
                                                tracking = True)
    
    tenaga_medis_count        = fields.Integer( string  = '# Tenaga Kerja', 
                                                copy    = False, 
                                                compute = '_compute_tenaga_medis_count', )
    
    # Name Get untuk Master Ketenagaan
    def name_get(self):
        res = []
        for rec in self: res.append((rec.id, '%s' % (rec.bidang_ketenagaan)))
        return res
    
    # Sequence untuk Master Ketenagaan berdasarkan Selection yang dipilih
    @api.model
    def create(self, vals):
        if vals['unit_kerja'] == 'dokter':
            vals['kode_ketenagaan'] = self.env['ir.sequence'].next_by_code('master.ketenagaan.dokter')
        if vals['unit_kerja'] == 'perawat':
            vals['kode_ketenagaan'] = self.env['ir.sequence'].next_by_code('master.ketenagaan.perawat')
        if vals['unit_kerja'] == 'nonmedis':
            vals['kode_ketenagaan'] = self.env['ir.sequence'].next_by_code('master.ketenagaan.nonmedis')
        return super(MasterKetenagaan, self).create(vals)

    # Compute Tenaga Medis di Ketenagaan Terkait
    def _compute_tenaga_medis_count(self):
        for rec in self:
            read_partner_ids = self.env['res.partner'].search([]).filtered(lambda r: rec.id in r.master_ketenagaan_id.ids)
            rec.tenaga_medis_count = len(read_partner_ids.ids)
    