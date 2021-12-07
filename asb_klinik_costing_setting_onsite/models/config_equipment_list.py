from odoo import _, api, fields, models
from odoo.exceptions import UserError

class ConfigEquipmentList(models.Model):
    _name            = 'config.equipment.list'
    _description     = 'Config Equipment List'
    _inherit         = ['mail.thread', 'mail.activity.mixin']
    
    name             = fields.Char( string   = "Equipment's Name", 
                                    index    = True,
                                    required = True,
                                    tracking = True)
    
    owned_cost       = fields.Float( string   = 'Owned Cost (IDR)',
                                     digits   = (10,2),
                                     default  = 0.0,
                                     required = True,
                                     tracking = True)
    
    rental_cost      = fields.Float( string   = 'Rental Cost (IDR)',
                                     digits   = (10,2),
                                     default  = 0.0,
                                     required = True,
                                     tracking = True)
    
    updated_date     = fields.Date(  string       = 'Updated Date', 
                                     default      = fields.Date.today(),
                                     readonly     = True,
                                     tracking     = True)
    
    updated_user     = fields.Many2one( 'res.users', 
                                        string    = 'Updated By',
                                        default   = lambda self: self.env.user, 
                                        readonly  = True, 
                                        index     = True,
                                        tracking  = True)
    
    # Check Equipment List sebelum dihapus
    def unlink(self):
        equipment_list_ids          = self.env['config.equipment.list.line'].search([('equipment_list_id', '=' , self.ids)])
        if equipment_list_ids:
            raise UserError(_('Kamu tidak bisa menghapus Data karena Data terhubung dengan Package MCU yang ada')) 
        res = super(ConfigEquipmentList, self).unlink()
        return res

class ConfigEquipmentListLine(models.Model):
    _name               = 'config.equipment.list.line'
    _description        = 'Config Equipment List Line'
    _inherit            = ['mail.thread', 'mail.activity.mixin']
    
    equipment_list_id   = fields.Many2one(  'config.equipment.list', 
                                            string     = 'Equipment', 
                                            index      = True, 
                                            required   = True,
                                            store      = True,
                                            ondelete   = 'cascade',
                                            tracking   = True)
    
    name                = fields.Char(  string   = "Equipment's Name", 
                                        index    = True,
                                        store    = True,
                                        related  = 'equipment_list_id.name',
                                        tracking = True)
    
    owned_cost          = fields.Float( string   = 'Owned Cost (IDR)',
                                        digits   = (10,2),
                                        store    = True,
                                        related  = 'equipment_list_id.owned_cost',
                                        tracking = True)
    
    rental_cost         = fields.Float( string   = 'Rental Cost (IDR)',
                                        digits   = (10,2),
                                        store    = True,
                                        related  = 'equipment_list_id.rental_cost',
                                        tracking = True)
    
    owned_quantity      = fields.Integer ( string   = 'Owned',
                                           default  = 0,
                                           required = True,
                                           tracking = True)
    
    rental_quantity     = fields.Integer( string    = 'Rental',
                                          default   = 0,
                                          required  = True,
                                          tracking  = True)
    
    days                = fields.Integer( string    = 'Days', 
                                          required  = True)
    
    total_price         = fields.Float( string   = 'Total Price (IDR)', 
                                        compute  = '_compute_total_price',
                                        store    = True,
                                        tracking = True)
    
    updated_date        = fields.Date(  string       = 'Updated Date', 
                                        default      = fields.Date.today(),
                                        readonly     = True,
                                        tracking     = True)
    
    updated_user        = fields.Many2one( 'res.users', 
                                            string    = 'Updated By',
                                            default   = lambda self: self.env.user, 
                                            readonly  = True, 
                                            index     = True,
                                            tracking  = True)
    
    # Mendapatkan Total Price dari Equipment List
    @api.depends('owned_quantity', 'rental_quantity', 'owned_cost', 'rental_cost', 'days')
    def _compute_total_price(self):
        for rec in self:
            rec.total_price = ((rec.owned_quantity * rec.owned_cost) + (rec.rental_quantity * rec.rental_cost)) * rec.days
    