from odoo import _, api, fields, models
    
class MasterPemeriksaanStatusPasien(models.TransientModel):
    _name               = 'master.pemeriksaan.status.pasien'
    _description        = 'Master Pemeriksaan Status Pasien'
    
    @api.model
    def default_get(self, fields):
        res = super(MasterPemeriksaanStatusPasien, self).default_get(fields)        
        
        if self._context.get('active_id'):
            registration_id             = self._context.get('active_id')
            pemeriksaan_poli_ids        = self.env['list.pemeriksaan.poli'].search([('registration_id', '=', registration_id)])
            res['registration_id']      = self._context.get('active_id')
            res['list_pemeriksaan_ids'] = pemeriksaan_poli_ids
        
        if self._context.get('is_status'):
            res['is_status']        = self._context.get('is_status')
            
        return res
    
    registration_id     = fields.Many2one( 'master.registration', 
                                           string   = 'Nama Pasien',
                                           readonly = True,
                                           store    = True)
    
    name                = fields.Char( string  = 'No. Registrasi',
                                       readonly = True,
                                       store    = True,
                                       related  = 'registration_id.name')
    
    no_medical_report   = fields.Char( string   = 'No. MR',
                                       readonly = True,
                                       store    = True,
                                       related  = 'registration_id.no_medical_report')
    
    faskes_id           = fields.Many2one( 'master.fasilitas.kesehatan', 
                                           string   = 'Fasilitas Kesehatan',
                                           readonly = True,
                                           store    = True,
                                           related  = 'registration_id.faskes_id')
    
    waktu_cek_lab       = fields.Char(  string   = 'Waktu Pemeriksaan Lab',
                                        store    = True,
                                        readonly = True,
                                        related  = 'registration_id.waktu_cek_lab')
    
    is_done_perawat     = fields.Boolean( string   = 'Done Perawat',
                                          default  = False,
                                          readonly = True,
                                          store    = True,
                                          related  = 'registration_id.is_done_perawat')
    
    on_progress         = fields.Char( string   = 'On Progress', 
                                       store    = True, 
                                       readonly = True,
                                       related  = 'registration_id.on_progress')
    
    pemeriksaan_perawat = fields.Char( compute  = '_compute_pemeriksaan_perawat', 
                                       string   = 'Pemeriksaan Perawat', 
                                       store    = True)
    
    is_status           = fields.Boolean( string   = 'Status', 
                                          default  = False,
                                          readonly = True,
                                          store    = True)
    
    is_blood_group_prandial     = fields.Boolean(   string   = 'Status Gula Darah Post Prandial', 
                                                    readonly = True,
                                                    store    = True,
                                                    related  = 'registration_id.is_blood_group_prandial')
    
    list_pemeriksaan_ids = fields.Many2many( 'list.pemeriksaan.poli', 
                                             string = 'Status Pemeriksaan',
                                             readonly = True,
                                             store    = True)
    
    # Cek Status Pemeriksaan Perawat
    @api.depends('is_done_perawat')
    def _compute_pemeriksaan_perawat(self):
        for rec in self: rec.pemeriksaan_perawat = "Done" if rec.is_done_perawat else "Not Yet"