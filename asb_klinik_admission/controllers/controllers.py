# -*- coding: utf-8 -*-
# from odoo import http


# class AsbKlinikAdmission(http.Controller):
#     @http.route('/asb_klinik_admission/asb_klinik_admission/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/asb_klinik_admission/asb_klinik_admission/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('asb_klinik_admission.listing', {
#             'root': '/asb_klinik_admission/asb_klinik_admission',
#             'objects': http.request.env['asb_klinik_admission.asb_klinik_admission'].search([]),
#         })

#     @http.route('/asb_klinik_admission/asb_klinik_admission/objects/<model("asb_klinik_admission.asb_klinik_admission"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('asb_klinik_admission.object', {
#             'object': obj
#         })
