# -*- coding: utf-8 -*-
from odoo import api, fields, models, exceptions, _
from odoo.exceptions import UserError, ValidationError


class PermintaanRadiologi(models.Model):
    _name           = 'permintaan.radiologi'
    _description    = 'Permintaan radiologi'
    _rec_name       = 'product_id'

    product_id      = fields.Many2one('product.product', string = 'Product')
    harga_jual      = fields.Float(compute = '_compute_harga_jual', string = 'Harga Jual')
    keterangan      = fields.Text(string = 'Keterangan')
    registration_id = fields.Many2one('master.registration', string = 'Master Registration')
    product_ids     = fields.Many2many('product.product', compute = '_compute_product_ids', string = 'Product IDS')
    currency_id     = fields.Many2one('res.currency', 'Currency', default = lambda self: self.env.company.currency_id.id, readonly = True)

    @api.depends('product_id')
    def _compute_product_ids(self):
        self.product_ids = False
        for rec in self:
            rec.product_ids = self.env['product.product'].sudo().search([('poli_unit_id.nama_poli_unit', 'ilike', 'radiologi')])

    @api.onchange('registration_id')
    def _onchange_registration_id(self):
        upkeep_block = []

        if self.registration_id:
            for i in self.registration_id.permintaan_radiologi_ids:
                if not i.product_id.id in upkeep_block:
                    upkeep_block.append(i.product_id.id)
        return {
            'domain': {
                'product_id': [('poli_unit_id.nama_poli_unit', 'ilike', 'radiologi'), ('id', 'not in', upkeep_block)]
            }
        }

    @api.depends('product_id')
    def _compute_harga_jual(self):
        for rec in self:
            harga_khusus = self.env['master.tindakan.layanan.line'].sudo().search(
                [('pricelist_id.perusahaan_id', '=', rec.registration_id.perusahaan_id.id), ('master_tindakan_id', '=', rec.product_id.id)], limit=1).harga_khusus
            if harga_khusus:
                rec.harga_jual = harga_khusus
            else:
                rec.harga_jual = rec.product_id.list_price


class MasterRegistration(models.Model):
    _inherit        = 'master.registration'
    _description    = 'Master Registration'

    permintaan_radiologi_ids    = fields.One2many('permintaan.radiologi', 'registration_id', string = 'Permintaan radiologi')
    cost_permintaan_radiologi   = fields.Float(compute = '_compute_cost_permintaan_radiologi', string = 'Total')

    @api.depends('permintaan_radiologi_ids')
    def _compute_cost_permintaan_radiologi(self):
        self.cost_permintaan_radiologi = 0
        for rec in self:
            rec.cost_permintaan_radiologi = sum(rec.permintaan_radiologi_ids.mapped('harga_jual'))
