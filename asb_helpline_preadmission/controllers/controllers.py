# -*- coding: utf-8 -*-
# from odoo import http


# class AsbHelpline(http.Controller):
#     @http.route('/asb_helpline/asb_helpline/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/asb_helpline/asb_helpline/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('asb_helpline.listing', {
#             'root': '/asb_helpline/asb_helpline',
#             'objects': http.request.env['asb_helpline.asb_helpline'].search([]),
#         })

#     @http.route('/asb_helpline/asb_helpline/objects/<model("asb_helpline.asb_helpline"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('asb_helpline.object', {
#             'object': obj
#         })
