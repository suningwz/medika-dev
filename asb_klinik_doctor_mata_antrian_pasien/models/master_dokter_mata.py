from odoo import api, fields, models, exceptions, _
from odoo.exceptions import UserError, ValidationError
import re

class MasterRegistration(models.Model):
    _inherit            = 'master.registration'
    _description        = 'Master Registration'
    
    status_antrian_dokter_mata = fields.Selection([
                                                    ('waiting', 'Waiting'),
                                                    ('progress', 'On Progress')
                                                  ], string     = 'Status Antrian Dokter Mata', 
                                                     readonly   = True, 
                                                     default    = 'waiting')
    
    is_done_poli_mata           = fields.Boolean(   string   = 'Done Poli Mata',
                                                    default  = False,
                                                    readonly = True)
    
    status_pemeriksaan_dokter_mata   = fields.Char(string = 'Status Pemeriksaan Dokter', copy = False, default = 'Not Yet')
    
    edit_dokter_mata_hide_css = fields.Html(sanitize = False, compute = '_compute_edit_dokter_mata_hide_css')
    
    get_is_poli_mata    = fields.Boolean(compute = '_compute_get_is_poli_mata', string = 'Get Poli Mata', store = True)
    
    
    nama_dokter_mata            = fields.Many2one( 'res.users', 
                                                    string    = 'Nama Dokter',
                                                    store     = True, 
                                                    index     = True,
                                                    tracking  = True)
    # Baca
    kacamata_sebelumnya_baca    = fields.Char(string = 'Kacamata Sebelumnya')
    depth_perception            = fields.Selection( [
                                                        ('normal', 'Normal'),
                                                        ('abnormal', 'Abnormal / Tidak Normal')
                                                    ], string = 'Depth Perception')
    
    # Mata Kanan
    kacamata_sebelumnya_kanan   = fields.Char(string = 'Kacamata Sebelumnya')
    tanpa_kacamata_jauh_kanan   = fields.Char(string = 'Tanpa Kacamata Jauh')
    tanpa_kacamata_dekat_kanan  = fields.Char(string = 'Tanpa Kacamata Dekat')
    koreksi_jauh_kanan          = fields.Char(string = 'Koreksi Jauh')
    koreksi_dekat_kanan         = fields.Char(string = 'Koreksi Dekat')
    tonometri_kanan             = fields.Float(string = 'Tonometri', digits=(3, 2), default = 0.0)
    lensa_kanan                 = fields.Char(string = 'Lensa')
    funduscopy_kanan            = fields.Char(string = 'Funduscopy')
    
    # Mata Kiri
    kacamata_sebelumnya_kiri   = fields.Char(string = 'Kacamata Sebelumnya')
    tanpa_kacamata_jauh_kiri   = fields.Char(string = 'Tanpa Kacamata Jauh')
    tanpa_kacamata_dekat_kiri  = fields.Char(string = 'Tanpa Kacamata Dekat')
    koreksi_jauh_kiri          = fields.Char(string = 'Koreksi Jauh')
    koreksi_dekat_kiri         = fields.Char(string = 'Koreksi Dekat')
    tonometri_kiri             = fields.Float(string = 'Tonometri', digits = (3, 2), default = 0.0)
    lensa_kiri                 = fields.Char(string = 'Lensa')
    funduscopy_kiri            = fields.Char(string = 'Funduscopy')
    
    # Umum
    tes_buta_warna      = fields.Selection( [
                                                ('normal', 'Normal'),
                                                ('partian', 'Partial Colour Blindness'),
                                                ('total', 'Total Colour Blindness')
                                            ], string = 'Tes Buta Warna')
    
    lapang_pandang      = fields.Selection( [
                                                ('normal', 'Normal'),
                                                ('abnormal', 'Abnormal / Tidak Normal')
                                            ], string = 'Lapang Pandang')
    
    temuan_medis        = fields.Text(string = 'Temuan Medis')
    
    kesimpulan          = fields.Selection( [
                                                ('normal', 'Normal'),
                                                ('abnormal', 'Abnormal / Tidak Normal')
                                            ], string = 'Kesimpulan')
    
    status_tonometri    = fields.Char(compute = '_compute_status_tonometri', string = 'Status Tonometri')
    
    @api.depends('tonometri_kanan', 'tonometri_kiri')
    def _compute_status_tonometri(self):
        for rec in self:
            rec.status_tonometri = "Normal" if (10 <= rec.tonometri_kanan <= 20) and (10 <= rec.tonometri_kiri <= 20) else "Tidak Diketahui" if rec.tonometri_kanan == 0 and rec.tonometri_kiri == 0 else "Abnormal"
    
    # Cek Poli Mata
    @api.depends('examination_list_ids', 'poli_unit_ids', 'jenis_perjanjian')
    def _compute_get_is_poli_mata(self):
        self.get_is_poli_mata = False
        for rec in self:
            if rec.jenis_perjanjian == 'mcu' or rec.jenis_perjanjian == 'onsite':
                cek_examination = rec.examination_list_ids + rec.additional_examination_ids
                for poli in cek_examination:
                    if re.search('Mata', str(poli.poli_unit_id.nama_poli_unit), re.IGNORECASE):
                        rec.get_is_poli_mata = True
                
            if rec.jenis_perjanjian == 'mc':
                cek_poli_unit = rec.poli_unit_ids
                for poli in cek_poli_unit:
                    if re.search('Mata', str(poli.nama_poli_unit), re.IGNORECASE):
                        rec.get_is_poli_mata = True
    
    @api.depends('status_antrian_dokter_mata')
    def _compute_edit_dokter_mata_hide_css(self):
        for rec in self:
            if rec.status_antrian_dokter_mata == 'waiting':
                rec.edit_dokter_mata_hide_css = '<style>.o_form_button_edit {display: none !important;}</style>'
            else:
                rec.edit_dokter_mata_hide_css = False
    
    def dokter_mata_panggil(self):
        for rec in self:
            if rec.status_antrian == 'progress':
                raise ValidationError("Pasien sedang menjalani Pemeriksaan di {}".format(rec.on_progress))
            elif re.search('Progress', str(rec.status_makan), re.IGNORECASE):
                raise ValidationError("Pasien sedang {}".format(rec.on_progress))
            else:
                data_registrasi = self.env['master.registration'].search([]).filtered(lambda r: rec.id in r.ids)
                data_registrasi.write({'status_antrian': 'progress', 'on_progress' : 'Poli Mata', 'status_antrian_dokter_mata' : 'progress'})
                rec.nama_dokter_mata = self.env.user.id
    
    def dokter_mata_lewati(self):
        for rec in self:
            data_registrasi = self.env['master.registration'].search([]).filtered(lambda r: rec.id in r.ids)
            data_registrasi.write({'status_antrian': 'waiting', 'on_progress' : 'Unit Perawat', 'status_antrian_dokter_mata' : 'waiting'})
            rec.nama_dokter_mata = False
    
    def dokter_mata_done(self):
        for rec in self:
            data_registrasi = self.env['master.registration'].search([]).filtered(lambda r: rec.id in r.ids)
            data_registrasi.write({'on_progress' : 'Unit Perawat', 'status_antrian': 'waiting', 'status_pemeriksaan_dokter_mata': 'Done', 'is_done_poli_mata': True, 'is_dokter': True, 'status_antrian_dokter_mata' : 'waiting'})
            status_poli_umum = self.env['list.pemeriksaan.poli'].search([('poli_unit_id', '=', self.env.user.poli_unit_id.id), ('registration_id', '=', self.id)])
            status_poli_umum.status = 'Done'
            if rec.jenis_perjanjian == 'mc':
                pemeriksaan = [id for data in [rec.detail_pemeriksaan_mc_ids.product_id.ids, rec.permintaan_lab_ids.product_id.ids, rec.permintaan_radiologi_ids.product_id.ids] for id in data]
                data_registrasi.write({'examination_list_ids':[(6, 0, pemeriksaan)]})
