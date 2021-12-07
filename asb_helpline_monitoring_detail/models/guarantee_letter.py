from odoo import models, fields, api
from datetime import date

class GuaranteeLetter(models.Model):
    _inherit = 'guarantee.letter'

    monitoring_detail_line = fields.One2many('monitoring.detail', 'letter_id', string='Monitoring Detail')

    @api.onchange('monitoring_detail_line')
    def _onchange_monitoring_detail_line(self):
        for rec in self:
            for detail in rec.monitoring_detail_line:
                if detail.last_fu == date.today():
                    rec.daily_fu = True