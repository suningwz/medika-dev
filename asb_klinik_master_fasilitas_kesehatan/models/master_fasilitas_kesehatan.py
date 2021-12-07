from odoo import _, api, fields, models

class MasterFasilitasKesehatan(models.Model):
    _name                       = 'master.fasilitas.kesehatan'
    _description                = 'Master Fasilitas Kesehatan'
    _parent_name                = 'parent_id'
    _parent_store               = True
    _rec_name                   = 'nama_faskes'
    _order                      = 'name'
    _inherit                    = ['mail.thread', 'mail.activity.mixin']
    
    @api.model
    def _get_default_country(self):
        country = self.env['res.country'].search([('code', '=', 'ID')], limit=1)
        return country
    
    parent_path                 = fields.Char( index = True,
                                               copy  = False)
    
    parent_id                   = fields.Many2one( 'master.fasilitas.kesehatan', 
                                                   string   = 'Parent Fasilitas Kesehatan', 
                                                   index    = True,
                                                   copy     = False, 
                                                   ondelete = 'cascade')
    
    child_id                    = fields.One2many( 'master.fasilitas.kesehatan', 
                                                   'parent_id', 
                                                   string   = 'Child Fasilitas Kesehatan',
                                                   copy     = False)
    
    name                        = fields.Char(  string      = 'Kode Fasilitas Kesehatan',
                                                default     = 'New', 
                                                readonly    = True,
                                                copy        = False)
    
    nama_faskes                 = fields.Char( string   = 'Nama Fas. Kesehatan', 
                                               required = True,
                                               tracking = True)
    
    kode_faskes                 = fields.Char(  string='Kode Unit',
                                                required = True,
                                                tracking = True)
    
    color                       = fields.Integer( string    = 'Pilih Warna Fas. Kes.',
                                                  copy      = False)
    
    status                      = fields.Char( compute  = '_get_status',
                                               store    = True)
    
    active                      = fields.Boolean( default   = True)
    
    semua_unit                  = fields.Boolean( string    = 'Semua Unit',
                                                  default   = False)
    
    total_quota_mcu_direct      = fields.Integer( string    = 'Tot. Quota MCU Dir.', 
                                                  compute   = '_compute_total_quota_mcu_direct',
                                                  store     = True)
    
    total_quota_mcu_online      = fields.Integer( string    = 'Tot Quota MCU Onl.',
                                                  compute   = '_compute_total_quota_mcu_online',
                                                  store     = True)
    
    total_quota_mcu             = fields.Integer( string    = 'Total Quota MCU', 
                                                  compute   = '_compute_total_quota_mcu',
                                                  store     = True)
    
    tenaga_medis_count          = fields.Integer( string    = '# Tenaga Medis', 
                                                  compute   = '_compute_tenaga_medis_count', 
                                                  copy      = False)
    
    surat_izin_count            = fields.Integer( string    = '# Surat Izin', 
                                                  compute   = '_compute_surat_izin_count', 
                                                  copy      = False)
    
    # Alamat
    country_id              = fields.Many2one( 'res.country', 
                                               string   = 'Country', 
                                               ondelete = 'restrict',
                                               default  = _get_default_country, 
                                               tracking = True)
    
    state_id                = fields.Many2one( 'res.country.state', "State", 
                                               domain   = "[('country_id', '=', country_id)]",
                                               ondelete = 'restrict',
                                               copy     = False, 
                                               tracking = True)
    
    city_id                 = fields.Many2one( 'res.state.city', 'Kabupaten', 
                                               domain   = "[('state_id', '=', state_id)]",
                                               ondelete = 'restrict',
                                               copy     = False, 
                                               tracking = True)
    
    kecamatan_id            = fields.Many2one( 'res.city.kecamatan', 'Kecamatan', 
                                               domain   = [('city_id', '=', 'city_id')],
                                               ondelete = 'restrict',
                                               copy     = False, 
                                               tracking = True)
    
    kelurahan_id            = fields.Many2one( 'res.kecamatan.kelurahan', 'Kelurahan', 
                                               domain   = "[('kecamatan_id','=',kecamatan_id)]",
                                               ondelete = 'restrict',
                                               copy     = False, 
                                               tracking = True)
    
    street                  = fields.Char( tracking = True,
                                           copy     = False)
    
    street2                 = fields.Char( tracking = True,
                                           copy     = False)
    
    zip                     = fields.Char( change_default = True,
                                           copy      = False, 
                                           tracking = True)
    
    city                    = fields.Char( tracking = True,
                                           copy     = False)
    
    # Relasi
    poli_unit_ids               = fields.Many2many( 'master.poli.unit', 
                                                    string   = 'Poli / Unit',
                                                    required = True)
    
    penanggung_jawab_id         = fields.Many2one( 'res.partner', 
                                                   string   = 'Penanggung Jawab',
                                                   copy     = False,
                                                   domain   = [('is_dokter', '=', True)],
                                                   tracking = True)
    
    jadwal_quota_mcu_line       = fields.One2many( 'master.jadwal.quota.mcu', 
                                                   'faskes_id', 
                                                   string   = 'Jadwal & Quota MCU')
    
    # Sequence untuk Fasilitas Kesehatan
    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('master.fasilitas.kesehatan.sequence')
        return super(MasterFasilitasKesehatan, self).create(vals)
    
    # Untuk Fungsi Duplicate Fasilitas Kesehatan
    def copy(self, data = {}):
        
        data['nama_faskes'] = "{} (Copy)".format(self.nama_faskes)
        data['kode_faskes'] =  "{} (Copy)".format(self.kode_faskes)
        
        res     = super(MasterFasilitasKesehatan, self).copy(data = data)
        return res
    
    # Name Get untuk Fasilitas Kesehatan
    def name_get(self):
        res = []
        for rec in self: res.append((rec.id, '%s' % (rec.nama_faskes)))
        return res
    
    @api.onchange('country_id')
    def _onchange_country_id(self):
        if self.country_id and self.country_id != self.state_id.country_id:
            self.state_id = False
            self.city_id = False
            self.kecamatan_id = False
            self.kelurahan_id = False

    @api.onchange('state_id')
    def _onchange_state_id(self):
        if self.state_id and self.city_id != self.city_id.state_id:
            self.city_id = False
            self.kecamatan_id = False
            self.kelurahan_id = False

    @api.onchange('city_id')
    def _onchange_city_id(self):
        if self.city_id and self.kecamatan_id != self.kecamatan_id.city_id:
            self.kecamatan_id = False
            self.kelurahan_id = False
    
    @api.onchange('kecamatan_id')
    def _onchange_kecamatan_id(self):
        if self.kecamatan_id and self.kelurahan_id != self.kelurahan_id.kecamatan_id:
            self.kelurahan_id = False
    
    # Pilih Semua Poli Unit yang Tersedia
    @api.onchange('semua_unit')
    def pilih_semua_unit(self):
        poli_unit_ids = self.env['master.poli.unit'].search([])
        for rec in self: rec.poli_unit_ids = [(6, 0, [data.id for data in poli_unit_ids])] if rec.semua_unit else [(5, 0, 0)]
    
    # Get Status dari Fasilitas Kesehatan
    @api.depends('active')
    def _get_status(self):
        for rec in self: rec.status = "Aktif" if rec.active else "Tidak Aktif"
    
    # Compute Total Quota MCU Direct
    @api.depends('jadwal_quota_mcu_line.quota_mcu_direct')
    def _compute_total_quota_mcu_direct(self):
        for rec in self: rec.total_quota_mcu_direct = sum(rec.jadwal_quota_mcu_line.mapped('quota_mcu_direct'))
    
    # Compute Total Quota MCU Online
    @api.depends('jadwal_quota_mcu_line.quota_mcu_online')
    def _compute_total_quota_mcu_online(self):
        for rec in self: rec.total_quota_mcu_online = sum(rec.jadwal_quota_mcu_line.mapped('quota_mcu_online'))
    
    # Compute Total Quota MCU
    @api.depends('total_quota_mcu_direct', 'total_quota_mcu_online')
    def _compute_total_quota_mcu(self):
        for rec in self: rec.total_quota_mcu = rec.total_quota_mcu_direct + rec.total_quota_mcu_online
    
    # Compute Tenaga Medis untuk Faskes Terkait
    def _compute_tenaga_medis_count(self):
        for rec in self:
            read_partner_ids = self.env['res.partner'].search([]).filtered(lambda r: rec.id in r.faskes_ids.ids)
            rec.tenaga_medis_count = len(read_partner_ids.ids)
    
    # Compute Dokumen dari Faskes Terkait
    def _compute_surat_izin_count(self):
        for rec in self:
            read_surat_izin_ids = self.env['master.dokumen'].search([]).filtered(lambda r: rec.id in r.faskes_id.ids)
            rec.surat_izin_count = len(read_surat_izin_ids.ids)

class MasterJadwalQuotaMCU(models.Model):
    _inherit            = 'master.jadwal.quota.mcu'
    _description        = 'Master Jadwal Quota MCU'
    
    faskes_id           = fields.Many2one( 'master.fasilitas.kesehatan', 
                                            string      = 'Fasilitas Kesehatan ID',
                                            index       = True,
                                            ondelete    = 'cascade')