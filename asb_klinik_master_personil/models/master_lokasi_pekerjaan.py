from odoo import _, api, fields, models

class MasterLokasiPekerjaan(models.Model):
    _name               = 'master.lokasi.pekerjaan'
    _description        = 'Master Lokasi Pekerjaan'
    
    name                = fields.Char(string = 'Lokasi Pekerjaan')