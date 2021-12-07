# -*- coding: utf-8 -*-
from odoo import api, fields, models, exceptions, _
from odoo.exceptions import UserError, ValidationError
import re

class MasterRegistration(models.Model):
    _inherit            = 'master.registration'
    _description        = 'Master Registration'
    
    status_antrian_dokter_umum = fields.Selection([
                                                    ('waiting', 'Waiting'),
                                                    ('progress', 'On Progress')
                                                  ], string     = 'Status Antrian Dokter Umum', 
                                                     readonly   = True, 
                                                     default    = 'waiting')
    
    is_done_poli_umum               = fields.Boolean(   string   = 'Done Poli Umum',
                                                        default  = False,
                                                        readonly = True)
    status_pemeriksaan_dokter_umum  = fields.Char(string = 'Status Pemeriksaan Dokter', copy = False, default = 'Not Yet')
    catatan                         = fields.Text(string = 'Catatan')
    edukasi                         = fields.Text(string = 'Edukasi')

    # Dokter
    users_dokter_id                 = fields.Many2one('res.users', string = 'Dokter')
    dokter_image                    = fields.Binary(related = 'dokter_id.image_1920')

    # Notebook MCU Anamnesa
    keluhan_riwayat_penyakit        = fields.Char(string = 'Keluhan Saat Ini & Riwayat Penyakit Sekarang (Present Complaint & History of Present Illness)')

    # Notebook MCU Pemeriksaan Fisik
    keadaan_umum    = fields.Selection( [
                                            ('baik', 'Baik (Good)'),
                                            ('sakit', 'Sakit (Sick)'),
                                        ], string = 'Keadaan Umum (General Appearance)')
    bentuk_badan    = fields.Selection( [
                                            ('athleticus', 'Athleticus'),
                                            ('picnicus', 'Picnicus'),
                                            ('astenicus', 'Astenicus'),
                                        ], string = 'Bentuk Badan (Body Shape)')

    # Notebook MCU JCS
    poin_jk             = fields.Integer(compute = '_compute_poin_jk', string = 'Poin Jenis Kelamin', store = True)
    poin_umur           = fields.Integer(compute = '_compute_poin_umur', string = 'Poin Umur', store = True)
    poin_tekanan_darah  = fields.Integer(compute = '_compute_poin_tekanan_darah', string = 'Poin Tekanan Darah', store = True)
    poin_imt            = fields.Integer(compute = '_compute_poin_imt', string = 'Poin IMT', store = True)
    
    # Notebook MC Pemeriksaan Fisik
    subjektif_anamnesa  = fields.Text(string = 'Subjektif Anamnesa')
    objektif            = fields.Text(string = 'Objektif')
    assessment          = fields.Text(string = 'Assessment')
    plan_id             = fields.Many2one('master.plan', string = 'Plan')

    # Hide Edit Button
    edit_dokter_umum_hide_css = fields.Html(sanitize = False, compute = '_compute_edit_dokter_umum_hide_css')
    
    # Cek Poli Umum
    get_is_poli_umum    = fields.Boolean(compute = '_compute_get_is_poli_umum', string = 'Get Poli Umum', store = True)
    
    # Cek Poli Umum
    @api.depends('examination_list_ids', 'poli_unit_ids', 'jenis_perjanjian')
    def _compute_get_is_poli_umum(self):
        self.get_is_poli_umum = False
        for rec in self:
            if rec.jenis_perjanjian == 'mcu' or rec.jenis_perjanjian == 'onsite':
                cek_examination = rec.examination_list_ids + rec.additional_examination_ids
                for poli in cek_examination:
                    if re.search('Umum', str(poli.poli_unit_id.nama_poli_unit), re.IGNORECASE):
                        rec.get_is_poli_umum = True
                
            if rec.jenis_perjanjian == 'mc':
                cek_poli_unit = rec.poli_unit_ids
                for poli in cek_poli_unit:
                    if re.search('Umum', str(poli.nama_poli_unit), re.IGNORECASE):
                        rec.get_is_poli_umum = True
    
    @api.depends('jenis_kelamin')
    def _compute_poin_jk(self):
        self.poin_jk = 0
        for rec in self:
            if rec.jenis_kelamin:
                rec.poin_jk = 1 if rec.jenis_kelamin == 'laki' else 0

    @api.depends('umur')
    def _compute_poin_umur(self):
        self.poin_umur = 0
        for rec in self:
            if rec.umur:
                umur = int(rec.umur)
                if umur <= 34:
                    rec.poin_umur = -4
                elif umur >= 35 and umur <= 39:
                    rec.poin_umur = -3
                elif umur >= 40 and umur <= 44:
                    rec.poin_umur = -2
                elif umur >= 45 and umur <= 49:
                    rec.poin_umur = -0
                elif umur >= 50 and umur <= 54:
                    rec.poin_umur = 1
                elif umur >= 55 and umur <= 59:
                    rec.poin_umur = 2
                elif umur >= 65:
                    rec.poin_umur = 3

    @api.depends('tekanan_sistolik', 'tekanan_diastolik')
    def _compute_poin_tekanan_darah(self):
        self.poin_tekanan_darah = 0
        for rec in self:
            if rec.tekanan_sistolik < 130 and rec.tekanan_diastolik < 85:
                rec.poin_tekanan_darah = 0
            elif (rec.tekanan_sistolik >= 130 and rec.tekanan_sistolik <= 139) and (rec.tekanan_diastolik >= 85 and rec.tekanan_diastolik <= 89):
                rec.poin_tekanan_darah = 1
            elif (rec.tekanan_sistolik >= 140 and rec.tekanan_sistolik <= 159) and (rec.tekanan_diastolik >= 90 and rec.tekanan_diastolik <= 99):
                rec.poin_tekanan_darah = 2
            elif (rec.tekanan_sistolik >= 160 and rec.tekanan_sistolik <= 179) and (rec.tekanan_diastolik >= 100 and rec.tekanan_diastolik <= 109):
                rec.poin_tekanan_darah = 3
            elif (rec.tekanan_sistolik >= 180) and (rec.tekanan_diastolik >= 110):
                rec.poin_tekanan_darah = 4

    @api.depends('indeks_massa_tubuh')
    def _compute_poin_imt(self):
        self.poin_imt = 0
        for rec in self:
            if rec.indeks_massa_tubuh >= 25.99:
                rec.poin_imt = 0
            elif rec.indeks_massa_tubuh >= 26 and rec.indeks_massa_tubuh <= 29.99:
                rec.poin_imt = 1
            elif rec.indeks_massa_tubuh >= 30:
                rec.poin_imt = 2

    @api.depends('status_antrian_dokter_umum')
    def _compute_edit_dokter_umum_hide_css(self):
        for rec in self:
            if rec.status_antrian_dokter_umum == 'waiting':
                rec.edit_dokter_umum_hide_css = '<style>.o_form_button_edit {display: none !important;}</style>'
            else:
                rec.edit_dokter_umum_hide_css = False

    # Button Panggil
    def dokter_umum_panggil(self):
        for rec in self:
            if rec.status_antrian == 'progress':
                raise ValidationError("Pasien sedang menjalani Pemeriksaan di {}".format(rec.on_progress))
            elif re.search('Progress', str(rec.status_makan), re.IGNORECASE):
                raise ValidationError("Pasien sedang {}".format(rec.on_progress))
            else:
                data_registrasi = self.env['master.registration'].search([]).filtered(lambda r: rec.id in r.ids)
                data_registrasi.write({'status_antrian': 'progress', 'on_progress' : 'Poli Umum', 'status_antrian_dokter_umum' : 'progress'})
                rec.users_dokter_id = self.env.user.id

    # Button Notif
    def dokter_umum_notif(self):
        pass

    # Button Lewati
    def dokter_umum_lewati(self):
        for rec in self:
            data_registrasi = self.env['master.registration'].search([]).filtered(lambda r: rec.id in r.ids)
            data_registrasi.write({'status_antrian': 'waiting', 'on_progress' : 'Unit Perawat', 'status_antrian_dokter_umum' : 'waiting'})
            rec.users_dokter_id = False

    # Button Done
    def dokter_umum_done(self):
        for rec in self:
            data_registrasi = self.env['master.registration'].search([]).filtered(lambda r: rec.id in r.ids)
            data_registrasi.write({'on_progress' : 'Unit Perawat', 'status_antrian': 'waiting', 'status_antrian_dokter_umum' : 'waiting', 'status_pemeriksaan_dokter_umum': 'Done', 'is_done_poli_umum': True, 'is_dokter': True})
            status_poli_umum = self.env['list.pemeriksaan.poli'].search([('poli_unit_id', '=', self.env.user.poli_unit_id.id), ('registration_id', '=', self.id)])
            status_poli_umum.status = 'Done'
            if rec.jenis_perjanjian == 'mc':
                pemeriksaan = [id for data in [rec.detail_pemeriksaan_mc_ids.product_id.ids, rec.permintaan_lab_ids.product_id.ids, rec.permintaan_radiologi_ids.product_id.ids] for id in data]
                data_registrasi.write({'examination_list_ids':[(6, 0, pemeriksaan)]})
