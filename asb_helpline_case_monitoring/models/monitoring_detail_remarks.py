from odoo import models, fields, api, _

class MonitoringDetailRemarks(models.TransientModel):
    _name = 'monitoring.detail.remarks'
    _description = ' Monitoring Detail Remarks Wizard'
    
    name = fields.Char(string='Name')
    remarks = fields.Char(string='Remarks')
    detail_id = fields.Many2one('monitoring.detail', string='Detail')

    def add_remarks(self):
        cost_containment_lines = []
        for rec in self:
            cost_containment = {
                    'name' : rec.name,
                    'remarks': rec.remarks,
                    'detail_id': rec.detail_id._origin.id,
                }
            cost_containment_lines.append((0, 0, cost_containment))
            if rec.name == 'Upcoding':
                rec.detail_id.upcoding = True
            if rec.name == 'Unbundling':
                rec.detail_id.unbundling = True
            if rec.name == 'Time in OR':
                rec.detail_id.time_in_or = True
            if rec.name == 'Phantom Billing':
                rec.detail_id.phantom_billing = True
            if rec.name == 'Self-Referrals':
                rec.detail_id.self_referrals = True
            if rec.name == 'Cancelled Service':
                rec.detail_id.cancelled_service = True
            if rec.name == 'Inflated Hospital Bills':
                rec.detail_id.inflated_hospital = True
            if rec.name == 'Incorrect Charge for Type Room':
                rec.detail_id.incorrect_charge = True
            if rec.name == 'Unnecessary Treatment':
                rec.detail_id.unnecessary_treatment = True
            rec.detail_id.cost_containment_line = cost_containment_lines