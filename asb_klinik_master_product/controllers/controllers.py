# -*- coding: utf-8 -*-
# from odoo import http


# class AsbMasterProduct(http.Controller):
#     @http.route('/asb_master_product/asb_master_product/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/asb_master_product/asb_master_product/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('asb_master_product.listing', {
#             'root': '/asb_master_product/asb_master_product',
#             'objects': http.request.env['asb_master_product.asb_master_product'].search([]),
#         })

#     @http.route('/asb_master_product/asb_master_product/objects/<model("asb_master_product.asb_master_product"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('asb_master_product.object', {
#             'object': obj
#         })
