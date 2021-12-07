# -*- coding: utf-8 -*-

from odoo import models, fields, api


class BenefitMaster(models.Model):
    _name = 'benefit.master'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
    _description = 'Benefit Master'

    name = fields.Char(string='Category Name', store=True, tracking=True)
    item_code = fields.Char(string='Code', tracking=True)
    helpline = fields.Boolean(string='Create Case Monitoring')
    category = fields.Selection([
        ('ip', 'IP'),
        ('op', 'OP'),
        ('de', 'DE'),
        ('eg', 'EG'),
        ('ma', 'MA'),
        ('mcu', 'MCU'),
        ('ot', 'OT'),
    ], string='Category', tracking=True)
