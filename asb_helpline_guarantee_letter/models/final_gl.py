from odoo import models, fields, api, _
from datetime import date, timedelta
from odoo.exceptions import ValidationError

class FinalGL(models.Model):
    _name = 'final.gl'
    _description = 'Final GL'
    _rec_name = 'detail_id'

    @api.model
    def create(self,vals):
        res = super(FinalGL, self).create(vals)
        this_line_per_day_limit = self.env['member.per.day.limit'].search([('final_gl_id','=',False)])
        if this_line_per_day_limit:
            for rec in this_line_per_day_limit:
                rec.unlink()
        return res

    def write(self, vals):
        res = super(FinalGL, self).write(vals)
        this_line_per_day_limit = self.env['member.per.day.limit'].search([('final_gl_id','=',False)])
        if this_line_per_day_limit:
            for rec in this_line_per_day_limit:
                rec.unlink()
        return res

    def action_view(self):
        for rec in self:
            rec.letter_id.final_gl_benefit = rec.detail_id.benefit_id.name
            rec.letter_id.final_gl_max_per_visit = rec.detail_id.max_per_visit
            rec.letter_id.final_gl_max_day_per_year = rec.detail_id.max_day_per_year

    @api.depends('detail_id')
    def _compute_limit(self):
        for rec in self:
            days = 0
            if rec.detail_id:
                rec.limit = rec.detail_id.inner_limit
                for line in rec.letter_id.final_gl_line:
                    if line.detail_id == rec.detail_id:
                        days += line.days
                if not rec.service_date:
                    rec.service_date = rec.letter_id.admission_date + timedelta(days=days)
                if rec.letter_id.admission_date and rec.letter_id.discharge_date and not rec.days:
                    delta = (rec.letter_id.discharge_date - rec.letter_id.admission_date)
                    if delta.days < 0:
                        raise ValidationError (_("Discharge date can not be earlier than admission date"))
                    rec.days = delta.days + 1
            else:
                rec.limit = []
    
    letter_id = fields.Many2one('guarantee.letter', string='Guarantee Letter', ondelete='cascade')

    # @api.onchange('letter_id','detail_id')
    # def _onchange_letter_id(self):
    #     letter_detail = []

    #     if self.letter_id:
    #         for line in self.letter_id.final_gl_line:
    #             if line.detail_id.id not in letter_detail:
    #                 letter_detail.append(line.detail_id.id)
                
    #     return {
    #         'domain' : {
    #             'detail_id' : [('id','not in',letter_detail),('id','in',self.get_detail_ids.ids)]
    #         }
    #     }

    detail_id = fields.Many2one('header.detail', string='Benefit (Member)')
    get_detail_ids = fields.Many2many('header.detail', compute='_compute_get_benefit_ids', string='Detail Domain')
    benefit_id = fields.Many2one('benefit.benefit', string='Benefit')
    get_benefit_ids = fields.Many2many('benefit.benefit', compute='_compute_get_benefit_ids', string='Benefit Domain')
    
    @api.depends('letter_id.benefit_master_id')
    def _compute_get_benefit_ids(self):
        domain_detail = []
        for rec in self:
            if rec.letter_id.member:
                if rec.letter_id.header_id:
                    for detail in rec.letter_id.header_id.detail_line:
                        domain_detail = [('id', '=', detail.id)]
                        domain_benefit = [('id', '=', detail.benefit_id.id)]
                        rec.get_detail_ids += self.env['header.detail'].search(domain_detail)
                        rec.get_benefit_ids += self.env['benefit.benefit'].search(domain_benefit)
                else:
                    rec.get_detail_ids = []
                    rec.get_benefit_ids = []
            if not rec.letter_id.member:
                if rec.letter_id.benefit_master_id:
                    rec.get_benefit_ids = self.env['benefit.benefit'].search([('master_id','=',rec.letter_id.benefit_master_id.id)])
                    rec.get_detail_ids = []
                else:
                    rec.get_detail_ids = []
                    rec.get_benefit_ids = []
    
    @api.onchange('benefit_id')
    def _onchange_benefit_id(self):
        for rec in self:
            if rec.benefit_id:
                for detail in rec.get_detail_ids:
                    if detail.benefit_id == rec.benefit_id:
                        rec.detail_id = detail._origin.id


    limit = fields.Float(compute='_compute_limit', string='Limit')
    days = fields.Integer(string='Days')
    actual_amount = fields.Float(string='Actual Amount')
    charge = fields.Float(string='Charge')
    total_amount = fields.Float(string='Total Amount')
    deductible_amount = fields.Float(string='Deductible Amount')
    excess_amount = fields.Float(string='Excess Amount (temp)')
    approved_amount = fields.Float(string='Approved')
    cover_amount = fields.Float(compute='_compute_cover_amount', string='Cover (temp)', store=True, tracking=True)
    real_excess_amount = fields.Float(string='Excess Amount')
    real_cover_amount = fields.Float(compute='_compute_real_cover_amount', string='Cover')

    member_per_day_limit_line = fields.One2many('member.per.day.limit', 'final_gl_id', string='Member day limit')

    @api.onchange('cover_amount','detail_id','service_date')
    def _onchange_excess_amount_deductible(self):
        for rec in self:
            rec.calculate_deductible()

    def calculate_deductible(self):
        for rec in self:
            if rec.letter_id.member:
                rec.deductible_amount = rec.detail_id.header_id.deductible

                if rec.detail_id.header_id.deductible_period == 'onetime':
                    gl = self.env['guarantee.letter'].search([('member_id','=',rec.letter_id.member_id.id),('id','!=',rec.letter_id._origin.id)])
                    for letter in gl:
                        # Get final GL record for the same header
                        for line in letter.final_gl_line:
                            if line.detail_id in rec.detail_id.header_id.detail_line and line not in rec.letter_id.final_gl_line._origin:
                                rec.deductible_amount -= line.cover_amount
                    for self_line in rec.letter_id.final_gl_line:
                        if (self_line.detail_id in rec.detail_id.header_id.detail_line and self_line.detail_id != rec.detail_id) or (self_line.detail_id == rec.detail_id and self_line.service_date != rec.service_date):
                            rec.deductible_amount -= self_line.cover_amount

                elif rec.detail_id.header_id.deductible_period == 'annual':
                    if rec.letter_id.admission_date < rec.letter_id.end_policy_date:
                        gl = self.env['guarantee.letter'].search([('member_id','=',rec.letter_id.member_id.id),('id','!=',rec.letter_id._origin.id),('admission_date','<=',rec.letter_id.end_policy_date),('admission_date','>=',rec.letter_id.effective_date_member)])
                    elif rec.letter_id.admission_date > rec.letter_id.end_policy_date:
                        gl = self.env['guarantee.letter'].search([('member_id','=',rec.letter_id.member_id.id),('id','!=',rec.letter_id._origin.id),('admission_date','>',rec.letter_id.end_policy_date)])
                    for letter in gl:
                        # Get final GL record for the same header
                        for line in letter.final_gl_line:
                            if line.detail_id in rec.detail_id.header_id.detail_line and line not in rec.letter_id.final_gl_line._origin:
                                rec.deductible_amount -= line.cover_amount
                    for self_line in rec.letter_id.final_gl_line:
                        if (self_line.detail_id in rec.detail_id.header_id.detail_line and self_line.detail_id != rec.detail_id) or (self_line.detail_id == rec.detail_id and self_line.service_date != rec.service_date):
                            rec.deductible_amount -= self_line.cover_amount

                elif rec.detail_id.header_id.deductible_period == 'visit':
                    for self_line in rec.letter_id.final_gl_line:
                        if (self_line.detail_id in rec.detail_id.header_id.detail_line and self_line.detail_id != rec.detail_id) or (self_line.detail_id == rec.detail_id and self_line.service_date != rec.service_date) :
                            rec.deductible_amount -= self_line.cover_amount
                
                if rec.deductible_amount < 0:
                    rec.deductible_amount = 0

        
    remaining_limit = fields.Float(string='Remaining Limit')
    total_days = fields.Integer(string='Total Days')
    annual_limit = fields.Float(string='Annual Limit')
    excess_remarks = fields.Char(string='Excess Remarks')
    excess_comment = fields.Selection([
        ('overlimit', 'Overlimit'),
        ('vitamin', 'Vitamin not cover'),
        ('food', 'Food Suplement not cover'),
        ('30', 'Overlimit'),
        ('60', 'Overlimit'),
        ('item', 'Item not cover'),
        ('family', 'Family not cover'),
        ('vaccination', 'Vaccination not cover'),
        ('drug', 'Drugs not cover'),
        ('treatment', 'Treatment not cover'),
    ], string='Excess Comment')
    company_id = fields.Many2one('res.company', 'Company', default=lambda self: self.env.user.company_id.id, index=1, tracking=True)
    currency_id = fields.Many2one('res.currency', 'Currency', default=lambda self: self.env.user.company_id.currency_id.id, required=True, tracking=True)
    excess = fields.Boolean(string='Excess')
    patient_paid = fields.Float(string='Patient Paid')
    service_date = fields.Date(string='Service Date')
    admin_comment = fields.Char(string='Admin Comment')
    exclusion = fields.Boolean(string='Exclusion')
    remarks = fields.Float(string='Discount')
    coinsurance = fields.Float(string='Co-Insurance')
    coshare = fields.Float(string='Co-Payment')

    # @api.onchange('exclusion')
    # def _onchange_exclusion(self):
    #     for rec in self:
    #         if rec.exclusion:
    #             rec.excess_amount = rec.total_amount
    
    # @api.onchange('excess_amount')
    # def _onchange_excess_amount(self):
    #     for rec in self:
    #         if rec.exclusion:
    #             rec._compute_cover_amount

    @api.onchange('days','charge')
    def _onchange_limit_days(self):
        for rec in self:
            if rec.days and rec.charge:
                rec.total_amount = rec.charge
                rec.actual_amount = rec.total_amount / rec.days
            if rec.letter_id.provider_id:
                discount = self.env['provider.discount'].search([('partner_id','=',rec.letter_id.provider_id.id)])
                for record in discount:
                    for benefit in discount.benefit_line:
                        if benefit.benefit_id == rec.detail_id.benefit_id:
                            rec.total_amount = rec.charge * ((1 - benefit.discount))
                            rec.actual_amount = rec.total_amount / rec.days
                            rec.remarks = '%s%%' % (benefit.discount * 100)
            if rec.detail_id.header_id.coinsurance:
                rec.total_amount -= rec.charge * (rec.detail_id.header_id.coinsurance)
                rec.actual_amount = rec.total_amount / rec.days
                rec.coinsurance = rec.detail_id.header_id.coinsurance


    @api.onchange('detail_id')
    def _onchange_detail_id(self):
        for rec in self:
            # if rec.detail_id and not rec.detail_id.header_id.deductible_period:
            #     raise ValidationError (_("Deductible period for selected category is not set"))
            remaining = rec.limit
            total_days = 0

            # calculate self lines
            for self_line in rec.letter_id.final_gl_line:
                if self_line.detail_id == rec.detail_id and self_line != rec:
                    remaining -= self_line.real_cover_amount
                    if remaining < 0 and rec.limit != -1:
                        remaining = 0
                    total_days += self_line.days

            if rec.letter_id.member_id and remaining != -1:
                if rec.detail_id.header_id.limit_selection == 'family':
                    # Get Guarantee Letter for member with the same member number
                    gl = self.env['guarantee.letter'].search([('member','=',rec.letter_id.member),('member_number','=',rec.letter_id.member_id.member_number),('id','!=',rec.letter_id._origin.id),('admission_date','<=',rec.letter_id.end_policy_date),('admission_date','>=',rec.letter_id.effective_date_member)])
                    for letter in gl:
                        # Get final GL record for the same benefit
                        for line in letter.final_gl_line:
                            if line.detail_id == rec.detail_id and line.id != rec._origin.id and line not in rec.letter_id.final_gl_line._origin:
                                remaining -= line.real_cover_amount
                                if remaining < 0 and rec.limit != -1:
                                    remaining = 0
                                total_days += line.days
                elif rec.detail_id.header_id.limit_selection == 'individu':
                    # Get Guarantee Letter for the same member
                    gl = self.env['guarantee.letter'].search([('member_id','=',rec.letter_id.member_id.id),('id','!=',rec.letter_id._origin.id),('admission_date','<=',rec.letter_id.end_policy_date),('admission_date','>=',rec.letter_id.effective_date_member)])
                    for letter in gl:
                        # Get final GL record for the same benefit
                        for line in letter.final_gl_line :
                            if line.detail_id == rec.detail_id and line.id != rec._origin.id and line not in rec.letter_id.final_gl_line._origin:
                                remaining -= line.real_cover_amount
                                if remaining < 0 and rec.limit != -1:
                                    remaining = 0
                                total_days += line.days
            rec.remaining_limit = remaining
            rec.total_days = total_days
                

    # excess_amount = fields.Float(compute='_compute_excess_amount', string='Temp Excess Amount', store=True)
    
    @api.onchange('actual_amount','exclusion','service_date')
    def _onchange_compute_excess_amount(self):
        for rec in self:
            # if rec.exclusion:
            #     rec.excess_amount = rec.total_amount
            # if rec.letter_id.provider_check == 'not_provider':
            #     rec.excess_amount = rec.total_amount
            #     rec._onchange_calculate_real_excess_amount()
            # if rec.letter_id.policy_status == 'N' and rec.letter_id.admission_date >= rec.letter_id.end_policy_date:
            #     rec.excess_amount = rec.total_amount
            # else:
            rec.calculate_excess()

    def calculate_excess(self):
        for rec in self:
            total_visit = 1
            per_day_limit = 0
            rec.excess_amount = 0
            rec.excess_remarks = False
            remaining = rec.remaining_limit
            deductible = rec.deductible_amount
            total_days = rec.total_days
            if rec.letter_id.member_id and rec.detail_id:
                # Get Guarantee Letter for the same member
                gl = self.env['guarantee.letter'].search([('member_id','=',rec.letter_id.member_id.id),('id','!=',False),('admission_date','=',rec.letter_id.admission_date)])
                for letter in gl:
                    # Get final GL record for the same benefit
                    for line in letter.final_gl_line:
                        if line.detail_id == rec.detail_id and line not in rec.letter_id.final_gl_line:
                            total_visit += 1
                result = rec.total_amount - remaining

                # Reset related per day limit on edit
                # member_benefit_per_day_limit = self.env['member.per.day.limit'].search([('member_id','=',rec.letter_id.member_id.id),('detail_id','=',rec.detail_id.id),('service_date','=',rec.service_date)])
                this_line_per_day_limit = self.env['member.per.day.limit'].search([('member_id','=',rec.letter_id.member_id.id),('detail_id','=',rec.detail_id.id),('final_gl_id','=',rec.id),('final_gl_id','!=',False)])
                if len(rec.member_per_day_limit_line) != rec.days:
                    for usage in this_line_per_day_limit:
                        usage.final_gl_id = False
                        usage.member_id = False
                    rec.member_per_day_limit_line = [(5,0,0)]

                # # Check if visit exceed max day per year NEED CHECK CONDITION MAX PER DAY
                # if total_days > rec.detail_id.max_day_per_year and rec.detail_id.max_day_per_year != -1:
                #     rec.excess = True
                #     rec.excess_amount = rec.total_amount
                #     rec.excess_remarks = ("Max day per year reached. ")
                #     return
                # if (total_days + rec.days) > rec.detail_id.max_day_per_year and rec.detail_id.max_day_per_year != -1:
                #     excess_days = (total_days + rec.days) - rec.detail_id.max_day_per_year
                #     provided = (rec.days - excess_days) * rec.actual_amount
                #     if rec.actual_amount > rec.detail_id.max_per_visit :
                #         provided = (rec.days - excess_days) * (rec.detail_id.max_per_visit)
                #     if excess_days > 0:
                #         rec.excess = True
                #         rec.excess_amount = excess_days * rec.actual_amount
                #         if provided > remaining and remaining != -1:
                #             if provided > rec.detail_id.max_per_visit and rec.detail_id.max_per_visit != -1:
                #                 if remaining > rec.detail_id.max_per_visit:
                #                     if provided > (rec.detail_id.max_per_day - per_day_limit) and rec.detail_id.max_per_day != -1:
                #                         rec.excess_amount += provided - (rec.detail_id.max_per_day - per_day_limit)
                #                         rec.excess_remarks = ("Max day per year and max per day reached. ")
                #                     else:
                #                         rec.excess_amount += provided - rec.detail_id.max_per_visit
                #                         rec.excess_remarks = ("Max day per year and max per visit reached. ")
                #                 if remaining < rec.detail_id.max_per_visit:
                #                     if provided > (rec.detail_id.max_per_day - per_day_limit) and rec.detail_id.max_per_day != -1:
                #                         rec.excess_amount += provided - (rec.detail_id.max_per_day - per_day_limit)
                #                         rec.excess_remarks = ("Max day per year and max per day reached. ")
                #                     else:
                #                         rec.excess_amount += provided - remaining
                #                         rec.excess_remarks = ("Max day per year and limit reached. ")
                #             else:
                #                 if provided > (rec.detail_id.max_per_day - per_day_limit) and rec.detail_id.max_per_day != -1:
                #                     rec.excess_amount += provided - (rec.detail_id.max_per_day - per_day_limit)
                #                     rec.excess_remarks = ("Max day per year and max per day reached. ")
                #                 if provided < (rec.detail_id.max_per_day - per_day_limit) or rec.detail_id.max_per_day != -1:
                #                     rec.excess_amount += provided - remaining
                #                     rec.excess_remarks = ("Max day per year and limit reached. ")
                #         if provided < remaining or remaining == -1:
                #             if provided > rec.detail_id.max_per_visit and rec.detail_id.max_per_visit != -1:
                #                 rec.excess_amount = rec.total_amount - provided
                #                 # rec.excess_amount += rec.total_amount - provided - rec.detail_id.max_per_visit
                #                 rec.excess_remarks = ("Max day per year and max per visit reached. ")
                #                 return
                #     else:
                #         if rec.total_amount > remaining and remaining != -1:
                #             if rec.total_amount > rec.detail_id.max_per_visit:
                #                 if remaining < rec.detail_id.max_per_visit:
                #                     rec.excess_amount = rec.total_amount - remaining
                #                     rec.excess_remarks = ("Limit reached. ")
                #                 else:
                #                     rec.excess_amount = rec.total_amount - rec.detail_id.max_per_visit
                #                     rec.excess_remarks = ("Max per visit reached. ")
                #         if rec.total_amount < remaining or remaining != -1:
                #             if rec.total_amount > rec.detail_id.max_per_visit:
                #                 rec.excess_amount = rec.total_amount - rec.detail_id.max_per_visit
                #                 rec.excess_remarks = ("Max per visit reached. ")
                #     return
                    
                # # Check if visit exceed max per day #NEED REVISI
                # if total_visit > rec.detail_id.max_per_day and rec.detail_id.max_per_day != -1:
                #     rec.excess_amount = rec.total_amount
                #     rec.excess_remarks = ("Max visit per day reached. ")
                #     return

                # # Check if visit exceed per day limit #NEED REVISI
                # if per_day_limit >= rec.detail_id.per_day_limit and rec.detail_id.per_day_limit != -1:
                #     rec.excess_amount =  rec.total_amount
                #     rec.excess_remarks = ("Per Day Limit reached. ")
                #     return

                # Check excess condition per day
                for day in range(rec.days):
                    service_date = rec.service_date + timedelta(days=day)
                    member_benefit_per_day_limit = self.env['member.per.day.limit'].search([('member_id','=',rec.letter_id.member_id.id),('detail_id','=',rec.detail_id.id),('service_date','=',service_date),('final_gl_id','!=',rec._origin.id),('final_gl_id','!=',False)])
                    this_line_per_day_limit = self.env['member.per.day.limit'].search([('member_id','=',rec.letter_id.member_id.id),('detail_id','=',rec.detail_id.id),('service_date','=',service_date),('final_gl_id','=',rec.id),('final_gl_id','!=',False)])
                    # detail_day_visit = self.env['member.per.day.limit'].search([('member_id','=',rec.letter_id.member_id.id),('detail_id','=',rec.detail_id.id),('service_date','=',service_date),('per_day_limit_used','>',0),('final_gl_id','!=',False)])
                    
                    # Create member per day limit for selected benefit
                    if not this_line_per_day_limit:
                        this_line_per_day_limit = this_line_per_day_limit.create({
                            'final_gl_id': rec.id,
                            'member_id': rec.letter_id.member_id.id,
                            'service_date': service_date,
                            'detail_id': rec.detail_id.id,
                            'per_day_limit': rec.detail_id.per_day_limit,
                            'max_per_day': rec.detail_id.max_per_day,
                            # 'per_day_limit_used' : rec.actual_amount,
                            # 'per_day_visit_used' : 1,
                        })
                        rec.member_per_day_limit_line += this_line_per_day_limit

                    if rec.letter_id.provider_check == 'not_provider':
                        this_line_per_day_limit.excess_amount = rec.actual_amount
                        rec.excess_remarks = ("Not client's provider")
                        continue

                    if rec.letter_id.policy_status == 'N' and rec.letter_id.admission_date >= rec.letter_id.end_policy_date:
                        this_line_per_day_limit.excess_amount = rec.actual_amount
                        rec.excess_remarks = ("Member not active")
                        continue
                    
                    # Check if visit exceed max day per year
                    total_days += 1
                    if total_days > rec.detail_id.max_day_per_year and rec.detail_id.max_day_per_year != -1:
                        this_line_per_day_limit.excess_amount = rec.actual_amount
                        rec.excess_amount += this_line_per_day_limit.excess_amount
                        rec.excess_remarks = ("Max day per year")
                        continue

                    # Check if visit exceed max per day
                    # need confirm visit definition, per admission date or per service date?
                    if total_visit > rec.detail_id.max_per_day and rec.detail_id.max_per_day != -1:
                        this_line_per_day_limit.excess_amount = rec.actual_amount
                        rec.excess_amount += this_line_per_day_limit.excess_amount
                        rec.excess_remarks = ("Max visit per day")
                        continue

                    day_benefit_limit_used = 0
                    for limit in member_benefit_per_day_limit:
                        day_benefit_limit_used += limit.per_day_limit_used
                    
                    # if remaining limit per day + actual amount greater than per day limit
                    if (day_benefit_limit_used + rec.actual_amount) > rec.detail_id.per_day_limit and rec.detail_id.per_day_limit != -1:
                        # if rec.days == 1:
                        #     this_line_per_day_limit.excess_amount = rec.actual_amount - (rec.detail_id.per_day_limit - day_benefit_limit_used)
                        #     rec.excess_amount = this_line_per_day_limit.excess_amount
                        #     rec.excess_remarks = ("Overlimit")
                        #     return
                        # rec.excess_amount = rec.days * (rec.actual_amount - (rec.detail_id.per_day_limit - per_day_limit))
                        # rec.excess_amount += rec.actual_amount - (rec.detail_id.per_day_limit - day_benefit_limit_used)
                        day_excess = rec.actual_amount - (rec.detail_id.per_day_limit - day_benefit_limit_used)

                        # if remaining limit greater than remaining per day limit or unlimited
                        if remaining >= (rec.detail_id.per_day_limit - day_benefit_limit_used) or remaining == -1:

                            # if max per visit less than remaining per day limit
                            if rec.detail_id.max_per_visit <= (rec.detail_id.per_day_limit - day_benefit_limit_used):
                            # if rec.detail_id.max_per_visit <= (rec.detail_id.per_day_limit - day_benefit_limit_used) and rec.detail_id.max_per_visit != -1:
                                
                                # if cover amount (rec.actual_amount - day_excess) greater than max per visit, cover limited to max per visit
                                if (rec.actual_amount - day_excess) >= rec.detail_id.max_per_visit and rec.detail_id.max_per_visit != -1:
                                    
                                    # if remaining limit greater than max per visit
                                    # remaining limit is greater than remaining per day limit
                                    # max per visit is less than remaining per day limit
                                    # remaining limit is greater than max per visit
                                    if remaining >= rec.detail_id.max_per_visit or remaining == -1:
                                        this_line_per_day_limit.excess_amount = rec.actual_amount - rec.detail_id.max_per_visit
                                        rec.excess_amount += this_line_per_day_limit.excess_amount
                                        rec.excess_remarks = ("Overlimit")
                                        continue
                                    
                                    # if remaining limit less than max per visit
                                    # impossible condition
                                    elif remaining < rec.detail_id.max_per_visit and remaining != -1:
                                        this_line_per_day_limit.excess_amount = rec.actual_amount - remaining
                                        rec.excess_amount += this_line_per_day_limit.excess_amount
                                        rec.excess_remarks = ("Overlimit")
                                        continue
                                # if cover amount (rec.actual_amount - day_excess) less than max per visit
                                elif (rec.actual_amount - day_excess) < rec.detail_id.max_per_visit or rec.detail_id.max_per_visit == -1:
                                    # if remaining limit greater than cover amount
                                    # remaining limit is greater than remaining per day limit
                                    # max per visit is less than remaining per day limit
                                    # remaining limit is greater than max per visit
                                    # cover amount is less than max per visit
                                    if remaining >= (rec.actual_amount - day_excess) or remaining == -1:
                                        this_line_per_day_limit.excess_amount = day_excess
                                        rec.excess_amount += this_line_per_day_limit.excess_amount
                                        rec.excess_remarks = ("Overlimit")
                                        this_line_per_day_limit.cover_amount = rec.actual_amount - this_line_per_day_limit.excess_amount
                                        if remaining != -1 and deductible <= this_line_per_day_limit.cover_amount:
                                            remaining -= this_line_per_day_limit.cover_amount - deductible
                                        elif deductible >= this_line_per_day_limit.cover_amount:
                                            deductible -= this_line_per_day_limit.cover_amount
                                        continue
                                    # if remaining limit less than cover amount
                                    # impossible condition
                                    elif remaining < (rec.actual_amount - day_excess) and remaining != -1:
                                        this_line_per_day_limit.excess_amount = rec.actual_amount - remaining
                                        rec.excess_amount += this_line_per_day_limit.excess_amount
                                        rec.excess_remarks = ("Overlimit")
                                        if remaining != -1 and deductible <= this_line_per_day_limit.cover_amount:
                                            remaining -= this_line_per_day_limit.cover_amount - deductible
                                            deductible -= this_line_per_day_limit.cover_amount
                                        elif deductible >= this_line_per_day_limit.cover_amount:
                                            deductible -= this_line_per_day_limit.cover_amount
                                        continue

                            # if max per visit greater than remaining per day limit
                            if rec.detail_id.max_per_visit > (rec.detail_id.per_day_limit - day_benefit_limit_used) or rec.detail_id.max_per_visit == -1:
                                # if cover amount (rec.actual_amount - day_excess) greater than remaining per day limit, cover limited to remaining per day limit
                                if (rec.actual_amount - day_excess) >= (rec.detail_id.per_day_limit - day_benefit_limit_used) and rec.detail_id.per_day_limit != -1:
                                    this_line_per_day_limit.excess_amount = day_excess
                                    rec.excess_amount += this_line_per_day_limit.excess_amount
                                    rec.excess_remarks = ("Overlimit")

                                # if cover amount (rec.actual_amount - day_excess) less than remaining per day limit
                                elif (rec.actual_amount - day_excess) < rec.detail_id.per_day_limit:
                                    # if remaining limit greater than cover amount
                                    # remaining limit is greater than remaining per day limit
                                    # remaining per day limit is greater than cover amount
                                    # remaining limit is greater than cover amount
                                    if remaining > (rec.actual_amount - day_excess) or remaining == -1:
                                        this_line_per_day_limit.excess_amount = rec.actual_amount - day_excess
                                        rec.excess_amount += this_line_per_day_limit.excess_amount
                                        rec.excess_remarks = ("Overlimit")
                                        continue
                                    
                        # if remaining limit less than remaining per day limit
                        if remaining < (rec.detail_id.per_day_limit - day_benefit_limit_used) or remaining != -1:

                            # if max per visit less than remaining
                            if rec.detail_id.max_per_visit <= remaining and rec.detail_id.max_per_visit != -1:
                            # if rec.detail_id.max_per_visit <= (rec.detail_id.per_day_limit - day_benefit_limit_used) and rec.detail_id.max_per_visit != -1:
                                
                                # if cover amount (rec.actual_amount - day_excess) greater than max per visit, cover limited to max per visit
                                if (rec.actual_amount - day_excess) >= rec.detail_id.max_per_visit and rec.detail_id.max_per_visit != -1:
                                    
                                    # if remaining limit greater than max per visit
                                    # remaining limit is greater than remaining per day limit
                                    # max per visit is less than remaining per day limit
                                    # remaining limit is greater than max per visit
                                    if remaining >= rec.detail_id.max_per_visit or remaining == -1:
                                        this_line_per_day_limit.excess_amount = rec.actual_amount - rec.detail_id.max_per_visit
                                        rec.excess_amount += this_line_per_day_limit.excess_amount
                                        rec.excess_remarks = ("Overlimit")
                                        continue
                                    
                                    # if remaining limit less than max per visit
                                    elif remaining < rec.detail_id.max_per_visit and remaining != -1:
                                        this_line_per_day_limit.excess_amount = rec.actual_amount - remaining
                                        rec.excess_amount += this_line_per_day_limit.excess_amount
                                        rec.excess_remarks = ("Overlimit")
                                        continue
                                # if cover amount (rec.actual_amount - day_excess) less than max per visit
                                elif (rec.actual_amount - day_excess) < rec.detail_id.max_per_visit or rec.detail_id.max_per_visit == -1:
                                    # if remaining limit greater than cover amount
                                    # remaining limit is greater than remaining per day limit
                                    # max per visit is less than remaining per day limit
                                    # remaining limit is greater than max per visit
                                    # cover amount is less than max per visit
                                    if remaining >= (rec.actual_amount - day_excess):
                                        this_line_per_day_limit.excess_amount = day_excess
                                        rec.excess_amount += this_line_per_day_limit.excess_amount
                                        rec.excess_remarks = ("Overlimit")
                                        this_line_per_day_limit.cover_amount = rec.actual_amount - this_line_per_day_limit.excess_amount
                                        if remaining != -1 and deductible <= this_line_per_day_limit.cover_amount:
                                            remaining -= this_line_per_day_limit.cover_amount - deductible
                                            deductible -= this_line_per_day_limit.cover_amount
                                        elif deductible >= this_line_per_day_limit.cover_amount:
                                            deductible -= this_line_per_day_limit.cover_amount
                                        continue
                                    # if remaining limit less than cover amount
                                    # impossible condition
                                    elif remaining < (rec.actual_amount - day_excess) and remaining != -1:
                                        this_line_per_day_limit.excess_amount = rec.actual_amount - remaining
                                        rec.excess_amount += this_line_per_day_limit.excess_amount
                                        rec.excess_remarks = ("Overlimit")
                                        this_line_per_day_limit.cover_amount = rec.actual_amount - this_line_per_day_limit.excess_amount
                                        if remaining != -1 and deductible <= this_line_per_day_limit.cover_amount:
                                            remaining -= this_line_per_day_limit.cover_amount - deductible
                                            deductible -= this_line_per_day_limit.cover_amount
                                        elif deductible >= this_line_per_day_limit.cover_amount:
                                            deductible -= this_line_per_day_limit.cover_amount
                                        continue

                            # if max per visit greater than remaining
                            if rec.detail_id.max_per_visit > remaining or rec.detail_id.max_per_visit == -1:
                                # if cover amount (rec.actual_amount - day_excess) greater than remaining, cover limited to remaining
                                if (rec.actual_amount - day_excess) >= remaining:
                                    this_line_per_day_limit.excess_amount = rec.actual_amount - remaining
                                    rec.excess_amount += this_line_per_day_limit.excess_amount
                                    rec.excess_remarks = ("Overlimit")

                                # if cover amount (rec.actual_amount - day_excess) less than remaining
                                elif (rec.actual_amount - day_excess) < remaining:
                                    # if remaining limit greater than cover amount
                                    # remaining limit is greater than remaining per day limit
                                    # remaining per day limit is greater than cover amount
                                    # remaining limit is greater than cover amount
                                    if remaining > (rec.actual_amount - day_excess) or remaining == -1:
                                        this_line_per_day_limit.excess_amount = rec.actual_amount - (rec.actual_amount - day_excess)
                                        rec.excess_amount += this_line_per_day_limit.excess_amount
                                        rec.excess_remarks = ("Overlimit")
                                        continue

                        # if remaining limit less than remaining per day limit
                        if remaining < (rec.detail_id.per_day_limit - day_benefit_limit_used) and remaining != -1:
                            rec.excess_amount = rec.days * (rec.actual_amount - (rec.detail_id.per_day_limit - per_day_limit))
                            # if cover amount (rec.actual_amount - day_excess) greater than max per visit
                            # if remaining limit greater than max per visit
                            if remaining > rec.detail_id.max_per_visit and rec.detail_id.max_per_visit != -1:
                                this_line_per_day_limit.excess_amount = rec.actual_amount - rec.detail_id.max_per_visit
                                rec.excess_amount += this_line_per_day_limit.excess_amount 
                                rec.excess_remarks = ("Overlimit")
                                continue
                            # if remaining limit less than max per visit
                            elif remaining < rec.detail_id.max_per_visit or rec.detail_id.max_per_visit == -1:
                                this_line_per_day_limit.excess_amount = rec.actual_amount - remaining
                                rec.excess_amount += this_line_per_day_limit.excess_amount 
                                rec.excess_remarks = ("Overlimit")
                                continue
                
                
                    # Check if actual amount exceed max per visit
                    # if actual amount greater than max per visit
                    if (rec.actual_amount) >= rec.detail_id.max_per_visit and rec.detail_id.max_per_visit != -1:
                        # if remaining limit greater than max per visit
                        if remaining > rec.detail_id.max_per_visit or remaining == -1:
                            this_line_per_day_limit.excess_amount = rec.actual_amount - rec.detail_id.max_per_visit
                            rec.excess_amount += this_line_per_day_limit.excess_amount
                            rec.excess_remarks = ("Overlimit")
                            continue
                        # if remaining limit less than max per visit
                        elif remaining < rec.detail_id.max_per_visit and remaining != -1:
                            this_line_per_day_limit.excess_amount = rec.actual_amount - remaining
                            rec.excess_amount += this_line_per_day_limit.excess_amount
                            rec.excess_remarks = ("Overlimit")
                            continue
                    # if actual amount less than max per visit
                    elif (rec.actual_amount) < rec.detail_id.max_per_visit or rec.detail_id.max_per_visit == -1:
                        # if remaining limit less than actual amount
                        if remaining <= rec.actual_amount and remaining != -1:
                            this_line_per_day_limit.excess_amount = rec.actual_amount - remaining
                            rec.excess_amount += this_line_per_day_limit.excess_amount 
                            rec.excess_remarks = ("Overlimit")
                            this_line_per_day_limit.cover_amount = rec.actual_amount - this_line_per_day_limit.excess_amount
                            if remaining != -1 and deductible <= this_line_per_day_limit.cover_amount:
                                remaining -= this_line_per_day_limit.cover_amount - deductible
                                deductible -= this_line_per_day_limit.cover_amount
                            elif deductible >= this_line_per_day_limit.cover_amount:
                                deductible -= this_line_per_day_limit.cover_amount
                            continue
                        # if remaining limit greater than actual amount
                        elif remaining > rec.actual_amount or remaining == -1:
                            this_line_per_day_limit.excess_amount = 0
                            rec.excess_amount = 0
                            this_line_per_day_limit.cover_amount = rec.actual_amount - this_line_per_day_limit.excess_amount
                            if remaining != -1 and deductible <= this_line_per_day_limit.cover_amount:
                                remaining -= this_line_per_day_limit.cover_amount - deductible
                                deductible -= 0
                            elif deductible >= this_line_per_day_limit.cover_amount:
                                deductible -= this_line_per_day_limit.cover_amount
                            continue
            else:
                rec.excess_amount = 0
    
    
    @api.depends('excess_amount')
    def _compute_cover_amount(self):
        for rec in self:
            rec.cover_amount = 0
            for day in range(rec.days):
                service_date = rec.service_date + timedelta(days=day)
                this_line_per_day_limit = self.env['member.per.day.limit'].search([('member_id','=',rec.letter_id.member_id.id),('detail_id','=',rec.detail_id.id),('service_date','=',service_date),('final_gl_id','=',rec.id),('final_gl_id','!=',False)])
                for line in rec.member_per_day_limit_line:
                    if service_date == line.service_date:
                        this_line_per_day_limit = line
                this_line_per_day_limit.cover_amount = rec.actual_amount - this_line_per_day_limit.excess_amount
                rec.cover_amount += this_line_per_day_limit.cover_amount
                rec._compute_real_cover_amount

    @api.depends('deductible_amount','cover_amount')
    def _compute_real_cover_amount(self):
        for rec in self:
            rec.real_cover_amount = 0
            deductible = rec.deductible_amount
            for day in range(rec.days):
                service_date = rec.service_date + timedelta(days=day)
                this_line_per_day_limit = self.env['member.per.day.limit'].search([('member_id','=',rec.letter_id.member_id.id),('detail_id','=',rec.detail_id.id),('service_date','=',service_date),('final_gl_id','=',rec.id),('final_gl_id','!=',False)])
                for line in rec.member_per_day_limit_line:
                    if service_date == line.service_date:
                        this_line_per_day_limit = line
                if deductible <= this_line_per_day_limit.cover_amount:
                    this_line_per_day_limit.per_day_limit_used = this_line_per_day_limit.cover_amount - deductible
                    rec.real_cover_amount += this_line_per_day_limit.per_day_limit_used
                    deductible = 0
                elif deductible >= this_line_per_day_limit.cover_amount:
                    rec.real_cover_amount += 0
                    deductible -= this_line_per_day_limit.cover_amount
    
    @api.onchange('real_cover_amount','patient_paid','excess_amount','member_per_day_limit_line')
    def _onchange_calculate_real_excess_amount(self):
        for rec in self:
            rec.real_excess_amount = 0
            for day in range(rec.days):
                service_date = rec.service_date + timedelta(days=day)
                this_line_per_day_limit = self.env['member.per.day.limit'].search([('member_id','=',rec.letter_id.member_id.id),('detail_id','=',rec.detail_id.id),('service_date','=',service_date),('final_gl_id','=',rec.id),('final_gl_id','!=',False)])
                for line in rec.member_per_day_limit_line:
                    if service_date == line.service_date:
                        this_line_per_day_limit = line
                rec.real_excess_amount += this_line_per_day_limit.excess_amount + this_line_per_day_limit.cover_amount - this_line_per_day_limit.per_day_limit_used
            rec.real_excess_amount -= rec.patient_paid
            # rec.real_excess_amount = rec.excess_amount - rec.patient_paid
    
    @api.onchange('real_cover_amount','patient_paid','real_excess_amount')
    def _onchange_calculate_approved_amount(self):
        for rec in self:
            rec.approved_amount = rec.real_cover_amount + rec.real_excess_amount

    @api.onchange('real_excess_amount')
    def _onchange_real_excess_amount(self):
        for rec in self:
            if rec.real_excess_amount != (rec.excess_amount + rec.cover_amount - rec.real_cover_amount - rec.patient_paid):
                rec.excess_amount = 0
                rec.cover_amount = 0
                for day in range(rec.days):
                    edit_excess = rec.real_excess_amount / rec.days
                    service_date = rec.service_date + timedelta(days=day)
                    this_line_per_day_limit = self.env['member.per.day.limit'].search([('member_id','=',rec.letter_id.member_id.id),('detail_id','=',rec.detail_id.id),('service_date','=',service_date),('final_gl_id','=',rec.id),('final_gl_id','!=',False)])
                    for line in rec.member_per_day_limit_line:
                        if service_date == line.service_date:
                            this_line_per_day_limit = line
                    this_line_per_day_limit.excess_amount = rec.actual_amount - edit_excess
                    rec.excess_amount += this_line_per_day_limit.excess_amount
                    this_line_per_day_limit.cover_amount = rec.actual_amount - this_line_per_day_limit.excess_amount
                    rec.cover_amount += this_line_per_day_limit.cover_amount
                    rec._compute_real_cover_amount
                # rec.excess_amount = rec.real_excess_amount - rec.cover_amount + rec.real_cover_amount + rec.patient_paid
                # rec.excess_amount = rec.real_excess_amount + rec.patient_paid
