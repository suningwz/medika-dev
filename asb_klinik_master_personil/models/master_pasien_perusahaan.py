from odoo import _, api, fields, models, tools, SUPERUSER_ID
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
import re
from odoo.exceptions import UserError, ValidationError
from odoo.osv.expression import NEGATIVE_TERM_OPERATORS

class MasterPasienPerusahaan(models.Model):
    _inherit                    = 'res.partner'
    _description                = 'Res Partner'
    
    is_pasien                   = fields.Boolean( string    = 'Pasien', 
                                                  readonly  = True, 
                                                  default   = False)
    
    is_perusahaan               = fields.Boolean( string    = 'Perusahaan', 
                                                  readonly  = True, 
                                                  default   = False)
    
    is_pic_perusahaan           = fields.Boolean( string    = 'PIC Perusahaan', 
                                                  readonly  = True, 
                                                  default   = False)
    
    perusahaan_id               = fields.Many2one( 'res.partner', 
                                                   string   = 'Nama Perusahaan', 
                                                   copy     = False,
                                                   domain   = [('is_company', '=', True), '|', '&', ('is_perusahaan', '=', True), ('status_perusahaan', '=', 'approved'), '&', ('client', '=', True), ('client_state', '=', 'enabled')])
    
    pic_perusahaan_line         = fields.One2many( 'res.partner', 
                                                   'parent_id', 
                                                   string   = 'PIC Perusahaan',
                                                   copy     = False,
                                                   tracking = True)
    
    no_ktp                      = fields.Char(string        = 'No. KTP / Paspor',
                                              copy          = False,
                                              tracking      = True)
    
    nik_pegawai                 = fields.Char(string        = 'NIK Pegawai',
                                              copy          = False,
                                              tracking      = True)
    
    mulai_bekerja               = fields.Date(string    = 'Mulai Bekerja',
                                              copy      = False,
                                              tracking  = True)
    
    jenis_pekerjaan_id          = fields.Many2one( 'master.jenis.pekerjaan', 
                                                   string   = 'Jenis Pekerjaan',
                                                   copy     = False,
                                                   tracking = True)
    
    warga_negara                = fields.Selection( [
                                                        ('wni', 'WNI'),
                                                        ('wna', 'WNA'),
                                                    ],  string   = 'Kewarganegaraan',
                                                        tracking = True)
    
    status_pegawai              = fields.Selection( [
                                                        ('aktif', 'Aktif'),
                                                        ('nonaktif', 'Tidak Aktif'),
                                                    ],  string   = 'Status Kepegawaian',
                                                        tracking = True)
    
    shift_kerja                 = fields.Selection( [
                                                        ('shift', 'Shift'),
                                                        ('nonshift', 'Non-Shift'),
                                                    ],  string   = 'Shift Kerja',
                                                        tracking = True)
    
    lokasi_pekerjaan_id         = fields.Many2one( 'master.lokasi.pekerjaan', 
                                                   string   = 'Lokasi Pekerjaan',
                                                   copy     = False,
                                                   tracking = True)
    
    umur                        = fields.Char( string   = 'Umur', 
                                               default  = "-",
                                               compute  = '_compute_umur',
                                               store    = True)
    
    is_pekerjaan                = fields.Boolean(   string  = 'Informasi Pekerjaan', 
                                                    default = False,
                                                    compute = '_compute_is_pekerjaan',
                                                    store   = True)
    
    status_perusahaan           = fields.Selection( [
                                                        ('draft', 'Draft'),
                                                        ('waiting', 'Waiting to Approve'),
                                                        ('approved', 'Approved'),
                                                        ('rejected', 'Rejected'),
                                                    ],  string   = 'Status New Customer',
                                                        default  = 'draft',
                                                        copy     = False)
    
    is_status_pic               = fields.Boolean(string = 'Status PIC', default = False, Store = True)
    
    map_link_perusahaan         = fields.Char(string = 'Map Link', tracking = True)
    perusahaan_latitude         = fields.Float(string = 'Geo Latitude', digits = (16, 10))
    perusahaan_longitude        = fields.Float(string = 'Geo Longitude', digits = (16, 10))

    @api.onchange('map_link_perusahaan')
    def _onchange_map_link_perusahaan(self):
        if self.map_link_perusahaan:
            text = str(self.map_link_perusahaan)
            text = text.split('@')
            if len(text) <= 1:
                raise ValidationError(_("Invalid Link Submited!"))
            else:
                text = text.pop(1)
                text = text.split(',')
                self.perusahaan_latitude = text.pop(0)
                self.perusahaan_longitude = text.pop(0)
    
    def get_lat_long_perusahaan(self):
        search_name = str(self.name.replace(" ", "+"))
        url = 'https://www.google.com/maps/place/%s' %search_name
        return {
            'name'     : 'Go to Google Maps',
            'type'     : 'ir.actions.act_url',
            'target'   : 'new',
            'url'      : url
            }
    
    # Kalkulasi Umur berdasarkan Tanggal Lahir Pasien
    @api.depends('tanggal_lahir')
    def _compute_umur(self):
        for rec in self: rec.umur = relativedelta(date.today(), rec.tanggal_lahir).years
        
    # Aktifkan is Pekerjaan
    @api.depends('perusahaan_id')
    def _compute_is_pekerjaan(self):
        for rec in self: rec.is_pekerjaan = True if re.search('One Time', str(rec.perusahaan_id.name), re.IGNORECASE) else False

    # Name Get untuk Pasien
    def name_get(self):
        res = []
        for rec in self: 
            if rec.is_pasien:
                res.append((rec.id, '%s - %s' % (rec.no_ktp, rec.name)))
            else:
                res.append((rec.id, '%s' % (rec.name)))
        return res
    
    # Untuk Search Data Pasien
    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        args = args or []
        domain = []
        if name:
            domain = ['|', ('no_ktp', 'ilike', name),
                      ('name', operator, name)]
            if operator in NEGATIVE_TERM_OPERATORS:
                domain = ['&', '!'] + domain[1:]
        return self.search(domain + args, limit=limit).name_get()
    
    # Button Action Confirm
    def action_request_new_customer(self):
        return self.write({'status_perusahaan': 'waiting'})
    
    # Button Action Set to Draft
    def action_set_to_draft_new_customer(self):
        return self.write({'status_perusahaan': 'draft'})
    
    # Button Action Cancel
    def action_cancel_new_customer(self):
        return self.write({'status_perusahaan': 'rejected'})
    
    # Button Action Approve
    def action_approve_new_customer(self):
        return self.write({'status_perusahaan': 'approved'})
    
    def _create_pic_user(self):
        users       = self.env['res.users'].with_user(SUPERUSER_ID)
        user_id     = users.search([('login', '=', self.email), '|', ('active', '=', True), ('active', '=', False)])
        print(user_id)
        if not user_id:
            self.is_status_pic = True
            user_id = users.create(
                {
                    'login'                 : self.email,
                    'partner_id'            : self.id,
                    'email'                 : self.email,
                    'password'              : 12345,
                }
            ) 
        else:
            user_id.active = True
            self.is_status_pic = True
        return user_id
    
    def _open_pic_user(self, user_id):
        view_id = self.env.ref('base.view_users_form').id
        return {
            'type': 'ir.actions.act_window',
            'name': 'User',
            'view_mode': 'form',
            'res_model': 'res.users',
            'target': 'current',
            'res_id': user_id.id,
            'views': [[view_id, 'form']],
        }
    
    def action_create_pic_user(self):
        for rec in self:
            user_id = rec._create_pic_user()
            return rec._open_pic_user(user_id)
        
    def action_deactive_pic_user(self):
        for rec in self:
            users       = self.env['res.users'].with_user(SUPERUSER_ID)
            user_id     = users.search([('login', '=', self.email)])
            if user_id:
                user_id.active = False
                self.is_status_pic = False