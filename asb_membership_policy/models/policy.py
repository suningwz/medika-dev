# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from datetime import datetime, date
from odoo.exceptions import UserError, ValidationError

class PolicyPolicy(models.Model):
    _name = 'policy.policy'
    _description = 'Policy'    
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
    _rec_name ='policy_number'

    def _compute_member_count(self):
        for record in self:
            record.member_count = self.env['res.partner'].search_count([('policy_id', '=', self.id)])
    
    partner_id = fields.Many2one('res.partner', string='Partner')
    client_id = fields.Many2one('res.partner', string='Client Name', domain=[('client','=',True)], tracking=True)
    member_line = fields.One2many('policy.member.line', 'policy_id', string='Members', ondelete="cascade", tracking=True)
    policy_date = fields.Date(string='Policy Date', tracking=True)
    policy_number = fields.Char(string='Policy Number', tracking=True)
    effective_date = fields.Date(string='Effective Date', tracking=True)
    expired_date = fields.Date(string='Expired Date', tracking=True)
    request_date = fields.Date(string='Request Date', tracking=True)
    term_condition = fields.Binary(string='Terms & Conditions', tracking=True)
    notes = fields.Text(string='Notes', tracking=True)
    member_count = fields.Integer(compute='_compute_member_count', string='Member')

    state = fields.Selection([
        ('inactive', 'Inactive'),
        ('active', 'Active'),
    ], string='Status', default='inactive')
    policy_type = fields.Selection([
        ('aso', 'ASO'),
        ('tpa', 'TPA'),
        ('insurance', 'Insurance'),
        ('indemnity', 'Indemnity'),
        ('managed', 'Managed Care'),
    ], string='Policy Type')
    card_type = fields.Selection([
        ('show', 'Show Card'),
        ('swipe', 'Swipe Card'),
    ], string='Card Type')

    @api.model
    def create(self, vals):
        vals['policy_number'] = self.env['ir.sequence'].next_by_code(
            'policy.policy')
        return super(PolicyPolicy, self).create(vals)

    @api.model
    def update_state(self):
        current_date = date.today()
        self.search([('effective_date', '<=', current_date),('expired_date', '>=', current_date)]).write({'state': 'active'})
        self.search(['|',('effective_date', '>', current_date),('expired_date', '<', current_date)]).write({'state': 'inactive'})

    @api.onchange('effective_date','expired_date','client_id')
    def _onchange_effective_date(self):
        for x in self:
            current_date = date.today()
            current_id = ((str(x.id))[6:])
            if x.effective_date and x.expired_date:
                # if self.effective_date > self.expired_date or self.expired_date < self.effective_date:
                #         raise ValidationError(_("Effective date does not match with expired date."))
                if x.effective_date <= current_date and x.expired_date >= current_date:
                    for rec in x.search([]):
                        if x.partner_id == rec.partner_id and rec.state == 'active' and rec.id != current_id:
                            raise ValidationError(_("Another active policy for this group already exist."))
                    x.write({'state': 'active'})
                else:
                    x.write({'state': 'inactive'})

    def action_duplicate(self):
        self.ensure_one()
        policy_copy = self.copy()
        if policy_copy:
            context = dict(self.env.context)
            context['form_view_initial_mode'] = 'edit'
            return {
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'res_model': 'policy.policy',
                'res_id': policy_copy.id,
                'context': context,
            }
        return False

class PolicyMemberLine(models.Model):
    _name = 'policy.member.line'
    _description = 'Policy Member Line'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
    _rec_name = 'member_id'
    
    policy_id = fields.Many2one('policy.policy', string='Policy')
    member_id = fields.Many2one('res.partner', string='Member', domain=[('member','=',True)], tracking=True)
    # product_id = fields.Many2one('master.product', string='Product', tracking=True)
    state = fields.Selection([
        ('inactive', 'Inactive'),
        ('active', 'Active'),
    ], string='Status', default='inactive', tracking=True)

    def write(self, vals):
        res = super().write(vals)
        for rec in self:
            if vals.get('state') :
                message = "Update member: %s" % (rec.member_id.name)
                rec.policy_id.message_post(body=message)
        return res

    def unlink(self):
        for rec in self:
                message = "Remove member: %s" % (rec.member_id.name)
                rec.policy_id.message_post(body=message)
        return super().unlink()

# class PolicyProductLine(models.Model):
#     _name = 'policy.product.line'
#     _description = 'Policy Product Line'
    
#     name = fields.Char(string='Products')
#     policy_id = fields.Many2one('policy.policy', string='Policy')
#     master_product_id = fields.Many2one('master.product', string='Product')
#     product_code = fields.Char(string='Product Code', related='master_product_id.product_code')
#     product_type = fields.Char(string='Product Type', related='master_product_id.product_type')
#     product_status = fields.Selection([
#         ('key', 'value')
#     ], string='Product Status', related='master_product_id.product_status')
