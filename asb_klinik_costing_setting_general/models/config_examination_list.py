from odoo import _, api, fields, models

class ConfigExaminationList(models.Model):
    _name               = 'config.examination.list'
    _description        = 'Config Examination List'
    _inherit            = ['mail.thread', 'mail.activity.mixin']
    
    master_tindakan_id     = fields.Many2one( 'product.product', 
                                                string   = 'Tindakan / Layanan',
                                                required = True,
                                                tracking = True,
                                                domain   = [('is_service', '=', True)])
    
    name                    = fields.Char(  string    = 'Examination List', 
                                            store     = True,
                                            related   = 'master_tindakan_id.name',
                                            tracking  = True)
    
    poli_unit_id            = fields.Many2one(  'master.poli.unit', 
                                                string    = 'Default Poli / Unit', 
                                                store     = True,
                                                related   = 'master_tindakan_id.poli_unit_id',
                                                tracking  = True,
                                                readonly  = True,
                                                domain    = [('kategori', 'in', ['poli', 'penunjang'])])
    
    total_beban_langsung    = fields.Float( string   = 'Total Beban Langsung', 
                                            digits   = (10,2),
                                            store    = True,
                                            related  = 'master_tindakan_id.total_beban_langsung',
                                            tracking = True)
    
    list_price              = fields.Float( string   = 'Harga Jual', 
                                            digits   = (10,2),
                                            store    = True,
                                            related  = 'master_tindakan_id.list_price',
                                            tracking = True)
    
    updated_date            = fields.Date(  string       = 'Updated Date', 
                                            default      = fields.Date.today(),
                                            readonly     = True,
                                            store        = True,
                                            tracking     = True)
    
    updated_user            = fields.Many2one( 'res.users', 
                                                string    = 'Updated By',
                                                default   = lambda self: self.env.user, 
                                                readonly  = True, 
                                                index     = True,
                                                store     = True,
                                                tracking  = True)
    