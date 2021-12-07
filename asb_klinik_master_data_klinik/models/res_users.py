from odoo import _, api, fields, models

class ResUsers(models.Model):
    _inherit            = 'res.users'
    _description        = 'Res Users'
    
    # Halaman yang muncul ketika pertama kali Login
    @api.model
    def _get_mysetting(self):
        action = self.env.ref('asb_klinik_master_data_klinik.profile_user_action').read()[0]
        action.update ({
            'name'      : 'Profile User',
            'type'      : 'ir.actions.act_window',
            'view_mode' : 'form',
            'res_model' : 'res.users',
            'res_id'    : self.env.user.id,
            'target'    : 'fullscreen',
            'view_id'   : self.env.ref('asb_klinik_master_data_klinik.profile_user_view_form').id,
            'context'   : {'no_create': True}
        })
        return action
    
    # Halaman Profile User
    @api.model
    def _get_myprofile(self):
        action = self.env.ref('asb_klinik_master_data_klinik.profile_user_menu_action').read()[0]
        action.update ({
            'name'      : 'Profile User',
            'type'      : 'ir.actions.act_window',
            'view_mode' : 'form',
            'res_model' : 'res.users',
            'res_id'    : self.env.user.id,
            'target'    : 'current',
            'view_id'   : self.env.ref('asb_klinik_master_data_klinik.profile_user_menu_view_form').id,
            'context'   : {'no_create': True}
        })
        return action
    
    # Action untuk Menuju Halaman Main Menu
    def action_main_menu(self):
        if self.faskes_id:
            view_id = self.env.ref('asb_klinik_master_data_klinik.profile_user_menu_view_form').id,
            return {
                'type': 'ir.actions.act_window',
                'name': 'Profile User',
                'view_mode': 'form',
                'res_model': 'res.users',
                'target': 'main',
                'res_id': self.env.user.id,
                'views': [[view_id, 'form']],
            }
        else: 
            return{ 'warning' : 
                    {
                        'title': "Invalid Data Check - In",
                        'message': "Pilih Klinik Terlebih Dahulu untuk Data Check - In"
                    }}