# -*- coding: utf-8 -*-
import re
from odoo import models, fields, api, _
from datetime import datetime, date
from odoo.exceptions import UserError, ValidationError


class ExportProviderActivity(models.TransientModel):
    _name = 'export.provider.activity'
    _description = 'Export Provider Activity'

    name = fields.Char(string='Name')
    from_date = fields.Date(string='From Date')
    to_date = fields.Date(string='To Date')

    def export_activity(self):
        report_action = self.env.ref('asb_master_provider_activity.action_report_provider_activity').report_action(self)
        report_action['close_on_report_download'] = True
        return report_action
