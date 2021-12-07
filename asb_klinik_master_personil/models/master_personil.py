from odoo import _, api, fields, models, tools, SUPERUSER_ID
from odoo.exceptions import UserError, ValidationError

class MasterPersonil(models.Model):
    _inherit            = 'res.partner'
    _description        = 'Master Personil'
    
    @api.model
    def _get_default_country(self):
        country = self.env['res.country'].search([('code', '=', 'ID')], limit=1)
        return country
    
    # General
    country_id                  = fields.Many2one( 'res.country', 
                                                   string   = 'Country',
                                                   default  = _get_default_country)
    
    is_master                   = fields.Boolean( string    = 'Master', 
                                                  readonly  = True, 
                                                  default   = False)
    
    is_klinik                   = fields.Boolean( string    = 'Klinik', 
                                                  readonly  = True, 
                                                  default   = False)

    is_dokter                   = fields.Boolean( string    = 'Dokter', 
                                                  readonly  = True, 
                                                  default   = False)
    
    is_perawat                  = fields.Boolean( string    = 'Perawat', 
                                                  readonly  = True, 
                                                  default   = False)
    
    is_non_medis                = fields.Boolean( string    = 'Tenaga Non-Medis', 
                                                  readonly  = True, 
                                                  default   = False)
    
    kode                        = fields.Char( string   = 'ID Personil', 
                                               copy     = False, 
                                               default  = "-", 
                                               readonly = True)

    kode_perusahaan             = fields.Char( string   = 'ID Government',
                                               copy     = False,
                                               tracking = True)
    
    tempat_lahir                = fields.Char( string   = 'Tempat Lahir',
                                               copy     = False,
                                               tracking = True)
    
    tanggal_lahir               = fields.Date( string   = 'Tanggal Lahir',
                                               copy     = False,
                                               tracking = True)
    
    jenis_kelamin               = fields.Selection( [
                                                        ('laki', 'Laki-Laki'),
                                                        ('perempuan', 'Perempuan'),
                                                    ],  string   = 'Jenis Kelamin',
                                                        copy     = False,
                                                        tracking = True)
    
    status_perkawinan           = fields.Selection( [
                                                        ('lajang', 'Lajang'),
                                                        ('menikah', 'Menikah'),
                                                        ('dudajanda', 'Duda / Janda'),
                                                    ],  string   = 'Status Perkawinan',
                                                        copy     = False,
                                                        tracking = True)
    
    unit_kerja                  = fields.Selection( [
                                                        ('dokter', 'Dokter'),
                                                        ('perawat', 'Perawat'),
                                                        ('nonmedis', 'Tenaga Non-Medis'),
                                                    ],  string   = 'Unit Kerja')
    
    berkas_dokumen_count        = fields.Integer( string    = '# Dokumen', 
                                                  compute   = '_compute_berkas_dokumen_count', 
                                                  copy      = False)
    
    # Relasi
    master_ketenagaan_id        = fields.Many2one( 'master.ketenagaan', 
                                                   string   = 'Bidang Ketenagaan',
                                                   tracking = True)
    
    poli_unit_id                = fields.Many2one( 'master.poli.unit', 
                                                   string   = 'Poli / Unit',
                                                   tracking = True)
    
    faskes_ids                  = fields.Many2many( 'master.fasilitas.kesehatan', 
                                                    string      = 'Fasilitas Kesehatan',
                                                    tracking    = True)
    
    master_ketenagaan_ids       = fields.Many2many( 'master.ketenagaan', 
                                                    compute='_compute_master_ketenagaan_ids')
    
    poli_unit_ids               = fields.Many2many( 'master.poli.unit', 
                                                    compute='_compute_poli_unit_ids')
    
    # Filter Ketenagaan berdasarkan Bidangnya
    @api.depends('is_dokter', 'is_perawat', 'is_non_medis')
    def _compute_master_ketenagaan_ids(self):
        for data in self:
            domain_master_ketenagaan    = []
            
            if data.is_dokter:
                domain_master_ketenagaan += [('unit_kerja', '=', 'dokter')]
            if data.is_perawat:
                domain_master_ketenagaan += [('unit_kerja', '=', 'perawat')]
            if data.is_non_medis:
                domain_master_ketenagaan += [('unit_kerja', '=', 'nonmedis')]
                
            data.master_ketenagaan_ids  = self.env['master.ketenagaan'].search(domain_master_ketenagaan)
    
    # Filter Poli Unit berdasarkan Bidangnya
    @api.depends('is_dokter', 'is_perawat', 'is_non_medis', 'faskes_ids')
    def _compute_poli_unit_ids(self):
        for data in self:
            domain_poli_unit    = []
            
            if data.is_dokter and data.faskes_ids:
                domain_poli_unit += [('id', 'in', data.faskes_ids.poli_unit_ids.ids), ('kategori', 'in', ['poli', 'penunjang'])]
            if data.is_perawat and data.faskes_ids:
                domain_poli_unit += [('id', 'in', data.faskes_ids.poli_unit_ids.ids), ('kategori', 'in', ['poli', 'penunjang'])]
            if data.is_non_medis and data.faskes_ids:
                domain_poli_unit += [('id', 'in', data.faskes_ids.poli_unit_ids.ids), ('kategori', '=', 'unit')]
                
            data.poli_unit_ids   = self.env['master.poli.unit'].search(domain_poli_unit)
    
    # Menghapus Data Poli dan Ketenagaan apabila Faskes kosong
    @api.onchange('faskes_ids')
    def compute_faskes_ids(self):
        for rec in self:
            if not rec.faskes_ids:
                rec.poli_unit_id            = False
                rec.master_ketenagaan_id    = False
            if rec.faskes_ids and rec.poli_unit_id not in rec.faskes_ids.poli_unit_ids:
                rec.poli_unit_id            = False
    
    # Sequence ID untuk Personil
    @api.model
    def create(self, vals):
        
        if not vals.get('unit_kerja',False):
            vals['unit_kerja'] = False
        
        if vals['unit_kerja'] == 'dokter':
            vals['kode'] = self.env['ir.sequence'].next_by_code('res.partner.personil.dokter')
        if vals['unit_kerja'] == 'perawat':
            vals['kode'] = self.env['ir.sequence'].next_by_code('res.partner.personil.perawat')
        if vals['unit_kerja'] == 'nonmedis':
            vals['kode'] = self.env['ir.sequence'].next_by_code('res.partner.personil.nonmedis')

        return super(MasterPersonil, self).create(vals)
    
    # Fungsi untuk Membuat User
    def _create_user(self):
        users       = self.env['res.users'].with_user(SUPERUSER_ID)
        user_id     = users.search([('login', '=', self.email)])
        if not user_id:
            user_id = users.create(
                {
                    'login'                 : self.email,
                    'partner_id'            : self.id,
                    'email'                 : self.email,
                    'password'              : 12345,
                    'unit_kerja'            : self.unit_kerja,
                    'master_ketenagaan_id'  : self.master_ketenagaan_id.id,
                    'faskes_ids'            : self.faskes_ids.ids,
                    'poli_unit_id'          : self.poli_unit_id.id,
                    'faskes_id'             : self.faskes_ids.ids[0],
                }
            ) 
        return user_id
    
    # Fungsi untuk Membuka User Menu yang telah dibuat
    def _open_user(self, user_id):
        view_id = self.env.ref('base.view_users_form').id
        return {
            'type': 'ir.actions.act_window',
            'name': 'User',
            'view_mode': 'form',
            'res_model': 'res.users',
            'target': 'current',
            'res_id': user_id.id,
            'views': [[view_id, 'form']],
        }
    
    # Action untuk Membuat User
    def action_create_user(self):
        for rec in self:
            user_id = rec._create_user()
            return rec._open_user(user_id)
    
    # Menghitung Jumlah Dokumen dari Personil Terkait
    def _compute_berkas_dokumen_count(self):
        for rec in self:
            read_berkas_dokumen_count_ids = self.env['master.dokumen'].search([]).filtered(lambda r: rec.id in r.partner_id.ids)
            rec.berkas_dokumen_count      = len(read_berkas_dokumen_count_ids.ids)
    