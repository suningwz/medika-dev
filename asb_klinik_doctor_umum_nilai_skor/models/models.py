# -*- coding: utf-8 -*-

from odoo import api, fields, models, exceptions, _
from odoo.exceptions import UserError, ValidationError

class MasterRegistration(models.Model):
    _inherit            = 'master.registration'
    _description        = 'Doctor Umum Antrian Pasien'

    nilai_skor          = fields.Integer(compute = '_compute_nilai_skor', string = 'Nilai Skor', store = True)
    
    @api.depends('poin_jk','poin_umur','poin_tekanan_darah','poin_imt','poin_merokok','poin_diabetes_melitus','poin_aktivitas_fisik')
    def _compute_nilai_skor(self):
        for rec in self:
            rec.nilai_skor = rec.poin_jk + rec.poin_umur + rec.poin_tekanan_darah + rec.poin_imt + rec.poin_merokok + rec.poin_diabetes_melitus + rec.poin_aktivitas_fisik