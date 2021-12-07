from odoo import models, fields, api, _

class HelplineMasterPractitioner(models.Model):
    _name = 'helpline.master.practitioner'
    _description = 'Helpline Master Practitioner'
    
    name = fields.Char(string='Name')