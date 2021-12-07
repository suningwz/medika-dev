# -*- coding: utf-8 -*-
# from odoo import http


# class AsbMasterDokumen(http.Controller):
#     @http.route('/asb_master_dokumen/asb_master_dokumen/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/asb_master_dokumen/asb_master_dokumen/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('asb_master_dokumen.listing', {
#             'root': '/asb_master_dokumen/asb_master_dokumen',
#             'objects': http.request.env['asb_master_dokumen.asb_master_dokumen'].search([]),
#         })

#     @http.route('/asb_master_dokumen/asb_master_dokumen/objects/<model("asb_master_dokumen.asb_master_dokumen"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('asb_master_dokumen.object', {
#             'object': obj
#         })
