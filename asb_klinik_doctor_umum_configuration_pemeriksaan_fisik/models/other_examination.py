# -*- coding: utf-8 -*-

from odoo import api, fields, models, exceptions, _
from odoo.exceptions import UserError, ValidationError

class MasterRegistration(models.Model):
    _inherit    = 'master.registration'

    fungsi_koordinasi       = fields.Selection( [
                                                    ('tidak_diperiksa', 'Tidak Diperiksa (Not Examined)'),
                                                    ('normal', 'Normal (Normal)'),
                                                    ('tidak_normal', 'Tidak Normal (Abnormal)'),
                                                ], tracking = True, string = 'Fungsi Koordinasi', default = 'normal')
    des_fungsi_koordinasi   = fields.Char(string = 'Deskripsi Fungsi Koordinasi', tracking = True)
    romberg_test            = fields.Selection( [
                                                    ('negatif', 'Negatif (Negative)'),
                                                    ('positif', 'Positif (Positive)'),
                                                ], tracking = True, string = 'Romberg Test')
    des_romberg_test        = fields.Char(string = 'Deskripsi Romberg Test', tracking = True)