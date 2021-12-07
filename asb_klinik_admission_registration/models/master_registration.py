from odoo import _, api, fields, models, tools, SUPERUSER_ID
import datetime, re
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, ValidationError

class MasterRegistration(models.Model):
    _name                   = 'master.registration'
    _description            = 'Master Registration'
    _inherit                = ['mail.thread', 'mail.activity.mixin', 'lab.mysql.connect']
        
    @api.model
    def _get_default_no_antrian(self):
        data_registrasi = self.env['master.registration'].search([('tanggal_registrasi', '=', fields.Date.today())], order='no_antrian desc', limit=1).no_antrian
        no_antrian      = data_registrasi + 1 if data_registrasi else 1
        return no_antrian
    
    @api.model
    def _get_default_no_registrasi(self):
        data_registrasi = self.env['master.registration'].search([('tanggal_registrasi', '=', fields.Date.today())], order='no_registrasi desc', limit=1).no_registrasi
        no_registrasi   = data_registrasi + 1 if data_registrasi else 1
        return no_registrasi
    
    state                   = fields.Selection( [
                                                    ('draft', 'Draft'),
                                                    ('confirm', 'Confirmed'),
                                                    ('going', 'Ongoing'),
                                                    ('done', 'Done'),
                                                    ('cancel', 'Cancelled'),
                                                ],  string   = 'Status', 
                                                    default  = 'draft',
                                                    copy     = False,
                                                    tracking = True)
    
    on_progress             = fields.Char( string   = 'On Progress', 
                                           default  = "Admission",
                                           store    = True, 
                                           readonly = True)
    
    name                    = fields.Char( string   = 'No. Registrasi', 
                                           default  = "New",
                                           required = True, 
                                           readonly = True)
    
    no_antrian              = fields.Integer( string   = 'No. Antrian', 
                                              required = True, 
                                              readonly = True,
                                              default  = _get_default_no_antrian,
                                              tracking = True, 
                                              states   = {'draft': [('readonly', False)]})
    
    no_registrasi           = fields.Integer( string    = 'No. Registrasi', 
                                              default   = _get_default_no_registrasi,
                                              store     = True,
                                              readonly  = True)
    
    tanggal_registrasi      = fields.Date( string   = 'Tanggal Registrasi', 
                                           default  = fields.Date.today(), 
                                           readonly = True, 
                                           tracking = True, 
                                           states   = {'draft': [('readonly', False)]})
    
    status_kunjungan        = fields.Selection( [
                                                    ('tanpa', 'Tanpa Perjanjian'),
                                                    ('perjanjian', 'Perjanjian'),
                                                    ('prioritas', 'Prioritas'),
                                                ],  string      = 'Status Kunjungan', 
                                                    required    = True,
                                                    default     = 'tanpa',
                                                    readonly    = True, 
                                                    tracking    = True, 
                                                    states      = {'draft': [('readonly', False)]})
    
    status_gl               = fields.Selection( [
                                                    ('ya', 'Ya'),
                                                    ('tidak', 'Tidak'),
                                                ],  string      = 'Status GL', 
                                                    default     = 'tidak', 
                                                    readonly    = True, 
                                                    tracking    = True, 
                                                    states      = {'draft': [('readonly', False)]})
    
    no_gl                   = fields.Char( string   = 'No. GL', 
                                           readonly = True,
                                           tracking = True, 
                                           states   = {'draft': [('readonly', False)]})
    
    jenis_perjanjian        = fields.Selection( [
                                                    ('mc', 'MC'),
                                                    ('mcu', 'MCU'),
                                                    ('onsite', 'MCU Onsite'),
                                                ],  string   = 'Jenis Perjanjian',
                                                    readonly = True,
                                                    tracking = True,  
                                                    states   = {'draft': [('readonly', False)]})
    
    tipe_transaksi          = fields.Selection( [
                                                    ('mc', 'MC'),
                                                    ('mcu', 'MCU'),
                                                    ('provider', 'MCU Provider'),
                                                    ('onsite', 'MCU Onsite'),
                                                ],  string   = 'Tipe Transaksi',
                                                    readonly = True,
                                                    tracking = True,  
                                                    states   = {'draft': [('readonly', False)]})
    
    tipe_pengiriman         = fields.Selection( [
                                                    ('normal', 'Normal'),
                                                    ('sameday', 'Sameday Service'),
                                                ],  string      = 'Tipe Pengiriman', 
                                                    default     = 'normal', 
                                                    readonly    = True, 
                                                    tracking    = True, 
                                                    states      = {'draft': [('readonly', False)]})
    
    tanggal_pembuatan       = fields.Date( string   = 'Created Date', 
                                           default  = fields.Date.today(),
                                           readonly = True, 
                                           tracking = True)
    
    tanggal_confirm         = fields.Date( string   = 'Confirmed Date', 
                                           readonly = True, 
                                           tracking = True)
    
    user_create             = fields.Many2one( 'res.users', 
                                               string    = 'Created By',
                                               default   = lambda self: self.env.user, 
                                               readonly  = True, 
                                               index     = True,
                                               tracking  = True)
    
    user_approve            = fields.Many2one( 'res.users',
                                               string   = 'Approved By',
                                               readonly = True, 
                                               index    = True, 
                                               tracking = True)
    
    faskes_id               = fields.Many2one( 'master.fasilitas.kesehatan', 
                                               string   = 'Fasilitas Kesehatan',
                                               store    = True,
                                               readonly = True, 
                                               index    = True,
                                               default  = lambda self: self.env.user.faskes_id.id)
    
    code                    = fields.Char(  string   = 'Kode Unit',
                                            readonly = True, 
                                            store    = True,
                                            related  = 'faskes_id.kode_faskes')
    
    # Relasi ke Pasien
    pasien_id               = fields.Many2one(  'res.partner', 
                                                string   = 'Nama Pasien', 
                                                domain   = [('is_pasien', '=', True)], 
                                                readonly = True, 
                                                tracking = True, 
                                                states   = {'draft': [('readonly', False)]})
    
    image_1920              = fields.Image( string    = 'Gambar',
                                            max_width = 512, max_height = 512, store = True,
                                            readonly  = True, 
                                            states    = {'draft': [('readonly', False)]})
    
    display_name            = fields.Char(  string   = 'Nama Pasien', 
                                            related  = 'pasien_id.display_name',
                                            store    = True)
    
    no_ktp                  = fields.Char( string   = 'No. KTP', 
                                           store    = True,
                                           related  = 'pasien_id.no_ktp')
    
    email                   = fields.Char( string   = "Email Pasien", 
                                           store    = True,
                                           related  = 'pasien_id.email')
    
    mobile                  = fields.Char( string   = "Nomor HP", 
                                           store    = True,
                                           related  = 'pasien_id.mobile')
    
    umur                    = fields.Char( string   = 'Umur', 
                                           related  = 'pasien_id.umur',
                                           store    = True)
    
    tempat_lahir            = fields.Char( string   = 'Tempat Lahir',
                                           store    = True,
                                           related  = 'pasien_id.tempat_lahir')
    
    tanggal_lahir           = fields.Date( string   = 'Tanggal Lahir', 
                                           store    = True,
                                           related  = 'pasien_id.tanggal_lahir')
    
    warga_negara            = fields.Selection( store   = True,
                                                related = 'pasien_id.warga_negara')
    
    jenis_kelamin           = fields.Selection( store   = True,
                                                related = 'pasien_id.jenis_kelamin')
    
    street                  = fields.Char( store   = True,
                                           related = 'pasien_id.street')
    
    street2                 = fields.Char( store   = True,
                                           related = 'pasien_id.street2')
    
    zip                     = fields.Char( change_default   = True, 
                                           store            = True,
                                           related          = 'pasien_id.zip')
    
    city                    = fields.Char( store   = True,
                                           related = 'pasien_id.city')
    
    city_id                     = fields.Many2one( 'res.state.city', 'Kabupaten', 
                                                    domain   = "[('state_id', '=', state_id)]",
                                                    ondelete = 'restrict',
                                                    related  = 'pasien_id.city_id')
    
    kecamatan_id                = fields.Many2one( 'res.city.kecamatan', 'Kecamatan', 
                                                    domain   = [('city_id', '=', 'city_id')],
                                                    ondelete = 'restrict',
                                                    related  = 'pasien_id.kecamatan_id')
    
    kelurahan_id                = fields.Many2one( 'res.kecamatan.kelurahan', 'Kelurahan', 
                                                    domain   = "[('kecamatan_id','=',kecamatan_id)]",
                                                    ondelete = 'restrict',
                                                    related  = 'pasien_id.kelurahan_id')
    
    state_id                = fields.Many2one(  'res.country.state', 
                                                string   = 'State', 
                                                ondelete = 'restrict',
                                                store    = True, 
                                                domain   = "[('country_id', '=?', country_id)]", 
                                                related  = 'pasien_id.state_id')
    
    country_id              = fields.Many2one(  'res.country', 
                                                string   = 'Country', 
                                                ondelete = 'restrict', 
                                                store    = True,
                                                related  = 'pasien_id.country_id')
    
    country_name            = fields.Char(  string  = 'Country Name',
                                            store   = True, 
                                            related = 'country_id.name')
    
    state_name              = fields.Char(  string  = 'State Name',
                                            store   = True, 
                                            related = 'state_id.name')
    
    city_name               = fields.Char(  string  = 'City Name',
                                            store   = True, 
                                            related = 'city_id.name')
    
    kecamatan_name          = fields.Char(  string  = 'Kecamatan Name',
                                            store   = True, 
                                            related = 'kecamatan_id.name')
    
    kelurahan_name          = fields.Char(  string  = 'Kelurahan Name',
                                            store   = True, 
                                            related = 'kelurahan_id.name')
    
    # Relasi ke Perusahaan
    perusahaan_id           = fields.Many2one(  'res.partner', 
                                                string   = 'Perusahaan', 
                                                readonly = True,
                                                required = True,
                                                ondelete = 'restrict', 
                                                tracking = True, 
                                                store    = True,
                                                states   = {'draft': [('readonly', False)]})
    
    nik_pegawai             = fields.Char( string   = 'NIK Pegawai', 
                                           store     = True,
                                           related  = 'pasien_id.nik_pegawai')
    
    status_pegawai          = fields.Selection( string   = 'Status Kepegawaian',
                                                store    = True,
                                                related  = 'pasien_id.status_pegawai')
    
    mulai_bekerja           = fields.Date( string    = 'Mulai Bekerja',
                                           store     = True,
                                           related   = 'pasien_id.mulai_bekerja')
    
    jenis_pekerjaan_id      = fields.Many2one( 'master.jenis.pekerjaan', 
                                               string   = 'Jenis Pekerjaan',
                                               store    = True,
                                               related  = 'pasien_id.jenis_pekerjaan_id')
    
    shift_kerja             = fields.Selection( string   = 'Shift Kerja',
                                                store    = True,
                                                related  = 'pasien_id.shift_kerja')
    
    lokasi_pekerjaan_id     = fields.Many2one(  'master.lokasi.pekerjaan',
                                                store    = True, 
                                                related  = 'pasien_id.lokasi_pekerjaan_id')
    
    function                = fields.Char( string    = 'Posisi / Jabatan',
                                           store     = True,
                                           related   = 'pasien_id.function')
    
    # Relasi ke Paket MCU
    examination_list_ids    = fields.Many2many( 'product.product', 
                                                store    = True,
                                                readonly = True,
                                                tracking = True,
                                                states   = {'draft': [('readonly', False)]})
    
    sampling_list_ids       = fields.Many2many( 'master.sampling', 
                                                string   ='Sampling List',
                                                compute  = '_get_sampling_list',
                                                readonly = True,
                                                store    = True,
                                                copy     = False)
    
    # Related Data dari Reservasi 
    reservation_id          = fields.Many2one(  'master.reservation', 
                                                string = 'Data Reservasi',
                                                readonly = True,
                                                states   = {'draft': [('readonly', False)]})
    
    is_perjanjian           = fields.Boolean( string    = 'Laboratorium', 
                                              store     = True,
                                              default   = False)
    
    is_perjanjian_mcu       = fields.Boolean( string    = 'Laboratorium', 
                                              store     = True,
                                              default   = False)
    
    is_done_perawat         = fields.Boolean(   string   = 'Done Perawat',
                                                default  = False,
                                                readonly = True)
    
    poli_unit_ids           = fields.Many2many( 'master.poli.unit', 
                                                string      = 'Poli / Unit', 
                                                copy        = False,
                                                tracking    = True,
                                                readonly    = True)
    
    dokter_id               = fields.Many2one(  'res.partner', 
                                                string   = 'Nama Dokter',
                                                copy     = False,
                                                readonly = True, 
                                                tracking = True)
    
    nama_dokter             = fields.Char(  string  = 'Nama Dokter',
                                            store   = True, 
                                            related = 'dokter_id.display_name')
    
    kode                    = fields.Char(  string  = 'ID Personil',
                                            store   = True, 
                                            related = 'dokter_id.kode')
    
    package_mcu_id          = fields.Many2one( 'package.mcu', 
                                                string   = 'Package MCU',
                                                readonly = True, 
                                                tracking = True,
                                                copy     = False)
    
    list_package_id         = fields.Many2one( 'list.package', 
                                                string   = 'List Package', 
                                                readonly = True, 
                                                tracking = True,
                                                copy     = False)
    
    certificate_ids         = fields.Many2many( 'config.certificate.list', 
                                                string   = 'Sertifikat', 
                                                related  = 'list_package_id.certificate_ids',
                                                tracking = True)
    
    bahasa_hasil            = fields.Selection( [
                                                    ('indonesia', 'Indonesia'),
                                                    ('inggris', 'Inggris'),
                                                ],  string   = 'Bahasa Hasil', 
                                                    default  = 'inggris', 
                                                    store    = True,
                                                    tracking = True)
    
    price_paket             = fields.Float( string   = 'Price Paket MCU (IDR)',
                                            store    = True,
                                            tracking = True,
                                            related  = 'reservation_id.price_paket')
    
    fix_price_paket         = fields.Float( string   = 'Total Cost Keseluruhan (IDR)',
                                            store    = True,
                                            tracking = True,
                                            related  = 'reservation_id.fix_price_paket')
    
    fixed_costing_line      = fields.One2many(  'config.fixed.costing.line', 
                                                'registration_id', 
                                                string   = 'Fixed Costing',
                                                readonly = True,
                                                store    = True,
                                                copy     = False,
                                                tracking = True)

    currency_id             = fields.Many2one( 'res.currency', 'Currency',
                                                default  = lambda self: self.env.company.currency_id.id,
                                                readonly = True)
    
    total_cost_examination_list = fields.Float( string   = 'Total Cost Examination List (IDR)',
                                                store    = True,
                                                tracking = True,
                                                compute  = '_compute_total_cost_examination_list')
    
    total_cost_sampling         = fields.Float( string   = 'Total Cost Sampling (IDR)', 
                                                store    = True,
                                                tracking = True, 
                                                compute  = '_compute_total_cost_sampling')
    
    total_cost                  = fields.Float( string   = 'Total Cost (IDR)', 
                                                store    = True,
                                                tracking = True,
                                                compute  = '_compute_total_cost')
    
    package_mcu_ids             = fields.Many2many( 'package.mcu', 
                                                    compute = '_compute_package_mcu_ids')
    
    list_package_ids            = fields.Many2many( 'list.package', 
                                                    compute = '_compute_list_package_ids')
    
    perusahaan_ids              = fields.Many2many( 'res.partner', 
                                                    compute = '_compute_perusahaan')
    
    poli_ids                    = fields.Many2many( 'master.poli.unit', 
                                                    compute = '_compute_poli_ids')
    
    dokter_ids                  = fields.Many2many( 'res.partner', 
                                                    compute = '_compute_dokter_ids')
    
    status_kunjungan_ids        = fields.Many2many( 'master.reservation', 
                                                    compute = '_compute_status_kunjungan_ids')
    
    examination_ids             = fields.Many2many( 'product.product', 
                                                    string  = 'Examination',
                                                    compute = '_compute_examination_ids')
    
    no_record                   = fields.Integer( string    = 'No. Record',
                                                  store     = True, 
                                                  readonly  = True)
    
    no_medical_report           = fields.Char(  string   = 'No. MR',
                                                store    = True, 
                                                readonly = True)
    
    status_antrian              = fields.Selection( [
                                                        ('waiting', 'Waiting'),
                                                        ('progress', 'On Progress'),
                                                        ('done', 'Done'),
                                                    ],  string   = 'Status',
                                                        store    = True,
                                                        default  = 'waiting',
                                                        readonly = True)
    
    filter_examination_ids      = fields.Many2many( 'product.product', 
                                                    compute = '_compute_filter_examination_ids')
    
    additional_examination_ids  = fields.Many2many( 'product.product', 
                                                    relation = 'additional_examination_list',
                                                    column1  = 'examination_id', 
                                                    column2  = 'registration_id',
                                                    string   = 'Additional Examination List',
                                                    store    = True,
                                                    readonly = True, 
                                                    tracking = True,
                                                    copy     = False,
                                                    states   = {'draft': [('readonly', False)]})
    
    total_cost_examination_ids  = fields.Float( string   = 'Total Cost Additional Examination List (IDR)', 
                                                store    = True,
                                                tracking = True, 
                                                compute  = '_compute_total_cost_examination_ids')
    
    is_makan                    = fields.Boolean(   string   = 'Status Makan',
                                                    default  = False,
                                                    store    = True,
                                                    compute  = '_get_makan',
                                                    readonly = True)
    
    is_blood_group_fasting      = fields.Boolean(   string   = 'Status Gula Darah Fasting',
                                                    default  = False,
                                                    store    = True,
                                                    compute  = '_get_gula_darah',
                                                    readonly = True)
    
    status_pp                   = fields.Char(  string    = 'Status PP', 
                                                copy      = False,
                                                compute   = '_get_status_pp')
    
    is_blood_group_prandial     = fields.Boolean(   string   = 'Status Gula Darah Post Prandial',
                                                    default  = False,
                                                    store    = True,
                                                    compute  = '_get_gula_darah',
                                                    readonly = True)
    
    waktu_pemeriksaan_lab       = fields.Datetime(  string   = 'Waktu Pemeriksaan Lab',
                                                    store    = True,
                                                    readonly = True)
    
    waktu_cek_lab               = fields.Char(  string   = 'Waktu Cek Lab', 
                                                copy     = False,
                                                store    = True,
                                                readonly = True)
    
    def print_data_pasien(self):
        return self.env.ref('asb_klinik_admission_registration.print_data_pasien').report_action(self)
    
    @api.depends('fixed_costing_line')
    def _get_makan(self):
        for rec in self:
            for data in rec.fixed_costing_line:
                if re.search('meal', str(data.fixed_costing_id.name), re.IGNORECASE):
                    rec.is_makan = True
                    return
                else:
                    rec.is_makan = False
                    
    @api.depends('additional_examination_ids', 'examination_list_ids')
    def _get_gula_darah(self):
        for rec in self:
            result = [data.name for record in [rec.additional_examination_ids, rec.examination_list_ids] for data in record]
            for data in result:
                if re.search('fasting', str(data), re.IGNORECASE):
                    rec.is_blood_group_fasting = True
                elif re.search('prandial', str(data), re.IGNORECASE):
                    rec.is_blood_group_prandial = True
                else:
                    pass
                
    @api.depends('is_blood_group_fasting', 'is_blood_group_prandial')
    def _get_status_pp(self):
        for rec in self:
            rec.status_pp = "Yes" if rec.is_blood_group_fasting and rec.is_blood_group_prandial else "No"
    
    # Cron Job : Update State
    @api.model
    def update_state_registration(self):
        record = self.search([
            ('state', 'in', ['draft', 'confirm', 'going']), 
            ('tanggal_registrasi', '<', fields.Date.today()),
        ])
        for rec in record:
            rec.write({
                'state'         : 'cancel', 
                'status_antrian': 'done'
        }   )
        return True
    
    # Ambil Data Dashboard Registrasi untuk Hari Ini
    @api.model
    def retrieve_dashboard(self):
        self.check_access_rights('read')
        result = {
            'total_registrasi_today'    : 0,
            'total_mc'                  : 0,
            'total_mcu'                 : 0,
            'waiting_list_today'        : 0,
        }
        
        mr                                = self.env['master.registration']
        m_reservation                     = self.env['master.reservation']
        result['total_registrasi_today']  = mr.search_count([('tanggal_registrasi', '=', fields.Date.today()), ('faskes_id', '=', self.env.user.faskes_id.id)])
        result['total_mcu']               = mr.search_count([('tipe_transaksi', 'in', ['mcu', 'onsite', 'provider']), ('tanggal_registrasi', '=', fields.Date.today()), ('faskes_id', '=', self.env.user.faskes_id.id)])
        result['total_mc']                = mr.search_count([('tipe_transaksi', '=', 'mc'), ('tanggal_registrasi', '=', fields.Date.today()), ('faskes_id', '=', self.env.user.faskes_id.id)])
        result['waiting_list_today']      = m_reservation.search_count([('state', '=', 'confirm'), ('tanggal_reservasi', '=', fields.Date.today()), ('faskes_id', '=', self.env.user.faskes_id.id)])
        
        return result
    
    # Sequence dan Ubah Status Data Reservasi berdasarkan Data yang dipilih
    @api.model
    def create(self, vals):
        vals['name']                            = self.env['ir.sequence'].next_by_code('master.registration.sequence')
        self.env['master.reservation'].search([]).filtered(lambda r: vals['reservation_id'] in r.ids).write({'state' : 'done'})
        return super(MasterRegistration, self).create(vals)
    
    # Button Action untuk Cek Status Pemeriksaan
    def status_pemeriksaan_wizard(self):
        return {
            'type'          : 'ir.actions.act_window',
            'res_model'     : 'master.pemeriksaan.status.pasien',
            'view_mode'     : 'form',
            'target'        : 'new',
        }
    
    # Button Action Confirm
    def action_confirm(self):
        self.ensure_one()
        pemeriksaan_ids = self.env['list.pemeriksaan.poli'].with_user(SUPERUSER_ID).search([('registration_id', '=', self.id)])
        if not pemeriksaan_ids:
            if self.jenis_perjanjian == 'mc':
                for poli_unit in self.poli_unit_ids.ids:
                    pemeriksaan_ids.create({
                        'registration_id'   : self.id,
                        'poli_unit_id'      : poli_unit,
                        'status'            : 'Not Yet',
                    })
            if self.jenis_perjanjian in ['mcu', 'onsite']:
                result = list(set([id for id in self.examination_list_ids.poli_unit_id.ids] + [id for id in self.additional_examination_ids.poli_unit_id.ids]))
                for poli_unit in result:
                    pemeriksaan_ids.create({
                        'registration_id'   : self.id,
                        'poli_unit_id'      : poli_unit,
                        'status'            : 'Not Yet',
                    })
        vals = {
                'jenis_kelamin'         : self.jenis_kelamin,
                'tanggal_lahir'         : self.tanggal_lahir.strftime("%Y%m%d%H%M%S"),
                'tanggal_registrasi'    : self.tanggal_registrasi.strftime("%Y%m%d%H%M%S"),
                'kode'                  : self.kode,
                'nama_dokter'           : self.nama_dokter,
                'examination_list_ids'  : [id for data in [self.examination_list_ids.ids, self.additional_examination_ids.ids] for id in data],
                'no_medical_report'     : self.no_medical_report,
                'display_name'          : self.display_name,
                'street'                : self.street,
                'kelurahan_name'        : self.kelurahan_name,
                'kecamatan_name'        : self.kecamatan_name,
                'city_name'             : self.city_name,
                'state_name'            : self.state_name,
                'country_name'          : self.country_name,
                'name'                  : self.name,
        }
        self._check_data_to_mysql(vals)
        return self.write({
                            'state'          : 'confirm',
                            'tanggal_confirm': fields.Date.today(),
                            'user_approve'   : self.env.user
                         })
    
    # Button Action Set to Draft
    def action_set_to_draft(self):
        self.ensure_one()
        for rec in self:
            if rec.is_done_perawat:
                raise ValidationError("Data Pasien yang sudah melakukan Pemeriksaan di Perawat. Tidak dapat diubah")
            else:
                data_pemeriksaan    = self.env['list.pemeriksaan.poli'].with_user(SUPERUSER_ID).search([('registration_id', '=', self.id)]).unlink()
                return self.write({'state': 'draft'})
    
    # Button Action Cancel
    def action_cancel(self):
        return self.write({'state': 'cancel'})
    
    # Ambil Data Perusahaan berdasarkan Data Pasien
    @api.onchange('pasien_id')
    def compute_perusahaan_id(self):
        for rec in self:
            if not rec.pasien_id:
                rec.perusahaan_id = rec.no_medical_report = rec.no_record = False
            else:
                perusahaan_ids      = self.env['res.partner'].search([
                    ('is_company', '=', True), '|', '&', ('is_perusahaan', '=', True), 
                    ('status_perusahaan', '=', 'approved'), '&', ('client', '=', True), 
                    ('client_state', '=', 'enabled')]).ids
                if rec.pasien_id.perusahaan_id.id in perusahaan_ids:
                    rec.perusahaan_id = rec.pasien_id.perusahaan_id.id
                    rec.poli_unit_ids = rec.dokter_id = False
                    data_registrasi   = [
                    (d['no_medical_report'], d['no_record']) 
                    for d in self.with_user(SUPERUSER_ID).read_group(
                    [('pasien_id', '=', rec.pasien_id.id)],
                    ['no_medical_report', 'no_record'],
                    ['no_medical_report', 'no_record'], lazy=False)]
                    
                    if data_registrasi:
                        rec.no_medical_report = data_registrasi[0][0]
                        rec.no_record = data_registrasi[0][1]
                    else:
                        data_faskes   = [
                        (d['no_record']) 
                        for d in self.read_group(
                        [('faskes_id', '=', rec.faskes_id.id)],
                        ['no_record'], ['no_record'], lazy=False)]
                        
                        if data_faskes:
                            rec.no_record = int(data_faskes[0]) + 1
                        else:
                            rec.no_record = 1
                        rec.no_medical_report = rec.code + "000" + str(rec.no_record) if rec.code else "FASKES" + "000" + str(rec.no_record)
                else:
                    rec.pasien_id = rec.perusahaan_id = rec.poli_unit_ids = rec.dokter_id = False
                    message         = "Data Perusahaan Pasien Belum Terverifikasi"
                    return{ 'warning':{
                                'title': "Invalid Data Perusahaan",
                                'message': message
                            }}
                
    # Pesan Warning yang muncul ketika No. Antrian yang diinput sudah pernah dilakukan pada Hari Tersebut
    @api.onchange('no_antrian')
    def compute_no_antrian(self):
        for rec in self:
            data_registrasi = self.search([('tanggal_registrasi', '=', fields.Date.today())], order='no_antrian desc', limit=1).no_antrian
            if rec.no_antrian <= data_registrasi:
                rec.no_antrian  = rec.no_registrasi
                message         = "Nomor Antrian sudah Terdaftar. Nomor Antrian Terakhir : {}".format(data_registrasi)
                return{ 'warning':{
                    'title': "Invalid No. Antrian",
                    'message': message
                }}
                            
    # Ambil Data Pasien dari Data Reservasi
    @api.onchange('reservation_id', 'poli_unit_ids', 'status_kunjungan')
    def _onchange_is_perjanjian(self):
        for rec in self:
            data, values, lines = [], [], [(5, 0, 0)]
            if rec.status_kunjungan == 'tanpa':
                if rec.poli_unit_ids:
                    rec.is_perjanjian = True
                    poli_penunjang = [data.kategori for data in rec.poli_unit_ids]
                    rec.is_perjanjian_mcu = True if any(data == 'poli' for data in poli_penunjang if poli_penunjang) else False
                    if any(data == 'poli' for data in poli_penunjang if poli_penunjang):
                        rec.examination_list_ids = False
                    if rec.dokter_id.poli_unit_id not in rec.poli_unit_ids:
                        rec.dokter_id = False
                else:
                    rec.is_perjanjian = False
                    rec.dokter_id = False
            else:
                if rec.reservation_id.id:
                    rec.is_perjanjian       = True
                    rec.is_perjanjian_mcu   = True
                    data_reservation_ids = self.env['master.reservation'].search([]).filtered(lambda r: rec.reservation_id.id in r.ids)
                    for res in data_reservation_ids:
                        rec.pasien_id, rec.tipe_pengiriman, rec.jenis_perjanjian = res.pasien_id.id, res.tipe_pengiriman, res.jenis_perjanjian
                        rec.tipe_transaksi, rec.status_gl, rec.no_gl, rec.bahasa_hasil = res.jenis_perjanjian, res.status_gl, res.no_gl, res.bahasa_hasil
                        if rec.jenis_perjanjian != 'mc':
                            rec.fixed_costing_line = rec.examination_list_ids = rec.dokter_id = rec.poli_unit_ids = False
                        if rec.jenis_perjanjian != 'mcu' or rec.jenis_perjanjian != 'onsite':
                            rec.package_mcu_id = rec.list_package_id = rec.fixed_costing_line = rec.examination_list_ids = False
                        if rec.jenis_perjanjian == 'mc':
                            rec.poli_unit_ids, rec.dokter_id = res.poli_unit_ids.ids, res.dokter_id.id
                            if rec.poli_unit_ids:
                                poli_penunjang = [data.kategori for data in rec.poli_unit_ids]
                                values += [id for id in res.additional_examination_ids.ids if res.additional_examination_ids]
                        if rec.jenis_perjanjian == 'mcu' or rec.jenis_perjanjian == 'onsite':
                            rec.is_perjanjian_mcu = True
                            rec.package_mcu_id, rec.list_package_id = res.package_mcu_id.id, res.list_package_id.id
                            data += [id for id in res.additional_examination_ids.ids if res.additional_examination_ids]
                            values += [id for id in res.list_package_id.examination_list_ids.master_tindakan_id.ids if rec.list_package_id]
                            val = [{
                                'fixed_costing_id'  : line.fixed_costing_id.id,
                                'name'              : line.name,
                                'cost_in_house'     : line.cost_in_house,
                                'cost_onsite'       : line.cost_onsite
                            } for line in res.list_package_id.fixed_costing_line if rec.list_package_id]
                            lines += [(0, 0, data) for data in val]
                    rec.fixed_costing_line   = lines
                    rec.examination_list_ids = [(6, 0, values)]
                    rec.additional_examination_ids = [(6, 0, data)]
                else:
                    rec.is_perjanjian = False
                    rec.is_perjanjian_mcu = False
    
    # Ubah Kondisi Field berdasarkan Status Kunjungan yang dipilih
    @api.onchange('status_kunjungan')
    def _onchange_status_kunjungan(self):
        for rec in self:
            if rec.status_kunjungan == 'tanpa':
                rec.tipe_transaksi, rec.jenis_perjanjian, rec.tipe_pengiriman, rec.status_gl, rec.bahasa_hasil = 'mc', 'mc', 'normal', 'tidak', 'inggris'
                rec.reservation_id = rec.pasien_id = rec.dokter_id = rec.poli_unit_ids = rec.package_mcu_id = rec.list_package_id = rec.examination_list_ids = rec.fixed_costing_line = False
            else:
                rec.tipe_transaksi = rec.jenis_perjanjian = rec.status_gl = rec.tipe_pengiriman = rec.reservation_id = rec.bahasa_hasil = False
                rec.pasien_id = rec.poli_unit_ids = rec.package_mcu_id = rec.dokter_id = rec.list_package_id = rec.examination_list_ids = rec.fixed_costing_line = False
    
    # Notif Warning pada Tipe Transaksi
    @api.onchange('tipe_transaksi')
    def _onchange_tipe_transaksi(self):
        for rec in self:
            if rec.tipe_transaksi != 'mc' and rec.status_kunjungan == 'tanpa':
                rec.tipe_transaksi = 'mc'
                return{ 'warning':{
                    'title': "Invalid Tipe Transaksi",
                    'message': "Untuk Status Kunjungan yang dipilih, Tipe Transaksi yang diizinkan hanyalah MC"
                }}
    
    # Notif Warning pada Jneis Perjanjian
    @api.onchange('jenis_perjanjian')
    def _onchange_jenis_perjanjian(self):
        for rec in self:
            if rec.jenis_perjanjian != 'mc' and rec.status_kunjungan == 'tanpa':
                rec.jenis_perjanjian = 'mc'
                return{ 'warning':{
                    'title': "Invalid Jenis Perjanjian",
                    'message': "Untuk Status Kunjungan yang dipilih, Jenis Perjanjian yang diizinkan hanyalah MC"
                }}
    
    # Filter Poli Unit berdasarkan Faskes dari User
    @api.depends('faskes_id')
    def _compute_poli_ids(self):
        for rec in self:
            domain   = [('kategori', 'in', ['poli', 'penunjang'])]
            if rec.faskes_id:
                domain += [('id', 'in', rec.faskes_id.poli_unit_ids.ids)]
            rec.poli_ids = self.env['master.poli.unit'].search(domain)
    
    # Filter Dokter berdasarkan Faskes dan Poli
    @api.depends('poli_unit_ids', 'faskes_id')
    def _compute_dokter_ids(self):
        for rec in self:
            domain   = [('is_dokter', '=', True)]
            if rec.poli_unit_ids:
                domain += [('poli_unit_id', 'in', rec.poli_unit_ids.ids)]
            rec.dokter_ids = self.env['res.partner'].search(domain).filtered(lambda r : rec.faskes_id.id in r.faskes_ids.ids)
    
    # Filter Data Reservasi berdasarkan Status Kunjungan
    @api.depends('status_kunjungan')
    def _compute_status_kunjungan_ids(self):
        for data in self:
            domain   = [('state', '=', 'confirm'), ('tanggal_reservasi', '=', fields.Date.today())]
            if data.status_kunjungan == 'prioritas':
                domain += [('status_kunjungan', '=', 'prioritas')]
            if data.status_kunjungan == 'perjanjian':
                domain += [('status_kunjungan', '=', 'perjanjian')]
            data.status_kunjungan_ids = self.env['master.reservation'].search(domain)
    
    # Filter Perusahaan berdasarkan Data Pasien
    @api.depends('pasien_id')
    def _compute_perusahaan(self):
        for data in self:
            domain   = [('is_company', '=', True)]
            if data.pasien_id:
                domain += [('id', '=', data.pasien_id.perusahaan_id.id)]
            data.perusahaan_ids = self.env['res.partner'].search(domain)
            
    # Ambil Data Sampling berdasarkan Examination List
    @api.depends('examination_list_ids', 'additional_examination_ids')
    def _get_sampling_list(self):
        for record in self:
            val = []
            if record.examination_list_ids:
                for data in record.examination_list_ids.ids:
                    master_sampling_ids = self.env['master.sampling'].search([]).filtered(lambda r: data in r.master_action_ids.ids)
                    val += [rec.id for rec in master_sampling_ids if master_sampling_ids and rec.id not in val]
            if record.additional_examination_ids:
                for rec in record.additional_examination_ids:
                    master_sampling_ids = self.env['master.sampling'].search([]).filtered(lambda r: rec in r.master_action_ids.ids)
                    val += [data.id for data in master_sampling_ids if master_sampling_ids and data.id not in val]
            record.sampling_list_ids = [(6, 0, val)]
            
    @api.depends('examination_list_ids', 'jenis_perjanjian')
    def _compute_filter_examination_ids(self):
        for data in self:         
            domain_examination_ids         = [('is_service', '=', True)]   
            if data.examination_list_ids and data.jenis_perjanjian in ['mcu', 'onsite']:
                domain_examination_ids     += [('id', 'not in', data.examination_list_ids.ids)]
            data.filter_examination_ids       = self.env['product.product'].search(domain_examination_ids)
    
    # Filter Examination List berdasarkan Poli / Unit
    @api.depends('poli_unit_ids', 'is_perjanjian')
    def _compute_examination_ids(self):
        for data in self:
            domain_examination_ids   = [('is_service', '=', True)]
            if data.is_perjanjian and data.poli_unit_ids:
                domain_examination_ids     += [('poli_unit_id', 'in', data.poli_unit_ids.ids)]
            data.examination_ids = self.env['product.product'].search(domain_examination_ids)
    
    # Filter Data Package MCU berdasarkan Jenis Perjanjian dan Perusahaan yang dipilih
    @api.depends('perusahaan_id', 'jenis_perjanjian')
    def _compute_package_mcu_ids(self):
        for data in self:         
            domain_packet_mcu       = [('state' , '=' , 'approved'), ('status' , '=' , 'Active')]   
            if data.perusahaan_id:
                domain_packet_mcu   += [('perusahaan_id', '=', data.perusahaan_id.id)]
            if data.jenis_perjanjian:
                if data.jenis_perjanjian == 'mcu':
                    domain_packet_mcu   += [('in_house', '=', True)]
                if data.jenis_perjanjian == 'onsite':
                    domain_packet_mcu   += [('onsite', '=', True)]
            data.package_mcu_ids   = self.env['package.mcu'].search(domain_packet_mcu)
    
    # Filter Paket berdasarkan Package MCU yang dipilih
    @api.depends('package_mcu_id')
    def _compute_list_package_ids(self):
        for data in self:         
            domain_list_package         = []   
            if data.package_mcu_id:
                domain_list_package     += [('package_mcu_id', '=', data.package_mcu_id.id)]
            data.list_package_ids       = self.env['list.package'].search(domain_list_package)
            
    @api.depends('additional_examination_ids.list_price')
    def _compute_total_cost_examination_ids(self):
        for rec in self:
            rec.total_cost_examination_ids  = sum(rec.additional_examination_ids.mapped('list_price'))
    
    # Total Cost Sampling
    @api.depends('sampling_list_ids.total_cost')
    def _compute_total_cost_sampling(self):
        for rec in self:
            rec.total_cost_sampling  = sum(rec.sampling_list_ids.mapped('total_cost'))
    
    # Total Cost Examination List
    @api.depends('examination_list_ids.list_price')
    def _compute_total_cost_examination_list(self):
        for rec in self:
            rec.total_cost_examination_list  = sum(rec.examination_list_ids.mapped('list_price'))
    
    # Total Cost Keseluruhan
    @api.depends('total_cost_examination_list', 'total_cost_sampling', 'fix_price_paket', 'total_cost_examination_ids')
    def _compute_total_cost(self):
        for rec in self:
            if rec.jenis_perjanjian == 'mc':
                rec.total_cost      = rec.total_cost_examination_list + rec.total_cost_sampling
            if rec.jenis_perjanjian == 'mcu' or rec.jenis_perjanjian == 'onsite':
                rec.total_cost      = rec.fix_price_paket + rec.total_cost_examination_ids

class ConfigFixedCostingLine(models.Model):
    _inherit        = 'config.fixed.costing.line'
    _description    = 'Config Fixed Costing Line'
    
    registration_id = fields.Many2one( 'master.registration', 
                                        string   = 'Registration ID',
                                        index    = True,
                                        ondelete = 'cascade')
    
class ListPemeriksaanPoli(models.Model):
    _inherit            = 'list.pemeriksaan.poli'
    _description        = 'List Pemeriksaan Poli'
    
    registration_id     = fields.Many2one('master.registration', 
                                          string   = 'Registrasi',
                                          index    = True,
                                          ondelete = 'cascade')