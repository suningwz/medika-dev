# -*- coding: utf-8 -*-
# from odoo import http


# class AsbMasterPoliUnit(http.Controller):
#     @http.route('/asb_master_poli_unit/asb_master_poli_unit/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/asb_master_poli_unit/asb_master_poli_unit/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('asb_master_poli_unit.listing', {
#             'root': '/asb_master_poli_unit/asb_master_poli_unit',
#             'objects': http.request.env['asb_master_poli_unit.asb_master_poli_unit'].search([]),
#         })

#     @http.route('/asb_master_poli_unit/asb_master_poli_unit/objects/<model("asb_master_poli_unit.asb_master_poli_unit"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('asb_master_poli_unit.object', {
#             'object': obj
#         })
