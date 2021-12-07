# -*- coding: utf-8 -*-
import re
from odoo import models, fields, api, _
from datetime import date, datetime
from odoo.exceptions import UserError, ValidationError

import qrcode
import base64
from io import BytesIO


class ResPartner(models.Model):
    _inherit = 'res.partner'
    # remove sql constraint for item code in res partner use Check(1=1)
    _sql_constraints = [
        ('item_code_uniq', 'Check(1=1)', 'Provider code must be uniq!'),
    ]
    # _order = 'remaining_contract, remaining_contract_int desc'

    provider_state = fields.Selection([
        ('draft', 'Draft'),
        ('enabled', 'Enabled'),
        ('disabled', 'Disabled'),
    ], string='Status', default='draft', tracking=True)

    provider = fields.Boolean(string='Is Provider')
    provider_type = fields.Selection([
        ('non', 'Non Provider'),
        ('provider', 'Provider'),
    ], string='Provider Type', default='non', store=True)
    provider_code = fields.Char(string='Provider Code', tracking=True)
    edc_number = fields.Char(string='EDC Number', tracking=True)
    qr_code_name = fields.Char(string='QR Code Name', tracking=True)
    qr_code = fields.Image(max_width=192, max_height=192, compute='_compute_qr_code', store=True, tracking=True)
    finance_marketing = fields.Selection([
        ('none', 'None'),
        ('finance', 'Finance'),
        ('marketing', 'Marketing'),
    ], string='Finance/Marketing')
    is_pic = fields.Boolean()
    provider_facility_line_ids = fields.One2many('provider.facility.line', 'partner_id', string='Facility Line', tracking=True)

    bank_id = fields.Many2one('bank.master', string='Bank')
    swift_code = fields.Char(string='SWIFT code', tracking=True)
    bank_account = fields.Char(string='Bank Account', tracking=True)
    bank_branch = fields.Char(string='Bank Branch', tracking=True)
    account_name = fields.Char(string='Account Name', tracking=True)
    provider_join_date = fields.Date(string='Provider Join Date', tracking=True, store=True)

    provider_join_date_month = fields.Char(compute='_compute_provider_join_date_month', string='Provider Join Date Month', store=True,)
    
    @api.depends('provider_join_date')
    def _compute_provider_join_date_month(self):
        self.provider_join_date_month = False
        for rec in self:
            if rec.provider and rec.provider_join_date:
                rec.provider_join_date_month = rec.provider_join_date.month
                    

    provider_join_date_year = fields.Char(compute='_compute_provider_join_date_year', string='Provider Join Date Year', store=True,)
    
    @api.depends('provider_join_date')
    def _compute_provider_join_date_year(self):
        self.provider_join_date_year = False
        for rec in self:
            if rec.provider and rec.provider_join_date:
                rec.provider_join_date_year = rec.provider_join_date.year
                    


    # @api.constrains('provider_code')
    # def check_name(self):
    #     for rec in self:
    #         if rec.provider:
    #             if not rec.provider_code:
    #                 raise UserError('Provider Code cannot be empty')

    # @api.onchange('provider_code')
    # def _onchange_provider_code(self):
    #     if not self.provider_code:
    #         self.provider_code = ''
    #     val = str(self.provider_code)
    #     self.provider_code = val.upper().replace(" ", "")
    # for rec in self:
    #     text = rec.provider_code.title()
    #     text = text.title()
    #     for code in text:
    #         if not code.isupper():
    #             text = text.replace(code, '')
    #     if rec.provider_code[0] == 'R' or 'r' and rec.provider_code[1] == 'S' or 's':
    #         text = text[1:]
    #         text = 'RS' + text
    #     rec.provider_code = text

    @api.depends('qr_code_name', 'name')
    def _compute_qr_code(self):
        for rec in self:
            if rec.qr_code_name:
                qr = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                    box_size=10,
                    border=4,
                )

                qr.add_data(rec.qr_code_name)
                qr.make(fit=True)
                img = qr.make_image()
                tmp = BytesIO()
                img.save(tmp, format="PNG")
                qr_img = base64.b64encode(tmp.getvalue())
                rec.qr_code = qr_img
            else:
                rec.qr_code = False

            # Create provider code
            if rec.name and rec.provider:
                if not rec.provider_code:
                    text = rec.name.title()
                    text = text.title()
                    for code in text:
                        if not code.isupper():
                            text = text.replace(code, '')
                    if len(rec.name) > 1:
                        if rec.name[0] in ('R', 'r') and rec.name[1] in ('S', 's'):
                            text = text[1:]
                            text = 'RS' + text
                    rec.provider_code = text
                if not rec.provider_join_date:
                    rec.provider_join_date = fields.Date.today()
                if not rec.provider_type:
                    rec.provider_type = "non"
                if rec.provider_type == 'provider':
                    # history = self.env['history.join']
                    # create_history = history.create({
                    #     'partner_id': rec.id,
                    #     'provider_join_date': rec.provider_join_date,
                    # })
                    history_join = []
                    value = {
                        'partner_id': rec.id,
                        'provider_join_date': rec.provider_join_date,
                    }
                    history_join.append((0, 0, value))
                    rec.history_join_line = history_join



    @api.model
    def check_condition_show_dialog(self, record_id, data_changed):
        if data_changed.get('provider_code'):
            check_provider_code = self.env['res.partner'].search([('provider_code', '=', data_changed['provider_code'])])
            for rec in check_provider_code:
                if rec.edit:
                    if len(check_provider_code) > 1:
                        return True
                    elif len(check_provider_code) == 1:
                        if rec.id == record_id:
                            return False
                        else:
                            return True
                if rec.edit == False and check_provider_code:
                    return True
        else:
            return False

    @api.onchange('name')
    def _onchange_name(self):
        for rec in self:
            if rec.name and rec.provider:
                text = rec.name.title()
                text = text.title()
                for code in text:
                    if not code.isupper():
                        text = text.replace(code, '')
                if len(rec.name) > 1:
                    if rec.name[0] in ('R', 'r') and rec.name[1] in ('S', 's'):
                        text = text[1:]
                        text = 'RS' + text
                rec.provider_code = text

    @api.onchange('qr_code_name')
    def _onchange_qr_code_name(self):
        if self.qr_code_name:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )

            qr.add_data(self.qr_code_name)
            qr.make(fit=True)
            img = qr.make_image()
            tmp = BytesIO()
            img.save(tmp, format="PNG")
            qr_img = base64.b64encode(tmp.getvalue())
            self.qr_code = qr_img
        else:
            self.qr_code = False

    def create_all_be_yes(self):
        for rec in self.provider_facility_line_ids:
            rec.is_yes = True
            rec.is_no = False

    def create_all_be_no(self):
        for rec in self.provider_facility_line_ids:
            rec.is_no = True
            rec.is_yes = False

    @api.model
    def default_get(self, fields):
        res = super(ResPartner, self).default_get(fields)
        provider_facility_line_ids = []
        facility_rec = self.env['provider.facility'].search([])
        for pro in facility_rec:
            line = (0, 0, {
                'facility_id': pro.id
            })
            provider_facility_line_ids.append(line)
        res.update({
            'provider_facility_line_ids': provider_facility_line_ids
        })
        return res

    def action_provider_enable(self):
        for provider in self:
            provider.provider_state = 'enabled'

    def action_provider_disable(self):
        for provider in self:
            provider.provider_state = 'disabled'

    def action_provider_draft(self):
        for provider in self:
            provider.provider_state = 'draft'

    pic_title_id = fields.Many2one('pic.title', string='PIC Title', tracking=True, ondelete='cascade')
    tid_information_line = fields.One2many('tid.information', 'partner_id', string='TID Information', tracking=True)
    rebate_discount = fields.Selection([
        ('rebate', 'Rebate'),
        ('discount', 'Discount'),
    ], string='Rebate/Discount', tracking=True)
    top = fields.Integer(string='TOP (days)', tracking=True)
    top_type = fields.Selection([
        ('working_days', 'Working Days'),
        ('calendar', 'Calendar')
    ], string='TOP Type', tracking=True)
    provider_sap_code = fields.Char(string='SAP Code (Provider)', tracking=True)
    provider_category = fields.Selection([
        ('apotik', 'Apotik'),
        ('klinik', 'Klinik'),
        ('lab', 'Laboratorium'),
        ('optik', 'Optik'),
        ('rs', 'RS'),
    ], string='Provider Category')

    @api.constrains('provider_sap_code')
    def check_name(self):
        for rec in self:
            if rec.provider:
                if rec.provider_sap_code:
                    if not rec.provider_sap_code.isdigit():
                        raise UserError('[%s] Input number only for SAP Code' % rec.name)

    edit = fields.Boolean(string='Edit', default=False)

    @api.model
    def create(self, vals):
        res = super(ResPartner, self).create(vals)
        res.update({
            'edit': True
        })
        return res

    id_char = fields.Char(compute='_compute_id_char', string='Provider ID', store=True,)

    @api.depends('name')
    def _compute_id_char(self):
        for rec in self:
            rec.id_char = str(rec._origin.id)

    remaining_contract = fields.Char(string='Remaining Contract', store=True,)
    remaining_contract_int = fields.Integer(string='Order Remaining Contract', default=-999999999)

    history_join_line = fields.One2many('history.join', 'partner_id', string='History Join Line')
    history_finished_line = fields.One2many('history.finished', 'partner_id', string='History Join Finished')

    def set_to_non_provider(self):
        for rec in self:
            rec.provider_type = 'non'
            rec.provider_join_date = fields.Date.today()
            # history = self.env['history.finished']
            # create_history = history.create({
            #     'partner_id': rec.id,
            #     'provider_finished_date': rec.provider_join_date,
            # })

            history_finished = []
            value = {
                'partner_id': rec.id,
                'provider_finished_date': rec.provider_join_date,
            }
            history_finished.append((0, 0, value))
            rec.history_finished_line = history_finished

    def set_to_provider(self):
        for rec in self:
            rec.provider_type = 'provider'
            rec.provider_join_date = fields.Date.today()
            # history = self.env['history.join']
            # create_history = history.create({
            #     'partner_id': rec.id,
            #     'provider_join_date': rec.provider_join_date,
            # })

            history_join = []
            value = {
                'partner_id': rec.id,
                'provider_join_date': rec.provider_join_date,
            }
            history_join.append((0, 0, value))
            rec.history_join_line = history_join
