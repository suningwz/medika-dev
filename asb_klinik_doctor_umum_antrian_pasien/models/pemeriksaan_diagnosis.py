# -*- coding: utf-8 -*-

from odoo import api, fields, models, exceptions, _
from odoo.exceptions import UserError, ValidationError


class PemeriksaanDiagnosis(models.Model):
    _name           = 'pemeriksaan.diagnosis'
    _description    = 'Pemeriksaan Diagnosis'
    _rec_name       = 'diagnosis_id'

    diagnosis_id    = fields.Many2one('diagnosis.diagnosis', string = 'ICD Diagnosis')
    tipe_diagnosa   = fields.Selection( [
                                            ('primer', 'Primer'),
                                            ('sekunder', 'Sekunder'),
                                        ], string = 'Tipe Diagnosa')
    jenis_kasus     = fields.Selection( [
                                            ('baru', 'Baru'),
                                            ('lama', 'Lama'),
                                        ], string = 'Jenis Kasus')
    registration_id = fields.Many2one('master.registration', string = 'Master Registration')

    @api.onchange('registration_id')
    def _onchange_registration_id(self):
        upkeep_block = []

        if self.registration_id:
            for i in self.registration_id.pemeriksaan_diagnosis_ids:
                if not i.diagnosis_id.id in upkeep_block:
                    upkeep_block.append(i.diagnosis_id.id)
        return {
            'domain': {
                'diagnosis_id': [('id', 'not in', upkeep_block)]
            }
        }


class MasterRegistration(models.Model):
    _inherit        = 'master.registration'
    _description    = 'Master Registration'

    pemeriksaan_diagnosis_ids = fields.One2many('pemeriksaan.diagnosis', 'registration_id', string = 'Pemeriksaan Diagnosis')
