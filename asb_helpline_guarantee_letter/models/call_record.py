from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class CallRecord(models.Model):
    _inherit = 'call.record'

    no_preadmission = fields.Boolean(string='Preadmission Skipped')
    
    create_gl = fields.Boolean(string='GL created')
    def action_create_gl(self):
        for rec in self:
            letter = self.env['guarantee.letter'].search([('call_id','=',self._origin.id)])
            if not letter:
                letter = self.env['guarantee.letter'].create({
                    'call_id' : rec._origin.id,
                    'claim_source' : 'eclaim',
                    'member' : rec.member,
                    'card_number_id' : rec.card_number_id.id,
                    'member_id' : rec.member_id.id,
                    'name' : rec.member_name,
                    'nik' : rec.nik,
                    'dob' : rec.member_id.birth_date,
                    'provider_id' : rec.provider_id.id,
                    'client_id' : rec.client_id.id,
                    'client_branch_id' : rec.member_id.client_branch_id.id,
                    'program_id' : rec.member_id.program_id.id,
                    'plan_id' : rec.member_id.program_plan_id.id,
                    'benefit' : rec.member_id.program_plan_id.name,
                    'member_number' : rec.member_id.member_number,
                    'gender' : rec.member_id.gender,
                    'relationship' : rec.relationship,
                    'suffix_id' : rec.member_id.suffix_id.id,
                    'marital_status' : rec.member_id.marital_status,
                    'policy_number' : rec.member_id.policy_number,
                    'join_date' : rec.member_id.join_date,
                    'start_date' : rec.member_id.start_date,
                    'effective_date_member' : rec.member_id.effective_date_member,
                    'end_date' : rec.member_id.end_date,
                    'end_policy_date' : rec.member_id.end_policy_date,
                    'policy_status' : rec.member_id.policy_status,
                })
                rec.create_gl = True
                rec.state = 'close'
        res = self.env['ir.actions.act_window']._for_xml_id('asb_helpline_guarantee_letter.call_record_gl_smart_button')
        res['res_id'] = letter.id
        res['target'] = 'main'
        res['context'] = {'form_view_initial_mode': 'edit'}
        return res

    def action_create_preadmission(self):
        for rec in self:
            letter = self.env['guarantee.letter'].search([('call_id','=',self._origin.id)])
            if not letter:
                letter = self.env['guarantee.letter'].create({
                    'preadmission' : True,
                    'preadmission_state' : 'open',
                    'call_id' : rec._origin.id,
                    'claim_source' : 'eclaim',
                    'member' : rec.member,
                    'card_number_id' : rec.card_number_id.id,
                    'member_id' : rec.member_id.id,
                    'name' : rec.member_name,
                    'nik' : rec.nik,
                    'dob' : rec.member_id.birth_date,
                    'provider_id' : rec.provider_id.id,
                    'client_id' : rec.client_id.id,
                    'client_branch_id' : rec.member_id.client_branch_id.id,
                    'program_id' : rec.member_id.program_id.id,
                    'plan_id' : rec.member_id.program_plan_id.id,
                    'benefit' : rec.member_id.program_plan_id.name,
                    'member_number' : rec.member_id.member_number,
                    'gender' : rec.member_id.gender,
                    'relationship' : rec.relationship,
                    'suffix_id' : rec.member_id.suffix_id.id,
                    'marital_status' : rec.member_id.marital_status,
                    'policy_number' : rec.member_id.policy_number,
                    'join_date' : rec.member_id.join_date,
                    'start_date' : rec.member_id.start_date,
                    'effective_date_member' : rec.member_id.effective_date_member,
                    'end_date' : rec.member_id.end_date,
                    'end_policy_date' : rec.member_id.end_policy_date,
                    'policy_status' : rec.member_id.policy_status,
                })
                rec.create_gl = True
                rec.state = 'close'
        res = self.env['ir.actions.act_window']._for_xml_id('asb_helpline_guarantee_letter.call_record_gl_smart_button')
        res['res_id'] = letter.id
        res['target'] = 'main'
        res['context'] = {'form_view_initial_mode': 'edit'}
        return res

    def claim_history(self):
        for rec in self:
            if not rec.member or not rec.member_id:
                raise ValidationError (_("Member field is false"))
            res = self.env['ir.actions.act_window']._for_xml_id('asb_helpline_guarantee_letter.gl_case_history_smart_button')
            res['domain'] = [('member_id', '=', rec.member_id.id)]
            res['target'] = 'main'
            return res

    def gl_smart_button(self):
        res = self.env['ir.actions.act_window']._for_xml_id('asb_helpline_guarantee_letter.call_record_gl_smart_button')
        gl = self.env['guarantee.letter'].search([('call_id','=',self._origin.id)])
        res['res_id'] = gl.id
        return res  