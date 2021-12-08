# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from datetime import date
from odoo.exceptions import ValidationError, UserError


class ProviderContract(models.Model):
    _name = 'provider.contract'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
    _description = 'Provider Contract'
    _order = 'partner_id, id desc, remaining_contract_int desc'

    name = fields.Char(default='New_', tracking=True)
    partner_id = fields.Many2one('res.partner', string='Provider Name', required="1", tracking=True,)
    # pks = fields.Char(related='name', string='PKS No.', tracking=True)
    pks = fields.Char(string='PKS No.', tracking=True)
    start_date = fields.Date(string='Start Date', tracking=True, required=True, default=fields.Date.today())
    end_date = fields.Date(string='End Date', tracking=True, required=True, )

    created_date = fields.Date(string='Created Date', default=lambda self: fields.datetime.now(), required=True, tracking=True)
    created_by = fields.Many2one('res.users', string='Created By', default=lambda self: self.env.user.id, required=True, tracking=True)
    attachment_number = fields.Integer(compute='_compute_attachment_number', string='Documents')

    def _compute_attachment_number(self):
        attachment_data = self.env['ir.attachment'].read_group(
            [('res_model', '=', 'provider.contract'), ('res_id', 'in', self.ids)], ['res_id'], ['res_id'])
        attachment = dict((data['res_id'], data['res_id_count']) for data in attachment_data)
        for contract in self:
            contract.attachment_number = attachment.get(contract.id, 0)

    def action_get_attachment_view(self):
        res = self.env['ir.actions.act_window']._for_xml_id('asb_binary_newtab.action_attachment')
        res['domain'] = [('res_model', '=', 'provider.contract'), ('res_id', 'in', self.ids)]
        res['context'] = {'default_res_model': 'provider.contract', 'default_res_id': self.id}
        return res

    def new_tab(self):
        for rec in self:
            result = []
            attachment = self.env['ir.attachment'].search(
                [('res_model', '=', 'provider.contract'), ('res_id', 'in', self.ids)])
            if len(attachment) > 1:
                raise ValidationError(_("There are more than 1 attachment"))
            url = '/web/content/%s' % attachment.id
            return {
                'name': 'Open Attachment',
                'type': 'ir.actions.act_url',
                'target': 'new',
                'url': url
            }

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
        result = super(ProviderContract, self).create(vals)
        for rec in result:
            if not rec.partner_id.provider_code:
                raise UserError("Provider Code cannot be empty")
            rec.name = self.env['ir.sequence'].next_by_code('provider.contract') + rec.partner_id.provider_code + '/PKS/' + \
                str(self.int_to_roman(rec.created_date.month)) + '/' + str(rec.created_date.year)
            return result

    # state_contract = fields.Selection([
    #     ('inactive', 'Inactive'),
    #     ('active', 'Active'),
    # ], string='State Contract', default='active')

    state = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ], string='State', default='draft')

    def set_commit(self):
        for rec in self:
            last_contract = self.env['provider.contract'].search([('partner_id', '=', rec.partner_id.id), ('id', '!=', rec.id)]).sorted('id', reverse=True)
            if last_contract:
                if last_contract[0].state == 'active':
                    raise UserError("You can activate this contract after the previous contract is inactive.!")
            # if last_contract:
            #     last_contract[0].write({
            #         'state': 'inactive'
            #     })
            # if rec.start_date <= last_contract[0].end_date:
            #     raise UserError("Start Date cannot be less than or equal to the End Date of the previous Contract!")
            rec.state = 'active'
            rec.partner_id.write({
                'remaining_contract': rec.remaining_contract,
                'remaining_contract_int': rec.remaining_contract_int
            })

    @api.onchange('start_date', 'end_date')
    def _onchange_date(self):
        for rec in self:
            if rec.start_date and rec.end_date:
                x = (rec.end_date - rec.start_date).days
                if x < 0:
                    return {
                        'warning': {'title': 'Error!', 'message': 'End Date referenced before Start Date!'},
                        'value': {'end_date': None, }
                    }
                # else:
                #     active = (date.today() - rec.start_date).days
                #     terminate = (rec.end_date - date.today()).days
                #     if active < 0:
                #         rec.state_contract = 'inactive'
                #     elif active >= 0 and terminate >= 0:
                #         rec.state_contract = 'active'
                #     else:
                #         rec.state_contract = 'inactive'

    remaining_contract = fields.Char(string='Remaining Contract')
    remaining_contract_int = fields.Integer(compute='_compute_remaining_contract', string='Order Remaining Contract', store=True,)

    @api.depends('start_date', 'end_date')
    def _compute_remaining_contract(self):
        self.remaining_contract = False
        today = date.today()
        for rec in self:
            if rec.start_date and rec.end_date:
                rec.remaining_contract_int = (today - rec.end_date).days
                if rec.remaining_contract_int in (-1, 0, 1):
                    rec.remaining_contract = str(rec.remaining_contract_int) + ' day'
                else:
                    rec.remaining_contract = str(rec.remaining_contract_int) + ' days'

        contract_active = self.search([('state', '=', 'active')])
        for rec in contract_active:
            rec.partner_id.write({
                'remaining_contract': rec.remaining_contract,
                'remaining_contract_int': rec.remaining_contract_int
            })

    # @api.model
    # def update_provider(self):
    #     contract_active = self.search([('state', '=', 'active')])
    #     for rec in contract_active:
    #         rec.partner_id.write({
    #             'remaining_contract': rec.remaining_contract,
    #             'remaining_contract_int': rec.remaining_contract_int
    #         })

    @api.model
    def update_state(self):
        today = date.today()
        self.search([])._compute_remaining_contract()
        # self.search([]).update_provider()
        # self.search([('start_date', '<=', today), ('end_date', '>=', today)]).write({'state': 'active'})
        self.search([('end_date', '<', today)]).write({'state': 'inactive'})
    
        # Name Get
    def name_get(self):
        res = []
        for rec in self:
            res.append((rec.id, '%s - %s (%s)' % (rec.partner_id.name, rec.name, rec.state)))
        return res


class ResPartner(models.Model):
    _inherit = 'res.partner'

    provider_contract_count = fields.Integer(compute='_compute_provider_contract', string='Contract')

    def _compute_provider_contract(self):
        # retrieve all children partners and prefetch 'parent_id' on them
        for x in self:
            all_partners = x.with_context(active_test=False).search([('id', 'child_of', x.ids)])
            all_partners.read(['parent_id'])

            provider_contract_groups = x.env['provider.contract'].read_group(
                domain=[('partner_id', 'in', all_partners.ids)],
                fields=['partner_id'], groupby=['partner_id']
            )
            partners = x.browse()
            for group in provider_contract_groups:
                partner = x.browse(group['partner_id'][0])
                while partner:
                    if partner in x:
                        partner.provider_contract_count += group['partner_id_count']
                        partners |= partner
                    partner = partner.parent_id
            (x - partners).provider_contract_count = 0
