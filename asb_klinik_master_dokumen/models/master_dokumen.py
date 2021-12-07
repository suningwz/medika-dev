from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError
import datetime

class MasterDokumen(models.Model):
    _name                       = 'master.dokumen'
    _description                = 'Master Dokumen'
    _rec_name                   = 'name'
    _order                      = 'name'
    _inherit                    = ['mail.thread', 'mail.activity.mixin']
    
    name                        = fields.Char( string   = 'No. Dokumen', 
                                               required = True, 
                                               copy     = False,
                                               tracking = True)
    
    status                      = fields.Char( string    = 'Status', 
                                               copy      = False,
                                               compute   = '_get_status')
    
    masa_berlaku                = fields.Date(  string      = 'Masa Berlaku',
                                                default     = fields.Date.today(), 
                                                required    = True,
                                                tracking    = True)
    
    nama_file                   = fields.Char( copy     = False,
                                               tracking = True)
    
    lampiran_file               = fields.Binary( string     = 'Berkas Pendukung',
                                                 copy       = False,
                                                 tracking   = True, 
                                                 attachment = True)
    
    kategori                    = fields.Selection( [
                                                        ('dokter', 'Dokter'),
                                                        ('perawat', 'Perawat'),
                                                        ('faskes', 'Fasilitas Kesehatan'),
                                                        ('nonmedis', 'Tenaga Non Medis')
                                                    ],  string      = 'Kategori', 
                                                        readonly    = True,
                                                        store       = True)
    
    jenis_dokumen_id            = fields.Many2one( 'master.jenis.dokumen', 
                                                   string   = 'Jenis Dokumen', 
                                                   required = True,
                                                   tracking = True)
    
    partner_id                  = fields.Many2one( 'res.partner', 
                                                   string   = 'Nama Personil', 
                                                   readonly = True,
                                                   ondelete = 'cascade')
    
    faskes_id                   = fields.Many2one( 'master.fasilitas.kesehatan', 
                                                   string   = 'Fasilitas Kesehatan', 
                                                   readonly = True,
                                                   ondelete = 'cascade')
    
    # Checking Format File yang diupload
    @api.constrains('lampiran_file')
    def _check_file(self):
       if str(self.nama_file.split(".")[1]) not in ['pdf', 'jpg', 'png', 'jpeg'] :
            raise ValidationError("File yang diupload tidak sesuai Format")
    
    # Get Status berdasarkan Masa Berlaku dari Dokumen
    @api.depends('masa_berlaku')
    def _get_status(self):
        tanggal_sekarang = datetime.date.today()
        for doc in self: 
            doc.status = "Aktif" if tanggal_sekarang <= doc.masa_berlaku else "Expired"