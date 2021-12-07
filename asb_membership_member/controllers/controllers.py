# -*- coding: utf-8 -*-
# from odoo import http


# class AsbMembershipMember(http.Controller):
#     @http.route('/asb_membership_member/asb_membership_member/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/asb_membership_member/asb_membership_member/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('asb_membership_member.listing', {
#             'root': '/asb_membership_member/asb_membership_member',
#             'objects': http.request.env['asb_membership_member.asb_membership_member'].search([]),
#         })

#     @http.route('/asb_membership_member/asb_membership_member/objects/<model("asb_membership_member.asb_membership_member"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('asb_membership_member.object', {
#             'object': obj
#         })
