# -*- coding: utf-8 -*-
# from odoo import http


# class AsbMasterKetenagaan(http.Controller):
#     @http.route('/asb_master_ketenagaan/asb_master_ketenagaan/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/asb_master_ketenagaan/asb_master_ketenagaan/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('asb_master_ketenagaan.listing', {
#             'root': '/asb_master_ketenagaan/asb_master_ketenagaan',
#             'objects': http.request.env['asb_master_ketenagaan.asb_master_ketenagaan'].search([]),
#         })

#     @http.route('/asb_master_ketenagaan/asb_master_ketenagaan/objects/<model("asb_master_ketenagaan.asb_master_ketenagaan"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('asb_master_ketenagaan.object', {
#             'object': obj
#         })
