from odoo import _, api, fields, models, tools, SUPERUSER_ID
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta

class MasterReservation(models.Model):
    _name                   = 'master.reservation'
    _description            = 'Master Reservation'
    _inherit                = ['mail.thread', 'mail.activity.mixin']
    
    name                    = fields.Char( string   = 'No. RSV.', 
                                           default  = "New",
                                           required = True, 
                                           readonly = True)
    
    no_gl                   = fields.Char( string   = 'No. GL', 
                                           readonly = True,
                                           tracking = True, 
                                           states   = {'draft': [('readonly', False)]})
    
    tanggal_reservasi       = fields.Date( string   = 'Tanggal Reservasi', 
                                           default  = fields.Date.today(), 
                                           readonly = True, 
                                           required = True,
                                           tracking = True, 
                                           states   = {'draft': [('readonly', False)]})
    
    faskes_id               = fields.Many2one( 'master.fasilitas.kesehatan', 
                                               string   = 'Fasilitas Kesehatan',
                                               readonly = True,
                                               store    = True, 
                                               index    = True,
                                               default  = lambda self: self.env.user.faskes_id.id)
    
    code                    = fields.Char(  string   ='Kode Unit',
                                            readonly = True, 
                                            store    = True,
                                            related  = 'faskes_id.kode_faskes')
    
    state                   = fields.Selection( [
                                                    ('draft', 'Draft'),
                                                    ('confirm', 'Confirmed'),
                                                    ('done', 'Registered'),
                                                    ('cancel', 'Cancelled'),
                                                ],  string   = 'Status', 
                                                    default  = 'draft',
                                                    copy     = False,
                                                    tracking = True)
    
    status_kunjungan        = fields.Selection( [
                                                    ('perjanjian', 'Perjanjian'),
                                                    ('prioritas', 'Prioritas'),
                                                ],  string      = 'Status Kunjungan', 
                                                    default     = 'perjanjian', 
                                                    readonly    = True, 
                                                    required    = True,
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
    
    tipe_pengiriman         = fields.Selection( [
                                                    ('normal', 'Normal'),
                                                    ('sameday', 'Sameday Service'),
                                                ],  string      = 'Tipe Pengiriman', 
                                                    default     = 'normal', 
                                                    readonly    = True, 
                                                    required    = True,
                                                    tracking    = True, 
                                                    states      = {'draft': [('readonly', False)]})
    
    tipe_rsv                = fields.Selection( [
                                                    ('direct', 'Direct'),
                                                    ('online', 'Online'),
                                                ],  string      = 'Tipe RSV.', 
                                                    default     = 'direct',
                                                    store       = True, 
                                                    readonly    = True)
    
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
    
    # Relasi ke Pasien
    pasien_id               = fields.Many2one( 'res.partner', 
                                                string   = 'Nama Pasien', 
                                                required = True,
                                                readonly = True, 
                                                tracking = True, 
                                                states   = {'draft': [('readonly', False)]})
    
    display_name            = fields.Char( string   = 'Nama Pasien', 
                                           related  = 'pasien_id.display_name')
    
    no_ktp                  = fields.Char( string   = 'No. KTP', 
                                           related  = 'pasien_id.no_ktp')
    
    email                   = fields.Char( string   = "Email Pasien", 
                                           related  = 'pasien_id.email')
    
    mobile                  = fields.Char( string   = "Nomor HP", 
                                           related  = 'pasien_id.mobile')
    
    umur                    = fields.Char( string   = 'Umur', 
                                           related  = 'pasien_id.umur',
                                           store    = True)
    
    tanggal_lahir           = fields.Date( string   = 'Tanggal Lahir', 
                                           related  = 'pasien_id.tanggal_lahir')
    
    warga_negara            = fields.Selection( related = 'pasien_id.warga_negara')
    
    jenis_kelamin           = fields.Selection( related = 'pasien_id.jenis_kelamin')
    
    street                  = fields.Char( related = 'pasien_id.street')
    
    street2                 = fields.Char( related = 'pasien_id.street2')
    
    zip                     = fields.Char( change_default = True, 
                                           related = 'pasien_id.zip')
    
    city                    = fields.Char( related = 'pasien_id.city')
    
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
    
    state_id                = fields.Many2one( 'res.country.state', 
                                                string   = 'State', 
                                                ondelete = 'restrict', 
                                                domain   = "[('country_id', '=?', country_id)]", 
                                                related  ='pasien_id.state_id')
    
    country_id              = fields.Many2one( 'res.country', 
                                                string   = 'Country', 
                                                ondelete = 'restrict', 
                                                related  = 'pasien_id.country_id')
    
    # Pekerjaan
    nik_pegawai             = fields.Char( string   = 'NIK Pegawai', 
                                           related  = 'pasien_id.nik_pegawai')
    
    status_pegawai          = fields.Selection( string   = 'Status Kepegawaian',
                                                related  = 'pasien_id.status_pegawai')
    
    mulai_bekerja           = fields.Date( string    = 'Mulai Bekerja',
                                           related   = 'pasien_id.mulai_bekerja')
    
    jenis_pekerjaan_id      = fields.Many2one( 'master.jenis.pekerjaan', 
                                                string   = 'Jenis Pekerjaan',
                                                related  = 'pasien_id.jenis_pekerjaan_id')
    
    shift_kerja             = fields.Selection( string   = 'Shift Kerja',
                                                related  = 'pasien_id.shift_kerja')
    
    lokasi_pekerjaan_id     = fields.Many2one( 'master.lokasi.pekerjaan', 
                                                related  = 'pasien_id.lokasi_pekerjaan_id')
    
    function                = fields.Char( string    = 'Posisi / Jabatan',
                                           related   = 'pasien_id.function')
    
    # Relasi ke Perusahaan
    perusahaan_id           = fields.Many2one(  'res.partner', 
                                                string   = 'Perusahaan', 
                                                readonly = True,
                                                required = True,
                                                ondelete = 'restrict', 
                                                tracking = True, 
                                                states   = {'draft': [('readonly', False)]})
    
    partner_id              = fields.Many2one( 'res.partner', string = 'PIC Perusahaan',
                                                readonly = True,
                                                required = True,
                                                tracking = True, 
                                                states   = {'draft': [('readonly', False)]})
    
    function                = fields.Char(  string   = 'Posisi / Jabatan',
                                            related  = 'partner_id.function',
                                            tracking = True)
    
    client_title_id         = fields.Many2one('pic.title', 
                                              string  = 'PIC Title', 
                                              related = 'partner_id.client_title_id',
                                              domain  = [('type', '=', 'client')])
    
    email_pic               = fields.Char(  string   = 'Email PIC', 
                                            related  = 'partner_id.email',
                                            tracking = True)
    
    mobile_pic              = fields.Char(  string   = 'No. HP PIC', 
                                            related  = 'partner_id.mobile',
                                            tracking = True)
    
    # Relasi ke Paket MCU
    poli_unit_ids           = fields.Many2many( 'master.poli.unit', 
                                                string      = 'Poli / Unit', 
                                                copy        = False,
                                                tracking    = True,
                                                readonly    = True, 
                                                states      = {'draft': [('readonly', False)]})
    
    dokter_id               = fields.Many2one( 'res.partner', 
                                                string   = 'Nama Dokter',
                                                copy     = False,
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
    
    package_mcu_id          = fields.Many2one( 'package.mcu', 
                                                string   = 'Package MCU',
                                                readonly = True, 
                                                tracking = True,
                                                copy     = False,
                                                states   = {'draft': [('readonly', False)]})
    
    list_package_id         = fields.Many2one( 'list.package', 
                                                string   = 'List Package', 
                                                readonly = True, 
                                                tracking = True,
                                                copy     = False,
                                                states   = {'draft': [('readonly', False)]})
    
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
    
    fixed_costing_line      = fields.One2many(  'config.fixed.costing.line', 
                                                'reservation_id', 
                                                string   = 'Fixed Costing',
                                                readonly = True,
                                                store    = True,
                                                copy     = False,
                                                tracking = True)
    
    examination_list_ids    = fields.Many2many( 'config.examination.list', 
                                                string   = 'Examination List',
                                                readonly = True,
                                                store    = True,
                                                copy     = False,
                                                tracking = True)
    
    sampling_list_ids       = fields.Many2many( 'master.sampling', 
                                                string   ='Sampling List',
                                                readonly = True,
                                                store    = True,
                                                copy     = False,
                                                tracking = True)
    
    price_paket             = fields.Float( string   = 'Price Paket MCU (IDR)',
                                            store    = True,
                                            tracking = True,
                                            related  = 'list_package_id.price_paket')
    
    fix_price_paket         = fields.Float( compute = '_compute_fix_price_paket', 
                                            string  = 'Total Cost Keseluruhan (IDR)',
                                            store   = True)
    
    currency_id             = fields.Many2one( 'res.currency', 'Currency',
                                                default  = lambda self: self.env.company.currency_id.id,
                                                readonly = True)
    
    package_mcu_ids         = fields.Many2many( 'package.mcu', 
                                                compute='_compute_package_mcu_ids')
    
    list_package_ids        = fields.Many2many( 'list.package', 
                                                compute='_compute_list_package_ids')
    
    perusahaan_ids          = fields.Many2many( 'res.partner', 
                                                compute = '_compute_perusahaan')
    
    partner_ids             = fields.Many2many( 'res.partner', 
                                                compute = '_compute_partner')
    
    pasien_ids             = fields.Many2many( 'res.partner', 
                                                compute = '_compute_pasien')
    
    poli_ids                = fields.Many2many( 'master.poli.unit', 
                                                compute = '_compute_poli_ids')
    
    dokter_ids              = fields.Many2many( 'res.partner', 
                                                compute = '_compute_dokter_ids')
    
    examination_ids         = fields.Many2many( 'product.product', 
                                                compute = '_compute_examination_ids')
    
    additional_examination_ids  = fields.Many2many( 'product.product', 
                                                    string   = 'Additional Examination List',
                                                    store    = True,
                                                    readonly = True, 
                                                    tracking = True,
                                                    copy     = False,
                                                    states   = {'draft': [('readonly', False)]})
    
    total_margin                = fields.Float( string   = 'Total Cost Margin (IDR)',
                                                readonly = True,
                                                store    = True,
                                                tracking = True)
    
    total_cost_examination_list = fields.Float( string   = 'Total Fixed Price Additional Examination List (IDR)',
                                                store    = True,
                                                readonly = True,
                                                tracking = True)
    
    total_list_price            = fields.Float( string   = 'Total Price Additional Examination List (IDR)',
                                                store    = True,
                                                readonly = True,
                                                tracking = True)
    
    edit_hide_css               = fields.Html( string    = 'CSS', 
                                               sanitize  = False, 
                                               compute   = '_compute_edit_hide_css')
    
    is_poli_penunjang           = fields.Boolean( string    = 'Poli Penunjang',
                                                  store     = True,
                                                  default   = False)
            
    # Cron Job : Update State
    @api.model
    def update_state_reservation(self):
        self.search([
            ('state', 'in', ['draft', 'confirm']), 
            ('tanggal_reservasi', '<', fields.Date.today()),
        ]).write({
            'state' : 'cancel'
        })
        return True
    
    # Ambil Data untuk Dashboard Data Reservasi / Hari ini
    @api.model
    def retrieve_dashboard(self):
        self.check_access_rights('read')
        result = {
            # Today
            'today_reservation'         : fields.Date.today().strftime('%d - %m - %Y'),
            'total_perjanjian_today'    : 0,
            'perjanjian_mc_today'       : 0,
            'perjanjian_mcu_today'      : 0,
            'registered_today'          : 0,
            'waiting_today'             : 0,
            'perjanjian_online_today'   : 0,
            'perjanjian_direct_today'   : 0,
            'spesialis_mata_today'      : 0,
            'spesialis_tht_today'       : 0,
            'spesialis_jantung_today'   : 0,
            'spesialis_dalam_today'     : 0,
            'spesialis_paru_today'      : 0,
            'dokter_gigi_today'         : 0,
            'dokter_umum_today'         : 0,
            'audiometri_today'          : 0,
            'spirometri_today'          : 0,
            'ekg_today'                 : 0,
            'treadmill_today'           : 0,
            
            # Tomorrow
            'tomorrow_reservation'       : (fields.Date.today() + relativedelta(days=1)).strftime('%d - %m - %Y'),
            'total_perjanjian_tomorrow'  : 0,
            'perjanjian_mc_tomorrow'     : 0,
            'perjanjian_mcu_tomorrow'    : 0,
            'registered_tomorrow'        : 0,
            'waiting_tomorrow'           : 0,
            'perjanjian_online_tomorrow' : 0,
            'perjanjian_direct_tomorrow' : 0,
            'spesialis_mata_tomorrow'    : 0,
            'spesialis_tht_tomorrow'     : 0,
            'spesialis_jantung_tomorrow' : 0,
            'spesialis_dalam_tomorrow'   : 0,
            'spesialis_paru_tomorrow'    : 0,
            'dokter_gigi_tomorrow'       : 0,
            'dokter_umum_tomorrow'       : 0,
            'audiometri_tomorrow'        : 0,
            'spirometri_tomorrow'        : 0,
            'ekg_tomorrow'               : 0,
            'treadmill_tomorrow'         : 0,
        }
        
        
        # Today
        mr                                = self.env['master.reservation']
        result['total_perjanjian_today']  = mr.search_count([('tanggal_reservasi', '=', fields.Date.today()), ('faskes_id', '=', self.env.user.faskes_id.id)])
        result['perjanjian_mc_today']     = mr.search_count([('jenis_perjanjian', '=', 'mc'), ('tanggal_reservasi', '=', fields.Date.today()), ('faskes_id', '=', self.env.user.faskes_id.id)])
        result['perjanjian_mcu_today']    = mr.search_count([('jenis_perjanjian', 'in', ['mcu', 'onsite']), ('tanggal_reservasi', '=', fields.Date.today()), ('faskes_id', '=', self.env.user.faskes_id.id)])
        result['registered_today']        = mr.search_count([('state', '=', 'done'), ('tanggal_reservasi', '=', fields.Date.today()), ('faskes_id', '=', self.env.user.faskes_id.id)])
        result['waiting_today']           = mr.search_count([('state', '=', 'draft'), ('tanggal_reservasi', '=', fields.Date.today()), ('faskes_id', '=', self.env.user.faskes_id.id)])
        result['perjanjian_direct_today'] = mr.search_count([('tipe_rsv', '=', 'direct'), ('tanggal_reservasi', '=', fields.Date.today()), ('faskes_id', '=', self.env.user.faskes_id.id)])
        result['perjanjian_online_today'] = mr.search_count([('tipe_rsv', '=', 'online'), ('tanggal_reservasi', '=', fields.Date.today()), ('faskes_id', '=', self.env.user.faskes_id.id)])
        result['spesialis_mata_today']    = mr.search_count([('tanggal_reservasi', '=', fields.Date.today()), ('faskes_id', '=', self.env.user.faskes_id.id), '|', ('poli_unit_ids.nama_poli_unit', 'ilike', 'mata'), '|', '&', ('examination_list_ids.poli_unit_id.nama_poli_unit', 'ilike', 'mata'), ('examination_list_ids.master_tindakan_id.kategori_produk_id.kategori_produk', 'ilike', 'konsul'), '&', ('additional_examination_ids.poli_unit_id.nama_poli_unit', 'ilike', 'mata'), ('additional_examination_ids.kategori_produk_id.kategori_produk', 'ilike', 'konsul')])
        result['spesialis_tht_today']     = mr.search_count([('tanggal_reservasi', '=', fields.Date.today()), ('faskes_id', '=', self.env.user.faskes_id.id), '|', ('poli_unit_ids.nama_poli_unit', 'ilike', 'tht'), '|', '&', ('examination_list_ids.poli_unit_id.nama_poli_unit', 'ilike', 'tht'), ('examination_list_ids.master_tindakan_id.kategori_produk_id.kategori_produk', 'ilike', 'konsul'), '&', ('additional_examination_ids.poli_unit_id.nama_poli_unit', 'ilike', 'tht'), ('additional_examination_ids.kategori_produk_id.kategori_produk', 'ilike', 'konsul')])
        result['spesialis_jantung_today'] = mr.search_count([('tanggal_reservasi', '=', fields.Date.today()), ('faskes_id', '=', self.env.user.faskes_id.id), '|', ('poli_unit_ids.nama_poli_unit', 'ilike', 'jantung'), '|', '&', ('examination_list_ids.poli_unit_id.nama_poli_unit', 'ilike', 'jantung'), ('examination_list_ids.master_tindakan_id.kategori_produk_id.kategori_produk', 'ilike', 'konsul'), '&', ('additional_examination_ids.poli_unit_id.nama_poli_unit', 'ilike', 'jantung'), ('additional_examination_ids.kategori_produk_id.kategori_produk', 'ilike', 'konsul')])
        result['spesialis_dalam_today']   = mr.search_count([('tanggal_reservasi', '=', fields.Date.today()), ('faskes_id', '=', self.env.user.faskes_id.id), '|', ('poli_unit_ids.nama_poli_unit', 'ilike', 'dalam'), '|', '&', ('examination_list_ids.poli_unit_id.nama_poli_unit', 'ilike', 'dalam'), ('examination_list_ids.master_tindakan_id.kategori_produk_id.kategori_produk', 'ilike', 'konsul'), '&', ('additional_examination_ids.poli_unit_id.nama_poli_unit', 'ilike', 'dalam'), ('additional_examination_ids.kategori_produk_id.kategori_produk', 'ilike', 'konsul')])
        result['spesialis_paru_today']    = mr.search_count([('tanggal_reservasi', '=', fields.Date.today()), ('faskes_id', '=', self.env.user.faskes_id.id), '|', ('poli_unit_ids.nama_poli_unit', 'ilike', 'paru'), '|', '&', ('examination_list_ids.poli_unit_id.nama_poli_unit', 'ilike', 'paru'), ('examination_list_ids.master_tindakan_id.kategori_produk_id.kategori_produk', 'ilike', 'konsul'), '&', ('additional_examination_ids.poli_unit_id.nama_poli_unit', 'ilike', 'paru'), ('additional_examination_ids.kategori_produk_id.kategori_produk', 'ilike', 'konsul')])
        result['dokter_gigi_today']       = mr.search_count([('tanggal_reservasi', '=', fields.Date.today()), ('faskes_id', '=', self.env.user.faskes_id.id), '|', '|', ('poli_unit_ids.nama_poli_unit', 'ilike', 'gigi'), ('examination_list_ids.poli_unit_id.nama_poli_unit', 'ilike', 'gigi'), ('additional_examination_ids.poli_unit_id.nama_poli_unit', 'ilike', 'gigi')])
        result['dokter_umum_today']       = mr.search_count([('tanggal_reservasi', '=', fields.Date.today()), ('faskes_id', '=', self.env.user.faskes_id.id), '|', '|', ('poli_unit_ids.nama_poli_unit', 'ilike', 'umum'), ('examination_list_ids.poli_unit_id.nama_poli_unit', 'ilike', 'umum'), ('additional_examination_ids.poli_unit_id.nama_poli_unit', 'ilike', 'umum')])
        result['audiometri_today']        = mr.search_count([('tanggal_reservasi', '=', fields.Date.today()), ('faskes_id', '=', self.env.user.faskes_id.id), '|', ('examination_list_ids.name', 'ilike', 'audiom'), ('additional_examination_ids.name', 'ilike', 'audiom')])
        result['spirometri_today']        = mr.search_count([('tanggal_reservasi', '=', fields.Date.today()), ('faskes_id', '=', self.env.user.faskes_id.id), '|', ('examination_list_ids.name', 'ilike', 'spirom'), ('additional_examination_ids.name', 'ilike', 'spirom')])
        result['ekg_today']               = mr.search_count([('tanggal_reservasi', '=', fields.Date.today()), ('faskes_id', '=', self.env.user.faskes_id.id), '|', ('examination_list_ids.name', 'ilike', 'ekg'), ('additional_examination_ids.name', 'ilike', 'ekg')])
        result['treadmill_today']         = mr.search_count([('tanggal_reservasi', '=', fields.Date.today()), ('faskes_id', '=', self.env.user.faskes_id.id), '|', ('examination_list_ids.name', 'ilike', 'treadmill'), ('additional_examination_ids.name', 'ilike', 'treadmill')])
        
        # Tomorrow
        result['total_perjanjian_tomorrow']  = mr.search_count([('tanggal_reservasi', '=', (fields.Date.today() + relativedelta(days=1))), ('faskes_id', '=', self.env.user.faskes_id.id)])
        result['perjanjian_mc_tomorrow']     = mr.search_count([('jenis_perjanjian', '=', 'mc'), ('tanggal_reservasi', '=', (fields.Date.today() + relativedelta(days=1))), ('faskes_id', '=', self.env.user.faskes_id.id)])
        result['perjanjian_mcu_tomorrow']    = mr.search_count([('jenis_perjanjian', 'in', ['mcu', 'onsite']), ('tanggal_reservasi', '=', (fields.Date.today() + relativedelta(days=1))), ('faskes_id', '=', self.env.user.faskes_id.id)])
        result['registered_tomorrow']        = mr.search_count([('state', '=', 'done'), ('tanggal_reservasi', '=', (fields.Date.today() + relativedelta(days=1))), ('faskes_id', '=', self.env.user.faskes_id.id)])
        result['waiting_tomorrow']           = mr.search_count([('state', '=', 'draft'), ('tanggal_reservasi', '=', (fields.Date.today() + relativedelta(days=1))), ('faskes_id', '=', self.env.user.faskes_id.id)])
        result['perjanjian_direct_tomorrow'] = mr.search_count([('tipe_rsv', '=', 'direct'), ('tanggal_reservasi', '=', (fields.Date.today() + relativedelta(days=1))), ('faskes_id', '=', self.env.user.faskes_id.id)])
        result['perjanjian_online_tomorrow'] = mr.search_count([('tipe_rsv', '=', 'online'), ('tanggal_reservasi', '=', (fields.Date.today() + relativedelta(days=1))), ('faskes_id', '=', self.env.user.faskes_id.id)])
        result['spesialis_mata_tomorrow']    = mr.search_count([('tanggal_reservasi', '=', (fields.Date.today() + relativedelta(days=1))), ('faskes_id', '=', self.env.user.faskes_id.id), '|', ('poli_unit_ids.nama_poli_unit', 'ilike', 'mata'), '|', '&', ('examination_list_ids.poli_unit_id.nama_poli_unit', 'ilike', 'mata'), ('examination_list_ids.master_tindakan_id.kategori_produk_id.kategori_produk', 'ilike', 'konsul'), '&', ('additional_examination_ids.poli_unit_id.nama_poli_unit', 'ilike', 'mata'), ('additional_examination_ids.kategori_produk_id.kategori_produk', 'ilike', 'konsul')])
        result['spesialis_tht_tomorrow']     = mr.search_count([('tanggal_reservasi', '=', (fields.Date.today() + relativedelta(days=1))), ('faskes_id', '=', self.env.user.faskes_id.id), '|', ('poli_unit_ids.nama_poli_unit', 'ilike', 'tht'), '|', '&', ('examination_list_ids.poli_unit_id.nama_poli_unit', 'ilike', 'tht'), ('examination_list_ids.master_tindakan_id.kategori_produk_id.kategori_produk', 'ilike', 'konsul'), '&', ('additional_examination_ids.poli_unit_id.nama_poli_unit', 'ilike', 'tht'), ('additional_examination_ids.kategori_produk_id.kategori_produk', 'ilike', 'konsul')])
        result['spesialis_jantung_tomorrow'] = mr.search_count([('tanggal_reservasi', '=', (fields.Date.today() + relativedelta(days=1))), ('faskes_id', '=', self.env.user.faskes_id.id), '|', ('poli_unit_ids.nama_poli_unit', 'ilike', 'jantung'), '|', '&', ('examination_list_ids.poli_unit_id.nama_poli_unit', 'ilike', 'jantung'), ('examination_list_ids.master_tindakan_id.kategori_produk_id.kategori_produk', 'ilike', 'konsul'), '&', ('additional_examination_ids.poli_unit_id.nama_poli_unit', 'ilike', 'jantung'), ('additional_examination_ids.kategori_produk_id.kategori_produk', 'ilike', 'konsul')])
        result['spesialis_dalam_tomorrow']   = mr.search_count([('tanggal_reservasi', '=', (fields.Date.today() + relativedelta(days=1))), ('faskes_id', '=', self.env.user.faskes_id.id), '|', ('poli_unit_ids.nama_poli_unit', 'ilike', 'dalam'), '|', '&', ('examination_list_ids.poli_unit_id.nama_poli_unit', 'ilike', 'dalam'), ('examination_list_ids.master_tindakan_id.kategori_produk_id.kategori_produk', 'ilike', 'konsul'), '&', ('additional_examination_ids.poli_unit_id.nama_poli_unit', 'ilike', 'dalam'), ('additional_examination_ids.kategori_produk_id.kategori_produk', 'ilike', 'konsul')])
        result['spesialis_paru_tomorrow']    = mr.search_count([('tanggal_reservasi', '=', (fields.Date.today() + relativedelta(days=1))), ('faskes_id', '=', self.env.user.faskes_id.id), '|', ('poli_unit_ids.nama_poli_unit', 'ilike', 'paru'), '|', '&', ('examination_list_ids.poli_unit_id.nama_poli_unit', 'ilike', 'paru'), ('examination_list_ids.master_tindakan_id.kategori_produk_id.kategori_produk', 'ilike', 'konsul'), '&', ('additional_examination_ids.poli_unit_id.nama_poli_unit', 'ilike', 'paru'), ('additional_examination_ids.kategori_produk_id.kategori_produk', 'ilike', 'konsul')])
        result['dokter_gigi_tomorrow']       = mr.search_count([('tanggal_reservasi', '=', (fields.Date.today() + relativedelta(days=1))), ('faskes_id', '=', self.env.user.faskes_id.id), '|', '|', ('poli_unit_ids.nama_poli_unit', 'ilike', 'gigi'), ('examination_list_ids.poli_unit_id.nama_poli_unit', 'ilike', 'gigi'), ('additional_examination_ids.poli_unit_id.nama_poli_unit', 'ilike', 'gigi')])
        result['dokter_umum_tomorrow']       = mr.search_count([('tanggal_reservasi', '=', (fields.Date.today() + relativedelta(days=1))), ('faskes_id', '=', self.env.user.faskes_id.id), '|', '|', ('poli_unit_ids.nama_poli_unit', 'ilike', 'umum'), ('examination_list_ids.poli_unit_id.nama_poli_unit', 'ilike', 'umum'), ('additional_examination_ids.poli_unit_id.nama_poli_unit', 'ilike', 'umum')])
        result['audiometri_tomorrow']        = mr.search_count([('tanggal_reservasi', '=', (fields.Date.today() + relativedelta(days=1))), ('faskes_id', '=', self.env.user.faskes_id.id), '|', ('examination_list_ids.name', 'ilike', 'audiom'), ('additional_examination_ids.name', 'ilike', 'audiom')])
        result['spirometri_tomorrow']        = mr.search_count([('tanggal_reservasi', '=', (fields.Date.today() + relativedelta(days=1))), ('faskes_id', '=', self.env.user.faskes_id.id), '|', ('examination_list_ids.name', 'ilike', 'spirom'), ('additional_examination_ids.name', 'ilike', 'spirom')])
        result['ekg_tomorrow']               = mr.search_count([('tanggal_reservasi', '=', (fields.Date.today() + relativedelta(days=1))), ('faskes_id', '=', self.env.user.faskes_id.id), '|', ('examination_list_ids.name', 'ilike', 'ekg'), ('additional_examination_ids.name', 'ilike', 'ekg')])
        result['treadmill_tomorrow']         = mr.search_count([('tanggal_reservasi', '=', (fields.Date.today() + relativedelta(days=1))), ('faskes_id', '=', self.env.user.faskes_id.id), '|', ('examination_list_ids.name', 'ilike', 'treadmill'), ('additional_examination_ids.name', 'ilike', 'treadmill')])
        
        return result
    
    # Sequence
    @api.model
    def create(self, vals):
        vals['name']            = self.env['ir.sequence'].next_by_code('master.reservation.sequence')
        return super(MasterReservation, self).create(vals)
    
    # Name Get
    def name_get(self):
        res = []
        for rec in self:
            res.append((rec.id, '%s - %s - %s' % (rec.name, rec.display_name, rec.perusahaan_id.name)))
        return res
    
    # Button Action Confirm
    def action_confirm(self):
        return self.write({
                            'state'          : 'confirm',
                            'tanggal_confirm': fields.Date.today(),
                            'user_approve'   : self.env.user
                         })
    
    # Button Action Set to Draft
    def action_set_to_draft(self):
        return self.write({'state': 'draft'})
    
    # Button Action Cancel
    def action_cancel(self):
        return self.write({'state': 'cancel'})
    
    # Ambil Data Fixed Costing, Examination List dan Sampling dari Package ID yanf dipilih
    @api.onchange('list_package_id', 'poli_unit_ids')
    def _onchange_is_poli_penunjang(self):
        for rec in self:
            lines = [(5, 0, 0)]
            if rec.poli_unit_ids:
                poli_penunjang = [data.kategori for data in rec.poli_unit_ids]
                rec.is_poli_penunjang = False if any(data == 'poli' for data in poli_penunjang if poli_penunjang) else True
                if any(data == 'poli' for data in poli_penunjang if poli_penunjang):
                    rec.additional_examination_ids = False
            elif rec.list_package_id:
                rec.is_poli_penunjang = True
                rec.additional_examination_ids = False
                for line in rec.list_package_id.fixed_costing_line:
                    val = {
                        'fixed_costing_id'  : line.fixed_costing_id.id,
                        'name'              : line.name,
                        'cost_in_house'     : line.cost_in_house,
                        'cost_onsite'       : line.cost_onsite
                    } 
                    lines.append((0, 0, val))
                rec.fixed_costing_line         = lines
                rec.bahasa_hasil               = rec.list_package_id.bahasa_hasil
                rec.examination_list_ids       = rec.list_package_id.examination_list_ids
                rec.sampling_list_ids          = rec.list_package_id.sampling_list_ids
            else:
                rec.bahasa_hasil = 'inggris'
                rec.is_poli_penunjang = False
                rec.additional_examination_ids = False
    
    # Ambil Data Perusahaan berdasarkan Data Pasien
    @api.onchange('pasien_id')
    def compute_perusahaan_id(self):
        for rec in self:
            if not rec.pasien_id:
                rec.perusahaan_id = rec.list_package_id = rec.package_mcu_id = False
            else:
                perusahaan_ids      = self.env['res.partner'].search([
                    ('is_company', '=', True), '|', '&', ('is_perusahaan', '=', True), 
                    ('status_perusahaan', '=', 'approved'), '&', ('client', '=', True), 
                    ('client_state', '=', 'enabled')]).ids
                if rec.pasien_id.perusahaan_id.id in perusahaan_ids:
                    rec.perusahaan_id   = rec.pasien_id.perusahaan_id.id
                    rec.list_package_id = rec.package_mcu_id = False
                else:
                    rec.pasien_id = rec.perusahaan_id = rec.list_package_id = rec.package_mcu_id = False
                    message         = "Data Perusahaan Pasien Belum Terverifikasi"
                    return{ 'warning':{
                                'title': "Invalid Data Perusahaan",
                                'message': message
                            }}
    
    # Ambil List Data PIC Perusahaan berdasarkan Perusahaan yang dipilij
    @api.onchange('perusahaan_id')
    def compute_partner_id(self):
        for rec in self:
            if not rec.perusahaan_id:
                rec.partner_id      = rec.list_package_id = rec.package_mcu_id  = False
            else:
                rec.partner_id      = rec.perusahaan_id.pic_perusahaan_line.ids
                rec.list_package_id = rec.package_mcu_id  = False
    
    # Kosongkan Field Dokter apabila Poli Unit berubah
    @api.onchange('poli_unit_ids')
    def compute_dokter_id(self):
        for rec in self:
             rec.dokter_id      = False if not rec.poli_unit_ids else False
    
    # Kosongkan Field Package MCU, Paket, Poli Unit, atau Dokter berdasarkan Jenis Perjanjian
    @api.onchange('jenis_perjanjian')
    def compute_package_id(self):
        for rec in self:
            if rec.jenis_perjanjian != 'mcu' or rec.jenis_perjanjian != 'onsite':
                rec.package_mcu_id  = rec.list_package_id = False
            if rec.jenis_perjanjian != 'mc':
                rec.dokter_id       = rec.poli_unit_ids   = False
                    
    # Bersihkan Data yang berkaitan dengan Package MCU ketika ada perubahan
    @api.onchange('package_mcu_id')
    def compute_list_package_id(self):
        for rec in self:
            if not rec.package_mcu_id:
                rec.list_package_id = rec.fixed_costing_line = rec.examination_list_ids = rec.sampling_list_ids = rec.additional_examination_ids = False
            if rec.package_mcu_id:
                rec.list_package_id = rec.fixed_costing_line = rec.examination_list_ids = rec.sampling_list_ids = rec.additional_examination_ids = False
    
    # Perhitungan untuk Additional Examination List
    @api.onchange('additional_examination_ids')
    def compute_additional_examination_ids(self):
        for rec in self:
            values, values_margin = [], []
            values_list_price = [data.list_price for data in rec.additional_examination_ids if rec.additional_examination_ids]
            if rec.additional_examination_ids:
                for data in rec.additional_examination_ids:
                    record_pricelist_ids = self.env['master.tindakan.layanan.line'].search([('master_tindakan_id', 'in', data.ids)]).filtered(lambda r : rec.perusahaan_id.id in r.pricelist_id.perusahaan_id.ids)
                    values_margin += record_pricelist_ids.mapped('margin') if record_pricelist_ids else []
                    if record_pricelist_ids:
                        values += record_pricelist_ids.mapped('harga_khusus')
                    else:
                        values.append(data.list_price)            
            rec.total_margin, rec.total_list_price, rec.total_cost_examination_list = sum(values_margin), sum(values_list_price), sum(values)
            
    # Tombol Edit CSS
    @api.depends('state')
    def _compute_edit_hide_css(self):
        for rec in self:
            if rec.state not in ['draft']:
                rec.edit_hide_css = '<style>.o_form_button_edit {display: none !important;}</style>'
            else:
                rec.edit_hide_css = False
    
    # Filter Poli berdasarkan Faskes
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
    
    @api.depends('examination_list_ids.master_tindakan_id', 'is_poli_penunjang', 'poli_unit_ids')
    def _compute_examination_ids(self):
        for data in self:         
            domain_examination_ids         = [('is_service', '=', True)]   
            if data.examination_list_ids and data.is_poli_penunjang:
                domain_examination_ids     += [('id', 'not in', data.examination_list_ids.master_tindakan_id.ids)]
            if data.is_poli_penunjang and data.poli_unit_ids:
                domain_examination_ids     += [('poli_unit_id', 'in', data.poli_unit_ids.ids)]
            data.examination_ids       = self.env['product.product'].search(domain_examination_ids)
    
    # Perhitungan Fix Price Paket berdasarkan Tipe Pengiriman
    @api.depends('price_paket', 'tipe_pengiriman', 'total_cost_examination_list')
    def _compute_fix_price_paket(self):
        fix_price_paket = 0.0
        for rec in self:
            if rec.tipe_pengiriman == 'normal':
                rec.fix_price_paket = rec.price_paket + rec.total_cost_examination_list
            if rec.tipe_pengiriman == 'sameday':
                fix_price_paket     = rec.price_paket + rec.total_cost_examination_list
                rec.fix_price_paket = fix_price_paket + ((fix_price_paket * 50) / 100)
    
    # Filter Perusahaan berdasarkan Data Pasien
    @api.depends('pasien_id')
    def _compute_perusahaan(self):
        for data in self:
            domain   = [('is_company', '=', True), '|', '&', ('is_perusahaan', '=', True), ('status_perusahaan', '=', 'approved'), '&', ('client', '=', True), ('client_state', '=', 'enabled')]
            if data.pasien_id:
                domain += [('id', '=', data.pasien_id.perusahaan_id.id)]
            data.perusahaan_ids = self.env['res.partner'].search(domain)
            
    # Filter PIC berdasarkan Perusahaan yang dipilih
    @api.depends('perusahaan_id')
    def _compute_partner(self):
        for data in self:
            domain_partner = []
            if data.perusahaan_id:
                domain_partner  += [('parent_id', '=', data.perusahaan_id.id)]
            data.partner_ids = self.env['res.partner'].search(domain_partner)
            
    @api.depends('perusahaan_id')
    def _compute_pasien(self):
        for data in self:
            domain_pasien  = [('is_pasien', '=', True)]
            if data.perusahaan_id:
                domain_pasien   += [('perusahaan_id', '=', data.perusahaan_id.id)]
            data.pasien_ids  = self.env['res.partner'].search(domain_pasien)
     
    # Filter Data Package MCU berdasarkan Jenis Perjanjian dan Perusahaan yang dipilih
    @api.depends('perusahaan_id', 'jenis_perjanjian')
    def _compute_package_mcu_ids(self):
        for data in self:         
            domain_packet_mcu       = [('state' , '=' , 'approved'), ('end_date' , '>' , fields.Date.today())]   
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
    
class ConfigFixedCostingLine(models.Model):
    _inherit        = 'config.fixed.costing.line'
    _description    = 'Config Fixed Costing Line'
    
    reservation_id  = fields.Many2one( 'master.reservation', 
                                        string   = 'Reservation ID',
                                        index    = True,
                                        ondelete = 'cascade')
    
