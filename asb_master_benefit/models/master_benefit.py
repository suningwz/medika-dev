# -*- coding: utf-8 -*-

from odoo import api, fields, models, exceptions, _
from odoo.exceptions import UserError, ValidationError


class BenefitBenefit(models.Model):
    _name = 'benefit.benefit'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
    _description = 'Benefit Benefit'
    _sql_constraints = [
        ('item_code_uniq', 'UNIQUE (item_code)',  'You can not have two Benefit with the same code!')
    ]

    @api.constrains('name')
    def check_name(self):
        if not self.name.istitle():
            raise ValidationError(_("Name must title case"))

    master_id = fields.Many2one('benefit.master', string='Category', tracking=True, ondelete='cascade')
    partner_id = fields.Many2one('res.partner', string='Group', tracking=True)
    name = fields.Char(string='Benefit Name', tracking=True)
    item_code = fields.Char(string='Benefit Code', tracking=True, related='master_id.item_code')
    description = fields.Char(string='Description', tracking=True)
    edc_code_id = fields.Many2one('edc.master', string='EDC Code', tracking=True, ondelete='cascade')
    edc_name = fields.Char(string='EDC Name', tracking=True, related='edc_code_id.edc_name')
    alternate_code = fields.Char(string='Alternate Code', help='Item Category Alternate Code', tracking=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('enabled', 'Enabled'),
        ('disabled', 'Disabled'),
    ], string='Status', default='draft', tracking=True)

    @api.onchange('master_id')
    def _onchange_master_id(self):
        self.edc_code_id = False
        for rec in self:
            if rec.master_id:
                return {
                    'domain': {
                        'edc_code_id': [('benefit_master_id', '=', self.master_id.id)]
                    }
                }

    def set_enabled(self):
        for doc in self:
            doc.state = 'enabled'

    def set_disabled(self):
        for doc in self:
            doc.state = 'disabled'

    def set_draft(self):
        for doc in self:
            doc.state = 'draft'

    @api.onchange('name')
    def onchage_name(self):
        for i in self:
            if i.name:
                i.name = str(i.name).title()
            else:
                i.name = ''

    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        default = dict(default or {})
        default.update(
            name=_("%s (Copy)") % (self.name or ''))
        return super(BenefitBenefit, self).copy(default)
