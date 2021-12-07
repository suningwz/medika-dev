# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class Base(models.AbstractModel):
    _inherit = 'base'
    _description = 'Base'

    def get_formview_action(self, access_uid=None):
        """ Override this method in order to redirect many2one towards the right model depending on access_uid """
        res = super(Base, self).get_formview_action(access_uid=access_uid)
        if self._name == 'res.partner':
            if self.client:
                res.update({
                    'target': 'main'
                })
        return res
