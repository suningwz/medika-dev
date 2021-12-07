# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import date, datetime, timedelta
from odoo.exceptions import UserError


class GuaranteeLetter(models.Model):
    _inherit = 'guarantee.letter'
    _description = 'Guarantee Letter'

    @api.model
    def retrieve_eclaim_finance_dashboard(self):
        self.check_access_rights('read')
        so_pr_pending = self.search_count(['|', '|', ('so_number', '=', False), ('pr_number', '=', False), ('so_pr_date', '=', False), ('batch_approve', '=', True)])
        ar_pending = self.search_count(['|', ('ar_number', '=', False), ('ar_remarks', '=', False), ('batch_approve', '=', True)])
        po_pr_pending = self.search_count(['|', ('po_number', '=', False), ('po_remarks', '=', False), ('batch_approve', '=', True)])
        ap_pr_pending = self.search_count(['|', ('ap_number', '=', False), ('ap_remarks', '=', False), ('batch_approve', '=', True)])
        res = {
            "total_so_pr_pending": 0,
            "total_ar_pending": 0,
            "total_po_pending": 0,
            "total_ap_pending": 0,
        }
        res['total_so_pr_pending'] = so_pr_pending
        res['total_ar_pending'] = ar_pending
        res['total_po_pending'] = po_pr_pending
        res['total_ap_pending'] = ap_pr_pending
        return res

    so_number = fields.Char(string='Sales Order Number', tracking=True)
    pr_number = fields.Char(string='Purchase Requisition Number', tracking=True)
    so_pr_date = fields.Datetime(string='SO PR Date', tracking=True)

    ar_number = fields.Char(string='Account Receivable Number', tracking=True)
    ar_remarks = fields.Text(string='Remarks AR Team', tracking=True)

    po_number = fields.Char(string='Purchase Order Number', tracking=True)
    po_remarks = fields.Text(string='Remarks Procurement Team', tracking=True)

    ap_number = fields.Char(string='Account Payable Number', tracking=True)
    ap_remarks = fields.Text(string='Remarks AP Team', tracking=True)

    def paid(self):
        for rec in self:
            if not rec.ap_number:
                raise UserError('Input AP Number First!')
            elif not rec.ap_remarks:
                raise UserError('Input AP Remarks First!')
            else:
                rec.claim_status = 'paid'

    finance_due_date = fields.Integer(compute='_compute_finance_due_date', string='Due Date', store=True)
    finance_due_date_str = fields.Char(string='Due Date')

    @api.depends('admission_date','provider_id.top')
    def _compute_finance_due_date(self):
        for rec in self:
            if rec.service_type == 'cashless':
                if rec.admission_date and rec.provider_id.top:
                    due_date = rec.admission_date + timedelta(days=rec.provider_id.top)
                    rec.finance_due_date = (date.today() - due_date).days
                    if rec.provider_id.top_type == 'working_days':
                        start_date = date.today()
                        end_date = rec.finance_due_date
                        weekend = 1
                        while weekend:
                            weekend = 0
                            for day in range(abs(end_date)):
                                if start_date < due_date:
                                    start_date += timedelta(days=1)
                                if start_date.isoweekday() in [6,7]:
                                    due_date += timedelta(days=1)
                                    weekend += 1
                            print("start_date",start_date)
                            print("due_date",due_date)
                            print(rec.finance_due_date)
                            rec.finance_due_date = (date.today() - due_date).days
                            end_date = (start_date - due_date).days

                        start_date = date.today()
                        end_date = rec.finance_due_date
                        holiday = 1
                        while holiday:
                            timeoff = []
                            holiday = 0
                            holidays_ids = self.env['hr.holidays.public.line'].search([('date','>=',start_date),('date','<=',due_date)])
                            for record in holidays_ids:
                                timeoff.append(record.date)
                            for day in range(abs(end_date)):
                                start_date += timedelta(days=1)
                                if start_date in timeoff and start_date.isoweekday() not in [6,7]:
                                    due_date += timedelta(days=1)
                                    holiday += 1
                            rec.finance_due_date = (date.today() - due_date).days
                            end_date = (start_date - due_date).days

            if rec.service_type == 'reimburse':
                if rec.admission_date:
                    due_date = rec.admission_date + timedelta(days=5)
                    difference = date.today() - due_date
                    rec.finance_due_date = difference.days
            rec.finance_due_date_str = '%s' % rec.finance_due_date
            if rec.finance_due_date > 0:
                rec.finance_due_date_str = '+%s' % rec.finance_due_date
            if not rec.finance_due_date:
                rec.finance_due_date = False

    # @api.onchange('admission_date')
    # def _onchange_invoice_date(self):
    #     if self.admission_date and self.provider_id.top:
    #         self.invoice_date_due = self.invoice_date + timedelta(days=self.provider_id.top)
