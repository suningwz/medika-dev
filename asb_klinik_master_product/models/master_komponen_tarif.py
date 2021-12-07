from odoo import _, api, fields, models

class MasterKomponenTarif(models.Model):
    _name                   = 'master.komponen.tarif'
    _description            = 'Komponen Tarif'
    _rec_name               = 'alokasi_tarif'
    _order                  = 'name'
    _inherit                = ['mail.thread', 'mail.activity.mixin']
    
    name                    = fields.Char( string   = 'Kode Alokasi Tarif', 
                                           readonly = True, 
                                           default  = 'New')
    
    alokasi_tarif           = fields.Char(  string   = 'Alokasi Tarif', 
                                            required = True,
                                            tracking = True)
    
    # Name Get untuk Komponen Tarif
    def name_get(self):
        res = []
        for rec in self: res.append((rec.id, '%s' % (rec.alokasi_tarif)))
        return res
    
    # Sequence untuk Komponen Tarif
    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('master.komponen.tarif.sequence')
        return super(MasterKomponenTarif, self).create(vals)