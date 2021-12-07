from odoo import models, fields, api, _
from odoo.exceptions import UserError

class SuffixId(models.Model):
    _name = 'suffix.id'
    _description = 'Suffix Id'
    
    name = fields.Char(string='Suffix ID', required=True, )
    