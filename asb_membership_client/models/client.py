# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from datetime import date


class Client(models.Model):
    _inherit = 'res.partner'

    # def _compute_policy_count(self):
    #     for record in self:
    #         record.branch_count = self.env['policy.policy'].search_count([('client_id', '=', record.id)])

    def _compute_branch_count(self):
        for record in self:
            record.branch_count = self.env['client.branch'].search_count([('client_id', '=', record.id)])

    def _compute_client_activity(self):
        for record in self:
            record.client_activity_count = self.env['client.activity'].search_count([('client_id', '=', record.id)])

    client = fields.Boolean(string='Is Client')
    client_activity_count = fields.Integer(compute='_compute_client_activity', string='Activity')
    # member_line = fields.One2many('res.partner', 'parent_id', string='Member')
    # member_ids = fields.Many2many('res.partner','client_entity_member_rel','client_entity_id','entity_member_id', string='Member/Entity', tracking=True)
    client_provider_ids = fields.Many2many('res.partner', 'client_provider_rel', 'client_id', 'provider_id', string='Provider', tracking=True)
    client_branch_id = fields.Many2one('client.branch', string='Client Branch')
    s_condition = fields.Char(string='Spesial Condition', tracking=True,)
    diagnosis_ids = fields.Many2many('diagnosis.diagnosis', 'partner_id', string='Exclusion', tracking=True, ondelete='restrict')
    excess_charge = fields.Boolean(string='Excess Charge')
    front_card_member = fields.Binary(string='Front of Card Member')
    back_card_member = fields.Binary(string='Back of Card Member')
    effective_date = fields.Date(string='Effective Date', default=date.today(), tracking=True)
    expiry_date = fields.Date(string='Expiry Date', tracking=True)
    branch_count = fields.Integer(compute='_compute_branch_count', string='Branch')
    client_activity_count = fields.Integer(compute='_compute_client_activity', string='Activity')
    ref = fields.Char(string='SAP Code', index=True)
    sla_claim = fields.Integer(string='SLA Claim Reimbursement')
    claim_expiry_length = fields.Integer(string='Claim Expiry Length', tracking=True)
    cob_status = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No'),
    ], string='CoB Status')
    client_state = fields.Selection([
        ('draft', 'Draft'),
        ('enabled', 'Enabled'),
        ('disabled', 'Disabled'),
    ], string='Status', default='draft', tracking=True)

    @api.model
    def create(self, vals):
        result = super(Client, self).create(vals)
        for rec in result:
            num_id = rec.id
            if rec.client:
                self.create_ir_ui_view(num_id)
                self.create_ir_model_data(num_id)
                self.create_ir_actions_report(num_id)
            return result

    def create_ir_ui_view(self, num_id):
        view_id = self.env['ir.ui.view'].sudo().search([('name', '=', 'report_card_member'), ('xml_id', '=', 'asb_membership_member.report_card_member')])
        self.env['ir.ui.view'].sudo().create({
            'name': '%s Card Member' % num_id,
            'type': 'qweb',
            # 'key': '%d.%d' % (num_id, num_id),
            'key': '%s.card.member' % num_id,
            'priority': 16,
            'active': True,
            'arch_updated': False,
            'mode': 'primary',
            'arch_base': view_id.arch_db,
            'arch_db': view_id.arch_db,
            'arch_prev': False,
        })

    def create_ir_model_data(self, num_id):
        name = '%s Card Member' % num_id
        res_id = self.env['ir.ui.view'].sudo().search([('name', '=', name)])
        self.env['ir.model.data'].sudo().create({
            'name': '%s_Card_Member' % num_id,
            'module': num_id,
            'model': 'ir.ui.view',
            'res_id': res_id.id,
        })

    def create_ir_actions_report(self, num_id):
        paperformat_id = self.env['report.paperformat'].sudo().search([('name', '=', 'Card Member')])
        self.env['ir.actions.report'].sudo().create({
            'name': '%s Card Member' % num_id,
            'report_type': 'qweb-pdf',
            'paperformat_id': paperformat_id.id,
            'model': 'res.partner',
            # 'report_name': '%d.%d' % (num_id, num_id),
            'report_name': '%s.card.member' % num_id,
        })

    # def update_template(self):
    #     self.ensure_one()
    #     action_ref = self.env.ref('base.action_ui_view')
    #     # if not action_ref or len(self.report_name.split('.')) < 2:
    #     # return False
    #     name = '%s Card Member' % self.id
    #     action_data = action_ref.read()[0]
    #     action_data['domain'] = [('name', '=', name), ('type', '=', 'qweb')]
    #     return action_data

    def update_template(self):
        """Used in the ir.actions.report form view in order to search naively after the view(s)
        used in the rendering.
        """
        self.ensure_one()
        action_ref = self.env.ref('base.action_ui_view')
        name = '%s Card Member' % self.id
        action_data = action_ref.read()[0]
        form_id = self.env['ir.ui.view'].search([('name', 'ilike', name), ('type', '=', 'qweb')])
        action_data['views'] = [(self.env.ref('base.view_view_form').id, 'form')]
        action_data['res_id'] = form_id.id
        return action_data

    def action_client_enable(self):
        for client in self:
            client.client_state = 'enabled'

    def action_client_disable(self):
        for client in self:
            client.client_state = 'disabled'

    def action_client_draft(self):
        for client in self:
            client.client_state = 'draft'

    state_id = fields.Many2one('res.country.state', "State", domain="[('country_id','=',country_id)]")
    city_id = fields.Many2one('res.state.city', 'Kabupaten', domain="[('state_id','=',state_id)]")
    kecamatan_id = fields.Many2one('res.city.kecamatan', 'Kecamatan', domain=[('city_id', '=', 'city_id')])
    kelurahan_id = fields.Many2one('res.kecamatan.kelurahan', 'Kelurahan', domain="[('kecamatan_id','=',kecamatan_id)]")

    @api.onchange('country_id')
    def _onchange_country_id(self):
        for rec in self:
            if rec.country_id != rec.state_id.country_id:
                rec.state_id = False

    @api.onchange('state_id')
    def _onchange_state_id(self):
        for rec in self:
            if rec.city_id != rec.city_id.state_id:
                rec.city_id = False

    @api.onchange('city_id')
    def _onchange_city_id(self):
        for rec in self:
            if rec.kecamatan_id != rec.kecamatan_id.city_id:
                rec.kecamatan_id = False

    @api.onchange('kecamatan_id')
    def _onchange_kecamatan_id(self):
        for rec in self:
            if rec.kelurahan_id != rec.kelurahan_id.kecamatan_id:
                rec.kelurahan_id = False
