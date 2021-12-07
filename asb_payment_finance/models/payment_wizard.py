from odoo import models, fields, api
    
class PaymentPaidWizard(models.TransientModel):
    _name = 'payment.paid.wizard'
    _description = 'Payment Paid Wizard'
    
    name = fields.Char(string='Name')
    letter_ids = fields.Many2many('guarantee.letter', string='Claim')
    total_cover = fields.Float(string='Total Claim')
    total_charge = fields.Float(string='Total Charge')

    total_cover = fields.Float(compute='_compute_total_cover', string='Total Claim')
    total_excess = fields.Float(compute='_compute_total_excess', string='Total Excess')
    total_amount = fields.Float(compute='_compute_total_amount', string='Total Amount')
    total_approved = fields.Float(compute='_compute_total_approved', string='Total Approved')
    
    currency_id = fields.Many2one('res.currency', 'Currency', default=lambda self: self.env.user.company_id.currency_id.id, required=True, tracking=True)

    @api.depends('letter_ids')
    def _compute_total_cover(self):
        for rec in self:
            rec.total_cover = 0
            rec.total_excess = 0
            rec.total_amount = 0
            rec.total_approved = 0
            for letter in rec.letter_ids:
                rec.total_cover += letter.amount_cover
                rec.total_excess += letter.amount_excess
                rec.total_amount += letter.amount_total
                rec.total_approved += letter.amount_approved
    
    def action_finance_paid(self):
        for rec in self:
            for letter in rec.letter_ids:
                letter.paid()