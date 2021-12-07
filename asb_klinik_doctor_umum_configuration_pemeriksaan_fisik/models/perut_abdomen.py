# -*- coding: utf-8 -*-

from odoo import api, fields, models, exceptions, _
from odoo.exceptions import UserError, ValidationError

class MasterRegistration(models.Model):
    _inherit    = 'master.registration'

    bentuk      = fields.Selection( [
                                        ('cekung',          'Cekung (Concave)           '),
                                        ('datar',           'Datar (Flat)               '),
                                        ('cembung',         'Cembung (GLobular)         '),
                                    ], tracking = True, string = 'Bentuk (Form)', default = 'datar')
    palpasi     = fields.Selection( [
                                        ('supel',           'Supel (Suppel)             '),
                                        ('tidak',           'Tidak (No)                 '),
                                    ], tracking = True, string = 'Palpasi (Palpation)', default = 'supel')
    hati        = fields.Selection( [
                                        ('tidak_teraba',    'Tidak Teraba (Not Palpable)'),
                                        ('teraba',          'Teraba (Palpable)          '),
                                    ], tracking = True, string = 'Hati (Liver)', default = 'tidak_teraba')
    limpa       = fields.Selection( [
                                        ('tidak_teraba',    'Tidak Teraba (Not Palpable)'),
                                        ('teraba',          'Teraba (Palpable)          '),
                                    ], tracking = True, string = 'Limpa (Spleen)', default = 'tidak_teraba')
    ginjal      = fields.Selection( [
                                        ('ballotment',      'Ballotment                 '),
                                        ('no_ballotment',   'No Ballotment              '),
                                    ], tracking = True, string = 'Ginjal (Kidney)', default = 'no_ballotment')
    nyeri_ketok = fields.Selection( [
                                        ('tidak',           'Tidak (No)                 '),
                                        ('ya',              'Ya (Yes)                   '),
                                    ], tracking = True, string = 'Nyeri Ketok (CVA)', default = 'tidak')
    des_nyeri_ketok = fields.Char(string = 'Deskripsi Nyeri Ketok', tracking = True)
    hernia_inguinal = fields.Selection( [
                                            ('tidak',           'Tidak (No)                 '),
                                            ('ya',              'Ya (Yes)                   '),
                                        ], tracking = True, string = 'Hernia Inguinal', default = 'tidak')
    des_hernia_inguinal = fields.Char(string = 'Deskripsi Hernia Inguinal', tracking = True)