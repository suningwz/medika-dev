# -*- coding: utf-8 -*-
# from odoo import http


# class AsbKlinikAdmissionReservation(http.Controller):
#     @http.route('/asb_klinik_admission_reservation/asb_klinik_admission_reservation/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/asb_klinik_admission_reservation/asb_klinik_admission_reservation/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('asb_klinik_admission_reservation.listing', {
#             'root': '/asb_klinik_admission_reservation/asb_klinik_admission_reservation',
#             'objects': http.request.env['asb_klinik_admission_reservation.asb_klinik_admission_reservation'].search([]),
#         })

#     @http.route('/asb_klinik_admission_reservation/asb_klinik_admission_reservation/objects/<model("asb_klinik_admission_reservation.asb_klinik_admission_reservation"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('asb_klinik_admission_reservation.object', {
#             'object': obj
#         })
