# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from datetime import datetime, date


class ProviderDiscount(models.Model):
    _name = 'provider.discount'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
    _description = 'Provider Discount'
    _rec_name = 'partner_id'

    partner_id = fields.Many2one('res.partner', string='Provider Name', tracking=True, ondelete='cascade')
    benefit_category_id = fields.Many2one('benefit.master', string='Item Category', tracking=True)
    benefit_option = fields.Selection([
        ('all', 'All Category'),
        ('benefit', 'Benefit'),
        ('partial', 'Partial'),
    ], string='Category Option')
    benefit_id = fields.Many2one('benefit.benefit', string='Benefit Name', tracking=True)
    discount = fields.Float(string='Discount', tracking=True)
    remarks = fields.Many2one('master.remarks', string='Remarks', tracking=True)
    start_date = fields.Date(string='Start Date', default=date.today(), tracking=True)
    benefit_line = fields.One2many('discount.benefit', 'discount_id', string='Benefit Line')
    get_benefit_id_domain = fields.Many2many('benefit.benefit', compute='_compute_get_benefit_id_domain', string='Benefit Domain')
    created_date = fields.Date(string='Created Date', default=lambda self: fields.datetime.now(), required=True, tracking=True)
    created_by = fields.Many2one('res.users', string='Created By', default=lambda self: self.env.user.id, required=True, tracking=True)

    @api.onchange('benefit_category_id')
    def _onchange_(self):
        self.benefit_id = []

    @api.depends('benefit_category_id')
    def _compute_get_benefit_id_domain(self):
        for rec in self:
            if rec.benefit_category_id:
                rec.get_benefit_id_domain = self.env['benefit.benefit'].search([('master_id', '=', self.benefit_category_id.id)])
            if not rec.benefit_category_id:
                rec.get_benefit_id_domain = self.env['benefit.benefit'].search([('master_id', '=', self.benefit_category_id.id)])

    @api.onchange('benefit_option', 'discount', 'benefit_category_id')
    def _onchange_benefit_option(self):
        if self.benefit_option == 'all':
            self.benefit_category_id = []
            lines = [(5, 0, 0)]
            for rec in self.env['benefit.benefit'].search([]):
                for benefit in rec:
                    vals = {
                        'benefit_id': benefit.id,
                        'discount': self.discount,
                    }
                    lines.append((0, 0, vals))
            self.benefit_line = lines
        elif self.benefit_option == 'benefit':
            lines = [(5, 0, 0)]
            if self.benefit_category_id:
                for rec in self.env['benefit.benefit'].search([('master_id', '=', self.benefit_category_id.id)]):
                    for benefit in rec:
                        vals = {
                            'benefit_id': benefit.id,
                            'discount': self.discount,
                        }
                        lines.append((0, 0, vals))
            self.benefit_line = lines
        else:
            lines = [(5, 0, 0)]
            if self.benefit_category_id:
                for rec in self.env['benefit.benefit'].search([('master_id', '=', self.benefit_category_id.id)]):
                    for benefit in rec:
                        vals = {
                            'benefit_id': benefit.id,
                        }
                        lines.append((0, 0, vals))
            self.benefit_line = lines

    @api.model
    def create(self, vals):
        res = super(ProviderDiscount, self).create(vals)
        for rec in self:
            rec.partner_id.provider_discount_line.append((0, 0, vals))
        return res

class DiscountBenefit(models.Model):
    _name = 'discount.benefit'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
    _description = 'Discount Benefit'
    _rec_name = 'benefit_id'

    benefit_id = fields.Many2one('benefit.benefit', string='Benefit', tracking=True, required=True, ondelete='cascade')
    discount_id = fields.Many2one('provider.discount', string='Provider Discount', tracking=True)
    discount = fields.Float(string='Discount', tracking=True, store=True)
    get_benefit_id_domain = fields.Many2many('benefit.benefit', compute='_compute_get_benefit_id_domain', string='Benefit Domain')

    @api.depends('discount_id')
    def _compute_get_benefit_id_domain(self):
        for rec in self:
            if rec.discount_id.benefit_category_id:
                rec.get_benefit_id_domain = self.env['benefit.benefit'].search([('master_id', '=', self.discount_id.benefit_category_id.id)])
            if not rec.discount_id.benefit_category_id:
                rec.get_benefit_id_domain = self.env['benefit.benefit'].search([('master_id', '=', self.discount_id.benefit_category_id.id)])


class ResPartner(models.Model):
    _inherit = 'res.partner'

    provider_discount_count = fields.Integer(compute='_compute_provider_discount', string='Discount', store=True,)

    provider_discount_line = fields.One2many('provider.discount', 'partner_id', string='Provider Discount Line')

    @api.depends('provider_discount_line')
    def _compute_provider_discount(self):
        for record in self:
            record.provider_discount_count = self.env['provider.discount'].search_count([('partner_id', '=', record.id)])
