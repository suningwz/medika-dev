# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class asb_invisible_partner(models.Model):
#     _name = 'asb_invisible_partner.asb_invisible_partner'
#     _description = 'asb_invisible_partner.asb_invisible_partner'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
