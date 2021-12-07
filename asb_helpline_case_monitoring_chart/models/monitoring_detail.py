# -*- coding: utf-8 -*-

from odoo import models, fields, api

class CaseMonitoring(models.Model):
    _inherit = 'case.monitoring'
    _description = 'Case Monitoring'
    
    def get_monitoring_detail_data(self):
        detail_ids = self.env['monitoring.detail'].search([('case_id','=',self._origin.id)])
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
            'case_number': self.case_number or '',
            'title': title,
        }
        return result