# -*- coding: utf-8 -*-
# from odoo import http


# class AsbKlinikCostingTeam(http.Controller):
#     @http.route('/asb_klinik_costing_team/asb_klinik_costing_team/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/asb_klinik_costing_team/asb_klinik_costing_team/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('asb_klinik_costing_team.listing', {
#             'root': '/asb_klinik_costing_team/asb_klinik_costing_team',
#             'objects': http.request.env['asb_klinik_costing_team.asb_klinik_costing_team'].search([]),
#         })

#     @http.route('/asb_klinik_costing_team/asb_klinik_costing_team/objects/<model("asb_klinik_costing_team.asb_klinik_costing_team"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('asb_klinik_costing_team.object', {
#             'object': obj
#         })
