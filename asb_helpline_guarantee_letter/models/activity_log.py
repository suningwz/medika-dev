from odoo import models, fields, api


class GuaranteeLetter(models.Model):
    _inherit = 'guarantee.letter'
    _description = 'Guarantee Letter'
    
    activity_line = fields.One2many('helpline.activity.log', 'letter_id', string='Activity Log')
    def activity_log(self):
        for rec in self:
            res = self.env['ir.actions.act_window']._for_xml_id('asb_helpline_activity_log.helpline_activity_log_action_window')
            res['domain'] = [('letter_id', '=', rec._origin.id)]
            res['context'] = {'default_letter_id': rec._origin.id}
            res['target'] = 'main'
            return res

    @api.model
    def create(self, vals):
        res = super(GuaranteeLetter, self).create(vals)
        activity = res.env['helpline.activity.log'].create({
            'letter_id': res._origin.id,
            })
        return res