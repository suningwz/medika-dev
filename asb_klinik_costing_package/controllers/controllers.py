# -*- coding: utf-8 -*-
# from odoo import http


# class AsbKlinikCostingPackage(http.Controller):
#     @http.route('/asb_klinik_costing_package/asb_klinik_costing_package/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/asb_klinik_costing_package/asb_klinik_costing_package/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('asb_klinik_costing_package.listing', {
#             'root': '/asb_klinik_costing_package/asb_klinik_costing_package',
#             'objects': http.request.env['asb_klinik_costing_package.asb_klinik_costing_package'].search([]),
#         })

#     @http.route('/asb_klinik_costing_package/asb_klinik_costing_package/objects/<model("asb_klinik_costing_package.asb_klinik_costing_package"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('asb_klinik_costing_package.object', {
#             'object': obj
#         })
