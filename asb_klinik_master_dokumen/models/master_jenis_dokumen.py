from odoo import _, api, fields, models

class MasterJenisDokumen(models.Model):
    _name           = 'master.jenis.dokumen'
    _description    = 'Master Jenis Dokumen'
    
    name            = fields.Char( string = 'Jenis Dokumen')