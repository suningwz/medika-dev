# -*- coding: utf-8 -*-

from odoo import api, fields, models, exceptions, _
from odoo.exceptions import UserError, ValidationError

class MuskuloskletalExamination(models.Model):
    _name           = 'muskuloskletal.examination'
    _description    = 'Muskuloskletal Examination'
    _rec_name       = 'pemeriksaan_fisik_master_id'

    pemeriksaan_fisik_master_id = fields.Many2one('pemeriksaan.fisik.master', ondelete = 'cascade', 
                                                  string = 'Nama (Name)', tracking = True)
    status          = fields.Selection( [
                                            ('negatif', 'Negatif (Negative)'),
                                            ('positif', 'Positif (Positive)'),
                                        ], tracking = True, string = 'Status', default = 'negatif')
    negatif         = fields.Boolean(string = 'Negatif (Negative)', default = True, tracking = True)
    positif         = fields.Boolean(string = 'Positif (Positive)', default = False, tracking = True)
    deskripsi       = fields.Text(string = 'Deskripsi', tracking = True)
    registration_id = fields.Many2one('master.registration', string = 'Pasien', tracking = True)

    @api.onchange('positif')
    def _onchange_positif(self):
        for rec in self:
            if rec.positif == True:
                rec.status = 'positif'
                rec.negatif = False

            elif rec.positif == False and rec.negatif == False:
                rec.status = 'positif'
                rec.positif = True
                rec.negatif = False

    @api.onchange('negatif')
    def _onchange_negatif(self):
        for rec in self:
            if rec.negatif == True:
                rec.positif = False
                rec.status = 'negatif'

            elif rec.negatif == False and rec.positif == False:
                rec.negatif = True
                rec.positif = False
                rec.status = 'negatif'

class MasterRegistration(models.Model):
    _inherit            = 'master.registration'
    _description        = 'Doctor Umum Antrian Pasien'

    muskuloskletal_examination_line = fields.One2many( 'muskuloskletal.examination', 'registration_id', 
                                                       string = 'Muskuloskletal Examination', tracking = True)

    @api.model
    def default_get(self, fields):
        res = super(MasterRegistration, self).default_get(fields)
        muskuloskletal_examination_line = []
        muskuloskletal_examination_rec = self.env['pemeriksaan.fisik.master'].search([('tipe_pemeriksaan_fisik', '=', 'muskuloskletal')])
        for rec in muskuloskletal_examination_rec:
            line = (0, 0, {
                'pemeriksaan_fisik_master_id': rec.id
            })
            muskuloskletal_examination_line.append(line)
        res.update({
            'muskuloskletal_examination_line': muskuloskletal_examination_line
        })
        return res

class PemeriksaanFisikMaster(models.Model):
    _inherit        = 'pemeriksaan.fisik.master'
    _description    = 'Pemeriksaan Fisik Master'

    @api.model
    def create(self, vals):
        x = []
        res = super(PemeriksaanFisikMaster, self).create(vals)
        vals = {
            'pemeriksaan_fisik_master_id': res.id,
        }
        x.append((0, 0, vals))
        registration_rec = self.env['master.registration'].search([])
        for rec in registration_rec:
            if res.tipe_pemeriksaan_fisik == 'muskuloskletal':
                rec.write({'muskuloskletal_examination_line': x})
        return res