# -*- coding: utf-8 -*-
# from odoo import http


# class AsbHistoryPartner(http.Controller):
#     @http.route('/asb_history_partner/asb_history_partner/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/asb_history_partner/asb_history_partner/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('asb_history_partner.listing', {
#             'root': '/asb_history_partner/asb_history_partner',
#             'objects': http.request.env['asb_history_partner.asb_history_partner'].search([]),
#         })

#     @http.route('/asb_history_partner/asb_history_partner/objects/<model("asb_history_partner.asb_history_partner"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('asb_history_partner.object', {
#             'object': obj
#         })
