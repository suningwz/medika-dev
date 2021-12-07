from odoo import _, api, fields, models

class ResUsers(models.Model):
    _inherit            = 'res.users'
    _description        = 'Res Users'
    
    unit_kerja                  = fields.Selection( [
                                                        ('dokter', 'Dokter'),
                                                        ('perawat', 'Perawat'),
                                                        ('nonmedis', 'Tenaga Non-Medis'),
                                                    ],  string   = 'Unit Kerja')
    
    master_ketenagaan_id        = fields.Many2one( 'master.ketenagaan', 
                                                   string   = 'Bidang Ketenagaan')
    
    master_ketenagaan_ids       = fields.Many2many( 'master.ketenagaan', 
                                                    compute='_compute_master_ketenagaan_ids')
    
    # Filter Bidang Ketenagaan berdasarkan Unit Kerja
    @api.depends('unit_kerja')
    def _compute_master_ketenagaan_ids(self):
        for data in self:
            domain_master_ketenagaan    = []
            
            if data.unit_kerja == 'dokter':
                domain_master_ketenagaan += [('unit_kerja', '=', 'dokter')]
            if data.unit_kerja == 'perawat':
                domain_master_ketenagaan += [('unit_kerja', '=', 'perawat')]
            if data.unit_kerja == 'nonmedis':
                domain_master_ketenagaan += [('unit_kerja', '=', 'nonmedis')]
                
            data.master_ketenagaan_ids  = self.env['master.ketenagaan'].search(domain_master_ketenagaan)