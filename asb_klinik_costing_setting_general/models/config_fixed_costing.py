from odoo import _, api, fields, models
from odoo.exceptions import UserError

class ConfigFixedCosting(models.Model):
    _name               = 'config.fixed.costing'
    _description        = 'Config Fixed Costing'
    _inherit            = ['mail.thread', 'mail.activity.mixin']
    
    name                = fields.Char( string   = 'Nama Fixed Costing', 
                                       required = True,
                                       tracking = True)
    
    cost_in_house       = fields.Float( string   = 'Cost in House', 
                                        digits   = (10,2), required = True,
                                        tracking = True)
    
    cost_onsite         = fields.Float( string   = 'Cost Onsite', 
                                        digits   = (10,2), required = True,
                                        tracking = True)
    
    updated_date        = fields.Date(  string       = 'Updated Date', 
                                        default      = fields.Date.today(),
                                        readonly     = True,
                                        store        = True,
                                        tracking     = True)
    
    updated_user        = fields.Many2one( 'res.users', 
                                            string    = 'Updated By',
                                            default   = lambda self: self.env.user, 
                                            readonly  = True, 
                                            store     = True,
                                            index     = True,
                                            tracking  = True)

class ConfigFixedCostingLine(models.Model):
    _name                   = 'config.fixed.costing.line'
    _description            = 'Config Fixed Costing Line'
    
    fixed_costing_id        = fields.Many2one( 'config.fixed.costing',
                                                string   = 'Nama Fixed Costing',
                                                index    = True,
                                                required = True)
    
    name                    = fields.Char( string   = 'Nama Fixed Costing',
                                           required = True,
                                           store    = True)
    
    cost_in_house           = fields.Float( string  = 'Cost in House', 
                                            digits  = (10,2),
                                            store   = True)
    
    cost_onsite             = fields.Float( string  = 'Cost Onsite', 
                                            digits  = (10,2),
                                            store   = True)
