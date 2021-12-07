# -*- coding: utf-8 -*-

from odoo import api, fields, models, exceptions, _
from datetime import datetime, date
from odoo.exceptions import UserError, ValidationError


class CorrespondenceType(models.Model):
    _name = 'correspondence.type'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
    _description = 'Correspondence Type'

    name = fields.Char(string='Correspondence Type', tracking=True)
    ttd = fields.Image(string='Signature', tracking=True, max_width=120, max_height=120)
    ttd_name = fields.Char(string='Signee', tracking=True)
    title = fields.Char(string='Title', tracking=True)

    def associated_view_correspondence(self):
        correspondence = self.env['correspondence.correspondence'].sudo().search([('type_id', '=', self.id)])
        if not correspondence:
            raise UserError("Create Correspondence with Format of Latter '%s' First!" % self.name)
        self.ensure_one()
        action_ref = self.env.ref('base.action_ui_view')
        report_name = '%s Correspondence Type' % self.id
        action_data = action_ref.read()[0]
        form_id = self.env['ir.ui.view'].search([('name', 'ilike', report_name), ('type', '=', 'qweb')])
        action_data['views'] = [(self.env.ref('base.view_view_form').id, 'form')]
        action_data['res_id'] = form_id.id
        return action_data

    @api.model
    def create(self, vals):
        result = super(CorrespondenceType, self).create(vals)
        for rec in result:
            num_id = rec.id
            self.create_ir_ui_view(num_id)
            self.create_ir_model_data(num_id)
            self.create_ir_actions_report(num_id)
            return result

    def create_ir_ui_view(self, num_id):
        view_id = self.env['ir.ui.view'].sudo().search([('name', '=', 'report_correspondence_type'), ('xml_id', '=', 'asb_master_provider_correspondence.report_correspondence_type')])
        self.env['ir.ui.view'].sudo().create({
            'name': '%s Correspondence Type' % num_id,
            'type': 'qweb',
            'key': '%s.correspondence.type' % num_id,
            'priority': 16,
            'active': True,
            'arch_updated': False,
            'mode': 'primary',
            'arch_base': view_id.arch_db,
            'arch_db': view_id.arch_db,
            'arch_prev': False,
        })

    def create_ir_model_data(self, num_id):
        name = '%s Correspondence Type' % num_id
        res_id = self.env['ir.ui.view'].sudo().search([('name', '=', name)])
        self.env['ir.model.data'].sudo().create({
            'name': '%s_Correspondence_Type' % num_id,
            'module': num_id,
            'model': 'ir.ui.view',
            'res_id': res_id.id,
        })

    def create_ir_actions_report(self, num_id):
        self.env['ir.actions.report'].sudo().create({
            'name': '%s Correspondence Type' % num_id,
            'report_type': 'qweb-pdf',
            'model': 'correspondence.correspondence',
            'report_name': '%s.correspondence.type' % num_id,
            'paperformat_id': self.env.ref('asb_master_provider_correspondence.report_correspondence_format').id
        })

    def add_correspondence(self):
        form_view = [(self.env.ref('asb_master_provider_correspondence.correspondence_form').id, 'form')]
        res = self.env['ir.actions.act_window']._for_xml_id('asb_master_provider_correspondence.correspondence_action')
        res['context'] = {'default_type_id': self.id}
        res['view_mode'] = 'form'
        res['views'] = form_view
        res['domain'] = False
        return res
