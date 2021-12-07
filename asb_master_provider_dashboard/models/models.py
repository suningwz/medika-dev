# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'
    _description = 'Res Partner'

    @api.model
    def retrieve_master_provider_dashboard(self):
        self.check_access_rights('read')
        apotik = self.search_count([('provider', '=', True), ('provider_category', '=', 'apotik')])
        klinik = self.search_count([('provider', '=', True), ('provider_category', '=', 'klinik')])
        laboratorium = self.search_count([('provider', '=', True), ('provider_category', '=', 'lab')])
        optik = self.search_count([('provider', '=', True), ('provider_category', '=', 'optik')])
        rumah_sakit = self.search_count([('provider', '=', True), ('provider_category', '=', 'rs')])
        rebate = self.search_count([('provider', '=', True), ('rebate_detail_count', '>', 0)])
        discount = self.search_count([('provider', '=', True), ('provider_discount_count', '>', 0)])
        contract_60_hari = self.search_count([('provider', '=', True), ('remaining_contract_int', '>=', -60)])
        res = {
            "total_apotik": 0,
            "total_klinik": 0,
            "total_laboratorium": 0,
            "total_optik": 0,
            "total_rumah_sakit": 0,
            "total_rebate": 0,
            "total_discount": 0,
            "total_contract_60_hari": 0,
        }
        res['total_apotik'] = apotik
        res['total_klinik'] = klinik
        res['total_laboratorium'] = laboratorium
        res['total_optik'] = optik
        res['total_rumah_sakit'] = rumah_sakit
        res['total_rebate'] = rebate
        res['total_discount'] = discount
        res['total_contract_60_hari'] = contract_60_hari
        return res
    
    # Qweb method
    def _qweb_prepare_qcontext(self, view_id, domain):
        values = super(ResPartner, self)._qweb_prepare_qcontext(view_id, domain)
        values.update(self._get_value_provider())
        return values

    def _get_value_provider(self):
        # self.check_access_rights('read')
        provider = self.search_count([('provider', '=', True)])
        apotik = self.search_count([('provider', '=', True), ('provider_category', '=', 'apotik')])
        klinik = self.search_count([('provider', '=', True), ('provider_category', '=', 'klinik')])
        laboratorium = self.search_count([('provider', '=', True), ('provider_category', '=', 'lab')])
        optik = self.search_count([('provider', '=', True), ('provider_category', '=', 'optik')])
        rumah_sakit = self.search_count([('provider', '=', True), ('provider_category', '=', 'rs')])
        rebate = self.search_count([('provider', '=', True), ('rebate_detail_count', '>', 0)])
        discount = self.search_count([('provider', '=', True), ('provider_discount_count', '>', 0)])
        contract_60_hari = self.search_count([('provider', '=', True), ('remaining_contract_int', '>=', -60)])
        res = {
            "total_provider": 0,
            "total_apotik": 0,
            "total_klinik": 0,
            "total_laboratorium": 0,
            "total_optik": 0,
            "total_rumah_sakit": 0,
            "total_rebate": 0,
            "total_discount": 0,
            "total_contract_60_hari": 0,
        }
        res['total_provider'] = provider
        res['total_apotik'] = apotik
        res['total_klinik'] = klinik
        res['total_laboratorium'] = laboratorium
        res['total_optik'] = optik
        res['total_rumah_sakit'] = rumah_sakit
        res['total_rebate'] = rebate
        res['total_discount'] = discount
        res['total_contract_60_hari'] = contract_60_hari
        return res


    def get_jumlah_provider(self):
        month = [1,2,3,4,5]
        count = [10,11,13,14,15]
        title = 'Jumlah Provider'

        result = {
            'labels': month,
            'count': count,
            'title': title,
        }
        return result

    def get_penambahan_jumlah_provider(self):
        month = [1,2,3,5]
        count = [10,11,13,15]
        title = 'Penambahan Jumlah Provider'

        result = {
            'labels': month,
            'count': count,
            'title': title,
        }
        return result

    def get_penambahan_rebate(self):
        month = [1,2,3,4,5]
        count = [10,11,13,14]
        title = 'Penambahan Rebate'

        result = {
            'labels': month,
            'count': count,
            'title': title,
        }
        return result

    def get_provider_base_location(self):
        labels = ["Domestic","Mancanegara"]
        count = [1000,10]
        title = 'Provider Location'
        barColors = [
            "#b91d47",
            "#00aba9",
        ]

        result = {
            'labels': labels,
            'count': count,
            'title': title,
            'barColors': barColors,
        }
        return result
