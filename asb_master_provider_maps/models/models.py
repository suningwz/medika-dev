# -*- coding: utf-8 -*-
import re
from odoo import models, fields, api, _
from datetime import date
from odoo.exceptions import UserError, ValidationError

import qrcode
import base64

from io import BytesIO

from odoo.exceptions import UserError

class ResPartner(models.Model):
    _inherit = 'res.partner'

    map_link = fields.Char(string='Map Link', tracking=True)
    partner_latitude = fields.Float(string='Geo Latitude', digits=(16, 10))
    partner_longitude = fields.Float(string='Geo Longitude', digits=(16, 10))

    @api.onchange('map_link')
    def _onchange_map_link(self):
        if self.map_link:
            text = str(self.map_link)
            text = text.split('@')
            if len(text) <= 1:
                raise ValidationError(_("Invalid link submited!"))
            else:
                text = text.pop(1)
                text = text.split(',')
                self.partner_latitude = text.pop(0)
                self.partner_longitude = text.pop(0)
    
    def get_lat_long(self):
        search_name = str(self.name.replace(" ", "+"))
        url = 'https://www.google.com/maps/place/%s' %search_name
        return {
            'name'     : 'Go to Google Maps',
            'type'     : 'ir.actions.act_url',
            'target'   : 'new',
            'url'      : url
            }
    
    edit_geolocation_hide_css = fields.Html(string='Geolocation', sanitize=False, compute='_compute_edit_geolocation_hide_css')


    def _compute_edit_geolocation_hide_css(self):
        for rec in self:
            if not rec.provider:
                rec.edit_geolocation_hide_css = '<style>.o-map-button-marker-edit {display: none !important;}</style>'
            else:
                rec.edit_geolocation_hide_css = False
