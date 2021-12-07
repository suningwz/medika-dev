from odoo import models, fields, api
    
class MemberWizard(models.TransientModel):
    _name = 'policy.member.wizard'
    _description = 'Member Wizard'

    name = fields.Char(string='Add Member')
    member_ids = fields.Many2many('res.partner', string='Member',)
    policy_id = fields.Many2one('policy.policy', string='Policy')
    # product_id = fields.Many2one('master.product', string='Product')
    state = fields.Selection([
        ('inactive', 'Inactive'),
        ('active', 'Active'),
    ], string='Status', default='inactive')
    
    # @api.onchange('policy_id')
    # def _onchange_policy_id(self):
    #     self.member_ids = []
    #     if self.policy_id:
    #         return {'domain': {'member_ids': [('id', 'in', [rec.id for rec in self.policy_id.client_id.client_ids.entity_member_ids])]}}

    def add_policy_member(self):
        lines = []
        existing_member =[]
        policy = self.env['policy.policy'].search([('id', '=', self.policy_id.id)])
        for member in self.policy_id.member_line:
            existing_member += member.member_id
        for member in self.member_ids:
            vals = {
                'member_id' : member.id,
                # 'product_id': self.product_id.id,
                'state' : self.state,
            }
            if member in existing_member:
                existing_line = self.policy_id.member_line.search([('member_id', '=', member.id),('policy_id', '=', self.policy_id.id)])
                lines.append((1, existing_line.id, vals))
            else:
                lines.append((0, 0, vals))
        self.policy_id.member_line = lines