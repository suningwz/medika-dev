# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from datetime import date


class Partner(models.Model):
    _inherit = 'res.partner'

    benefit_limit_line = fields.One2many('member.benefit.limit', 'member_id', string='Benefit Limit')
    deductible_remaining_line = fields.One2many('member.deductible.remaining', 'member_id', string='Deductible Remaining')
    per_day_limit_line = fields.One2many('member.per.day.limit', 'member_id', string='Per Day Limit Remaining')

    # sum_utilized_limit = fields.Float(compute='compute_sum_utilized_limit', string='Sum all values of all records of the num field',)

    # @api.depends('name')
    # def compute_sum_utilized_limit(self):
    # fetch all records for your model and sum num field value
    # Iter on each records to set records_sum
    # self.sum_utilized_limit = 0
    # records_sum = sum(self.env["member.benefit.limit"].search([('member_id', '=', self.id)]).mapped('utilized_limit'))
    # if self.member:
    #     for rec in self:
    #         rec.sum_utilized_limit = records_sum

    def refresh_benefit(self):
        for rec in self:
            detail_lines = [(5, 0, 0)]
            deductible_lines = [(5, 0, 0)]

            # Get all member header
            for header in rec.program_plan_header_line:
                # Get all member detail
                for detail in header.detail_line:
                    detail_vals = {
                        'detail_id': detail.id,
                        'max_per_visit': detail.max_per_visit,
                        'max_day_per_year': detail.max_day_per_year,
                        'max_per_day': detail.max_per_day,
                        'inner_limit': detail.inner_limit,
                        'per_day_limit': detail.per_day_limit,
                        'currency_id': detail.currency_id.id,
                    }
                    detail_lines.append((0, 0, detail_vals))
                deductible_vals = {
                    'header_id': header.id,
                    'deductible': header.deductible,
                }
                deductible_lines.append((0, 0, deductible_vals))
            rec.benefit_limit_line = detail_lines
            rec.deductible_remaining_line = deductible_lines

            # Calculate benefit usage and limit for benefit_limit_line
            # Get Guarantee Letter for the same member
            gl = self.env['guarantee.letter'].search([('member_id', '=', self._origin.id), ('admission_date', '<=', self.end_policy_date), ('admission_date', '>=', self.effective_date_member)])
            benefit_daily_limit = []
            for benefit in rec.benefit_limit_line:
                total_days = 0
                total_visit = 0
                per_day_limit = 0
                utilized = 0
                remaining = benefit.inner_limit
                for letter in gl:
                    # Get final GL record for the same benefit
                    for line in letter.final_gl_line:
                        if line.detail_id == benefit.detail_id and line.real_cover_amount != 0:
                            utilized += line.real_cover_amount
                            if remaining != -1:
                                remaining -= line.real_cover_amount
                            # Check if day exceed max day per year
                            if benefit.max_day_per_year != -1:
                                # Utilized day per year
                                total_days += line.days
                            # Check if visit exceed max visit per day (DELETE)
                            if letter.admission_date == date.today():
                                if benefit.max_per_day != -1:
                                    total_visit += 1

                            # Check if visit exceed per day limit (ON PROGRESS)
                            if benefit.per_day_limit != -1:
                                per_day_limit += line.real_cover_amount
                                existing_limit = self.env['member.per.day.limit'].search(
                                    [('detail_id', '=', line.detail_id.id), ('service_date', '=', line.service_date), ('member_id', '=', rec._origin.id)])
                                if not existing_limit:
                                    rec.per_day_limit_line.create({
                                        'member_id': rec._origin.id,
                                        'service_date': line.service_date,
                                        'detail_id': line.detail_id.id,
                                        'per_day_limit': line.detail_id.per_day_limit,
                                        'max_per_day': line.detail_id.max_per_day,
                                        # 'per_day_limit_used' : line.real_cover_amount,
                                        # 'per_day_visit_used' : 1,
                                    })

                benefit.remaining_limit = remaining
                benefit.remaining_day = benefit.max_day_per_year - total_days

                benefit.utilized_limit = utilized
                benefit.utilized_day = total_days

            # Calculate remaining deductible
            for headers in rec.deductible_remaining_line:
                deductible_remaining = headers.header_id.deductible
                for letter in gl:
                    # Get final GL record for the same header
                    for line in letter.final_gl_line:
                        if line.detail_id in headers.header_id.detail_line:
                            deductible_remaining -= line.real_cover_amount
                if deductible_remaining < 0:
                    headers.deductible_remaining = 0
                else:
                    headers.deductible_remaining = deductible_remaining

            # Calculate per day limit  (ON PROGRESS)
            # already done in final gl
            # for limit in rec.per_day_limit_line:
            #     per_day_limit_used = 0
            #     for letter in gl:
            #         for line in letter.final_gl_line:
            #             if line.detail_id == limit.detail_id and line.service_date == limit.service_date:
            #                 if benefit.per_day_limit != -1:
            #                     existing_limit = self.env['member.per.day.limit'].search(
            #                         [('detail_id', '=', line.detail_id.id), ('service_date', '=', line.service_date), ('member_id', '=', rec._origin.id)])
            #                     if existing_limit:
            #                         per_day_limit_used += line.real_cover_amount
            #                         existing_limit.per_day_limit_used = per_day_limit_used

            for benefit in rec.benefit_limit_line:
                today_limit = self.env['member.per.day.limit'].search([('detail_id', '=', benefit.detail_id.id), ('service_date', '=', date.today()), ('member_id', '=', rec._origin.id)])
                benefit.remaining_limit_today = benefit.per_day_limit
                benefit.remaining_visit = benefit.max_per_day
                for limit in today_limit:
                    benefit.utilized_limit_today += limit.per_day_limit_used
                    benefit.remaining_limit_today -= limit.per_day_limit_used

                    benefit.utilized_visit += limit.per_day_visit_used
                    benefit.remaining_visit -= limit.per_day_visit_used

    def ticketing_member_limit(self):
        self.refresh_benefit()
        for benefit in self.benefit_limit_line:
            if benefit.max_per_visit not in [-1, 0]:
                benefit.member_ticketing_benefit_limit = benefit.max_per_visit
                benefit.member_ticketing_benefit_remarks = 'Max Per Visit'
            elif benefit.per_day_limit not in [-1, 0]:
                benefit.member_ticketing_benefit_limit = benefit.per_day_limit
                benefit.member_ticketing_benefit_remarks = 'Per Day Limit'
            # benefit.member_ticketing_benefit_usage = benefit.utilized_limit
            # benefit.member_ticketing_benefit_remaining_limit = benefit.remaining_limit

    def action_member_limit(self):
        self.refresh_benefit()
        res = self.env['ir.actions.act_window']._for_xml_id('asb_membership_member_limit.action_member_benefit_limit')
        res['context'] = {'active_id': self.id}
        return res


