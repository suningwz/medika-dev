# -*- coding: utf-8 -*-
# from odoo import http


# class AsbKlinikCosting(http.Controller):
#     @http.route('/asb_klinik_costing/asb_klinik_costing/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/asb_klinik_costing/asb_klinik_costing/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('asb_klinik_costing.listing', {
#             'root': '/asb_klinik_costing/asb_klinik_costing',
#             'objects': http.request.env['asb_klinik_costing.asb_klinik_costing'].search([]),
#         })

#     @http.route('/asb_klinik_costing/asb_klinik_costing/objects/<model("asb_klinik_costing.asb_klinik_costing"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('asb_klinik_costing.object', {
#             'object': obj
#         })
