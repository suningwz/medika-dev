# -*- coding: utf-8 -*-

from odoo import models, fields, api

class IrAttachment(models.Model):
    _inherit = 'ir.attachment'
    _description = 'Ir Attachment'
    
    def new_tab(self):
        attachment = self.id
        url = '/web/content/%s' % attachment
        return {
            'name'     : 'Open Attachment',
            'type'     : 'ir.actions.act_url',
            'target'   : 'new',
            'url'      : url
            }