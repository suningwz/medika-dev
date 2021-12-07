from odoo import _, api, fields, models
from odoo.exceptions import UserError

class ConfigTransportasiAkomodasi(models.Model):
    _name               = 'config.transportasi.akomodasi'
    _description        = 'Config Transportasi Akomodasi'
    _inherit            = ['mail.thread', 'mail.activity.mixin']
    
    name                = fields.Char(  string   = "Nama Transportasi / Akomodasi", 
                                        index    = True,
                                        required = True,
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
    
    def unlink(self):
        transportasi_akomodasi_ids     = self.env['config.transportasi.akomodasi.line'].search([('transportasi_akomodasi_id', '=' , self.ids)])
        if transportasi_akomodasi_ids:
            raise UserError(_('Kamu tidak bisa menghapus Data karena Data terhubung dengan Package MCU yang ada')) 
        res = super(ConfigTransportasiAkomodasi, self).unlink()
        return res
    
class ConfigTransportasiAkomodasiLine(models.Model):
    _name                       = 'config.transportasi.akomodasi.line'
    _description                = 'Config Transportasi Akomodasi Line'
    _inherit                    = ['mail.thread', 'mail.activity.mixin']
    
    transportasi_akomodasi_id   = fields.Many2one(  'config.transportasi.akomodasi', 
                                                    string     = 'Transportasi / Akomodasi', 
                                                    index      = True, 
                                                    required   = True,
                                                    store      = True,
                                                    ondelete   = 'cascade',
                                                    tracking   = True)
    
    name                        = fields.Char(  string   = "Nama Transportasi / Akomodasi", 
                                                index    = True,
                                                store    = True,
                                                related  = 'transportasi_akomodasi_id.name',
                                                tracking = True)
    
    days                        = fields.Integer( string    = 'Days', 
                                                  required  = True)
    
    transako_cost               = fields.Float( string   = 'Nominal Cost (IDR)',
                                                digits   = (10,2),
                                                required = True,
                                                default  = 0.0,
                                                tracking = True)
    
    transako_quantity           = fields.Integer ( string   = 'Qty',
                                                   default  = 0,
                                                   required = True,
                                                   tracking = True)
    
    total_price                 = fields.Float( string   = 'Total Price (IDR)', 
                                                compute  = '_compute_total_price',
                                                store    = True,
                                                tracking = True)
    
    updated_date                = fields.Date(  string       = 'Updated Date', 
                                                default      = fields.Date.today(),
                                                readonly     = True,
                                                tracking     = True)
    
    updated_user                = fields.Many2one( 'res.users', 
                                                    string    = 'Updated By',
                                                    default   = lambda self: self.env.user, 
                                                    readonly  = True, 
                                                    index     = True,
                                                    tracking  = True)
    
    # Mendapatkan Total Price Transportasi / Akomodasi
    @api.depends('transako_cost', 'transako_quantity', 'days')
    def _compute_total_price(self):
        for rec in self:
            rec.total_price = (rec.transako_cost * rec.transako_quantity) * rec.days