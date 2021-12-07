# -*- coding: utf-8 -*-

from odoo import models, fields, api


class EdcMaster(models.Model):
    _name = 'edc.master'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
    _description = 'Edc Master'
    _rec_name = 'edc_code'

    benefit_master_id = fields.Many2one('benefit.master', string='Category', tracking=True, required=True, ondelete='cascade')
    edc_name = fields.Char(string='EDC Name', tracking=True, required=True, )
    edc_code = fields.Char(string='EDC Code', tracking=True, required=True, )
