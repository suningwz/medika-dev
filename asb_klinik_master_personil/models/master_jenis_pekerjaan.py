from odoo import _, api, fields, models

class MasterJenisPekerjaan(models.Model):
    _name               = 'master.jenis.pekerjaan'
    _description        = 'Master Jenis Pekerjaan'
    
    name                = fields.Char(string = 'Jenis Pekerjaan')