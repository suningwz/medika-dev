# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from datetime import date
from odoo.exceptions import ValidationError

class ClientActivity(models.Model):
    _name = 'client.activity'
    _description = 'Client Activity'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
    _rec_name = 'client_id'
    
    client_id = fields.Many2one('res.partner', string='Client', tracking=True)
    datetime = fields.Datetime(string='Date', tracking=True)
    pks = fields.Char(string='PKS No.', tracking=True)
    venue = fields.Text(string='Venue', tracking=True)
    subject = fields.Char(string='Subject', tracking=True)
    participant_ids = fields.Many2many('activity.participant', string='Participants')
    attachment = fields.Many2many('ir.attachment', string='Attachment')
    activity_line = fields.One2many('client.activity.line', 'activity_id', string='Activity')
    created_date = fields.Date(string='Created Date', default=lambda self: fields.datetime.now(), required=True, tracking=True)
    created_by = fields.Many2one('res.users', string='Created By', default=lambda self: self.env.user.id, required=True, tracking=True)
    attachment_number = fields.Integer(compute='_compute_attachment_number', string='Documents')

    def _compute_attachment_number(self):
        attachment_data = self.env['ir.attachment'].read_group(
            [('res_model', '=', 'client.activity'), ('res_id', 'in', self.ids)], ['res_id'], ['res_id'])
        attachment = dict((data['res_id'], data['res_id_count']) for data in attachment_data)
        for activity in self:
            activity.attachment_number = attachment.get(activity.id, 0)

    def action_get_attachment_view(self):
        res = self.env['ir.actions.act_window']._for_xml_id('asb_binary_newtab.action_client_activity_attachment')
        res['domain'] = [('res_model', '=', 'client.activity'), ('res_id', 'in', self.ids)]
        res['context'] = {'default_res_model': 'client.activity', 'default_res_id': self.id}
        return res

    def new_tab(self):
        for rec in self:
            attachment = self.env['ir.attachment'].search(
            [('res_model', '=', 'client.activity'), ('res_id', 'in', self.ids)])
            if len(attachment) > 1 :
                raise ValidationError(_("There are more than 1 attachment"))
            url = '/web/content/%s' % attachment.id
            return {
                'name'     : 'Go to website',
                'type'     : 'ir.actions.act_url',
                'target'   : 'new',
                'url'      : url
                }

class ActivityParticipant(models.Model):
    _name = 'activity.participant'
    _description = 'Activity Participant'
    
    name = fields.Char(string='Name', ondelete="cascade")

class ClientActivityLine(models.Model):
    _name = 'client.activity.line'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
    _description = 'Client Activity Line'
    
    activity_id = fields.Many2one('client.activity', string='Client Activity')
    subject = fields.Char(string='Subject')
    description = fields.Char(string='Description')
    pic = fields.Char(string='Person in Charge')
    due_date = fields.Date(string='Due Date')
    status = fields.Selection([
        ('ongoing', 'Ongoing'),
        ('closed', 'Closed'),
    ], string='Progress Status')
    created_date = fields.Date(string='Created Date', default=lambda self: fields.datetime.now(), required=True, tracking=True)
    created_by = fields.Many2one('res.users', string='Created By', default=lambda self: self.env.user.id, required=True, tracking=True)
