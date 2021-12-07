# -*- coding: utf-8 -*-

from odoo import _, api, fields, models, tools, SUPERUSER_ID
from odoo.exceptions import UserError, ValidationError


class PermintaanLab(models.Model):
    _name           = 'permintaan.lab'
    _description    = 'Permintaan Lab'
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
            rec.product_ids = self.env['product.product'].sudo().search([('poli_unit_id.nama_poli_unit', 'ilike', 'laboratorium')])

    @api.onchange('registration_id')
    def _onchange_registration_id(self):
        upkeep_block = []

        if self.registration_id:
            for i in self.registration_id.permintaan_lab_ids:
                if not i.product_id.id in upkeep_block:
                    upkeep_block.append(i.product_id.id)
        return {
            'domain': {
                'product_id': [('poli_unit_id.nama_poli_unit', 'ilike', 'laboratorium'), ('id', 'not in', upkeep_block)]
            }
        }
    
    @api.onchange('product_id')
    def _onchange_product_id(self):
        for rec in self:
            if rec.product_id:
                if rec.product_id.kode_lis == False:
                    rec.product_id = False
                    return{ 'warning':{
                                'title': "Invalid Kode LIS",
                                'message': "Kode LIS pada Tindakan yang dipilih tidak tersedia"
                            }}

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
    _inherit            = 'master.registration'
    _description        = 'Master Registration'

    permintaan_lab_ids  = fields.One2many('permintaan.lab', 'registration_id', string = 'Permintaan Lab')
    cost_permintaan_lab = fields.Float(compute = '_compute_cost_permintaan_lab', string = 'Total')

    @api.depends('permintaan_lab_ids')
    def _compute_cost_permintaan_lab(self):
        self.cost_permintaan_lab = 0
        for rec in self:
            rec.cost_permintaan_lab = sum(rec.permintaan_lab_ids.mapped('harga_jual'))
            
    def write(self, values):
        res = super(MasterRegistration, self).write(values)
        data_pasien = self.filtered(lambda r : self.id in r.ids).name
        data_ono = { 'ONO' : data_pasien }
        data_lab = { 'ONO' : [], 'id_product' : [] }
        data = self.env['permintaan.lab'].search([('registration_id', '=', self.id)])
        if data:
            data_lab['ONO'] += [rec.registration_id.name for rec in data[0] if rec.registration_id.name not in data_lab['ONO']]
            data_lab['id_product'] += [rec.product_id.id for rec in data if rec.product_id.id not in data_lab['id_product']]
            self._update_data_to_mysql(data_lab)
        if self.is_done_perawat and not data:
            self._update_null_lab_to_mysql(data_ono)
        return res
