# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from datetime import date


class ClientBranch(models.Model):
    _name = 'client.branch'
    _description = 'Client Branch'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']

    def refresh(self):
        pass

    name = fields.Char(string='Branch Name', tracking=True)
    client_id = fields.Many2one('res.partner', string='Client', tracking=True)
    contract_number = fields.Char(string='Contract Number')
    street = fields.Char(string='Street', tracking=True)
    street2 = fields.Char(string='Street2', tracking=True)
    zip = fields.Char(change_default=True, tracking=True)
    country_id = fields.Many2one('res.country', string='Country', ondelete='restrict', tracking=True)
    start_date = fields.Date(string='Effective Date', tracking=True, required=True, )
    end_date = fields.Date(string='Expiry Date', tracking=True, required=True, )
    branch_member_count = fields.Integer(compute='_compute_branch_member_count', string='Member')
    branch_program_count = fields.Integer(compute='_compute_branch_program_count', string='Program')
    created_date = fields.Date(string='Created Date', default=lambda self: fields.datetime.now(), required=True, tracking=True)
    created_by = fields.Many2one('res.users', string='Created By', default=lambda self: self.env.user.id, required=True, tracking=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('enabled', 'Enabled'),
        ('disabled', 'Disabled'),
    ], string='Status', default='draft', tracking=True)
    is_editable = fields.Boolean(string="Is editable", compute="_compute_is_editable", readonly=True, default=True)
    client_program_line = fields.One2many('client.program', 'client_branch_id', string='Client Program',)
    partner_line = fields.One2many('res.partner', 'client_branch_id', string='Member')

    state_id = fields.Many2one('res.country.state', "State", domain="[('country_id','=',country_id)]")
    city_id = fields.Many2one('res.state.city', 'Kabupaten', domain="[('state_id','=',state_id)]")
    kecamatan_id = fields.Many2one('res.city.kecamatan', 'Kecamatan', domain=[('city_id', '=', 'city_id')])
    kelurahan_id = fields.Many2one('res.kecamatan.kelurahan', 'Kelurahan', domain="[('kecamatan_id','=',kecamatan_id)]")

    def _compute_is_editable(self):
        for rec in self:
            if rec.state in ("enabled", "disabled"):
                rec.is_editable = False
            else:
                rec.is_editable = True

    def _compute_branch_program_count(self):
        for record in self:
            record.branch_program_count = self.env['client.program'].search_count([('client_branch_id', '=', self.id)])

    def _compute_branch_member_count(self):
        for record in self:
            record.branch_member_count = self.env['res.partner'].search_count([('client_branch_id', '=', self.id)])

    def enable(self):
        for rec in self:
            rec.state = 'enabled'

    def disable(self):
        for rec in self:
            rec.state = 'disabled'

    def draft(self):
        for rec in self:
            rec.state = 'draft'
