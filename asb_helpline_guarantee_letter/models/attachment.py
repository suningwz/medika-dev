from odoo import models, fields, api


class IrAttachment(models.Model):
    _inherit = 'ir.attachment'
    _description = 'Ir Attachment'
    
    @api.model
    def create(self,vals):
        res = super(IrAttachment, self).create(vals)
        if res.res_model == 'guarantee.letter':
            letter = self.env['guarantee.letter'].search([('id','=',res.res_id)])
            letter.attachment_ids = [(4,res._origin.id)]
        return res