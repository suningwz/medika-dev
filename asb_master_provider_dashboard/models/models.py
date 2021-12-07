# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime

class ResPartner(models.Model):
    _inherit = 'res.partner'
    _description = 'Res Partner'

    @api.model
    def retrieve_master_provider_dashboard(self):
        self.check_access_rights('read')
        apotik = self.search_count([('provider', '=', True), ('provider_type','=','provider') , ('provider_category', '=', 'apotik')])
        klinik = self.search_count([('provider', '=', True), ('provider_type','=','provider') , ('provider_category', '=', 'klinik')])
        laboratorium = self.search_count([('provider', '=', True), ('provider_type','=','provider') , ('provider_category', '=', 'lab')])
        optik = self.search_count([('provider', '=', True), ('provider_type','=','provider') , ('provider_category', '=', 'optik')])
        rumah_sakit = self.search_count([('provider', '=', True), ('provider_type','=','provider') , ('provider_category', '=', 'rs')])
        rebate = self.search_count([('provider', '=', True), ('provider_type','=','provider') , ('rebate_detail_count', '>', 0)])
        discount = self.search_count([('provider', '=', True), ('provider_type','=','provider') , ('provider_discount_count', '>', 0)])
        contract_60_hari = self.search_count([('provider', '=', True), ('provider_type','=','provider') , ('remaining_contract_int', '>=', -60)])
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
        provider = self.search_count([('provider', '=', True), ('provider_type','=','provider') ])
        apotik = self.search_count([('provider', '=', True), ('provider_type','=','provider') , ('provider_category', '=', 'apotik')])
        klinik = self.search_count([('provider', '=', True), ('provider_type','=','provider') , ('provider_category', '=', 'klinik')])
        laboratorium = self.search_count([('provider', '=', True), ('provider_type','=','provider') , ('provider_category', '=', 'lab')])
        optik = self.search_count([('provider', '=', True), ('provider_type','=','provider') , ('provider_category', '=', 'optik')])
        rumah_sakit = self.search_count([('provider', '=', True), ('provider_type','=','provider') , ('provider_category', '=', 'rs')])
        rebate = self.search_count([('provider', '=', True), ('provider_type','=','provider') , ('rebate_detail_count', '>', 0)])
        discount = self.search_count([('provider', '=', True), ('provider_type','=','provider') , ('provider_discount_count', '>', 0)])
        contract_60_hari = self.search_count([('provider', '=', True), ('provider_type','=','provider') , ('remaining_contract_int', '>=', -60)])
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
        # join = []
        # count = []
        # provider = self.env['res.partner'].search([("provider", "=", True)]).sorted('provider_join_date')
        # x = 0
        # for rec in provider:
        #     month_year = "%s %s" % (rec.provider_join_date.strftime("%b"), rec.provider_join_date.year)
        #     if month_year not in join:
        #         join.append(month_year)
        #         count_provider = self.search_count([('provider', '=', True), ('provider_type', '=', 'provider'), ('provider_join_date_month', '=',
        #                                            rec.provider_join_date.month), ('provider_join_date_year', '=', rec.provider_join_date.year)])
        #         x = x + count_provider
        #         count.append(x)
        
        # month = join
        # count = count
        # title = 'Jumlah Provider'

        # result = {
        #     'labels': month,
        #     'count': count,
        #     'title': title,
        # }
        # return result

        join = []
        count = []
        provider = self.env['res.partner'].search([("provider", "=", True)]).sorted('provider_join_date')
        history_join = self.env['history.join'].search([]).sorted('provider_join_date')
        x = 0
        for rec in history_join:
            month_year = "%s %s" % (rec.provider_join_date.strftime("%b"), rec.provider_join_date.year)
            if month_year not in join:
                join.append(month_year)
                count_provider_join = self.env['history.join'].search_count([('provider_join_date_month', '=', rec.provider_join_date.month), ('provider_join_date_year', '=', rec.provider_join_date.year)])
                count_provider_finished = self.env['history.finished'].search_count([('provider_finished_date_month', '=', rec.provider_join_date.month), ('provider_finished_date_year', '=', rec.provider_join_date.year)])
                
                x = x + count_provider_join - count_provider_finished
                count.append(x)
        
        month = join
        count = count
        title = 'Jumlah Provider'

        result = {
            'labels': month,
            'count': count,
            'title': title,
        }
        return result

    def get_penambahan_jumlah_provider(self):
        join = []
        count = []
        history_join = self.env['history.join'].search([]).sorted('provider_join_date')
        for rec in history_join:
            month_year = "%s %s" % (rec.provider_join_date.strftime("%b"), rec.provider_join_date.year)
            if month_year not in join:
                join.append(month_year)
                count_provider = self.env['history.join'].search_count([('provider_join_date_month', '=', rec.provider_join_date.month), ('provider_join_date_year', '=', rec.provider_join_date.year)])
                count.append(count_provider)

        month = join
        count = count
        title = 'Penambahan Jumlah Provider'

        result = {
            'labels': month,
            'count': count,
            'title': title,
        }
        return result



    def get_penambahan_rebate(self):
        month = []
        count = []
        rebate = self.env['rebate.detail'].search([]).sorted('created_date')
        for rec in rebate:
            month_year = "%s %s" % (rec.created_date.strftime("%b"), rec.created_date.year)
            if month_year not in month:
                month.append(month_year)
                count_rebate = self.env['rebate.detail'].search_count([('created_date_month', '=', rec.created_date.month), ('created_date_year', '=', rec.created_date.year)])
                count.append(count_rebate)

        month = month
        count = count
        title = 'Penambahan Rebate'

        result = {
            'labels': month,
            'count': count,
            'title': title,
        }
        return result

    def get_provider_base_location(self):
        indonesia = self.search_count([('provider', '=', True), ('provider_type', '=', 'provider'), ('country_id.name','=','Indonesia')])
        mancanegara = self.search_count([('provider', '=', True), ('provider_type', '=', 'provider'), ('country_id.name','!=','Indonesia')])
        labels = ["Domestic","Mancanegara"]
        count = [indonesia, mancanegara]
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
