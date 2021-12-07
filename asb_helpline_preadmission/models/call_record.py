from odoo import models, fields, api
from datetime import date, timedelta

class CallRecord(models.Model):
    _inherit = 'call.record'
    
    create_preadmission = fields.Boolean(string='Preadmission Created')
    
    def action_create_preadmission(self):
        for rec in self:
            rec.create_preadmission = True
            preadmission = self.env['pre.admission'].create({
                'call_id' : rec.id,
                'member' : rec.member,
                'card_number_id' : rec.card_number_id.id,
                'name' : rec.member_name,
                'member_id' : rec.member_id.id,
                'client_id' : rec.client_id.id,
                'provider_id' : rec.provider_id.id,
                'receive_date': date.today(),
            })
        res = self.env['ir.actions.act_window']._for_xml_id('asb_helpline_preadmission.call_record_preadmission_smart_button')
        res['res_id'] = preadmission.id
        return res
    
    def preadmission_smart_button(self):
        res = self.env['ir.actions.act_window']._for_xml_id('asb_helpline_preadmission.call_record_preadmission_smart_button')
        preadmission = self.env['pre.admission'].search([('call_id','=',self._origin.id)])
        res['res_id'] = preadmission.id
        return res    
