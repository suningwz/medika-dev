# -*- coding: utf-8 -*-

from odoo import api, fields, models, exceptions, _
from odoo.exceptions import UserError, ValidationError


class MedicalHistory(models.Model):
    _name               = 'medical.history'
    _description        = 'Medical History'
    _rec_name           = 'anamnesa_master_id'

    anamnesa_master_id  = fields.Many2one( 'anamnesa.master', ondelete = 'cascade', 
                                           string = 'Nama (Name)', tracking = True)
    status              = fields.Selection( [
                                                ('yes', 'Ya/Yes'),
                                                ('no', 'Tidak/No'),
                                            ], string = 'Status', tracking = True, default = 'no')
    yes                 = fields.Boolean(string = 'Ya/Yes', default = False, tracking = True)
    no                  = fields.Boolean(string = 'Tidak/No', default = True, tracking = True)
    deskripsi           = fields.Text(string = 'Deskripsi', tracking = True)
    registration_id     = fields.Many2one('master.registration', string = 'Pasien', tracking = True)

    @api.onchange('yes')
    def _onchange_yes(self):
        for rec in self:
            if rec.yes == True:
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

            elif rec.no == False and rec.yes == False:
                rec.no = True
                rec.yes = False
                rec.status = 'no'

class MasterRegistration(models.Model):
    _inherit            = 'master.registration'
    _description        = 'Doctor Umum Antrian Pasien'

    medical_history_line = fields.One2many( 'medical.history', 'registration_id',
                                            string = 'medical History', tracking = True)

    @api.model
    def default_get(self, fields):
        res = super(MasterRegistration, self).default_get(fields)
        medical_history_line = []
        medical_history_rec = self.env['anamnesa.master'].search([('anamnesa_type', '=', 'medical_history')])
        for rec in medical_history_rec:
            line = (0, 0, {
                'anamnesa_master_id': rec.id
            })
            medical_history_line.append(line)
        res.update({
            'medical_history_line': medical_history_line
        })
        return res

class AnamnesaMaster(models.Model):
    _inherit        = 'anamnesa.master'
    _description    = 'Anamnesa Master'

    @api.model
    def create(self, vals):
        x = []
        res = super(AnamnesaMaster, self).create(vals)
        vals = {
            'anamnesa_master_id': res.id,
        }
        x.append((0, 0, vals))
        registration_rec = self.env['master.registration'].search([])
        for rec in registration_rec:
            if res.anamnesa_type == 'medical_history':
                rec.write({'medical_history_line': x})
        return res
