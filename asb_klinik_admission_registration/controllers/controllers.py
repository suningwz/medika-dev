# -*- coding: utf-8 -*-
# from odoo import http


# class AsbKlinikAdmissionRegistration(http.Controller):
#     @http.route('/asb_klinik_admission_registration/asb_klinik_admission_registration/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/asb_klinik_admission_registration/asb_klinik_admission_registration/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('asb_klinik_admission_registration.listing', {
#             'root': '/asb_klinik_admission_registration/asb_klinik_admission_registration',
#             'objects': http.request.env['asb_klinik_admission_registration.asb_klinik_admission_registration'].search([]),
#         })

#     @http.route('/asb_klinik_admission_registration/asb_klinik_admission_registration/objects/<model("asb_klinik_admission_registration.asb_klinik_admission_registration"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('asb_klinik_admission_registration.object', {
#             'object': obj
#         })
