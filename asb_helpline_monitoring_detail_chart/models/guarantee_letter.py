# -*- coding: utf-8 -*-

from odoo import models, fields, api


class GuaranteeLetter(models.Model):
    _inherit = 'guarantee.letter'

    def action_view_monitoring_chart(self):
        action = self.env["ir.actions.actions"]._for_xml_id("asb_helpline_monitoring_detail_chart.helpline_monitoring_detail_chart_action")
        action['context'] = {
            'active_id': self.id,
            'active_ids': self.ids,
        }
        return action

    def get_monitoring_detail_data(self):
        detail_ids = self.env['monitoring.detail'].search([('letter_id', '=', self._origin.id)])
        title = 'General Condition'

        sistole, diastole, temperature, heart_rate, respiratory_rate, date_labels = [], [], [], [], [], []

        for detail in detail_ids:
            sistole.append(detail.sistole)
            diastole.append(detail.diastole)
            temperature.append(detail.temperature)
            heart_rate.append(detail.heart_rate)
            respiratory_rate.append(detail.respiratory_rate)
            date_labels.append(detail.last_fu)

        result = {
            'labels': date_labels,
            'sistole': sistole,
            'diastole': diastole,
            'temperature': temperature,
            'heart_rate': heart_rate,
            'respiratory_rate': respiratory_rate,
            'case_number': self.gl_number or '',
            'title': title,
        }
        return result

    def action_view_billing_chart(self):
        action = self.env["ir.actions.actions"]._for_xml_id("asb_helpline_monitoring_detail_chart.helpline_billing_chart_action")
        action['context'] = {
            'active_id': self.id,
            'active_ids': self.ids,
        }
        return action

    def get_billing_data(self):
        detail_ids = self.env['monitoring.detail'].search([('letter_id', '=', self._origin.id)])
        title = 'Billing'
        currency_label = detail_ids.currency_id.symbol or ''

        billing, date_labels = [], []

        for detail in detail_ids:
            billing.append(detail.billing)
            date_labels.append(detail.last_fu)

        result = {
            'labels': date_labels,
            'billing': billing,
            'case_number': self.gl_number or '',
            'currency_label': currency_label,
            'title': title,
        }
        return result
