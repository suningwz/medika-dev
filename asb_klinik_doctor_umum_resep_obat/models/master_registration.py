# -*- coding: utf-8 -*-

from odoo import api, fields, models, exceptions, _
from odoo.exceptions import UserError, ValidationError


class MasterRegistration(models.Model):
    _inherit            = 'master.registration'
    _description        = 'Master Registration'

    # Resep Obat
    resep_obat_line     = fields.One2many('resep.obat', 'registration_id', string = 'Resep Obat Line', tracking = True)
    total_resep_obat    = fields.Float(compute = '_compute_total_resep_obat', string = 'Total', tracking = True)

    @api.depends('resep_obat_line.total_detail_obat')
    def _compute_total_resep_obat(self):
        for rec in self:
            rec.total_resep_obat = sum(rec.resep_obat_line.mapped('total_detail_obat'))
