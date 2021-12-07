from odoo import models, fields, api, _
from datetime import date
from odoo.exceptions import UserError, ValidationError


class TidInformation(models.Model):
    _name = 'tid.information'
    _description = 'Tid Information'
    _rec_name = 'location'

    partner_id = fields.Many2one('res.partner', string='Provider')
    location = fields.Char(string='Location')
    device_number = fields.Char(string='Device Number')
    description = fields.Text(string='Description')
