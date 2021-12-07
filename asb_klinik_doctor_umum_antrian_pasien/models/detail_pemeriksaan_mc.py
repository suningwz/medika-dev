# -*- coding: utf-8 -*-

from odoo import api, fields, models, exceptions, _
from odoo.exceptions import UserError, ValidationError


class DetailPemeriksaanMc(models.Model):
    _name               = 'detail.pemeriksaan.mc'
    _description        = 'Detail Pemeriksaan Mc'

    product_id          = fields.Many2one('product.product', string = 'Nama Pemeriksaan')
    qty                 = fields.Integer(string = 'Qty', default = 1)
    poli_unit_id        = fields.Many2one('master.poli.unit', string = 'Poli / Unit', related = 'product_id.poli_unit_id')
    harga_satuan        = fields.Float(compute = '_compute_harga_satuan', string = 'Harga Satuan')
    registration_id     = fields.Many2one('master.registration', string = 'Registartion')
    tenaga_medis        = fields.Many2one('res.users', default = lambda self: self.env.user, string = 'Dokter')
    currency_id         = fields.Many2one('res.currency', 'Currency', default = lambda self: self.env.company.currency_id.id, readonly = True)
    product_ids         = fields.Many2many('product.product', compute = '_compute_product_ids', string = 'Product IDS')
    sub_total           = fields.Float(compute = '_compute_sub_total', string = 'Sub Total', store = True,)

    @api.depends('product_id')
    def _compute_product_ids(self):
        self.product_ids = False
        for rec in self:
            rec.product_ids = self.env['product.product'].sudo().search([('poli_unit_id', '=', self.env.user.poli_unit_id.id)])

    @api.depends('qty', 'harga_satuan')
    def _compute_sub_total(self):
        self.sub_total = 0
        for rec in self:
            rec.sub_total = rec.qty * rec.harga_satuan

    @api.onchange('registration_id')
    def _onchange_registration_id(self):
        upkeep_block = []

        if self.registration_id:
            for i in self.registration_id.detail_pemeriksaan_mc_ids:
                if not i.product_id.id in upkeep_block:
                    upkeep_block.append(i.product_id.id)
        return {
            'domain': {
                'product_id': [('poli_unit_id', '=', self.env.user.poli_unit_id.id), ('id', 'not in', upkeep_block)]
            }
        }

    @api.depends('product_id')
    def _compute_harga_satuan(self):
        for rec in self:
            harga_khusus = self.env['master.tindakan.layanan.line'].sudo().search(
                [('pricelist_id.perusahaan_id', '=', rec.registration_id.perusahaan_id.id), ('master_tindakan_id', '=', rec.product_id.id)], limit=1).harga_khusus
            if harga_khusus:
                rec.harga_satuan = harga_khusus
            else:
                rec.harga_satuan = rec.product_id.list_price

class MasterRegistration(models.Model):
    _inherit            = 'master.registration'
    _description        = 'Master Registration'

    detail_pemeriksaan_mc_ids   = fields.One2many('detail.pemeriksaan.mc', 'registration_id', string = 'Detail Pemeriksaan Ids')
    total_pemeriksaan_mc        = fields.Float(compute = '_compute_total', string = 'Total', store = True,)

    @api.depends('detail_pemeriksaan_mc_ids')
    def _compute_total(self):
        self.total_pemeriksaan_mc = 0
        for rec in self:
            rec.total_pemeriksaan_mc = sum(rec.detail_pemeriksaan_mc_ids.mapped('sub_total'))
