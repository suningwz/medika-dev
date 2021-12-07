from odoo import models, fields, api


class ResCompany(models.Model):
    _inherit = 'res.company'
    _description = 'Res Company'

    gl_ttd = fields.Image(string='Signature', tracking=True, max_width=120, max_height=120)
    gl_ttd_name = fields.Char(string='Signee', tracking=True)
    gl_title = fields.Char(string='Title', tracking=True)
