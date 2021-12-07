# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from datetime import datetime, date

class ProviderFacility(models.Model):
    _name = 'provider.facility'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
    _description = 'Provider Facility'
    _rec_name = 'category_id'
    _order = 'category_id'

    partner_id = fields.Many2one('res.partner', string='Partner')
    category_id = fields.Many2one('facility.category', string='Facility Category', tracking=True, ondelete='restrict')
    facility_name = fields.Char(string='Facility Name', tracking=True)
    created_date = fields.Datetime(string='Created Date', default=datetime.now(), required=True, tracking=True)
    created_by = fields.Many2one('res.users', string='Created By', default=lambda self: self.env.user.id, required=True, tracking=True)

    def name_get(self):
        res = []
        for rec in self:
            res.append((rec.id, '%s - %s' % (rec.category_id.name, rec.facility_name)))
        return res

    @api.model
    def create(self, vals):
        x = []
        res = super(ProviderFacility, self).create(vals)
        vals = {'facility_id': res.id,}
        x.append((0, 0, vals))
        partner_rec = self.env['res.partner'].search([('provider','=',True)])
        for rec in partner_rec:
            rec.write({'provider_facility_line_ids': x})
        return res


class ProviderFacilityLine(models.Model):
    _name = 'provider.facility.line'
    _description = 'Provider Facility Line'
    _order = 'facility_id'

    partner_id = fields.Many2one('res.partner', string='Partner', ondelete='cascade')
    facility_id = fields.Many2one('provider.facility', string='Facility', ondelete='cascade')
    is_yes = fields.Boolean('Yes', )
    is_no = fields.Boolean('No', default=True)
    category_id = fields.Many2one(related='facility_id.category_id')
    facility_name = fields.Char(related='facility_id.facility_name')
    
    @api.onchange('is_yes')
    def onchange_attendance(self):
        if self.is_yes:
            self.is_yes = True
            self.is_no = False
        if self.is_yes == False and self.is_yes == False:
            self.is_no = True

    @api.onchange('is_no')
    def onchange_absent(self):
        if self.is_no:
            self.is_no = True
            self.is_yes = False
        if self.is_yes == False and self.is_yes == False:
            self.is_no = True