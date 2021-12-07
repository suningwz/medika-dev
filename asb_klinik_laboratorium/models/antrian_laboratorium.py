# -*- coding: utf-8 -*-
from odoo import api, fields, models, exceptions, _
from odoo.exceptions import UserError, ValidationError
import re, datetime

class MasterRegistration(models.Model):
    _inherit        = 'master.registration'
    _description    = 'Master Registration'
    
    status_antrian_laboratorium = fields.Selection([
                                                    ('waiting', 'Waiting'),
                                                    ('progress', 'On Progress')
                                                  ], string     = 'Status Antrian Laboratorium', 
                                                     readonly   = True, 
                                                     default    = 'waiting')

    status_pemeriksaan_laboratorium = fields.Char(string = 'Status Pemeriksaan Laboratorium', copy = False, default = 'Not Yet')
    
    is_done_laboratorium = fields.Boolean(string    = 'Done Laboratorium',
                                          default   = False,
                                          readonly  = True)
    # hide edit button laboratorium
    edit_laboratorium_hide_css = fields.Html(sanitize=False, compute='_compute_edit_laboratorium_hide_css', tracking=True)

    # cek poli laboratorium
    get_is_laboratorium     = fields.Boolean(   compute = '_compute_get_is_laboratorium', 
                                                string  = 'Get Poli Laboratorium', 
                                                store   = True)
    
    nama_laboran            = fields.Many2one( 'res.users', 
                                                string    = 'Nama Laboran',
                                                store     = True, 
                                                index     = True,
                                                tracking  = True)

    @api.depends('examination_list_ids', 'permintaan_lab_ids')
    def _compute_get_is_laboratorium(self):
        self.get_is_laboratorium = False
        for rec in self:
            cek_examination = rec.examination_list_ids + rec.additional_examination_ids
            for poli in cek_examination:
                if re.search('labora', str(poli.poli_unit_id.nama_poli_unit), re.IGNORECASE):
                    rec.get_is_laboratorium = True
                    return
                
            cek_poli_unit = rec.poli_unit_ids
            cek_laboratorium_ids = self.env['permintaan.lab'].sudo().search([('registration_id', '=', self.id)], limit=1)
            for poli in cek_poli_unit:
                if re.search('labora', str(poli.nama_poli_unit), re.IGNORECASE):
                    if cek_laboratorium_ids:
                        rec.get_is_laboratorium = True
                        return

    @api.depends('status_antrian_laboratorium')
    def _compute_edit_laboratorium_hide_css(self):
        for rec in self:
            if rec.status_antrian_laboratorium == 'waiting':
                rec.edit_laboratorium_hide_css = '<style>.o_form_button_edit {display: none !important;}</style>'
            else:
                rec.edit_laboratorium_hide_css = False
                
    # Button Panggil
    def laboratorium_panggil(self):
        for rec in self:
            waktu_sekarang = datetime.datetime.now()
            if rec.status_antrian == 'progress':
                raise ValidationError("Pasien sedang menjalani Pemeriksaan di {}".format(rec.on_progress))
            elif re.search('Progress', str(rec.status_makan), re.IGNORECASE):
                raise ValidationError("Pasien sedang {}".format(rec.on_progress))
            elif re.search('Tahap', str(rec.status_pemeriksaan_laboratorium), re.IGNORECASE) and not rec.is_done_makan:
                raise ValidationError("Pasien sudah melalui Tahap 1 Pemeriksaan. Silahkan kembali setelah 2 Jam Makan")
            elif rec.is_done_makan and waktu_sekarang < rec.waktu_pemeriksaan_lab:
                raise ValidationError("Belum memasuki waktu Pemeriksaan Lab Tahap 2")
            else:
                data_registrasi = self.env['master.registration'].search([]).filtered(lambda r: rec.id in r.ids)
                data_registrasi.write({'state' : 'going', 'status_antrian': 'progress', 'on_progress': 'Laboratorium', 'status_antrian_laboratorium' : 'progress'})
                rec.nama_laboran = self.env.user.id

    # Button Notif
    def laboratorium_notif(self):
        pass

    # Button Lewati
    def laboratorium_lewati(self):
        for rec in self:
            data_registrasi = self.env['master.registration'].search([]).filtered(lambda r: rec.id in r.ids)
            data_registrasi.write({'state' : 'confirm', 'status_antrian': 'waiting', 'on_progress': 'Admission / Unit Perawat', 'status_antrian_laboratorium' : 'waiting'})
            rec.nama_laboran = False

    # Button Done
    def laboratorium_done(self):
        for rec in self:
            if rec.is_blood_group_prandial:
                data_registrasi = self.env['master.registration'].search([]).filtered(lambda r: rec.id in r.ids)
                data_registrasi.write({'on_progress' : 'Unit Perawat', 'status_antrian': 'waiting', 'is_done_laboratorium': False, 'status_pemeriksaan_laboratorium': 'Tahap 1', 'status_antrian_laboratorium' : 'waiting'})
                status_laboratorium = self.env['list.pemeriksaan.poli'].search([('poli_unit_id', '=', self.env.user.poli_unit_id.id), ('registration_id', '=', self.id)])
                status_laboratorium.status = 'Tahap 1'
            if not rec.is_blood_group_prandial:
                data_registrasi = self.env['master.registration'].search([]).filtered(lambda r: rec.id in r.ids)
                data_registrasi.write({'on_progress' : 'Unit Perawat', 'status_antrian': 'waiting', 'is_done_laboratorium': True, 'status_pemeriksaan_laboratorium': 'Done', 'status_antrian_laboratorium' : 'waiting'})
                status_laboratorium = self.env['list.pemeriksaan.poli'].search([('poli_unit_id', '=', self.env.user.poli_unit_id.id), ('registration_id', '=', self.id)])
                status_laboratorium.status = 'Done'
            if rec.is_done_makan and re.search('Tahap', str(rec.status_pemeriksaan_laboratorium), re.IGNORECASE):
                data_registrasi = self.env['master.registration'].search([]).filtered(lambda r: rec.id in r.ids)
                data_registrasi.write({'on_progress' : 'Unit Perawat', 'status_antrian': 'waiting', 'is_done_laboratorium': True, 'status_pemeriksaan_laboratorium': 'Done', 'status_antrian_laboratorium' : 'waiting'})
                status_laboratorium = self.env['list.pemeriksaan.poli'].search([('poli_unit_id', '=', self.env.user.poli_unit_id.id), ('registration_id', '=', self.id)])
                status_laboratorium.status = 'Done'