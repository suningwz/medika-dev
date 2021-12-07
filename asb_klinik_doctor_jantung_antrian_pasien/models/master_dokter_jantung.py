from odoo import api, fields, models, exceptions, _
from odoo.exceptions import UserError, ValidationError
import re

class MasterRegistration(models.Model):
    _inherit            = 'master.registration'
    _description        = 'Master Registration'
    
    status_antrian_dokter_jantung = fields.Selection([
                                                    ('waiting', 'Waiting'),
                                                    ('progress', 'On Progress')
                                                  ], string     = 'Status Antrian Dokter Jantung', 
                                                     readonly   = True, 
                                                     default    = 'waiting')
    
    is_done_poli_jantung           = fields.Boolean(   string   = 'Done Poli Jantung',
                                                    default  = False,
                                                    readonly = True)
    
    status_pemeriksaan_dokter_jantung   = fields.Char(string = 'Status Pemeriksaan Dokter', copy = False, default = 'Not Yet')
    
    hasil_pemeriksaan_jantung_treadmill = fields.Text(string = 'Hasil Pemeriksaan')
    temuan_medis_jantung_treadmill      = fields.Text(string = 'Temuan Medis')
    saran_jantung_treadmill             = fields.Text(string = 'Saran')
    kesimpulan_treadmill                = fields.Selection( [
                                                                ('normal', 'Normal'),
                                                                ('abnormal', 'Abnormal / Tidak Normal')
                                                            ], string = 'Kesimpulan')
    hasil_pemeriksaan_jantung_ekg   = fields.Text(string = 'Hasil Pemeriksaan')
    temuan_medis_jantung_ekg        = fields.Text(string = 'Temuan Medis')
    saran_jantung_ekg               = fields.Text(string = 'Saran')
    kesimpulan_ekg                  = fields.Selection( [
                                                            ('normal', 'Normal'),
                                                            ('abnormal', 'Abnormal / Tidak Normal')
                                                        ], string = 'Kesimpulan')
    penyakit_jantung_bawaan     = fields.Selection( [
                                                        ('ya', 'Ya'),
                                                        ('tidak', 'Tidak'),
                                                    ], string = 'Riwayat Penyakit Jantung Bawaan?')
    penyakit_jantung_didapat    = fields.Selection( [
                                                        ('ya', 'Ya'),
                                                        ('tidak', 'Tidak'),
                                                    ], string = 'Riwayat Penyakit Jantung Didapat?')
    kateririsasi_jantung        = fields.Selection( [
                                                        ('ya', 'Ya'),
                                                        ('tidak', 'Tidak'),
                                                    ], string = 'Riwayat Kateririsasi Jantung?')
    operasi_jantung             = fields.Selection( [
                                                        ('ya', 'Ya'),
                                                        ('tidak', 'Tidak'),
                                                    ], string = 'Riwayat Operasi Jantung?')
    penyakit_rheumatic          = fields.Selection( [
                                                        ('ya', 'Ya'),
                                                        ('tidak', 'Tidak'),
                                                    ], string = 'Riwayat Penyakit Rheumatic (Osteoarthritis Genu)?')
    istirahat_cukup             = fields.Selection( [
                                                        ('ya', 'Ya'),
                                                        ('tidak', 'Tidak'),
                                                    ], string = 'Istirahat cukup sehari sebelum Treadmill?')
    
    edit_dokter_jantung_hide_css = fields.Html(sanitize = False, compute = '_compute_edit_dokter_jantung_hide_css')
    get_is_poli_jantung         = fields.Boolean(compute = '_compute_get_is_poli_jantung', string = 'Get Poli Jantung', store = True)
    
    @api.depends('examination_list_ids', 'poli_unit_ids', 'jenis_perjanjian')
    def _compute_get_is_poli_jantung(self):
        self.get_is_poli_jantung = False
        for rec in self:
            if rec.jenis_perjanjian == 'mcu' or rec.jenis_perjanjian == 'onsite':
                cek_examination = rec.examination_list_ids + rec.additional_examination_ids
                for poli in cek_examination:
                    if re.search('Jantung', str(poli.poli_unit_id.nama_poli_unit), re.IGNORECASE):
                        rec.get_is_poli_jantung = True
                
            if rec.jenis_perjanjian == 'mc':
                cek_poli_unit = rec.poli_unit_ids
                for poli in cek_poli_unit:
                    if re.search('Jantung', str(poli.nama_poli_unit), re.IGNORECASE):
                        rec.get_is_poli_jantung = True
    
    @api.depends('status_antrian_dokter_jantung')
    def _compute_edit_dokter_jantung_hide_css(self):
        for rec in self:
            if rec.status_antrian_dokter_jantung == 'waiting':
                rec.edit_dokter_jantung_hide_css = '<style>.o_form_button_edit {display: none !important;}</style>'
            else:
                rec.edit_dokter_jantung_hide_css = False
    
    def dokter_jantung_panggil(self):
        for rec in self:
            if rec.status_antrian == 'progress':
                raise ValidationError("Pasien sedang menjalani Pemeriksaan di {}".format(rec.on_progress))
            elif re.search('Progress', str(rec.status_makan), re.IGNORECASE):
                raise ValidationError("Pasien sedang {}".format(rec.on_progress))
            else:
                data_registrasi = self.env['master.registration'].search([]).filtered(lambda r: rec.id in r.ids)
                data_registrasi.write({'status_antrian': 'progress', 'on_progress' : 'Poli Jantung', 'status_antrian_dokter_jantung' : 'progress'})
                rec.users_dokter_id = self.env.user.id
    
    def dokter_jantung_lewati(self):
        for rec in self:
            data_registrasi = self.env['master.registration'].search([]).filtered(lambda r: rec.id in r.ids)
            data_registrasi.write({'status_antrian': 'waiting', 'on_progress' : 'Unit Perawat', 'status_antrian_dokter_jantung' : 'waiting'})
            rec.users_dokter_id = False
    
    def dokter_jantung_done(self):
        for rec in self:
            data_registrasi = self.env['master.registration'].search([]).filtered(lambda r: rec.id in r.ids)
            data_registrasi.write({'on_progress' : 'Unit Perawat', 'status_antrian': 'waiting', 'status_pemeriksaan_dokter_jantung': 'Done', 'is_done_poli_jantung': True, 'is_dokter': True, 'status_antrian_dokter_jantung' : 'waiting'})
            status_poli_umum = self.env['list.pemeriksaan.poli'].search([('poli_unit_id', '=', self.env.user.poli_unit_id.id), ('registration_id', '=', self.id)])
            status_poli_umum.status = 'Done'
            if rec.jenis_perjanjian == 'mc':
                pemeriksaan = [id for data in [rec.detail_pemeriksaan_mc_ids.product_id.ids, rec.permintaan_lab_ids.product_id.ids, rec.permintaan_radiologi_ids.product_id.ids] for id in data]
                data_registrasi.write({'examination_list_ids':[(6, 0, pemeriksaan)]})