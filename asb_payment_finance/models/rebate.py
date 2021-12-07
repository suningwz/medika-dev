from odoo import models, fields, api

class PaymentRebate(models.Model):
    _name = 'payment.rebate'
    _description = 'Payment Rebate'
    _rec_name = 'payment_number'
    
    payment_number = fields.Char(string='Payment Number')
    provider_id = fields.Many2one('res.partner', string='Provider', domain=[('provider', '=', True)])
    rebate_amount = fields.Float(string='Rebate Amount')
    payment_date = fields.Datetime(string='Payment Date')
    member = fields.Selection([
        ('member', 'Member'),
        ('nonmember', 'Non Member'),
    ], string='Member')
    currency_id = fields.Many2one('res.currency', 'Currency', default=lambda self: self.env.user.company_id.currency_id.id, required=True, tracking=True)

    