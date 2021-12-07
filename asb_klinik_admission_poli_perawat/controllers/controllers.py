# -*- coding: utf-8 -*-
# from odoo import http


# class AsbKlinikAdmissionPoliPerawat(http.Controller):
#     @http.route('/asb_klinik_admission_poli_perawat/asb_klinik_admission_poli_perawat/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/asb_klinik_admission_poli_perawat/asb_klinik_admission_poli_perawat/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('asb_klinik_admission_poli_perawat.listing', {
#             'root': '/asb_klinik_admission_poli_perawat/asb_klinik_admission_poli_perawat',
#             'objects': http.request.env['asb_klinik_admission_poli_perawat.asb_klinik_admission_poli_perawat'].search([]),
#         })

#     @http.route('/asb_klinik_admission_poli_perawat/asb_klinik_admission_poli_perawat/objects/<model("asb_klinik_admission_poli_perawat.asb_klinik_admission_poli_perawat"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('asb_klinik_admission_poli_perawat.object', {
#             'object': obj
#         })
