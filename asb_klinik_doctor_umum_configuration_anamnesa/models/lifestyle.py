# -*- coding: utf-8 -*-

from odoo import api, fields, models, exceptions, _
from odoo.exceptions import UserError, ValidationError


class LifestyleLifestyle(models.Model):
    _name           = 'lifestyle.lifestyle'
    _description    = 'Lifestyle Lifestyle'
    _rec_name       = 'anamnesa_master_id'

    anamnesa_master_id  = fields.Many2one('anamnesa.master', ondelete = 'cascade', string = 'Nama (Name)', tracking = True)
    status              = fields.Selection( [
                                                ('yes', 'Ya/Yes'),
                                                ('no', 'Tidak/No'),
                                                ('berhenti', 'Sudah Berhenti'),
                                                ('ringan', 'Ringan'),
                                                ('sedang', 'Sedang'),
                                                ('berat', 'Berat'),
                                            ], string = 'Status', tracking = True, default = 'no')
    yes                 = fields.Boolean(string = 'Ya/Yes', default = False, tracking = True)
    no                  = fields.Boolean(string = 'Tidak/No', default = True, tracking = True)
    deskripsi           = fields.Text(string = 'Deskripsi', tracking = True)
    registration_id     = fields.Many2one('master.registration', string = 'Pasien', tracking = True)
    form                = fields.Boolean(string = 'Form', tracking = True)

    # wizard
    berhenti_merokok    = fields.Float(string = 'Terakhir Merokok (Bulan)', tracking = True)
    batang              = fields.Float(string = 'x̄ Batang/Hari', tracking = True)
    tahun_merokok       = fields.Float(string = 'Lama Merokok (Tahun)', tracking = True)

    lifestyle_form      = fields.Selection( [
                                                ('merokok', 'Form Merokok (Smoking)'),
                                                ('olahraga', 'Form Olahraga (Exercise)'),
                                            ], string = 'Lifestyle Form', tracking = True)

    @api.onchange('yes')
    def _onchange_yes(self):
        for rec in self:
            if rec.yes == True:
                if rec.anamnesa_master_id.nama == 'Merokok' or rec.anamnesa_master_id.nama == 'merokok'\
                        or rec.anamnesa_master_id.nama == 'Olahraga' or rec.anamnesa_master_id.nama == 'olahraga':
                    return {
                        'warning': {'title': 'Warning!', 'message': 'Untuk menyunting record ini tekan tombol Setup!'},
                        'value': {
                            'status': 'no',
                            'yes': False,
                            'no': True,
                        }
                    }
                else:
                    rec.status = 'yes'
                    rec.no = False

            elif rec.yes == False and rec.no == False:
                rec.status = 'yes'
                rec.yes = True
                rec.no = False

    @api.onchange('no')
    def _onchange_no(self):
        for rec in self:
            if rec.no == True:
                rec.yes = False
                rec.status = 'no'
                rec.deskripsi = False

            elif rec.no == False and rec.yes == False:
                rec.no = True
                rec.yes = False
                rec.status = 'no'

    def setup(self):
        for rec in self:
            if rec.lifestyle_form == 'merokok':
                return {
                    'name': "Kebiasaan (Lifestyle)",
                    'type': 'ir.actions.act_window',
                    'res_model': 'lifestyle.merokok.wizard',
                    'view_mode': 'form',
                    'view_type': 'form',
                    'views': [(False, 'form')],
                    'context': {
                        'default_lifestyle_id': self.id,
                        'default_status': self.status,
                        'default_deskripsi': self.deskripsi,
                        'default_berhenti_merokok': self.berhenti_merokok,
                        'default_batang': self.batang,
                        'default_tahun_merokok': self.tahun_merokok
                    },
                    'target': 'new',
                }
            elif rec.lifestyle_form == 'olahraga':
                return {
                    'name': "Olahraga (Exercise)",
                    'type': 'ir.actions.act_window',
                    'res_model': 'lifestyle.olahraga.wizard',
                    'view_mode': 'form',
                    'view_type': 'form',
                    'views': [(False, 'form')],
                    'context': {
                        'default_lifestyle_id': self.id,
                        'default_status': self.status,
                        'default_deskripsi': self.deskripsi,
                    },
                    'target': 'new',
                }


