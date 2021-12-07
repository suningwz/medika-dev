from odoo import _, api, fields, models, tools, SUPERUSER_ID
from odoo.exceptions import UserError, ValidationError
import re
from datetime import date, timedelta, datetime

class MasterRegistration(models.Model):
    _inherit            = 'master.registration'
    _description        = 'Master Registration'
    
    # Punya Fitur Antrian Pasien
    is_poli_unit        = fields.Boolean( string   = 'Pemeriksaan Fisik',
                                          default  = False)
    
    is_dokter           = fields.Boolean(   string   = 'Done Dokter',
                                            default  = False,
                                            readonly = True)
    
    is_progress_makan   = fields.Boolean(   string   = 'Progress Makan',
                                            default  = False,
                                            store    = True,
                                            readonly = True)
    
    is_done_makan       = fields.Boolean(   string   = 'Done Makan',
                                            default  = False,
                                            store    = True,
                                            readonly = True)
    
    status_makan        = fields.Char(  string    = 'Status Makan', 
                                        copy      = False,
                                        compute   = '_get_status_makan')
    
    # Pemeriksaan Fisik : Tanda Vital
    berat_badan         = fields.Float( string   = 'Berat Badan (kg)', 
                                        digits   = (3,2),
                                        readonly = True, 
                                        tracking = True, 
                                        states   = {'going': [('readonly', False)]})
    
    tinggi_badan        = fields.Float( string   = 'Tinggi Badan (cm)', 
                                        digits   = (3,2),
                                        readonly = True, 
                                        tracking = True, 
                                        states   = {'going': [('readonly', False)]})
    
    indeks_massa_tubuh  = fields.Float( string   = 'Indeks Massa Tubuh', 
                                        digits   = (3,2),
                                        store    = True, 
                                        compute  = '_compute_indeks_massa_tubuh',
                                        tracking = True)
    
    berat_ideal         = fields.Float( string   = 'Berat Ideal (kg)', 
                                        digits   = (3,2),
                                        store    = True, 
                                        compute  = '_compute_berat_ideal',
                                        tracking = True)
    
    kesimpulan_imt      = fields.Selection( [
                                                ('underweight', 'Underweight'),
                                                ('normal', 'Normal'),
                                                ('overweight', 'Overweight'),
                                                ('obesitas', 'Obesitas'),
                                            ], string   = 'Kesimpulan IMT',
                                               tracking = True, 
                                               compute  = '_compute_kesimpulan_imt',
                                               store    = True)
    
    tekanan_sistolik    = fields.Integer( string   = 'Tek. Sistolik (mmHG)',
                                          readonly = True, 
                                          tracking = True, 
                                          states   = {'going': [('readonly', False)]})
    
    tekanan_diastolik   = fields.Integer( string   = 'Tek. Diastolik (mmHG)',
                                          readonly = True, 
                                          tracking = True, 
                                          states   = {'going': [('readonly', False)]})
    
    klasifikasi         = fields.Selection( [
                                                ('rendah', 'Tekanan Darah Rendah'),
                                                ('normal', 'Normal'),
                                                ('pra', 'Pra - Hipertensi'),
                                                ('hipertensi', 'Hipertensi'),
                                            ], string   = 'Klasifikasi',
                                               compute  = '_compute_klasifikasi',
                                               store    = True,
                                               tracking = True)
    
    nadi                = fields.Integer( string   = 'Nadi (kali / menit)',
                                          readonly = True, 
                                          tracking = True, 
                                          states   = {'going': [('readonly', False)]})
    
    respiratory_rate    = fields.Integer( string   = 'Respiratory Rate (kali / menit)',
                                          readonly = True, 
                                          tracking = True, 
                                          states   = {'going': [('readonly', False)]})
    
    suhu_tubuh          = fields.Float( string   = 'Suhu Tubuh (°C)', 
                                        digits   = (3,2),
                                        readonly = True, 
                                        tracking = True, 
                                        states   = {'going': [('readonly', False)]})
    
    # Pemeriksaan Fisik : Tanda Fisik
    lingkar_leher       = fields.Float( string   = 'Lingkar Leher (cm)', digits=(3, 2),
                                        readonly = True, 
                                        tracking = True, 
                                        states   = {'going': [('readonly', False)]})
    
    lingkar_lengan      = fields.Float( string   = 'Lingkar Lengan (cm)', digits=(3, 2),
                                        readonly = True, 
                                        tracking = True, 
                                        states   = {'going': [('readonly', False)]})
    
    lingkar_dada        = fields.Float( string   = 'Lingkar Dada (cm)', digits=(3, 2),
                                        readonly = True, 
                                        tracking = True, 
                                        states   = {'going': [('readonly', False)]})
    
    lingkar_perut       = fields.Float( string   = 'Lingkar Perut (cm)', digits=(3, 2),
                                        readonly = True, 
                                        tracking = True, 
                                        states   = {'going': [('readonly', False)]})
    
    status              = fields.Char(  string    = 'Status Pemeriksaan', 
                                        copy      = False,
                                        compute   = '_get_status')
    
    edit_hide_css       = fields.Html(  string     = 'CSS', 
                                        sanitize   = False, 
                                        compute    = '_compute_edit_hide_css')
    
    pemeriksaan_perawat = fields.Char( compute  = '_compute_pemeriksaan_perawat', 
                                       string   = 'Status Pemeriksaan Perawat', 
                                       store    = True)
    
    nama_perawat        = fields.Many2one( 'res.users', 
                                            string    = 'Nama Perawat',
                                            store     = True, 
                                            index     = True,
                                            tracking  = True)
    
    status_antrian_perawat = fields.Selection(  [
                                                    ('waiting', 'Waiting'),
                                                    ('progress', 'On Progress')
                                                ],  string     = 'Status Antrian Laboratorium', 
                                                    readonly   = True, 
                                                    default    = 'waiting')
    
    def action_proses_makan(self):
        self.ensure_one()
        if self.status_antrian == 'progress':
                raise ValidationError("Pasien sedang menjalani Pemeriksaan di {}".format(self.on_progress))
        else:
            return self.write({
                'is_progress_makan' : True,
                'on_progress'       : 'Makan',
            })
        
    def action_done_makan(self):
        self.ensure_one()
        if self.is_blood_group_prandial:
            waktu_pemeriksaan_lab = datetime.now() + timedelta(hours=2)
            waktu_cek_lab = (datetime.now() + timedelta(hours=9)).strftime("%H:%M:%S")
            return self.write({
                'is_done_makan'         : True,
                'on_progress'           : 'Unit Perawat',
                'waktu_pemeriksaan_lab' : waktu_pemeriksaan_lab,
                'waktu_cek_lab'         : str(waktu_cek_lab)
            })
        else:
            return self.write({
                'is_done_makan'         : True,
                'on_progress'           : 'Unit Perawat',
            })
        
    @api.depends('is_progress_makan', 'is_done_makan')
    def _get_status_makan(self):
        for rec in self: rec.status_makan = "Done" if rec.is_done_makan else "On - Progress" if rec.is_progress_makan else "Not Yet"
    
    # Memunculkan Button Edit ketika Status Pasien pada In Progress
    @api.depends('status_antrian_perawat', 'is_done_perawat')
    def _compute_edit_hide_css(self):
        for rec in self:
            if rec.status_antrian_perawat == 'waiting' or rec.is_done_perawat:
                rec.edit_hide_css = '<style>.o_form_button_edit {display: none !important;}</style>'
            else:
                rec.edit_hide_css = False
    
    # Cek Status Pemeriksaan Pasien
    @api.depends('is_poli_unit', 'berat_badan', 'tinggi_badan', 'indeks_massa_tubuh', 'kesimpulan_imt', 'tekanan_sistolik', 'tekanan_diastolik', 'klasifikasi', 'nadi', 'respiratory_rate', 'suhu_tubuh', 'lingkar_leher', 'lingkar_lengan', 'lingkar_dada', 'lingkar_perut')
    def _get_status(self):
        data = []
        for rec in self:
            data        += [rec.berat_badan, rec.tinggi_badan, rec.indeks_massa_tubuh, rec.kesimpulan_imt, rec.tekanan_sistolik, rec.tekanan_diastolik, rec.klasifikasi, rec.nadi, rec.respiratory_rate, rec.suhu_tubuh, rec.lingkar_leher, rec.lingkar_lengan, rec.lingkar_dada, rec.lingkar_perut]
            rec.status  = "Done" if (rec.is_poli_unit) and (False not in data) else "Not Yet"
    
    @api.depends('is_done_perawat')
    def _compute_pemeriksaan_perawat(self):
        for rec in self: rec.pemeriksaan_perawat = "Done" if rec.is_done_perawat else "Not Yet"
    
    # Perhitungan untuk Klasifikasi Tekanan Darah
    @api.depends('tekanan_diastolik', 'tekanan_sistolik')
    def _compute_klasifikasi(self):
        for rec in self:
            if rec.tekanan_sistolik <= 90 or rec.tekanan_diastolik <= 60:
                rec.klasifikasi = 'rendah'
            elif 90 < rec.tekanan_sistolik <= 120 and 60 < rec.tekanan_diastolik <= 80:
                rec.klasifikasi = 'normal'
            elif rec.tekanan_sistolik <= 120 and rec.tekanan_diastolik > 80:
                rec.klasifikasi = 'pra'
            elif rec.tekanan_sistolik > 120 and rec.tekanan_diastolik <= 80:
                rec.klasifikasi = 'pra'
            elif 120 < rec.tekanan_sistolik <= 139 and 80 < rec.tekanan_diastolik <= 89:
                rec.klasifikasi = 'pra'
            elif rec.tekanan_sistolik > 140 and rec.tekanan_diastolik > 90:
                rec.klasifikasi = 'hipertensi'
    
    # Perhitungan untuk Indeks Massa Tubuh
    @api.depends('tinggi_badan', 'berat_badan')
    def _compute_indeks_massa_tubuh(self):
        for rec in self:
            tinggi_badan = 1.0 if rec.tinggi_badan == 0 else rec.tinggi_badan / 100
            rec.indeks_massa_tubuh = (rec.berat_badan / (tinggi_badan ** 2)) 
    
    # Perhitungan Berat Badan Ideal
    @api.depends('tinggi_badan', 'jenis_kelamin')
    def _compute_berat_ideal(self):
        for rec in self:
            if rec.jenis_kelamin == 'laki':
                rec.berat_ideal = 0 if rec.tinggi_badan == 0 else ( rec.tinggi_badan - 100 ) - ((( rec.tinggi_badan - 100) * 10) / 100)
            if rec.jenis_kelamin == 'perempuan':
                rec.berat_ideal = 0 if rec.tinggi_badan == 0 else ( rec.tinggi_badan - 100 ) - ((( rec.tinggi_badan - 100) * 15) / 100)
    
    # Mendapatkan Nilai IMT berdasarkan Indeks Massa Tubuh
    @api.depends('indeks_massa_tubuh', 'jenis_kelamin')
    def _compute_kesimpulan_imt(self):
        for rec in self:
            if rec.jenis_kelamin == 'laki':
                if rec.indeks_massa_tubuh < 18:
                    rec.kesimpulan_imt = 'underweight'
                elif 18 <= rec.indeks_massa_tubuh <= 25:
                    rec.kesimpulan_imt = 'normal'
                elif 25 < rec.indeks_massa_tubuh <= 27:
                    rec.kesimpulan_imt = 'overweight'
                elif rec.indeks_massa_tubuh > 27:
                    rec.kesimpulan_imt = 'obesitas'
            if rec.jenis_kelamin == 'perempuan':
                if rec.indeks_massa_tubuh < 17:
                    rec.kesimpulan_imt = 'underweight'
                elif 17 <= rec.indeks_massa_tubuh <= 23:
                    rec.kesimpulan_imt = 'normal'
                elif 23 < rec.indeks_massa_tubuh <= 27:
                    rec.kesimpulan_imt = 'overweight'
                elif rec.indeks_massa_tubuh > 27:
                    rec.kesimpulan_imt = 'obesitas'
    
    # Menghapus Data Pemeriksaan Fisik jika Pemeriksaan bernilai False
    @api.onchange('is_poli_unit')
    def _onchange_is_poli_unit(self):
        for rec in self:
            if not rec.is_poli_unit:
                rec.berat_badan = rec.tinggi_badan = rec.tekanan_sistolik = rec.tekanan_diastolik = rec.nadi = rec.respiratory_rate = rec.suhu_tubuh = False
                rec.lingkar_leher = rec.lingkar_lengan = rec.lingkar_dada = rec.lingkar_perut = False
    
    # Create List Status Pemeriksaan apabila Pasien dipanggil
    def action_panggil_pasien(self):
        for rec in self:
            if re.search('Progress', str(rec.status_makan), re.IGNORECASE):
                raise ValidationError("Pasien sedang {}".format(rec.on_progress))
            elif rec.status_antrian == 'progress':
                raise ValidationError("Pasien sedang menjalani Pemeriksaan di {}".format(rec.on_progress))
            else:
                self.filtered(lambda r: rec.id in r.ids).write({'nama_perawat': self.env.user, 'status_antrian' : 'progress', 'on_progress' : 'Unit Perawat', 'is_poli_unit' : True, 'state' : 'going', 'status_antrian_perawat' : 'progress'})
    
    # Action Done untuk Pasien setelah Pemeriksaan Poli Perawat
    def action_done_pasien(self):
        for rec in self:
            if rec.status == 'Done':
                self.filtered(lambda r: rec.id in r.ids).write({'status_antrian' : 'waiting', 'is_done_perawat' : True, 'status_antrian_perawat' : 'waiting'})
    
    # Button Action Unlock
    def action_unlock(self):
        for rec in self:
            if rec.status_antrian == 'progress':
                raise ValidationError("Pasien sedang menjalani Pemeriksaan di {}".format(rec.on_progress))
            elif rec.is_dokter:
                raise ValidationError("Data Pasien yang sudah melakukan Pemeriksaan di Dokter. Tidak dapat diubah")
            else:
                return self.filtered(lambda r: rec.id in r.ids).write(
                    {'status_antrian' : 'progress', 'is_done_perawat' : False, 'status_antrian_perawat' : 'waiting'})
    
    # Button Action Lewati
    def action_change_state(self):
        for rec in self:
            data_registrasi     = self.filtered(lambda r: rec.id in r.ids)
            data_registrasi.write(
                {'status_antrian'       : 'waiting',
                 'state'                : 'confirm', 
                 'on_progress'          : 'Admission',
                 'nama_perawat'         : False, 
                 'is_poli_unit'         : False,
                 'berat_badan'          : False,
                 'tinggi_badan'         : False,
                 'tekanan_sistolik'     : False,
                 'tekanan_diastolik'    : False,
                 'nadi'                 : False,
                 'respiratory_rate'     : False,
                 'suhu_tubuh'           : False,
                 'lingkar_leher'        : False,
                 'lingkar_lengan'       : False,
                 'lingkar_dada'         : False,
                 'lingkar_perut'        : False,
                 'status_antrian_perawat' : 'waiting',
                }
            )
        action = self.env.ref('asb_klinik_admission_poli_perawat.master_poli_perawat_action').read()[0]
        return action
         