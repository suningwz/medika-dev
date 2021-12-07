# -*- coding: utf-8 -*-

from odoo import api, fields, models, exceptions, _
from odoo.exceptions import UserError, ValidationError

class ExtrimitasExtrimities(models.Model):
    _name           = 'extrimitas.extrimities'
    _description    = 'Extrimitas Extrimities'
    _rec_name       = 'pemeriksaan_fisik_master_id'

    pemeriksaan_fisik_master_id = fields.Many2one( 'pemeriksaan.fisik.master', ondelete = 'cascade', 
                                                   string = 'Nama (Name)', tracking = True)
    status          = fields.Selection( [
                                            ('normal', 'Normal(Normal)'),
                                            ('tidak_normal', 'Tidak Nomal (Abnormal)'),
                                            ('tidak_diperiksa', 'Tidak Diperiksa (Not Examined)'),
                                        ], string = 'Status', tracking = True, default = 'normal')
    normal          = fields.Boolean(string = 'Normal (Normal)', default = True, tracking = True)
    tidak_normal    = fields.Boolean(string = 'Tidak Normal (Abnormal)', default = False, tracking = True)
    tidak_diperiksa = fields.Boolean(string = 'Tidak Diperiksa (Not Examined)', default = False, tracking = True)
    deskripsi       = fields.Text(string = 'Deskripsi', tracking = True)
    registration_id = fields.Many2one('master.registration', string = 'Pasien', tracking = True)

    @api.onchange('normal')
    def _onchange_normal(self):
        for rec in self:
            if rec.normal == True:
                rec.status = 'normal'
                rec.tidak_normal = False
                rec.tidak_diperiksa = False

            elif rec.tidak_normal == False and rec.tidak_diperiksa == False and rec.normal == False:
                rec.status = 'normal'
                rec.normal = True
                rec.tidak_normal = False
                rec.tidak_diperiksa = False

    @api.onchange('tidak_normal')
    def _onchange_tidak_normal(self):
        for rec in self:
            if rec.tidak_normal == True:
                rec.status = 'tidak_normal'
                rec.normal = False
                rec.tidak_diperiksa = False

            elif rec.tidak_normal == False and rec.tidak_diperiksa == False and rec.normal == False:
                rec.status = 'tidak_normal'
                rec.tidak_normal = True
                rec.normal = False
                rec.tidak_diperiksa = False

    @api.onchange('tidak_diperiksa')
    def _onchange_(self):
        for rec in self:
            if rec.tidak_diperiksa == True:
                rec.status = 'tidak_diperiksa'
                rec.normal = False
                rec.tidak_normal = False

            elif rec.tidak_normal == False and rec.tidak_diperiksa == False and rec.normal == False:
                rec.status = 'tidak_diperiksa'
                rec.tidak_diperiksa = True
                rec.tidak_normal = False
                rec.normal = False

class MasterRegistration(models.Model):
    _inherit        = 'master.registration'
    _description    = 'Doctor Umum Antrian Pasien'

    extrimitas_extrimities_line = fields.One2many( 'extrimitas.extrimities', 'registration_id', 
                                                   string = 'Extrimitas Extrimities', tracking = True)

    @api.model
    def default_get(self, fields):
        res = super(MasterRegistration, self).default_get(fields)
        extrimitas_extrimities_line = []
        extrimitas_extrimities_rec = self.env['pemeriksaan.fisik.master'].search([('tipe_pemeriksaan_fisik', '=', 'extrimitas')])
        for rec in extrimitas_extrimities_rec:
            line = (0, 0, {
                'pemeriksaan_fisik_master_id': rec.id
            })
            extrimitas_extrimities_line.append(line)
        res.update({
            'extrimitas_extrimities_line': extrimitas_extrimities_line
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
            if res.tipe_pemeriksaan_fisik == 'extrimitas':
                rec.write({'extrimitas_extrimities_line': x})
        return res
