# -*- coding: utf-8 -*-

from odoo import api, fields, models, exceptions, _
from odoo.exceptions import UserError, ValidationError


class FamilyHistory(models.Model):
    _name               = 'family.history'
    _description        = 'Family History'
    _rec_name           = 'anamnesa_master_id'

    anamnesa_master_id  = fields.Many2one('anamnesa.master', ondelete = 'cascade', string = 'Nama (Name)', tracking = True)
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

    family_history_line     = fields.One2many('family.history', 'registration_id', 
                                               string = 'Family History', tracking = True)
    status_diabetes_melitus = fields.Selection( [
                                                    ('yes', 'Ya/Yes'),
                                                    ('no', 'Tidak/No'),
                                                ], string  = 'Diabetes Melitus', 
                                                   compute = '_compute_status_diabetes_melitus', 
                                                   store   = True)
    poin_diabetes_melitus   = fields.Integer(compute = '_compute_poin_diabetes_melitus', string = 'Poin Diabetes Melitus')
    
    @api.model
    def default_get(self, fields):
        res = super(MasterRegistration, self).default_get(fields)
        family_history_line = []
        family_history_rec = self.env['anamnesa.master'].search([('anamnesa_type', '=', 'family_history')])
        for rec in family_history_rec:
            line = (0, 0, {
                'anamnesa_master_id': rec.id
            })
            family_history_line.append(line)
        res.update({
            'family_history_line': family_history_line
        })
        return res

    @api.depends('family_history_line')
    def _compute_status_diabetes_melitus(self):
        for rec in self.family_history_line:
            if rec.anamnesa_master_id.nama == 'Kencing Manis':
                self.status_diabetes_melitus = rec.status

    @api.depends('status_diabetes_melitus')
    def _compute_poin_diabetes_melitus(self):
        self.poin_diabetes_melitus = 0
        for rec in self:
            if rec.status_diabetes_melitus == 'yes':
                rec.poin_diabetes_melitus = 2
            else:
                rec.poin_diabetes_melitus = 0

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
            if res.anamnesa_type == 'family_history':
                rec.write({'family_history_line': x})
        return res
