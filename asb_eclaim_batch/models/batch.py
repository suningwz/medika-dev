# -*- coding: utf-8 -*-

# import odoo.exceptions
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import date, timedelta

class EclaimBatch(models.Model):
    _name = 'eclaim.batch'
    _description = 'Eclaim Batch'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
    _rec_name = 'batch_number'

    batch_number = fields.Char(string='Batch Number')
    receive_date = fields.Date(string='Date Received')
    payment_date = fields.Date(string='Date of Payment')
    invoice_number = fields.Char(string='Invoice Number')
    provider_id = fields.Many2one('res.partner', string='Provider', domain=[('provider', '=', True)])
    client_id = fields.Many2one('res.partner', string='Client Name', domain=[('client', '=', True)])
    member_id = fields.Many2one('res.partner', string='Member Name')
    total_claim = fields.Float(string='Total Claim')
    total_charge = fields.Float(string='Total Charge')
    administration_charge = fields.Float(string='Administration Charge')
    # invoice_detail_line = fields.One2many('eclaim.invoice.detail', 'batch_id', string='Claim Analyst')
    letter_ids = fields.Many2many('guarantee.letter', string='Claim Analyst')
    currency_id = fields.Many2one('res.currency', 'Currency', default=lambda self: self.env.user.company_id.currency_id.id, required=True, tracking=True)
    claim_type = fields.Selection([
        ('cashless', 'Cashless'),
        ('reimburse', 'Reimbursement'),
    ], string='Claim Type')
    client_type = fields.Selection([
        ('member', 'Member'),
        ('non_member', 'Nonmember'),
    ], string='Client Type')
    payment = fields.Selection([
        ('provider', 'Provider'),
        ('member', 'Member'),
    ], string='Payment to')
    state = fields.Selection([
        ('open', 'Open'),
        ('approved', 'Approved'),
        ('paid', 'Paid'),
    ], string='Status', default='open')

    due_date = fields.Integer(compute='_compute_due_date', string='Due Date (date)', store=True)
    due_date_str = fields.Char(string='Due Date')
    check_percentage = fields.Float(compute='_compute_check_percentage', string='Checker Percentage')
    
    @api.depends('letter_ids')
    def _compute_check_percentage(self):
        for rec in self:
            checker_count = 0
            for line in rec.letter_ids:
                if line.checker_flagging:    
                    checker_count += 1
            if rec.letter_ids:
                rec.check_percentage = checker_count / len(rec.letter_ids)
            else:
                rec.check_percentage = 0
    
    @api.depends('provider_id.top','client_id','claim_type','client_id.sla_claim','receive_date')
    def _compute_due_date(self):
        for rec in self:
            if rec.claim_type == 'cashless':
                if rec.provider_id.top and rec.receive_date:
                    due_date = rec.receive_date + timedelta(days=rec.provider_id.top)
                    rec.due_date = (date.today() - due_date).days
                    if rec.provider_id.top_type == 'working_days':
                        start_date = date.today()
                        end_date = rec.due_date
                        weekend = 1
                        while weekend:
                            weekend = 0
                            for day in range(abs(end_date)):
                                if start_date < due_date:
                                    start_date += timedelta(days=1)
                                if start_date.isoweekday() in [6,7]:
                                    due_date += timedelta(days=1)
                                    weekend += 1
                            rec.due_date = (date.today() - due_date).days
                            end_date = (start_date - due_date).days

                        start_date = date.today()
                        end_date = rec.due_date
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
                            rec.due_date = (date.today() - due_date).days
                            end_date = (start_date - due_date).days

            if rec.claim_type == 'reimburse':
                if rec.receive_date and rec.client_id.sla_claim:
                    due_date = rec.receive_date + timedelta(days=rec.client_id.sla_claim)
                    difference = date.today() - due_date
                    rec.due_date = difference.days
            rec.due_date_str = '%s' % rec.due_date
            if rec.due_date > 0:
                rec.due_date_str = '+%s' % rec.due_date
            if not rec.due_date:
                rec.due_date = False
    
    def update_due_date(self):
        batch = self.env['eclaim.batch'].search([('state','!=','paid')])
        for rec in batch:
            rec._compute_due_date()

    @api.model
    def create(self, vals):
        if vals.get('claim_type') == 'cashless':
            vals['batch_number'] = 'BATCH/C/' + self.env['ir.sequence'].next_by_code('eclaim.batch')
        if vals.get('claim_type') == 'reimburse':
            vals['batch_number'] = 'BATCH/R/' + self.env['ir.sequence'].next_by_code('eclaim.batch')
        return super(EclaimBatch, self).create(vals)

    def search_gl(self):
        action = self.env['ir.actions.act_window']._for_xml_id('asb_eclaim_batch.search_guarantee_letter_action')
        action['domain'] = [('id', 'in', self.letter_ids.ids)]
        action['context'] = "{'no_breadcrumbs': True}"
        action['target'] = "new"
        return action
    
    def action_approve(self):
        for rec in self:
            letter = []
            for line in rec.letter_ids:
                if line.claim_status not in ['completed','reject','decline']:
                    letter.append("%s" % line.claim_number)
                line.batch_approve = True
                line.claim_status = 'approved'
            if letter:
                warning = str(letter).replace("'",'')
                raise ValidationError (_("Claim is not completed for %s") % warning[1:-1])
        return self.write({'state': 'approved'})
