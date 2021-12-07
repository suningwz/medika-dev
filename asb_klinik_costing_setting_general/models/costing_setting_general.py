from odoo import _, api, fields, models

class CostingSettingGeneral(models.Model):
    _name                   = 'costing.setting.general'
    _description            = 'Costing Setting General'
    _inherit                = ['mail.thread', 'mail.activity.mixin']
    
    name                    = fields.Char( string   = 'Setting Costing General',
                                           default  = 'Setting Costing General',
                                           readonly = True,
                                           store    = False)

    fixed_costing_line      = fields.One2many( 'config.fixed.costing', 
                                               'setting_general_id', 
                                               string   = 'Fixed Costing Lines',
                                               tracking = True)
    
    certificate_list_line   = fields.One2many( 'config.certificate.list',
                                               'setting_general_id',
                                               string   = 'Certificate List Lines',
                                               tracking = True)
    
    examination_list_line   = fields.One2many( 'config.examination.list', 
                                               'setting_general_id', 
                                               string   = 'Examination List Lines',
                                               tracking = True)
    
    master_tindakan_ids    = fields.Many2many( 'product.product', 
                                                compute = '_compute_master_tindakan')
    
    # Filter untuk Tindakan / Layanan agar tidak Duplicate
    @api.depends('examination_list_line.master_tindakan_id')
    def _compute_master_tindakan(self):
        for data in self:
            domain = [('is_service', '=', True)]
            if data.examination_list_line:
                domain += [('id', 'not in', [line.master_tindakan_id.id for line in data.examination_list_line])]
            data.master_tindakan_ids = self.env['product.product'].search(domain)
    
    # Tampilan untuk Setting Costing General
    @api.model
    def _get_setting_general(self):
        action = self.env.ref('asb_klinik_costing_setting_general.costing_setting_general_action').read()[0]
        action.update ({
            'name': 'Setting General',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'costing.setting.general',
            'res_id': self.env['costing.setting.general'].search([], limit=1).id or self.id,
            'view_id': self.env.ref('asb_klinik_costing_setting_general.costing_setting_general_view_form').id,
            'context': {'no_create': True}
        })
        return action

class ConfigFixedCosting(models.Model):
    _inherit            = 'config.fixed.costing'
    _description        = 'Config Fixed Costing'
    
    setting_general_id  = fields.Many2one('costing.setting.general', 
                                            string     = 'Setting General',
                                            index      = True,
                                            ondelete   = 'cascade')
    
class ConfigCertificateList(models.Model):
    _inherit            = 'config.certificate.list'
    _description        = 'Config Certificate List'
    
    setting_general_id  = fields.Many2one('costing.setting.general', 
                                            string     = 'Setting General',
                                            index      = True,
                                            ondelete   = 'cascade')

class ConfigExaminationList(models.Model):
    _inherit            = 'config.examination.list'
    _description        = 'Config Examination List'
    
    setting_general_id  = fields.Many2one('costing.setting.general', 
                                            string     = 'Setting General',
                                            index      = True,
                                            ondelete   = 'cascade')
    