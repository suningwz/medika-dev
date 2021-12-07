# -*- coding: utf-8 -*-
import re
from odoo import models, fields, api, _
from datetime import datetime, date
from odoo.exceptions import UserError, ValidationError


class ProviderProvider(models.Model):
    _name = 'provider.provider'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
    _description = 'Provider'
    _rec_name = 'partner_id'

    partner_id = fields.Many2one('res.partner', string='Provider Name', tracking=True)
    notes = fields.Text(string='Activity Notes', tracking=True)
    created_by = fields.Many2one('res.users', string='Created By', default=lambda self: self.env.user.id, required=True, tracking=True)
    created_date = fields.Date(string='Created Date', default=datetime.today(), tracking=True)
    activity_date = fields.Date(string='Activity Date', default=datetime.today(), tracking=True)
    activity_id = fields.Many2one('provider.activity', string='Activity', tracking=True)
    company_id = fields.Many2one('res.company', 'Company', default=lambda self: self.env.user.company_id.id, index=1, tracking=True)
    up_id = fields.Many2one('res.partner', string='Up', tracking=True)
    # policy_id = fields.Many2one('policy.policy', string='Policy Number', tracking=True)
    policy_id = fields.Char(string='Policy Number', tracking=True)
    # policy_number = fields.Char(related='policy_id.policy_number', tracking=True)
    # policy_date = fields.Date(related='policy_id.policy_date', tracking=True)    
    policy_number = fields.Char(string='POLICY NUMBER', tracking=True)
    policy_date = fields.Date(string='POLICY DATE', tracking=True)    
    extension = fields.Integer(string='Extension', default=1, tracking=True)

    @api.onchange('extension')
    def _onchange_extension(self):
        if self.extension < 1:
            raise ValidationError(_("Extension cannot be empty"))
        else:
            pass    

    def int_to_roman(self, input):
        ints = (1000, 900,  500, 400, 100,  90, 50,  40, 10,  9,   5,  4,   1)
        nums = ('M',  'CM', 'D', 'CD','C', 'XC','L','XL','X','IX','V','IV','I')
         
        result = ""
        for i in range(len(ints)):
            count = int(input / ints[i])
            result += nums[i] * count
            input -= ints[i] * count
        return result

class ResPartner(models.Model):
    _inherit = 'res.partner'

    provider_count = fields.Integer(compute='_compute_provider_count', string='Providers')

    def _compute_provider_count(self):
        # retrieve all children partners and prefetch 'parent_id' on them
        for x in self:
            all_partners = x.with_context(active_test=False).search([('id', 'child_of', x.ids)])
            all_partners.read(['parent_id'])

            provider_groups = x.env['provider.provider'].read_group(
                domain=[('partner_id', 'in', all_partners.ids)],
                fields=['partner_id'], groupby=['partner_id']
            )
            partners = x.browse()
            for group in provider_groups:
                partner = x.browse(group['partner_id'][0])
                while partner:
                    if partner in x:
                        partner.provider_count += group['partner_id_count']
                        partners |= partner
                    partner = partner.parent_id
            (x - partners).provider_count = 0