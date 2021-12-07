# -*- coding: utf-8 -*-

from odoo import api, fields, models, exceptions, _
from odoo.exceptions import UserError, ValidationError
from random import randint

class DetailObat(models.Model):
    _name           = 'detail.obat'
    _inherit        = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
    _description    = 'Detail Obat'

    def _get_default_color(self):
        return randint(1, 11)

    product_id      = fields.Many2one('product.product', string = 'Product ID', tracking = True)
    name            = fields.Char(string = 'Description', tracking = True)
    qty             = fields.Integer(string = 'Qty', tracking = True)
    on_hand         = fields.Float(related = 'product_id.qty_available', tracking = True)
    uom_id          = fields.Many2one(related = 'product_id.uom_id', tracking = True)
    harga_jual      = fields.Float(compute = '_compute_harga_jual', string = 'Harga Jual')
    currency_id     = fields.Many2one('res.currency', 'Currency', default = lambda self: self.env.company.currency_id.id, readonly = True, tracking = True)
    sub_total       = fields.Float(compute = '_compute_sub_total', string = 'Sub Total', store = True, tracking = True)
    resep_obat_id   = fields.Many2one('resep.obat', string = 'Resep Obat ID', tracking = True)
    color           = fields.Integer(string = 'Color Index', default = _get_default_color, tracking = True)

    @api.depends('qty', 'harga_jual')
    def _compute_sub_total(self):
        self.sub_total = 0
        for rec in self:
            rec.sub_total = rec.qty * rec.harga_jual

    @api.onchange('product_id')
    def _onchange_product_id(self):
        for rec in self:
            if rec.product_id:
                rec.qty = 1
        self.name = self.product_id.name

    @api.onchange('qty')
    def _onchange_qty(self):
        for rec in self:
            if rec.product_id:
                if rec.qty > rec.on_hand:
                    return {
                        'warning': {'title': 'Warning!', 'message': 'Stok Obat Tersedia adalah %s!' % rec.on_hand},
                        'value': {'qty': rec.on_hand}
                    }

    @api.onchange('resep_obat_id')
    def _onchange_resep_obat_id(self):
        upkeep_block = []

        if self.resep_obat_id:
            for i in self.resep_obat_id.detail_obat_line:
                if not i.product_id.id in upkeep_block:
                    upkeep_block.append(i.product_id.id)
        return {
            'domain': {
                'product_id': [('jenis_persediaan', '=', 'obat'), ('id', 'not in', upkeep_block)]
            }
        }

    @api.depends('product_id')
    def _compute_harga_jual(self):
        for rec in self:
            harga_khusus = self.env['master.alat.obat.line'].sudo().search(
                [('pricelist_id.perusahaan_id', '=', rec.resep_obat_id.registration_id.perusahaan_id.id), ('master_alat_obat_id', '=', rec.product_id.id)], limit=1).harga_khusus
            if harga_khusus:
                rec.harga_jual = harga_khusus
            else:
                rec.harga_jual = rec.product_id.list_price
