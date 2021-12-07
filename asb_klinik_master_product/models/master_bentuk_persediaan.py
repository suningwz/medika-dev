from odoo import _, api, fields, models

class MasterBentukPersediaan(models.Model):
    _name                   = 'master.bentuk.persediaan'
    _description            = 'Bentuk Persediaan'
    
    name                    = fields.Char(string = 'Bentuk Persediaan')