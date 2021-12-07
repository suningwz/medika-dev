from odoo import models, fields, api

class GuaranteeLetter(models.Model):
    _inherit = 'guarantee.letter'
    _description = 'Guarantee Letter'
    
    case_monitoring_line = fields.One2many('case.monitoring', 'letter_id', string='Case Monitoring')

    # @api.model
    # def create(self, values):
    #     res = super(GuaranteeLetter, self).create(values)
    #     if res.header_id.benefit_category_id.helpline == True:
    #         diagnosis = []
    #         for diag in res.diagnosis_ids:
    #             diagnosis.append((4,diag.id))
    #         case = self.env['case.monitoring'].create({
    #             'letter_id' : res._origin.id,
    #             'member' : res.member,
    #             'card_number_id' : res.card_number_id.id,
    #             'member_id' : res.member_id.id,
    #             'nik' : res.member_id.nik,
    #             'dob' : res.member_id.birth_date,
    #             'client_id' : res.member_id.member_client_id.id,
    #             'name' : res.name,
    #             'diagnosis_ids' : diagnosis
    #         })
    #     return res