# -*- coding: utf-8 -*-
# from odoo import http


# class AsbKlinikDoctorJantungAntrianPasien(http.Controller):
#     @http.route('/asb_klinik_doctor_jantung_antrian_pasien/asb_klinik_doctor_jantung_antrian_pasien/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/asb_klinik_doctor_jantung_antrian_pasien/asb_klinik_doctor_jantung_antrian_pasien/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('asb_klinik_doctor_jantung_antrian_pasien.listing', {
#             'root': '/asb_klinik_doctor_jantung_antrian_pasien/asb_klinik_doctor_jantung_antrian_pasien',
#             'objects': http.request.env['asb_klinik_doctor_jantung_antrian_pasien.asb_klinik_doctor_jantung_antrian_pasien'].search([]),
#         })

#     @http.route('/asb_klinik_doctor_jantung_antrian_pasien/asb_klinik_doctor_jantung_antrian_pasien/objects/<model("asb_klinik_doctor_jantung_antrian_pasien.asb_klinik_doctor_jantung_antrian_pasien"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('asb_klinik_doctor_jantung_antrian_pasien.object', {
#             'object': obj
#         })
