from odoo import models, fields, api, _


class ResPartner(models.Model):
    _inherit = 'res.partner'
    _description = 'Res Partner'

    def write(self, vals):
        for rec in self:
            if vals.get('card_number'):
                rec.card_number_check()
            res = super(ResPartner, rec).write(vals)
            if rec.card_number and rec.member:
                card_number = self.env['card.number'].search([('name', '=', rec.card_number)])
                if not card_number:
                    rec.env['card.number'].create({
                        'name': rec.card_number
                    })
            return res

    def card_number_check(self):
        if self.card_number and self.member:
            card_number = self.env['card.number'].search([('name', '=', self.card_number)])
            if card_number:
                card_number.unlink()

    def unlink(self):
        for rec in self:
            if rec.card_number and rec.member:
                card_number = self.env['card.number'].search([('name', '=', rec.card_number)])
                if card_number:
                    card_number.unlink()
        res = super(ResPartner, self).unlink()
        return res


class CardNumber(models.Model):
    _name = 'card.number'
    _description = 'Card Number'

    name = fields.Char(string='Card Number')
