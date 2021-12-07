# -*- coding: utf-8 -*-
# from odoo import http


# class AsbMasterCostAllocation(http.Controller):
#     @http.route('/asb_master_cost_allocation/asb_master_cost_allocation/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/asb_master_cost_allocation/asb_master_cost_allocation/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('asb_master_cost_allocation.listing', {
#             'root': '/asb_master_cost_allocation/asb_master_cost_allocation',
#             'objects': http.request.env['asb_master_cost_allocation.asb_master_cost_allocation'].search([]),
#         })

#     @http.route('/asb_master_cost_allocation/asb_master_cost_allocation/objects/<model("asb_master_cost_allocation.asb_master_cost_allocation"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('asb_master_cost_allocation.object', {
#             'object': obj
#         })
