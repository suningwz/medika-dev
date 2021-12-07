from odoo import models, fields, api


class GuaranteeLetter(models.Model):
    _inherit = 'guarantee.letter'

    def action_member_limit(self):
        for rec in self:
            rec.member_id.refresh_benefit()
            res = self.env['ir.actions.act_window']._for_xml_id('asb_membership_member_limit.action_gl_member_benefit_limit')
            res['domain'] = [('member_id', '=', rec.member_id.id)]
            return res

class MemberPerDayLimit(models.Model):
    _inherit = 'member.per.day.limit'
    _description = 'Member Per Day Limit'
    
    excess_amount = fields.Float(string='Excess Amount')
    cover_amount = fields.Float(string='Cover Amount')
    final_gl_id = fields.Many2one('final.gl', string='Final GL', ondelete="cascade")

    # @api.model
    # def create(self,vals):
    #     for rec in self:
    #         res = super(MemberPerDayLimit, rec).create(vals)
    #         return res