# -*- coding: utf-8 -*-
import re
from odoo import models, fields, api, _
from datetime import datetime, date
from odoo.exceptions import UserError, ValidationError


class BankMaster(models.Model):
    _name = 'bank.master'
    _description = 'Bankk Master'

    name = fields.Char(string='Bank Name')
    code_bank = fields.Char(string='Bank Code')
    type = fields.Char(string='Bank Code Type')
    confirm = fields.Boolean(string='Confirm', default=True)

    def name_get(self):
        res = []
        for rec in self:
            res.append((rec.id, '%s - %s' % (rec.code_bank, rec.name)))
        return res
