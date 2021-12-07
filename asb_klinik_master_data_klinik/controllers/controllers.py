# -*- coding: utf-8 -*-
# from odoo import http


# class AsbMasterDataKlinik(http.Controller):
#     @http.route('/asb_master_data_klinik/asb_master_data_klinik/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/asb_master_data_klinik/asb_master_data_klinik/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('asb_master_data_klinik.listing', {
#             'root': '/asb_master_data_klinik/asb_master_data_klinik',
#             'objects': http.request.env['asb_master_data_klinik.asb_master_data_klinik'].search([]),
#         })

#     @http.route('/asb_master_data_klinik/asb_master_data_klinik/objects/<model("asb_master_data_klinik.asb_master_data_klinik"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('asb_master_data_klinik.object', {
#             'object': obj
#         })
