# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError


class IrUiView(models.Model):
    _inherit = 'ir.ui.view'
    _description = 'Ir Ui View'

    def print_view(self):
        action_name = self.name
        split = action_name.split(" ")
        if len(split) > 1:
            # client_id = int(split[0])
            client_id = split[0]
            client_branch_id = split[1]
            name_action = self.env['ir.actions.report'].sudo().search([('name', '=', action_name)])
            if split[2] == 'GL':
                letter = self.env['guarantee.letter'].sudo().search([('client_id', '=', int(client_id))])
                if not letter:
                    raise UserError('Create GL First')
                return name_action.report_action(letter.sorted('id')[0])
            elif split[2] == 'Member':
                partner = self.env['res.partner'].sudo().search([('member_client_id', '=', int(client_id))])
                if not partner:
                    raise UserError('Create Member First')
                return name_action.report_action(partner.sorted('id')[0])
            elif split[1] == 'Correspondence' and split[2] == 'Type':
                correspondence = self.env['correspondence.correspondence'].sudo().search([('type_id', '=', int(client_id))])
                if not correspondence:
                    raise UserError('Create Correspondence First')
                return name_action.report_action(correspondence.sorted('id')[0])
        if len(split) > 2:
            if split[3] == 'GL':
                letter = self.env['guarantee.letter'].sudo().search([('client_branch_id', '=', int(client_branch_id))])
                if not letter:
                    raise UserError('Create GL First')
                return name_action.report_action(letter.sorted('id')[0])
        if action_name == 'information_package_mcu':
            name_action = self.env['ir.actions.report'].sudo().search([('name', '=', 'Information Package MCU')])
            letter = self.env['list.package'].sudo().search([], limit=1)
            if not letter:
                    raise UserError('Package MCU not found')
            return name_action.report_action(letter.sorted('id')[0])
        if action_name == 'report_lmi':
            name_action = self.env['ir.actions.report'].sudo().search([('name', '=', 'LMI')])
            letter = self.env['guarantee.letter'].sudo().search([])
            if not letter:
                raise UserError('Create GL First')
            return name_action.report_action(letter.sorted('id')[0])
