# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime

class HelplineActivityLog(models.Model):
    _name = 'helpline.activity.log'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
    _description = 'Activity Log'
    _rec_name = 'description'
    
    description = fields.Char(string='Description')
    letter_id = fields.Many2one('guarantee.letter', string='Letter ID')
    contact_type = fields.Selection([
        ('admission', 'Admission'),
        ('pending', 'Analyst Pending Process'),
        ('start', 'Analyst Start Process'),
        ('approval', 'Approval Letter'),
        ('care', 'Customer Care'),
        ('care_in-telephone', 'Customer Care In-Telephone'),
        ('care_in-whatsapp', 'Customer Care In-WhatsApp'),
        ('care_out-telephone', 'Customer Care Out-Telephone'),
        ('care_out-whatsapp', 'Customer Care Out-WhatsApp'),
        ('survey', 'Customer Survey'),
        ('dispensasi', 'Dispensasi'),
        ('incomplete', 'Document Not Complete'),
        ('ex-gratia', 'Ex-Gratia'),
        ('treatment', 'Follow Up Treatment'),
        ('vital', 'Follow Up Vital Sign'),
        ('in-email', 'In-Email'),
        ('in-fax', 'In-Fax'),
        ('in-sms', 'In-SMS'),
        ('in-telephone', 'In-Telephone'),
        ('in-whatsapp', 'In-Whatsapp'),
        ('lma', 'Incoming HAF/LMA'),
        ('investigation', 'Investigation'),
        ('enquiry', 'Medical Enquiry'),
        ('monitoring', 'Monitoring'),
        ('note', 'Note'),
        ('out-email', 'Out-Email'),
        ('out-fax', 'Out-Fax'),
        ('out-sms', 'Out-SMS'),
        ('out-telephone', 'Out-Telephone'),
        ('out-telephone', 'Out-Telephone Not Success'),
        ('out-whatsapp', 'Out-Whatsapp'),
        ('provider', 'Provider'),
        ('cc', 'Refer to CC'),
        ('reference', 'Reference'),
        ('request_admin', 'Request to Admin'),
        ('letter', 'Send Approval Letter'),
        ('system', 'System-Generated'),
        ('blast', 'System-SMS Blast'),
        ('borderline', 'Technical Borderline'),
    ], string='Contact Type')
    contact_info = fields.Char(string='Contact Info')
    contact_person = fields.Char(string='Contact Person')
    status = fields.Char(string='Status')
    created_date = fields.Datetime(string='Created Date', default=lambda self: fields.datetime.now(), readonly=True, tracking=True)
    created_by = fields.Many2one('res.users', string='Created By', default=lambda self: self.env.user.id, readonly=True, tracking=True)
    edited_date = fields.Datetime(string='Edited Date', readonly=True, tracking=True)
    edited_by = fields.Many2one('res.users', string='Edited By', tracking=True)

# class GuaranteeLetter(models.Model):
#     _inherit = 'guarantee.letter'
#     _description = 'Guarantee Letter'
    
#     activity_line = fields.One2many('helpline.activity.log', 'letter_id', string='Activity Log')
#     def activity_log(self):
#         for rec in self:
#             res = self.env['ir.actions.act_window']._for_xml_id('asb_helpline_activity_log.helpline_activity_log_action_window')
#             res['domain'] = [('letter_id', '=', rec._origin.id)]
#             res['context'] = {'default_letter_id': rec._origin.id}
#             res['target'] = 'main'
#             return res

#     @api.model
#     def create(self, vals):
#         res = super(GuaranteeLetter, self).create(vals)
#         activity = res.env['helpline.activity.log'].create({
#             'letter_id': res._origin.id,
#             })
#         # res.call_record_line = [(4,activity.id)]
#         return res
