from odoo import _, api, fields, models

class ResUsers(models.Model):
    _inherit            = 'res.users'
    _description        = 'Res Users'
    
    faskes_id           = fields.Many2one( 'master.fasilitas.kesehatan', 
                                           string = 'Default Fas. Kesehatan')
    
    faskes_ids          = fields.Many2many( 'master.fasilitas.kesehatan', 
                                            string = 'Fas. Kesehatan')
    
    poli_unit_id        = fields.Many2one( 'master.poli.unit', 
                                           string = 'Poli / Unit')
    
    poli_unit_ids       = fields.Many2many( 'master.poli.unit', 
                                            compute='_compute_poli_unit_ids')
    
    # Filter Poli Unit yang Tersedia dari Faskes yang dipilih
    @api.depends('faskes_ids')
    def _compute_poli_unit_ids(self):
        for data in self:
            domain_poli_unit    = []
            
            if data.faskes_ids:
                domain_poli_unit += [('id', 'in', data.faskes_ids.poli_unit_ids.ids)]
                
            data.poli_unit_ids   = self.env['master.poli.unit'].search(domain_poli_unit)
    