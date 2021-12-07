from odoo import _, api, fields, models

class MasterPerawatLine(models.Model):
    _name               = 'master.perawat.line'
    _description        = 'Master Perawat Line'
    
    @api.model
    def _get_default_alokasi_tarif(self):
        alokasi_tarif       = self.env['master.komponen.tarif'].search([('alokasi_tarif', 'ilike', 'Jasa Perawat')], limit=1)
        return alokasi_tarif
    
    master_komponen_id      = fields.Many2one( 'master.komponen.tarif', 
                                               default  = _get_default_alokasi_tarif, 
                                               string   = 'Alokasi Jasa',
                                               readonly = True, 
                                               store    = True,
                                               ondelete = 'cascade')
    
    jenis_tindakan          = fields.Selection( [
                                                    ('mc', 'MC'),
                                                    ('mcu', 'MCU'),
                                                ], string  = 'Jenis Tindakan', 
                                                   required = True)
    
    partner_id              = fields.Many2one( 'res.partner', 
                                               string = 'Nama Perawat')
    
    persentase              = fields.Float( string = 'Persentase (%)', 
                                            digits = (3,1))
    
    nominal                 = fields.Float( string = 'Nominal', 
                                            digits = (10,1))