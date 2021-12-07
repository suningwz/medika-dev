from odoo import _, api, fields, models

class ListPackage(models.Model):
    _inherit = 'list.package'
    _description = 'List Package'

    def open_form(self):
        view_id = self.env.ref('asb_helpline_call_record_information.information_list_package_house_view_form').id
        return {
            'name': 'Package MCU',
            'view_type': 'form',
            'views': [(view_id, 'form')],
            'res_model': 'list.package',
            'view_id': view_id,
            'type': 'ir.actions.act_window',
            'res_id': self.id,
            'target': 'new',
            'context': "{'create': False}",
            'flags': {'mode': 'readonly'}
        }

    def download_examination(self):
        return self.env.ref('asb_helpline_call_record_information.action_print_list_package_mcu').report_action(self)
    
