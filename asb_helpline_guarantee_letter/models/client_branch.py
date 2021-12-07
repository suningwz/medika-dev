# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from datetime import date


class ClientBranch(models.Model):
    _inherit = 'client.branch'
    _description = 'Client Branch'

    @api.model
    def create(self, vals):
        result = super(ClientBranch, self).create(vals)
        for rec in result:
            self.create_report_gl_template(rec.id)
            return result

    def create_report_gl_template(self, rec_id):
        ##############################
        # CREATE TEMPLATE INITIAL GL #
        ##############################
        # create ir.ui.view
        template_initial = self.env['ir.ui.view'].sudo().search([('key', '=', 'asb_helpline_guarantee_letter.template_initial_gl')])
        view_initial = self.env['ir.ui.view'].sudo().create({
            'name': 'branch %s initial GL' % rec_id,
            'type': 'qweb',
            'key': 'gl_template.branch_%s_initial_gl' % (rec_id),
            'priority': 16,
            'active': True,
            'arch_updated': False,
            'mode': 'primary',
            'arch_base': template_initial.arch_base,
            'arch_db': template_initial.arch_db,
            'arch_prev': False,
        })
        # create ir.model.data
        self.env['ir.model.data'].sudo().create({
            'name': 'initial_gl_branch_%s' % rec_id,
            'module': 'gl_template',
            'model': 'ir.ui.view',
            'res_id': view_initial.id,
        })
        # create ir.actions.report
        paperformat_id = self.env['report.paperformat'].sudo().search([('name', '=', 'GL Template Format')])
        self.env['ir.actions.report'].sudo().create({
            'name': 'branch %s initial GL' % rec_id,
            'report_type': 'qweb-pdf',
            'paperformat_id': paperformat_id[0].id,
            'model': 'guarantee.letter',
            'report_name': 'gl_template.branch_%s_initial_gl' % (rec_id),
        })

        ##############################
        # CREATE TEMPLATE FINAL GL #
        ##############################
        # create ir.ui.view
        template_final = self.env['ir.ui.view'].sudo().search([('key', '=', 'asb_helpline_guarantee_letter.template_final_gl')])
        view_final = self.env['ir.ui.view'].sudo().create({
            'name': 'branch %s final GL' % rec_id,
            'type': 'qweb',
            'key': 'gl_template.branch_%s_final_gl' % (rec_id),
            'priority': 16,
            'active': True,
            'arch_updated': False,
            'mode': 'primary',
            'arch_base': template_final.arch_base,
            'arch_db': template_final.arch_db,
            'arch_prev': False,
        })

        # create ir.model.data
        self.env['ir.model.data'].sudo().create({
            'name': 'final_gl_branch_%s' % rec_id,
            'module': 'gl_template',
            'model': 'ir.ui.view',
            'res_id': view_final.id,
        })

        # create ir.actions.report
        paperformat_id = self.env['report.paperformat'].sudo().search([('name', '=', 'GL Template Format')])
        self.env['ir.actions.report'].sudo().create({
            'name': 'branch %s final GL' % rec_id,
            'report_type': 'qweb-pdf',
            'paperformat_id': paperformat_id[0].id,
            'model': 'guarantee.letter',
            'report_name': 'gl_template.branch_%s_final_gl' % (rec_id),
        })

    def update_initial_qweb(self):
        self.ensure_one()
        action_ref = self.env.ref('base.action_ui_view')
        name = 'branch %s initial GL' % self.id
        action_data = action_ref.read()[0]
        form_id = self.env['ir.ui.view'].search([('name', 'ilike', name), ('type', '=', 'qweb')])
        action_data['views'] = [(self.env.ref('base.view_view_form').id, 'form')]
        action_data['res_id'] = form_id.id
        return action_data

    def update_final_qweb(self):
        self.ensure_one()
        action_ref = self.env.ref('base.action_ui_view')
        name = 'branch %s final GL' % self.id
        action_data = action_ref.read()[0]
        form_id = self.env['ir.ui.view'].search([('name', 'ilike', name), ('type', '=', 'qweb')])
        action_data['views'] = [(self.env.ref('base.view_view_form').id, 'form')]
        action_data['res_id'] = form_id.id
        return action_data
