from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class MonitoringDetail(models.Model):
    _name = 'monitoring.detail'
    _description = 'Monitoring Detail'
    
    name = fields.Char(string='Subjective', required="1")
    letter_id = fields.Many2one('guarantee.letter', string='Letter ID')
    upcoding = fields.Boolean(string='Upcoding')
    unbundling = fields.Boolean(string='Unbundling')
    time_in_or = fields.Boolean(string='Time in OR')
    phantom_billing = fields.Boolean(string='Phantom Billing')
    self_referrals = fields.Boolean(string='Self-Referrals')
    cancelled_service = fields.Boolean(string='Cancelled Service')
    inflated_hospital = fields.Boolean(string='Inflated Hospital Bills')
    incorrect_charge = fields.Boolean(string='Incorrect Charge for Type Room')
    unnecessary_treatment = fields.Boolean(string='Unnecessary Treatment')
    sistole = fields.Float(string='Sistole')
    diastole = fields.Float(string='Diastole')
    temperature = fields.Float(string='Temperature')
    physical_examination = fields.Char(string='Physical Examination')
    laboratory = fields.Char(string='Laboratory')
    imaging = fields.Char(string='Imaging')
    other = fields.Char(string='Other Treatment')
    drugs = fields.Char(string='Drugs')
    heart_rate = fields.Float(string='Heart Rate')
    respiratory_rate = fields.Float(string='Respiratory Rate')
    infusion = fields.Char(string='Infusion')
    physical_examination_date = fields.Date(string='Physical Examination Date')
    laboratory_date = fields.Date(string='Laboratory Date')
    imaging_date = fields.Date(string='Imaging Date')
    other_date = fields.Date(string='Other Treatment Date')
    billing = fields.Float(string='Billing')
    plan_discharge = fields.Char(string='Plan Discharge')
    informer = fields.Char(string='Informer')
    diagnosis = fields.Char(string='Diagnosis')
    date_discharge = fields.Date(string='Date Discharge')
    department_informer = fields.Char(string='Department Informer')
    last_fu = fields.Date(string='Last Follow Up')
    file_upload = fields.Binary(string='File')
    filename = fields.Char(string='Filename')
    remarks = fields.Char(string='Remarks')
    cost_containment_line = fields.One2many('cost.containment.line', 'detail_id', string='Cost Containment', ondelete="cascade")
    currency_id = fields.Many2one('res.currency', 'Currency', default=lambda self: self.env.user.company_id.currency_id.id, required=True, tracking=True)
    type_selection = fields.Selection([
        ('key', 'value')
    ], string='Type')
    state = fields.Selection([
        ('pending', 'Pending'),
        ('process', 'On Process'),
        ('close', 'Closed'),
    ], string='Status', default="pending")

    def action_process(self):
        return self.write({'state': 'process'})

    def action_close(self):
        return self.write({'state': 'close'})

    def action_add_remarks(self):
        if self.upcoding == True:
            return False
        return {
            'name': "Remarks",
            'type': 'ir.actions.act_window',
            'res_model': 'monitoring.detail.remarks',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_detail_id': self._origin.id,
                }
            }

    def action_add_remarks_unbundling(self):
        if self.unbundling == True:
            return False
        res = self.env['ir.actions.act_window']._for_xml_id('asb_helpline_monitoring_detail.monitoring_detail_remarks_action_wizard')
        return res

    def action_add_remarks_time_in_or(self):
        if self.time_in_or == True:
            return False
        res = self.env['ir.actions.act_window']._for_xml_id('asb_helpline_monitoring_detail.monitoring_detail_remarks_action_wizard')
        return res

    def action_add_remarks_phantom_billing(self):
        if self.phantom_billing == True:
            return False
        res = self.env['ir.actions.act_window']._for_xml_id('asb_helpline_monitoring_detail.monitoring_detail_remarks_action_wizard')
        return res

    def action_add_remarks_self_referrals(self):
        if self.self_referrals == True:
            return False
        res = self.env['ir.actions.act_window']._for_xml_id('asb_helpline_monitoring_detail.monitoring_detail_remarks_action_wizard')
        return res

    def action_add_remarks_cancelled_service(self):
        if self.cancelled_service == True:
            return False
        res = self.env['ir.actions.act_window']._for_xml_id('asb_helpline_monitoring_detail.monitoring_detail_remarks_action_wizard')
        return res

    def action_add_remarks_inflated_hospital(self):
        if self.inflated_hospital == True:
            return False
        res = self.env['ir.actions.act_window']._for_xml_id('asb_helpline_monitoring_detail.monitoring_detail_remarks_action_wizard')
        return res

    def action_add_remarks_incorrect_charge(self):
        if self.incorrect_charge == True:
            return False
        res = self.env['ir.actions.act_window']._for_xml_id('asb_helpline_monitoring_detail.monitoring_detail_remarks_action_wizard')
        return res

    def action_add_remarks_unnecessary_treatment(self):
        if self.unnecessary_treatment == True:
            return False
        res = self.env['ir.actions.act_window']._for_xml_id('asb_helpline_monitoring_detail.monitoring_detail_remarks_action_wizard')
        return res


        #delete
    case_id = fields.Many2one('case.monitoring', string='Case Monitoring')
    created_date = fields.Datetime(string='Created Date', default=lambda self: fields.datetime.now(), readonly=True, tracking=True)
    created_by = fields.Many2one('res.users', string='Created By', default=lambda self: self.env.user.id, readonly=True, tracking=True)

class CostContainmentLine(models.Model):
    _name = 'cost.containment.line'
    _description = 'Cost Containment Line'

    name = fields.Char(string='Name')
    remarks = fields.Char(string='Remarks')
    detail_id = fields.Many2one('monitoring.detail', string='Detail')

    def unlink(self):
        for rec in self:
            if rec.detail_id:
                if rec.name == 'Upcoding':
                    rec.detail_id.upcoding = False
                if rec.name == 'Unbundling':
                    rec.detail_id.unbundling = False
                if rec.name == 'Time in OR':
                    rec.detail_id.time_in_or = False
                if rec.name == 'Phantom Billing':
                    rec.detail_id.phantom_billing = False
                if rec.name == 'Self-Referrals':
                    rec.detail_id.self_referrals = False
                if rec.name == 'Cancelled Service':
                    rec.detail_id.cancelled_service = False
                if rec.name == 'Inflated Hospital Bills':
                    rec.detail_id.inflated_hospital = False
                if rec.name == 'Incorrect Charge for Type Room':
                    rec.detail_id.incorrect_charge = False
                if rec.name == 'Unnecessary Treatment':
                    rec.detail_id.unnecessary_treatment = False
        return super(CostContainmentLine, self).unlink()