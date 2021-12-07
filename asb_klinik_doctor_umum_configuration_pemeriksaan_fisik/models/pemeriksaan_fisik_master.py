# -*- coding: utf-8 -*-

from odoo import api, fields, models, exceptions, _
from odoo.exceptions import UserError, ValidationError

class PemeriksaanFisikMaster(models.Model):
    _name           = 'pemeriksaan.fisik.master'
    _inherit        = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
    _description    = 'Pemeriksaan Fisik Master'

    tipe_pemeriksaan_fisik = fields.Selection(  [
                                                    ('kulit', 'Kulit'),
                                                    ('mata', 'Mata'),
                                                    ('tht', 'THT/ENT'),
                                                    ('mulut', 'Mulut'),
                                                    ('leher', 'Leher'),
                                                    ('dada', 'Dada'),
                                                    ('perut', 'Perut'),
                                                    ('extrimitas', 'Pemeriksaan Extrimitas'),
                                                    ('rectal', 'Pemeriksaan Rectal'),
                                                    ('muskuloskletal', 'Pemeriksaan Muskuloskletal'),
                                                    ('sensorik', 'Pemeriksaan Sensorik'),
                                                    ('motorik', 'Pemeriksaan Motorik'),
                                                    ('reflek', 'Pemeriksaan Reflek'),
                                                    ('lain', 'Pemeriksaan Lain-lain'),
                                                    ('limfatik', 'Pemeriksaan Limfatik'),
                                                ], string = 'Tipe Pemeriksaan Fisik', tracking = True)
    physical_examination_type = fields.Selection(   [
                                                        ('kulit', 'Skin'),
                                                        ('mata', 'Eye'),
                                                        ('tht', 'THT/ENT'),
                                                        ('mulut', 'Mouth'),
                                                        ('leher', 'Neck'),
                                                        ('dada', 'Chest'),
                                                        ('perut', 'Abdomen'),
                                                        ('extrimitas', 'Extrimities'),
                                                        ('rectal', 'Rectal Examination'),
                                                        ('muskuloskletal', 'Muskuloskletal Examination'),
                                                        ('sensorik', 'Sensoric Examination'),
                                                        ('motorik', 'Mototric Examination'),
                                                        ('reflek', 'Reflex Examination'),
                                                        ('lain', 'Other Examination'),
                                                        ('limfatik', 'Lymphe Examination'),
                                                    ], string = 'Physical Examination Type', tracking = True)
    name = fields.Char(string = 'Name', tracking = True)
    nama = fields.Char(string = 'Nama', tracking = True)
    
    @api.onchange('tipe_pemeriksaan_fisik')
    def _onchange_tipe_pemeriksaan_fisik(self):
        for rec in self:
            rec.physical_examination_type = rec.tipe_pemeriksaan_fisik

    def name_get(self):
        res = []
        for rec in self:
            res.append((rec.id, '%s (%s)' % (rec.nama, rec.name)))
        return res
