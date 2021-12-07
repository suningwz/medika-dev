# -*- coding: utf-8 -*-

# import odoo.exceptions
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta

class EclaimUserProductivity(models.Model):
    _name = 'eclaim.user.productivity'
    _description = 'Eclaim User Productivity'
    
    name = fields.Char(string='Name')

    # Qweb method
    def _qweb_prepare_qcontext(self, view_id, domain):
        values = super(EclaimUserProductivity, self)._qweb_prepare_qcontext(view_id, domain)
        values.update(self._get_productivity_values_today())
        return values

    def _get_productivity_values_today(self):
        eclaim_user = []
        eclaim = self.env['res.groups'].search([('name','=','User E-Claim')])
        for user in eclaim.users:
            ip_point = 0
            op_point = 0
            de_point = 0
            ot_point = 0
            ma_point = 0
            mcu_point = 0
            total_point = 0
            for productivity in user.user_productivity_line:
                if productivity.eclaim_category == 'ip':
                    ip_point += productivity.point
                if productivity.eclaim_category == 'op':
                    op_point += productivity.point
                if productivity.eclaim_category == 'de':
                    de_point += productivity.point
                if productivity.eclaim_category == 'ot':
                    ot_point += productivity.point
                if productivity.eclaim_category == 'ma':
                    ma_point += productivity.point
                if productivity.eclaim_category == 'mcu':
                    mcu_point += productivity.point
                total_point = ip_point + op_point + de_point + ot_point + ma_point + mcu_point

            eclaim_user.append({
                'name' : user.name,
                'ip' : ip_point,
                'op' : op_point,
                'de' : de_point,
                'ot' : ot_point,
                'ma' : ma_point,
                'mcu' : mcu_point,
                'total' : total_point,
                })
        dashboard = {
            'name': self.name,
            'eclaim_user': eclaim_user,
            'datetime': (datetime.now() + timedelta(hours=7)).strftime('%A, %d %B %H:%M:%S')
        }
        return dashboard