class MemberBenefitLimit(models.Model):
    _name = 'member.benefit.limit'
    _description = 'Member Benefit Limit'
    _rec_name = 'detail_id'

    member_id = fields.Many2one('res.partner', string='Member', ondelete='cascade')
    detail_id = fields.Many2one('header.detail', string='Benefit')
    max_per_day = fields.Integer(related="detail_id.max_per_day")
    max_day_per_year = fields.Integer(related="detail_id.max_day_per_year")
    max_per_visit = fields.Float(related="detail_id.max_per_visit")
    inner_limit = fields.Float(related="detail_id.inner_limit")
    per_day_limit = fields.Float(related="detail_id.per_day_limit")
    currency_id = fields.Many2one(related='detail_id.currency_id')
    company_id = fields.Many2one('res.company', 'Company', default=lambda self: self.env.user.company_id.id, index=1, tracking=True)

    remaining_day = fields.Integer(string='Remaining Day')
    remaining_visit = fields.Integer(string='Remaining Visit Today')
    remaining_limit = fields.Float(string='Remaining Inner Limit')
    remaining_limit_today = fields.Float(string='Remaining Limit Today')

    utilized_day = fields.Integer(string='Utilized Day')
    utilized_visit = fields.Integer(string='Utilized Visit Today')
    utilized_limit = fields.Float(string='Utilized Inner Limit')
    utilized_limit_today = fields.Float(string='Utilized Limit Today')

    member_ticketing_benefit_limit = fields.Float(string='Limit')
    member_ticketing_benefit_remarks = fields.Char(string='Remarks')

    @api.model
    def retrieve_membership_member_limit_dashboard(self, id=None):
        self.check_access_rights('read')
        if id:
            total_claim = sum(self.env['member.benefit.limit'].search([('member_id', '=', int(id))]).mapped('utilized_limit'))
            currency = self.env.company.currency_id.symbol
            res = {
                'total_claim': 0,
                'currency': currency,

            }
            res['total_claim'] = total_claim
            res['currency'] = currency
            return res


class MemberDeductibleRemaining(models.Model):
    _name = 'member.deductible.remaining'
    _description = 'Member Deductible Remaining'

    member_id = fields.Many2one('res.partner', string='Member', ondelete='cascade')
    header_id = fields.Many2one('program.plan.header', string='Header')
    deductible = fields.Float(string='Deductible')
    deductible_remaining = fields.Float(string='Deductible Remaining')


class MemberPerDayLimit(models.Model):
    _name = 'member.per.day.limit'
    _description = 'Member Per Day Limit'

    member_id = fields.Many2one('res.partner', string='Member', ondelete='cascade')
    service_date = fields.Date(string='Service Date')
    detail_id = fields.Many2one('header.detail', string='Detail')
    per_day_limit = fields.Float(related="detail_id.per_day_limit")
    per_day_limit_used = fields.Float(string="Per Day Used")
    max_per_day = fields.Integer(related="detail_id.max_per_day")
    per_day_visit_used = fields.Integer(string="Per Day Visit Remaining")
