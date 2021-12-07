# -*- coding: utf-8 -*-

from odoo import api, fields, models, exceptions, _
from odoo.exceptions import UserError, ValidationError


class MasterRegistration(models.Model):
    _inherit            = 'master.registration'
    _description        = 'Master Registration'

    total_biaya_mc      = fields.Float(compute = '_compute_total_biaya_mc', string = 'Total Biaya')

    @api.depends('total_pemeriksaan_mc', 'total_resep_obat', 'cost_permintaan_lab', 'cost_permintaan_radiologi')
    def _compute_total_biaya_mc(self):
        for rec in self:
            rec.total_biaya_mc = rec.total_pemeriksaan_mc + rec.total_resep_obat + rec.cost_permintaan_lab + rec.cost_permintaan_radiologi
