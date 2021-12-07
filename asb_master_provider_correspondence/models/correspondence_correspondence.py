# -*- coding: utf-8 -*-

from odoo import api, fields, models, exceptions, _
from datetime import datetime, date
from odoo.exceptions import UserError, ValidationError


class CorrespondenceCorrespondence(models.Model):
    _name = 'correspondence.correspondence'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
    _description = 'Correspondence Correspondence'

    @api.constrains('up_id')
    def check_up_id(self):
        res = self.env['res.partner'].search([('id', 'in', [rec.id for rec in self.partner_id.child_ids])])
        for rec in res:
            if self.up_id in rec:
                return
        if self.up_id:
            raise ValidationError(_("Unregistered Field 'Up'"))

    name = fields.Char(default='New_', tracking=True)
    type_id = fields.Many2one('correspondence.type', string='Format of Latter', required=True, tracking=True, ondelete="cascade")
    partner_id = fields.Many2one('res.partner', string='Provider Name', required=True, tracking=True, ondelete="cascade")
    created_date = fields.Date(string='Created Date', default=datetime.today(), required=True, tracking=True)
    created_by = fields.Many2one('res.users', string='Created By', default=lambda self: self.env.user.id, required=True, tracking=True)
    street = fields.Char(related='partner_id.street', store=True, tracking=True, ondelete="cascade")
    street2 = fields.Char(related='partner_id.street2', store=True, tracking=True, ondelete="cascade")
    city = fields.Char(related='partner_id.city', store=True, tracking=True, ondelete="cascade")
    state_id = fields.Many2one(related='partner_id.state_id', store=True, tracking=True, ondelete="cascade")
    zip = fields.Char(related='partner_id.zip', store=True, tracking=True)
    country_id = fields.Many2one(related='partner_id.country_id', store=True, ondelete="cascade")
    company_id = fields.Many2one('res.company', 'Company', default=lambda self: self.env.user.company_id.id, index=1, tracking=True)
    up_id = fields.Many2one('res.partner', string='Up', tracking=True, ondelete="cascade")
    up_ids = fields.Many2many('res.partner', string='Up ids', compute='_get_up_id_domain', ondelete="cascade")
    name_up_id = fields.Char(related='up_id.name', string='UP Name', ondelete="cascade")
    policy_id = fields.Many2one(string='Policy Number', tracking=True)
    policy_number = fields.Char(string='POLICY NUMBER', tracking=True)
    policy_date = fields.Date(string='POLICY DATE', tracking=True)
    extension = fields.Integer(string='Extension', default=1, tracking=True)

    @api.depends('partner_id')
    def _get_up_id_domain(self):
        self.up_ids = False
        for rec in self:
            if rec.partner_id:
                rec.up_ids = self.env['res.partner'].search([('id', 'in', [rec.id for rec in self.partner_id.child_ids])])

    def int_to_roman(self, input):
        ints = (1000, 900,  500, 400, 100,  90, 50,  40, 10,  9,   5,  4,   1)
        nums = ('M',  'CM', 'D', 'CD', 'C', 'XC', 'L', 'XL', 'X', 'IX', 'V', 'IV', 'I')

        result = ""
        for i in range(len(ints)):
            count = int(input / ints[i])
            result += nums[i] * count
            input -= ints[i] * count
        return result

    @api.model
    def create(self, vals):
        result = super(CorrespondenceCorrespondence, self).create(vals)
        for rec in result:
            rec.name = self.env['ir.sequence'].next_by_code('correspondence.correspondence') + rec.partner_id.provider_code + '/' + \
                str(self.int_to_roman(rec.created_date.month)) + '/' + str(rec.created_date.year)
            return result

    def print_letter(self):
        num_id = self.type_id.id
        name = '%s Correspondence Type' % num_id
        name_action = self.env['ir.actions.report'].sudo().search([('name', '=', name)])
        return name_action.report_action(self)

    def associated_view_correspondence(self):
        # correspondence = self.env['correspondence.correspondence'].sudo().search([('type_id', '=', self.id)])
        # if not correspondence:
        #     raise UserError("Create Correspondence with Format of Latter '%s' First!" % self.name)
        self.ensure_one()
        action_ref = self.env.ref('base.action_ui_view')
        report_name = '%s Correspondence Type' % self.type_id.id
        action_data = action_ref.read()[0]
        form_id = self.env['ir.ui.view'].search([('name', 'ilike', report_name), ('type', '=', 'qweb')])
        action_data['views'] = [(self.env.ref('base.view_view_form').id, 'form')]
        action_data['res_id'] = form_id.id
        return action_data
