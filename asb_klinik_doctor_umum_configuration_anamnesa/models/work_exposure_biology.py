# -*- coding: utf-8 -*-

from odoo import api, fields, models, exceptions, _
from odoo.exceptions import UserError, ValidationError


class WorkExposureBiology(models.Model):
    _name               = 'work.exposure.biology'
    _description        = 'Work Exposure Biology'
    _rec_name           = 'anamnesa_master_id'

    anamnesa_master_id  = fields.Many2one( 'anamnesa.master', ondelete = 'cascade', 
                                           string = 'Nama (Name)', tracking = True)
    status              = fields.Selection( [
                                                ('yes', 'Ya/Yes'),
                                                ('no', 'Tidak/No'),
                                                ('previous', 'Sebelum/Previous'),
                                            ], string = 'Status', tracking = True, default = 'no')
    yes                 = fields.Boolean(string = 'Ya/Yes', default = False, tracking = True)
    no                  = fields.Boolean(string = 'Tidak/No', default = True, tracking = True)
    previous            = fields.Boolean(string = 'Sebelum/Previous', default = False, tracking = True)
    deskripsi           = fields.Text(string = 'Deskripsi', tracking = True)
    registration_id     = fields.Many2one('master.registration', string = 'Pasien', tracking = True)

    @api.onchange('yes')
    def _onchange_yes(self):
        for rec in self:
            if rec.yes == True:
                rec.status = 'yes'
                rec.no = False
                rec.previous = False

            elif rec.no == False and rec.previous == False and rec.yes == False:
                rec.status = 'yes'
                rec.yes = True
                rec.no = False
                rec.previous = False

    @api.onchange('no')
    def _onchange_no(self):
        for rec in self:
            if rec.no == True:
                rec.status = 'no'
                rec.yes = False
                rec.previous = False

            elif rec.no == False and rec.previous == False and rec.yes == False:
                rec.status = 'no'
                rec.no = True
                rec.yes = False
                rec.previous = False

    @api.onchange('previous')
    def _onchange_(self):
        for rec in self:
            if rec.previous == True:
                rec.status = 'previous'
                rec.yes = False
                rec.no = False

            elif rec.no == False and rec.previous == False and rec.yes == False:
                rec.status = 'previous'
                rec.previous = True
                rec.no = False
                rec.yes = False

class MasterRegistration(models.Model):
    _inherit            = 'master.registration'
    _description        = 'Doctor Umum Antrian Pasien'

    work_exposure_biology_line = fields.One2many( 'work.exposure.biology', 'registration_id', 
                                                  string = 'Work Exposure Biology', tracking = True)

    @api.model
    def default_get(self, fields):
        res = super(MasterRegistration, self).default_get(fields)
        work_exposure_biology_line = []
        work_exposure_biology_rec = self.env['anamnesa.master'].search([('anamnesa_type', '=', 'exposure_biology')])
        for rec in work_exposure_biology_rec:
            line = (0, 0, {
                'anamnesa_master_id': rec.id
            })
            work_exposure_biology_line.append(line)
        res.update({
            'work_exposure_biology_line': work_exposure_biology_line
        })
        return res

class AnamnesaMaster(models.Model):
    _inherit            = 'anamnesa.master'
    _description        = 'Anamnesa Master'

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
            if res.anamnesa_type == 'exposure_biology':
                rec.write({'work_exposure_biology_line': x})
        return res
