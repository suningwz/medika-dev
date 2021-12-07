# -*- coding: utf-8 -*-
# from odoo import http


# class AsbKlinikCostingSetting(http.Controller):
#     @http.route('/asb_klinik_costing_setting/asb_klinik_costing_setting/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/asb_klinik_costing_setting/asb_klinik_costing_setting/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('asb_klinik_costing_setting.listing', {
#             'root': '/asb_klinik_costing_setting/asb_klinik_costing_setting',
#             'objects': http.request.env['asb_klinik_costing_setting.asb_klinik_costing_setting'].search([]),
#         })

#     @http.route('/asb_klinik_costing_setting/asb_klinik_costing_setting/objects/<model("asb_klinik_costing_setting.asb_klinik_costing_setting"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('asb_klinik_costing_setting.object', {
#             'object': obj
#         })
