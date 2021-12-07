from odoo import _, api, fields, models
import random
from odoo.exceptions import UserError

class ConfigCertificateList(models.Model):
    _name               = 'config.certificate.list'
    _description        = 'Config Certificate List'
    _inherit            = ['mail.thread', 'mail.activity.mixin']
    
    def _get_default_color(self):
        return random.randint(1, 11)
    
    name                = fields.Char( string       = 'Nama Sertifikat', 
                                       required     = True,
                                       tracking     = True)
    
    color               = fields.Integer( string    = 'Color Index', 
                                          default   = _get_default_color,
                                          store     = True)
    
    price               = fields.Float( string      = 'Harga Sertifikat', 
                                        digits      = (10,2), 
                                        required    = True,
                                        tracking    = True)
    
    cost                = fields.Float( string      = 'Cost Sertifikat', 
                                        digits      = (10,2), 
                                        required    = True,
                                        tracking    = True)
    
    updated_date        = fields.Date( string       = 'Updated Date', 
                                       default      = fields.Date.today(),
                                       readonly     = True,
                                       store        = True,
                                       tracking     = True)
    
    updated_user        = fields.Many2one( 'res.users', 
                                            string    = 'Updated By',
                                            default   = lambda self: self.env.user, 
                                            readonly  = True, 
                                            index     = True,
                                            store     = True,
                                            tracking  = True)
    
    