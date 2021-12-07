# -*- coding: utf-8 -*-

from odoo import api, fields, models, exceptions, _
from datetime import datetime, date
from odoo.exceptions import UserError, ValidationError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    correspondence_count = fields.Integer(compute='_compute_correspondence_count', string='Correspondence')

    def _compute_correspondence_count(self):
        # retrieve all children partners and prefetch 'parent_id' on them
        for x in self:
            all_partners = x.with_context(active_test=False).search([('id', 'child_of', x.ids)])
            all_partners.read(['parent_id'])

            provider_groups = x.env['correspondence.correspondence'].read_group(
                domain=[('partner_id', 'in', all_partners.ids)],
                fields=['partner_id'], groupby=['partner_id']
            )
            partners = x.browse()
            for group in provider_groups:
                partner = x.browse(group['partner_id'][0])
                while partner:
                    if partner in x:
                        partner.correspondence_count += group['partner_id_count']
                        partners |= partner
                    partner = partner.parent_id
            (x - partners).correspondence_count = 0
