# -*- coding: utf-8 -*-
# from odoo import http


# class AsbKlinikCostingSettingOnsite(http.Controller):
#     @http.route('/asb_klinik_costing_setting_onsite/asb_klinik_costing_setting_onsite/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/asb_klinik_costing_setting_onsite/asb_klinik_costing_setting_onsite/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('asb_klinik_costing_setting_onsite.listing', {
#             'root': '/asb_klinik_costing_setting_onsite/asb_klinik_costing_setting_onsite',
#             'objects': http.request.env['asb_klinik_costing_setting_onsite.asb_klinik_costing_setting_onsite'].search([]),
#         })

#     @http.route('/asb_klinik_costing_setting_onsite/asb_klinik_costing_setting_onsite/objects/<model("asb_klinik_costing_setting_onsite.asb_klinik_costing_setting_onsite"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('asb_klinik_costing_setting_onsite.object', {
#             'object': obj
#         })
