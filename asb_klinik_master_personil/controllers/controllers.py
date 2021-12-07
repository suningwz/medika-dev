# -*- coding: utf-8 -*-
# from odoo import http


# class AsbMasterPersonil(http.Controller):
#     @http.route('/asb_master_personil/asb_master_personil/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/asb_master_personil/asb_master_personil/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('asb_master_personil.listing', {
#             'root': '/asb_master_personil/asb_master_personil',
#             'objects': http.request.env['asb_master_personil.asb_master_personil'].search([]),
#         })

#     @http.route('/asb_master_personil/asb_master_personil/objects/<model("asb_master_personil.asb_master_personil"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('asb_master_personil.object', {
#             'object': obj
#         })