class MasterRegistration(models.Model):
    _inherit            = 'master.registration'
    _description        = 'Doctor Umum Antrian Pasien'

    lifestyle_lifestyle_line    = fields.One2many('lifestyle.lifestyle', 'registration_id', 
                                                   string = 'lifestyle lifestyle', tracking = True)
    status_olahraga             = fields.Selection( [
                                                        ('yes', 'Ya/Yes'),
                                                        ('no', 'Tidak/No'),
                                                        ('berhenti', 'Sudah Berhenti'),
                                                        ('ringan', 'Ringan'),
                                                        ('sedang', 'Sedang'),
                                                        ('berat', 'Berat'),
                                                    ], string  = 'Status Olahraga', tracking = True, 
                                                       default = 'no', compute = '_compute_status_olahraga')
    status_merokok              = fields.Selection( [
                                                        ('yes', 'Ya/Yes'),
                                                        ('no', 'Tidak/No'),
                                                        ('berhenti', 'Sudah Berhenti'),
                                                        ('ringan', 'Ringan'),
                                                        ('sedang', 'Sedang'),
                                                        ('berat', 'Berat'),
                                                    ], string  = 'Status Merokok', tracking = True, 
                                                       default = 'no', compute = '_compute_status_merokok')
    poin_aktivitas_fisik        = fields.Integer(compute = '_compute_poin_aktivitas_fisik', string = 'Poin Aktivitas Fisik')
    poin_merokok                = fields.Integer(compute = '_compute_poin_merokok', string = 'Poin Merokok')

    @api.depends('lifestyle_lifestyle_line')
    def _compute_status_olahraga(self):
        self.status_olahraga = False
        for rec in self.lifestyle_lifestyle_line:
            if rec.anamnesa_master_id.nama == 'Olahraga':
                self.status_olahraga = rec.status

    @api.depends('lifestyle_lifestyle_line')
    def _compute_status_merokok(self):
        self.status_merokok = False
        for rec in self.lifestyle_lifestyle_line:
            if rec.anamnesa_master_id.nama == 'Merokok':
                self.status_merokok = rec.status

    @api.depends('status_olahraga')
    def _compute_poin_aktivitas_fisik(self):
        self.poin_aktivitas_fisik = 0
        for rec in self:
            if rec.status_olahraga == 'no':
                rec.poin_aktivitas_fisik = 2
            elif rec.status_olahraga == 'ringan':
                rec.poin_aktivitas_fisik = 1
            elif rec.status_olahraga == 'sedang':
                rec.poin_aktivitas_fisik = 0
            elif rec.status_olahraga == 'berat':
                rec.poin_aktivitas_fisik = -3

    @api.depends('status_merokok')
    def _compute_poin_merokok(self):
        self.poin_merokok = 0
        for rec in self:
            if rec.status_merokok == 'yes':
                rec.poin_merokok = 0
            elif rec.status_merokok == 'no':
                rec.poin_merokok = 3
            elif rec.status_merokok == 'berhenti':
                rec.poin_merokok = 4

    @api.model
    def default_get(self, fields):
        res = super(MasterRegistration, self).default_get(fields)
        lifestyle_lifestyle_line = []
        lifestyle_rec = self.env['anamnesa.master'].search([('anamnesa_type', '=', 'lifestyle')])
        for rec in lifestyle_rec:
            line = (0, 0, {
                'anamnesa_master_id': rec.id,
                'form': rec.form,
                'lifestyle_form': rec.lifestyle_form,
            })
            lifestyle_lifestyle_line.append(line)
        res.update({
            'lifestyle_lifestyle_line': lifestyle_lifestyle_line
        })
        return res

class AnamnesaMaster(models.Model):
    _inherit        = 'anamnesa.master'
    _description    = 'Anamnesa Master'

    form            = fields.Boolean(string = 'Form', tracking = True)
    lifestyle_form  = fields.Selection( [
                                            ('merokok', 'Form Merokok (Smoking)'),
                                            ('olahraga', 'Form Olahraga (Exercise)'),
                                        ], string = 'Lifestyle Form', tracking = True)

    @api.model
    def create(self, vals):
        x = []
        deskripsi = ''
        res = super(AnamnesaMaster, self).create(vals)
        vals = {
            'anamnesa_master_id': res.id,
            'form': res.form,
            'lifestyle_form': res.lifestyle_form,
        }
        x.append((0, 0, vals))
        registration_rec = self.env['master.registration'].search([])
        for rec in registration_rec:
            if res.anamnesa_type == 'lifestyle':
                rec.write({'lifestyle_lifestyle_line': x})
        return res
