# -*- coding: utf-8 -*-

from odoo import models, fields, api

class CaseMonitoring(models.Model):
    _inherit = 'case.monitoring'
    _description = 'Case Monitoring'

    def action_view_monitoring_chart(self):
        action = self.env["ir.actions.actions"]._for_xml_id("asb_helpline_case_monitoring_chart.helpline_case_monitoring_chart_action")
        action['context'] = {
            'active_id': self.id,
            'active_ids': self.ids,
        }
        return action