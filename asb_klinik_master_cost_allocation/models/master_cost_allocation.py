from odoo import _, api, fields, models
    
class MasterAllocation(models.Model):
    _name                   = 'master.cost.allocation'
    _description            = 'Master Cost Allocation'
    _inherit                = ['mail.thread', 'mail.activity.mixin']
    
    name                        = fields.Char( string   = 'Setting Cost Allocation',
                                                default  = 'Setting Cost Allocation',
                                                readonly = True,
                                                store    = False)
    
    name_setting                = fields.Char( string   = 'Setting Cost Alat Kesehatan dan Obat',
                                                default  = 'Setting Cost Alat Kesehatan dan Obat',
                                                readonly = True,
                                                store    = False)
    
    direct_cost_allocation      = fields.Float( string   = 'Direct Cost (%)', 
                                                required = True,
                                                tracking = True)
    
    fixed_cost_allocation       = fields.Float( string   = 'Fixed Cost (%)', 
                                                required = True,
                                                tracking = True)
    
    profit_margin_allocation    = fields.Float(  string   = 'Profit Margin (%)', 
                                                 required = True,
                                                 tracking = True)
    
    profit_margin_product       = fields.Float(  string   = 'Profit Margin (%)', 
                                                 required = True,
                                                 tracking = True)
    
    ppn_product                 = fields.Float(  string   = 'PPn Product (%)', 
                                                 required = True,
                                                 tracking = True)
    
    # Halaman untuk Cost Allocation
    @api.model
    def _get_mysetting(self):
        action = self.env.ref('asb_klinik_master_cost_allocation.master_cost_allocation_action').read()[0]
        action.update ({
            'name': 'Master Cost Allocation',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'master.cost.allocation',
            'res_id': self.env['master.cost.allocation'].search([], limit=1).id or self.id,
            'view_id': self.env.ref('asb_klinik_master_cost_allocation.master_cost_allocation_view_form').id,
            'context': {'no_create': True}
        })
        return action
    