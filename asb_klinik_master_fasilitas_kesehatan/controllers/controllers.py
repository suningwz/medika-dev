# -*- coding: utf-8 -*-
# from odoo import http


# class AsbMasterFasilitasKesehatan(http.Controller):
#     @http.route('/asb_master_fasilitas_kesehatan/asb_master_fasilitas_kesehatan/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/asb_master_fasilitas_kesehatan/asb_master_fasilitas_kesehatan/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('asb_master_fasilitas_kesehatan.listing', {
#             'root': '/asb_master_fasilitas_kesehatan/asb_master_fasilitas_kesehatan',
#             'objects': http.request.env['asb_master_fasilitas_kesehatan.asb_master_fasilitas_kesehatan'].search([]),
#         })

#     @http.route('/asb_master_fasilitas_kesehatan/asb_master_fasilitas_kesehatan/objects/<model("asb_master_fasilitas_kesehatan.asb_master_fasilitas_kesehatan"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('asb_master_fasilitas_kesehatan.object', {
#             'object': obj
#         })
