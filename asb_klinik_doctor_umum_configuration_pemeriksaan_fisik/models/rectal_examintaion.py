# -*- coding: utf-8 -*-

from odoo import api, fields, models, exceptions, _
from odoo.exceptions import UserError, ValidationError


class MasterRegistration(models.Model):
    _inherit        = 'master.registration'

    hemorrhoid      = fields.Selection( [
                                            ('negatif', 'Negatif (Negative)'),
                                            ('positif', 'Positif (Positive)'),
                                        ], tracking = True, string = 'Hemorrhoid', default = 'negatif')
    des_hemorrhoid  = fields.Char(string = 'Deskripsi Hemorrhoid', tracking = True)
    anus            = fields.Selection( [
                                            ('tidak_diperiksa', 'Tidak Diperiksa (Not Examined)'),
                                            ('normal', 'Normal (Normal)'),
                                            ('tidak_normal', 'Tidak Normal (Abnormal)'),
                                        ], tracking = True, string = 'Anus (Rectum)', default = 'tidak_diperiksa')
    des_anus        = fields.Char(string = 'Deskripsi Anus (Rectum)', tracking = True)