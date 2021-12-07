from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class ResPartner(models.Model):
    _inherit = 'res.partner'
    _description = 'Res Partner'

    def delete_member(self):
        res = self.env['ir.actions.act_window']._for_xml_id('asb_member_deleted.action_remarks_member_deleted_wizard')
        res['context'] = {'default_partner_ids': self.ids}
        return res

    # override unlink ResPartner
    # def unlink(self):
    #     return super(ResPartner, self).unlink()


class RemarksMemberDeleted(models.TransientModel):
    _name = 'remarks.member.deleted'
    _description = 'Remarks Member Deleted'

    name = fields.Char(string='Remarks', required=True, )
    partner_ids = fields.Many2many('res.partner', string='Partner')

    def delete_member(self):
        for rec in self:
            for member in rec.partner_ids:
                self.env['member.deleted'].create({
                    'record_type': member.record_type,
                    'payor_id': member.payor_id,
                    'member_client_id': member.member_client_id.id,
                    'client_branch_id': member. client_branch_id.id,
                    'policy_number': member.policy_number,
                    'nik': member.nik,
                    'card_number': member.card_number,
                    'member_number': member.member_number,
                    'suffix_id': member.suffix_id.id,
                    'name': member.name,
                    'birth_date': member.birth_date,
                    'gender': member.gender,
                    'join_date': member.join_date,
                    'start_date': member.start_date,
                    'effective_date_member': member.effective_date_member,
                    'end_date': member.end_date,
                    'end_policy_date': member.end_policy_date,
                    'division': member.division,
                    'division_id': member.division_id,
                    'swift_code': member.swift_code,
                    'bank_id': member.bank_id.id,
                    'bank_account': member.bank_account,
                    'account_name': member.account_name,
                    'bank_branch': member.bank_branch,
                    'marital_status': member.marital_status,
                    'relationship': member.relationship,
                    'street': member.street,
                    # 'street2': address2,
                    'city_id': member.city_id.id,
                    'state_id': member.state_id.id,
                    'zip': member.zip,
                    'tlp_office': member.tlp_office,
                    'tlp_residence': member.tlp_residence,
                    'mobile': member.mobile,
                    'passport_no': member.passport_no,
                    'passport_country': member.passport_country,
                    'email': member.email,
                    'employment_status': member.employment_status,
                    'salary': member.salary,
                    'pre_existing': member.pre_existing,
                    'remarks': member.remarks,
                    'endorsement_date': member.endorsement_date,
                    'member_since': member.member_since,
                    'policy_status': member.policy_status,
                    'member_suspend': member.member_suspend,
                    'renewal_activation_date': member.renewal_activation_date,
                    'program_id': member.program_id.id,
                    'program_plan_id': member.program_plan_id.id,
                    'remarks': rec.name,
                })
                member.unlink()
