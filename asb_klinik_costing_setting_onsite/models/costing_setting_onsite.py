from odoo import _, api, fields, models

class CostingSettingOnsite(models.Model):
    _name                       = 'costing.setting.onsite'
    _description                = 'Costing Setting Onsite'
    _inherit                    = ['mail.thread', 'mail.activity.mixin']
    
    name                        = fields.Char(  string   = 'Setting Costing Onsite',
                                                default  = 'Setting Costing Onsite',
                                                readonly = True,
                                                store    = False)
    
    team_member_line            = fields.One2many(  'config.team.member', 
                                                    'setting_onsite_id', 
                                                    string   = 'Team Member Line',
                                                    tracking = True)
    
    equipment_status_line       = fields.One2many( 'config.equipment.list', 
                                                   'setting_onsite_id', 
                                                   string   = 'Equipment Status Line',
                                                   tracking = True)
    
    transportasi_akomodasi_line = fields.One2many( 'config.transportasi.akomodasi', 
                                                   'setting_onsite_id', 
                                                   string   = 'Transportasi / Akomodasi Line',
                                                   tracking = True)
    
    # Tampilan untuk Setting Costing Onsite
    @api.model
    def _get_setting_onsite(self):
        action = self.env.ref('asb_klinik_costing_setting_onsite.costing_setting_onsite_action').read()[0]
        action.update ({
            'name': 'Setting Costing Onsite',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'costing.setting.onsite',
            'res_id': self.env['costing.setting.onsite'].search([], limit=1).id or self.id,
            'view_id': self.env.ref('asb_klinik_costing_setting_onsite.costing_setting_onsite_view_form').id,
            'context': {'no_create': True}
        })
        return action

class ConfigTeamMember(models.Model):
    _inherit            = 'config.team.member'
    _description        = 'Config Team Member'
    
    setting_onsite_id   = fields.Many2one( 'costing.setting.onsite', 
                                            string     = 'Setting Onsite',
                                            index      = True,
                                            ondelete   = 'cascade')
    
class ConfigEquipmentList(models.Model):
    _inherit            = 'config.equipment.list'
    _description        = 'Config Equipment List'
    
    setting_onsite_id   = fields.Many2one( 'costing.setting.onsite', 
                                            string     = 'Setting Onsite',
                                            index      = True,
                                            ondelete   = 'cascade')

class ConfigTransportasiAkomodasi(models.Model):
    _inherit            = 'config.transportasi.akomodasi'
    _description        = 'Config Transportasi Akomodasi'
    
    setting_onsite_id   = fields.Many2one( 'costing.setting.onsite', 
                                            string     = 'Setting Onsite',
                                            index      = True,
                                            ondelete   = 'cascade')
    
    
    