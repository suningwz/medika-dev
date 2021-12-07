# -*- coding: utf-8 -*-

from odoo import api, fields, models, exceptions, _
from odoo.exceptions import UserError, ValidationError


class ResepObat(models.Model):
    _name           = 'resep.obat'
    _inherit        = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
    _description    = 'Resep Obat'

    package         = fields.Selection( [
                                            ('item', 'Item'),
                                            ('racikan', 'Racikan'),
                                        ], string = 'Package', tracking = True)
    deskripsi       = fields.Text(string = 'Deskripsi', tracking = True)
    product_id      = fields.Many2one('product.product', string = 'Product ID', tracking = True)
    jenis_racikan   = fields.Selection( [
                                            ('puyer', 'Puyer'),
                                            ('kapsul', 'Kapsul'),
                                        ], string = 'Jenis Racikan', tracking = True)
    qty             = fields.Integer(string = 'Qty', default = 1, tracking = True)
    signa           = fields.Char(string = 'Signa', tracking = True)
    registration_id = fields.Many2one('master.registration', string = 'Registration ID', tracking = True)
    detail_obat_line = fields.One2many('detail.obat', 'resep_obat_id', string = 'Detail Obat Line', tracking = True)
    on_hand         = fields.Float(related = 'product_id.qty_available', tracking = True)
    uom_id          = fields.Many2one(related = 'product_id.uom_id', tracking = True)
    harga_jual      = fields.Float(compute = '_compute_harga_jual', string = 'Harga Jual')
    sub_total       = fields.Float(string = 'Sub Total', store = True,)
    total_detail_obat = fields.Float(string = 'Sub Total', store = True, compute = '_compute_total', tracking = True)
    currency_id     = fields.Many2one('res.currency', 'Currency', default = lambda self: self.env.company.currency_id.id, readonly = True, tracking = True)

    @api.depends('product_id')
    def _compute_harga_jual(self):
        for rec in self:
            harga_khusus = self.env['master.alat.obat.line'].sudo().search(
                [('pricelist_id.perusahaan_id', '=', rec.registration_id.perusahaan_id.id), ('master_alat_obat_id', '=', rec.product_id.id)], limit=1).harga_khusus
            if harga_khusus:
                rec.harga_jual = harga_khusus
            else:
                rec.harga_jual = rec.product_id.list_price

    @api.depends('detail_obat_line')
    def _compute_total(self):
        self.total_detail_obat = 0
        for rec in self:
            rec.total_detail_obat = sum(rec.detail_obat_line.mapped('sub_total'))

    @api.onchange('product_id', 'qty')
    def _onchange_action_product_add(self):
        r = [(5, 0, 0)]
        value = {}
        if self.product_id:
            data = {'product_id': self.product_id.id,
                    'qty': self.qty,
                    'name': self.product_id.name
                    }
            r.append((0, 0, data))
            value.update(detail_obat_line=r)
            return {'value': value}

    @api.onchange('qty')
    def _onchange_qty(self):
        for rec in self:
            if rec.product_id:
                if rec.qty > rec.on_hand:
                    return {
                        'warning': {'title': 'Warning!', 'message': 'Stok Obat Tersedia adalah %s!' % rec.on_hand},
                        'value': {'qty': rec.on_hand}
                    }
