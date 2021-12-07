# -*- coding: utf-8 -*-
# from odoo import http


# class AsbKlinikAdmissionTeam(http.Controller):
#     @http.route('/asb_klinik_admission_team/asb_klinik_admission_team/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/asb_klinik_admission_team/asb_klinik_admission_team/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('asb_klinik_admission_team.listing', {
#             'root': '/asb_klinik_admission_team/asb_klinik_admission_team',
#             'objects': http.request.env['asb_klinik_admission_team.asb_klinik_admission_team'].search([]),
#         })

#     @http.route('/asb_klinik_admission_team/asb_klinik_admission_team/objects/<model("asb_klinik_admission_team.asb_klinik_admission_team"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('asb_klinik_admission_team.object', {
#             'object': obj
#         })
