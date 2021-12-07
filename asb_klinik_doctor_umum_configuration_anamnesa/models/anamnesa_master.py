# -*- coding: utf-8 -*-

from odoo import api, fields, models, exceptions, _
from odoo.exceptions import UserError, ValidationError


class AnamnesaMaster(models.Model):
    _name           = 'anamnesa.master'
    _inherit        = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
    _description    = 'Anamnesa Master'

    tipe_anamnesa   = fields.Selection( [
                                            ('riwayat_penyakit_terdahulu', 'Riwayat Penyakit Terdahulu'),
                                            ('khusus_wanita', 'Khusus Wanita'),
                                            ('kebiasaan', 'Kebiasaan'),
                                            ('riwayat_penyakit_keluarga', 'Riwayat Penyakit Keluarga'),
                                            ('paparan_fisik', 'Riwayat Paparan Pekerjaan Fisik'),
                                            ('paparan_kimia', 'Riwayat Paparan Pekerjaan Kimia'),
                                            ('paparan_biologi', 'Riwayat Paparan Pekerjaan Biologi'),
                                            ('paparan_ergonomi', 'Riwayat Paparan Pekerjaan Ergonomi'),
                                            ('paparan_psikologi', 'Riwayat Paparan Pekerjaan Psikologi'),
                                            ('paparan_lain', 'Riwayat Paparan Pekerjaan Lain-lain'),
                                        ], string = 'Tipe Anamnesa', tracking = True)
    anamnesa_type   = fields.Selection( [
                                            ('medical_history', 'Medical History'),
                                            ('special_for_woman', 'Special for Woman'),
                                            ('lifestyle', 'Lifestyle'),
                                            ('family_history', 'Family History'),
                                            ('exposure_physical', 'Work Exposure Physical'),
                                            ('exposure_chemical', 'Work Exposure Chemical'),
                                            ('exposure_biology', 'Work Exposure Biology'),
                                            ('exposure_ergonomics', 'Work Exposure Ergonimics'),
                                            ('exposure_psyichology', 'Work Exposure Psyichology'),
                                            ('exposure_other', 'Work Exposure Other'),
                                        ], string = 'Anamnesa Type', tracking = True)

    name        = fields.Char(string = 'Name', tracking = True)
    nama        = fields.Char(string = 'Nama', tracking = True)

    @api.onchange('tipe_anamnesa')
    def _onchange_tipe_anamnesa(self):
        for rec in self:
            if rec.tipe_anamnesa == 'riwayat_penyakit_terdahulu':
                rec.anamnesa_type = 'medical_history'
            elif rec.tipe_anamnesa == 'khusus_wanita':
                rec.anamnesa_type = 'special_for_woman'
            elif rec.tipe_anamnesa == 'kebiasaan':
                rec.anamnesa_type = 'lifestyle'
            elif rec.tipe_anamnesa == 'riwayat_penyakit_keluarga':
                rec.anamnesa_type = 'family_history'
            elif rec.tipe_anamnesa == 'paparan_fisik':
                rec.anamnesa_type = 'exposure_physical'
            elif rec.tipe_anamnesa == 'paparan_kimia':
                rec.anamnesa_type = 'exposure_chemical'
            elif rec.tipe_anamnesa == 'paparan_biologi':
                rec.anamnesa_type = 'exposure_biology'
            elif rec.tipe_anamnesa == 'paparan_ergonomi':
                rec.anamnesa_type = 'exposure_ergonomics'
            elif rec.tipe_anamnesa == 'paparan_psikologi':
                rec.anamnesa_type = 'exposure_psyichology'
            elif rec.tipe_anamnesa == 'paparan_lain':
                rec.anamnesa_type = 'exposure_other'

    def name_get(self):
        res = []
        for rec in self:
            res.append((rec.id, '%s (%s)' % (rec.nama, rec.name)))
        return res
