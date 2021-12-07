# -*- coding: utf-8 -*-

from odoo import api, fields, models, exceptions, _
from odoo.exceptions import UserError, ValidationError


class LifestyleOlahragaWizard(models.TransientModel):
    _name           = 'lifestyle.olahraga.wizard'
    _description    = 'Lifestyle Olahraga Wizard'

    name            = fields.Char(string = 'Name', default = 'Olahraga (Exercise)')
    lifestyle_id    = fields.Many2one('lifestyle.lifestyle', string = 'Lifestyle/Kebiasaan')
    status          = fields.Selection( [
                                            ('no', 'Tidak/No'),
                                            ('ringan', 'Ringan'),
                                            ('sedang', 'Sedang'),
                                            ('berat', 'Berat'),
                                        ], string = 'Status', tracking = True)
    deskripsi       = fields.Text(string = 'Deskripsi')

    def save(self):
        for rec in self.lifestyle_id:
            rec.status = self.status
            if rec.status == 'no':
                rec.no = True
                rec.yes = False
            if rec.status == 'ringan':
                rec.no = False
                rec.yes = True
            if rec.status == 'sedang':
                rec.no = False
                rec.yes = True
            if rec.status == 'berat':
                rec.no = False
                rec.yes = True
            rec.deskripsi = self.deskripsi

    @api.onchange('status')
    def _onchange_status(self):
        for rec in self:
            if rec.status == 'no':
                rec.deskripsi = 'Tidak'
            elif rec.status == 'ringan':
                rec.deskripsi = 'Olahraga Ringan'
            elif rec.status == 'sedang':
                rec.deskripsi = 'Olahraga Sedang'
            elif rec.status == 'berat':
                rec.deskripsi = 'Olahraga Berat'
