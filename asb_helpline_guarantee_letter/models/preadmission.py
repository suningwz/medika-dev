from odoo import models, fields, api

class PreAdmission(models.Model):
    _inherit = 'pre.admission'

    create_gl = fields.Boolean(string='GL created')

    def action_process(self):
        for rec in self:
            letter = []
            if self.call_id:
                letter = self.env['guarantee.letter'].search([('call_id','=',self.call_id.id)])
            if not letter:
                parent = self.env['res.partner'].search([('suffix_id.name','=','A'),('member_number','=',rec.member_id.member_number)])
                letter = self.env['guarantee.letter'].create({
                    'preadmission_id' : rec._origin.id,
                    'call_id' : rec.call_id.id,
                    'member' : rec.member,
                    'card_number_id' : rec.card_number_id.id,
                    'member_id' : rec.member_id.id,
                    'name' : rec.name,
                    'nik' : '%s / %s' % (rec.member_id.nik, parent.name),
                    'relationship' : rec.member_id.relationship,
                    'dob' : rec.member_id.birth_date,
                    'client_id' : rec.member_id.member_client_id.id,
                    'client_branch_id' : rec.member_id.client_branch_id.id,
                    'program_id' : rec.member_id.program_id.id,
                    'plan_id' : rec.member_id.program_plan_id.id,
                    'provider_id' : rec.provider_id.id,
                    'admission_date' : rec.admission_date,
                    'service_type' : rec.service_type,
                    'remarks' : rec.remarks,
                })
                rec.call_id.create_gl = True
            rec.create_gl = True
            rec.write({'state': 'process'})
        res = self.env['ir.actions.act_window']._for_xml_id('asb_helpline_guarantee_letter.preadmission_gl_smart_button')
        res['res_id'] = letter.id
        return res  
    
    def gl_smart_button(self):
        res = self.env['ir.actions.act_window']._for_xml_id('asb_helpline_guarantee_letter.preadmission_gl_smart_button')
        if self.call_id:
            gl = self.env['guarantee.letter'].search([('call_id','=',self.call_id.id)])
        else:
            gl = self.env['guarantee.letter'].search([('preadmission_id','=',self._origin.id)])
        res['res_id'] = gl.id
        return res  