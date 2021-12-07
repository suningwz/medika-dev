# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from datetime import date
from odoo.exceptions import ValidationError


class RebateDetail(models.Model):
    _name = 'rebate.detail'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
    _description = 'Provider Rebate Detail'
    _rec_name = 'partner_id'

    partner_id = fields.Many2one('res.partner', string='Provider Name', tracking=True, ondelete='cascade')
    benefit_category_id = fields.Many2one('benefit.master', string='Item Category', tracking=True)
    benefit_option = fields.Selection([
        ('all', 'All Category'),
        ('benefit', 'Benefit'),
        ('partial', 'Partial'),
    ], string='Category Option', tracking=True)
    benefit_id = fields.Many2one('benefit.benefit', string='Benefit Name', tracking=True)
    get_benefit_id_domain = fields.Many2many('benefit.benefit', compute='_compute_get_benefit_id_domain', string='Benefit Domain')
    rebate = fields.Float(string='Rebate', tracking=True)
    top = fields.Integer(related='partner_id.top', tracking=True)
    top_type = fields.Selection(related='partner_id.top_type', tracking=True)
    start_date = fields.Date(string='Start Date', default=date.today(), tracking=True)
    created_date = fields.Date(string='Created Date', default=lambda self: fields.datetime.now(), required=True, tracking=True)
    created_by = fields.Many2one('res.users', string='Created By', default=lambda self: self.env.user.id, required=True, tracking=True)
    benefit_line = fields.One2many('rebate.benefit', 'rebate_id', string='Benefit Lines')

    # @api.onchange('top')
    # def _onchange_top(self):
    #     if self.top:
    #         if not self.top.isdigit():
    #             raise ValidationError(_("TOP must be in number."))

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

    @api.onchange('benefit_option', 'rebate', 'benefit_category_id')
    def _onchange_benefit_option(self):
        if self.benefit_option == 'all':
            self.benefit_category_id = []
            lines = [(5, 0, 0)]
            for rec in self.env['benefit.benefit'].search([]):
                for benefit in rec:
                    vals = {
                        'benefit_id': benefit.id,
                        'rebate': self.rebate,
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
                            'rebate': self.rebate,
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
        res = super(RebateDetail, self).create(vals)
        for rec in self:
            rec.partner_id.rebate_detail_line.append((0, 0, vals))
        return res


class RebateBenefit(models.Model):
    _name = 'rebate.benefit'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
    _description = 'Rebate Benefit'
    _rec_name = 'benefit_id'

    benefit_id = fields.Many2one('benefit.benefit', string='Benefit', tracking=True, required=True, ondelete='cascade')
    rebate_id = fields.Many2one('rebate.detail', string='Provider Rebate', tracking=True)
    rebate = fields.Float(string='Rebate', tracking=True, store=True)
    get_benefit_id_domain = fields.Many2many('benefit.benefit', compute='_compute_get_benefit_id_domain', string='Benefit Domain')

    @api.depends('rebate_id')
    def _compute_get_benefit_id_domain(self):
        for rec in self:
            if rec.rebate_id.benefit_category_id:
                rec.get_benefit_id_domain = self.env['benefit.benefit'].search([('master_id', '=', self.rebate_id.benefit_category_id.id)])
            if not rec.rebate_id.benefit_category_id:
                rec.get_benefit_id_domain = self.env['benefit.benefit'].search([('master_id', '=', self.rebate_id.benefit_category_id.id)])


class ResPartner(models.Model):
    _inherit = 'res.partner'

    rebate_detail_count = fields.Integer(string='Rebate Detail', compute='_compute_rebate_detail_count', store=True,)
    rebate_detail_line = fields.One2many('rebate.detail', 'partner_id', string='Rebate Detail Line')

    @api.depends('rebate_detail_line')
    def _compute_rebate_detail_count(self):
        for record in self:
            record.rebate_detail_count = self.env['rebate.detail'].search_count([('partner_id', '=', record.id)])
