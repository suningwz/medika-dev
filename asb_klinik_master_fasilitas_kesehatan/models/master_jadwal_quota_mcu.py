from odoo import _, api, fields, models

class MasterJadwalQuotaMCU(models.Model):
    _name                       = 'master.jadwal.quota.mcu'
    _description                = 'Master Jadwal Quota MCU'
    
    start_time                  = fields.Float( string      = 'Jam Mulai', 
                                                required    = True, 
                                                digits      = (2,2))
    
    end_time                    = fields.Float( string      = 'Jam Selesai', 
                                                required    = True, 
                                                digits      = (2,2))
    
    quota_mcu_direct            = fields.Integer( string    = 'Quota MCU Direct', 
                                                  default   = 0, 
                                                  required  = True)
    
    quota_mcu_online            = fields.Integer( string    = 'Quota MCU Online', 
                                                  default   = 0, 
                                                  required  = True)