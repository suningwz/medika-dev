# -*- coding: utf-8 -*-

from odoo import api, fields, models, exceptions, _
from odoo.exceptions import UserError, ValidationError


class LifestyleMerokokWizard(models.TransientModel):
    _name           = 'lifestyle.merokok.wizard'
    _description    = 'Lifestyle Merokok Wizard'

    name            = fields.Char(string = 'Name', default = 'Merokok (Smoking)')
    status          = fields.Selection( [
                                            ('yes', 'Ya/Yes'),
                                            ('no', 'Tidak/No'),
                                            ('berhenti', 'Sudah Berhenti'),
                                        ], string = 'Status', tracking = True)
    batang          = fields.Float(string  = 'x̄ Batang/Hari', tracking = True)
    tahun_merokok   = fields.Float(string  = 'Lama Merokok (Tahun)', tracking = True)
    indeks_brinkman = fields.Float( compute = '_compute_indeks_brinkman', string = 'Indeks Brinkman', 
                                    tracking = True, store = True)
    klasifikasi     = fields.Selection( [
                                            ('ringan', 'Perokok Ringan'),
                                            ('sedang', 'Perokok Sedang'),
                                            ('berat', 'Perokok Berat'),
                                        ], string = 'Klasifikasi', tracking = True, compute = '_compute_klasifikasi', store = True)
    deskripsi       = fields.Text(string = 'Deskripsi', tracking = True)
    berhenti_merokok = fields.Float(string = 'Terakhir Merokok (Bulan)', tracking = True)
    lifestyle_id    = fields.Many2one('lifestyle.lifestyle', string = 'Lifestyle/Kebiasaan')

    @api.depends('batang', 'tahun_merokok')
    def _compute_indeks_brinkman(self):
        for rec in self:
            rec.indeks_brinkman = rec.batang * rec.tahun_merokok

    # https: // www.klikdokter.com/tanya-dokter/read/2780812/resiko-kanker-perokok-mneurut-perhitungan-index-brinkman
    # https: // id.wikibooks.org/wiki/Catatan_Dokter_Muda/Indeks_Brinkman
    @api.depends('indeks_brinkman')
    def _compute_klasifikasi(self):
        for rec in self:
            if rec.indeks_brinkman < 50:
                rec.klasifikasi = 'ringan'
                if rec.status == 'no':
                    rec.deskripsi = "Tidak Merokok"
                elif rec.status == 'yes':
                    rec.deskripsi = dict(rec._fields['klasifikasi'].selection).get(rec.klasifikasi)
            elif rec.indeks_brinkman >= 50 and rec.indeks_brinkman < 100:
                rec.klasifikasi = 'sedang'
                rec.deskripsi = dict(rec._fields['klasifikasi'].selection).get(rec.klasifikasi)
            else:
                rec.klasifikasi = 'berat'
                rec.deskripsi = dict(rec._fields['klasifikasi'].selection).get(rec.klasifikasi)

    @api.onchange('status')
    def _onchange_status(self):
        for rec in self:
            if rec.status == 'no':
                rec.batang = False
                rec.tahun_merokok = False
                rec.berhenti_merokok = False
                rec.deskripsi = 'Tidak Merokok'
            elif rec.status == 'berhenti':
                rec.batang = False
                rec.tahun_merokok = False
                rec.deskripsi = 'Sudah berhenti sejak %s bulan lalu' % rec.berhenti_merokok
            elif rec.status == 'yes':
                rec.berhenti_merokok = False
                rec.deskripsi = dict(rec._fields['klasifikasi'].selection).get(rec.klasifikasi)

    @api.onchange('berhenti_merokok')
    def _onchange_berhenti_merokok(self):
        for rec in self:
            if rec.status == 'berhenti':
                rec.deskripsi = 'Sudah berhenti sejak %s bulan lalu' % rec.berhenti_merokok

    def save(self):
        for rec in self.lifestyle_id:
            rec.status = self.status
            if rec.status == 'yes':
                rec.yes = True
                rec.no = False
            if rec.status == 'no':
                rec.yes = False
                rec.no = True
            if rec.status == 'berhenti':
                rec.yes = False
                rec.no = False
            rec.deskripsi = self.deskripsi
            rec.berhenti_merokok = self.berhenti_merokok
            rec.batang = self.batang
            rec.tahun_merokok = self.tahun_merokok
