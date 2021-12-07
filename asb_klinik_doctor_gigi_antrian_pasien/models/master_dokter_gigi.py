from odoo import api, fields, models, exceptions, _
from odoo.exceptions import UserError, ValidationError
import re

class MasterRegistration(models.Model):
    _inherit            = 'master.registration'
    _description        = 'Master Registration'
    
    status_antrian_dokter_gigi = fields.Selection([
                                                    ('waiting', 'Waiting'),
                                                    ('progress', 'On Progress')
                                                  ], string     = 'Status Antrian Dokter Gigi', 
                                                     readonly   = True, 
                                                     default    = 'waiting')
    
    is_done_poli_gigi           = fields.Boolean(   string   = 'Done Poli Gigi',
                                                    default  = False,
                                                    readonly = True)
    
    status_pemeriksaan_dokter_gigi   = fields.Char(string = 'Status Pemeriksaan Dokter', copy = False, default = 'Not Yet')
    
    plan_dokter_gigi            = fields.Text(string = 'Plan')
    
    nama_dokter_gigi            = fields.Many2one( 'res.users', 
                                                    string    = 'Nama Dokter',
                                                    store     = True, 
                                                    index     = True,
                                                    tracking  = True)
    
    gaki1   = fields.Char()
    gaki2   = fields.Char()
    gaki3   = fields.Char()
    gaki4   = fields.Char()
    gaki5   = fields.Char()
    gaki6   = fields.Char()
    gaki7   = fields.Char()
    gaki8   = fields.Char()
    
    gaka1   = fields.Char()
    gaka2   = fields.Char()
    gaka3   = fields.Char()
    gaka4   = fields.Char()
    gaka5   = fields.Char()
    gaka6   = fields.Char()
    gaka7   = fields.Char()
    gaka8   = fields.Char()
    
    gbki1   = fields.Char()
    gbki2   = fields.Char()
    gbki3   = fields.Char()
    gbki4   = fields.Char()
    gbki5   = fields.Char()
    gbki6   = fields.Char()
    gbki7   = fields.Char()
    gbki8   = fields.Char()
    
    gbka1   = fields.Char()
    gbka2   = fields.Char()
    gbka3   = fields.Char()
    gbka4   = fields.Char()
    gbka5   = fields.Char()
    gbka6   = fields.Char()
    gbka7   = fields.Char()
    gbka8   = fields.Char()
    
    edit_dokter_gigi_hide_css = fields.Html(sanitize = False, compute = '_compute_edit_dokter_gigi_hide_css')
    
    # Cek Poli Gigi
    get_is_poli_gigi    = fields.Boolean(compute = '_compute_get_is_poli_gigi', string = 'Get Poli Gigi', store = True)
    
    # Cek Poli Gigi
    @api.depends('examination_list_ids', 'poli_unit_ids', 'jenis_perjanjian')
    def _compute_get_is_poli_gigi(self):
        self.get_is_poli_gigi = False
        for rec in self:
            if rec.jenis_perjanjian == 'mcu' or rec.jenis_perjanjian == 'onsite':
                cek_examination = rec.examination_list_ids + rec.additional_examination_ids
                for poli in cek_examination:
                    if re.search('Gigi', str(poli.poli_unit_id.nama_poli_unit), re.IGNORECASE):
                        rec.get_is_poli_gigi = True
                
            if rec.jenis_perjanjian == 'mc':
                cek_poli_unit = rec.poli_unit_ids
                for poli in cek_poli_unit:
                    if re.search('Gigi', str(poli.nama_poli_unit), re.IGNORECASE):
                        rec.get_is_poli_gigi = True
    
    @api.depends('status_antrian_dokter_gigi')
    def _compute_edit_dokter_gigi_hide_css(self):
        for rec in self:
            if rec.status_antrian_dokter_gigi == 'waiting':
                rec.edit_dokter_gigi_hide_css = '<style>.o_form_button_edit {display: none !important;}</style>'
            else:
                rec.edit_dokter_gigi_hide_css = False
    
    def dokter_gigi_panggil(self):
        for rec in self:
            if rec.status_antrian == 'progress':
                raise ValidationError("Pasien sedang menjalani Pemeriksaan di {}".format(rec.on_progress))
            elif re.search('Progress', str(rec.status_makan), re.IGNORECASE):
                raise ValidationError("Pasien sedang {}".format(rec.on_progress))
            else:
                data_registrasi = self.env['master.registration'].search([]).filtered(lambda r: rec.id in r.ids)
                data_registrasi.write({'status_antrian': 'progress', 'on_progress' : 'Poli Gigi', 'status_antrian_dokter_gigi' : 'progress'})
                rec.nama_dokter_gigi = self.env.user.id
    
    def dokter_gigi_lewati(self):
        for rec in self:
            data_registrasi = self.env['master.registration'].search([]).filtered(lambda r: rec.id in r.ids)
            data_registrasi.write({'status_antrian': 'waiting', 'on_progress' : 'Unit Perawat', 'status_antrian_dokter_gigi' : 'waiting'})
            rec.nama_dokter_gigi = False
    
    def dokter_gigi_done(self):
        for rec in self:
            data_registrasi = self.env['master.registration'].search([]).filtered(lambda r: rec.id in r.ids)
            data_registrasi.write({'on_progress' : 'Unit Perawat', 'status_antrian': 'waiting', 'status_pemeriksaan_dokter_gigi': 'Done', 'is_done_poli_gigi': True, 'is_dokter': True, 'status_antrian_dokter_gigi' : 'waiting'})
            status_poli_umum = self.env['list.pemeriksaan.poli'].search([('poli_unit_id', '=', self.env.user.poli_unit_id.id), ('registration_id', '=', self.id)])
            status_poli_umum.status = 'Done'
            if rec.jenis_perjanjian == 'mc':
                pemeriksaan = [id for data in [rec.detail_pemeriksaan_mc_ids.product_id.ids, rec.permintaan_lab_ids.product_id.ids, rec.permintaan_radiologi_ids.product_id.ids] for id in data]
                data_registrasi.write({'examination_list_ids':[(6, 0, pemeriksaan)]})