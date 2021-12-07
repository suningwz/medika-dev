from odoo import models, fields, api

class ConfirmSendEmail(models.TransientModel):
    _name = 'confirm.send.email'
    _description = 'Confirm Send Email'
    
    guarantee_letter_id = fields.Many2one('guarantee.letter', string='Guarantee Letter')
    type_letter = fields.Selection([
        ('initial_gl', 'Initial GL'),
        ('final_gl', 'Final GL'),
    ], string='Type Letter')

    def send_by_email(self):
        for rec in self.guarantee_letter_id:
            if self.type_letter == 'initial_gl':
                template_id = self.env.ref('asb_helpline_guarantee_letter.initial_gl_email_template').id
                template = self.env['mail.template'].browse(template_id)
                template.send_mail(rec.id, force_send=True)
            elif self.type_letter == 'final_gl':
                template_id = self.env.ref('asb_helpline_guarantee_letter.final_gl_email_template').id
                template = self.env['mail.template'].browse(template_id)
                template.send_mail(rec.id, force_send=True)
