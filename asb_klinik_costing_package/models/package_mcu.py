from odoo import _, api, fields, models
import datetime
from odoo.exceptions import UserError, ValidationError

class PackageMCU(models.Model):
    _name                       = 'package.mcu'
    _description                = 'Package MCU'
    _rec_name                   = 'name'
    _parent_name                = 'parent_id'
    _parent_store               = True
    _order                      = 'perusahaan_id'
    _inherit                    = ['mail.thread', 'mail.activity.mixin']
    
    parent_path                 = fields.Char(index = True)
    
    parent_id                   = fields.Many2one( 'package.mcu', 
                                                    string   = 'Parent Package MCU', 
                                                    index    = True, 
                                                    ondelete = 'cascade',
                                                    copy     = False)
    
    child_id                    = fields.One2many(  'package.mcu', 
                                                    'parent_id', 
                                                    string   = 'Child Package MCU',
                                                    copy     = False)
    
    in_house                    = fields.Boolean(   string   = 'In House', 
                                                    default  = False,
                                                    readonly = True)
    
    onsite                      = fields.Boolean(   string    = 'Onsite', 
                                                    default   = False,
                                                    readonly  = True)
    
    name                        = fields.Char(  string   = 'No. Costing', 
                                                default  = 'New', 
                                                readonly = True,
                                                copy     = False)
    
    start_date                  = fields.Date(  string   = 'Start Date', 
                                                default  = fields.Date.today(), 
                                                readonly = True, 
                                                tracking = True,
                                                states   = {'draft': [('readonly', False)]})
    
    end_date                    = fields.Date(  string   = 'End Date', 
                                                default  = fields.Date.today(), 
                                                readonly = True, 
                                                tracking = True,
                                                states   = {'draft': [('readonly', False)]})
    
    delivery_days               = fields.Integer( string    = 'Delivery Days (Day)', 
                                                  default   = 1, 
                                                  readonly  = True, 
                                                  tracking  = True,
                                                  states    = {'draft': [('readonly', False)]})
    
    bahasa_hasil                = fields.Selection( [
                                                        ('indonesia', 'Indonesia'),
                                                        ('inggris', 'Inggris'),
                                                    ],  string      = 'Bahasa Hasil', 
                                                        default     = 'inggris', 
                                                        readonly    = True,
                                                        tracking    = True, 
                                                        states      = {'draft': [('readonly', False)]})
    
    state                       = fields.Selection( [
                                                        ('draft', 'Draft'),
                                                        ('waiting', 'Waiting to Medika Approval'),
                                                        ('client', 'Waiting for Client Approval'),
                                                        ('approved', 'Approved'),
                                                        ('rejected', 'Rejected')
                                                    ],  string      = 'Status', 
                                                        default     = 'draft',
                                                        tracking    = True,
                                                        copy        = False)
    
    status                      = fields.Char( string    = 'Status Package', 
                                               copy      = False,
                                               compute   = '_get_status')
    
    keterangan                  = fields.Text(  string   = 'Keterangan', 
                                                readonly = True,
                                                required = True, 
                                                tracking = True,
                                                states   = {'draft': [('readonly', False)]})
    
    # Punya Onsite
    total_patient               = fields.Integer(   string   = 'Total Pasien',
                                                    copy     = False,
                                                    readonly = True, 
                                                    tracking = True,
                                                    states   = {'draft': [('readonly', False)]})
    
    working_days               = fields.Integer( string    = 'Working Days (Day)', 
                                                  default   = 1, 
                                                  readonly  = True, 
                                                  tracking  = True,
                                                  states    = {'draft': [('readonly', False)]})
    
    # Relasi ke Perusahaan
    perusahaan_id               = fields.Many2one( 'res.partner', 
                                                    string   = 'Perusahaan', 
                                                    readonly = True,
                                                    required = True,
                                                    ondelete = 'restrict', 
                                                    tracking = True, 
                                                    states   = {'draft': [('readonly', False)]})
    
    partner_id                  = fields.Many2one( 'res.partner', string = 'PIC Perusahaan',
                                                    readonly = True,
                                                    required = True,
                                                    tracking = True,
                                                    states   = {'draft': [('readonly', False)]})
    
    function                    = fields.Char(  string   = 'Posisi / Jabatan',
                                                related  = 'partner_id.function',
                                                tracking = True)
    
    client_title_id             = fields.Many2one(  'pic.title', 
                                                    string  = 'PIC Title', 
                                                    related = 'partner_id.client_title_id',
                                                    domain  = [('type', '=', 'client')])
    
    email_pic                   = fields.Char(  string   = 'Email PIC', 
                                                related  = 'partner_id.email',
                                                tracking = True)
    
    mobile_pic                  = fields.Char(  string   = 'No. HP PIC', 
                                                related  = 'partner_id.mobile',
                                                tracking = True)
    
    street                      = fields.Char(  related  = 'perusahaan_id.street',
                                                tracking = True)
    
    street2                     = fields.Char(  related  = 'perusahaan_id.street2',
                                                tracking = True)
    
    zip                         = fields.Char(  change_default = True, 
                                                related  = 'perusahaan_id.zip',
                                                tracking = True)
    
    city                        = fields.Char(  related  = 'perusahaan_id.city',
                                                tracking = True)
    
    city_id                     = fields.Many2one( 'res.state.city', 'Kabupaten', 
                                                    domain   = "[('state_id', '=', state_id)]",
                                                    ondelete = 'restrict',
                                                    related  = 'perusahaan_id.city_id',
                                                    copy     = False, 
                                                    tracking = True)
    
    kecamatan_id                = fields.Many2one( 'res.city.kecamatan', 'Kecamatan', 
                                                    domain   = [('city_id', '=', 'city_id')],
                                                    ondelete = 'restrict',
                                                    related  = 'perusahaan_id.kecamatan_id',
                                                    copy     = False, 
                                                    tracking = True)
    
    kelurahan_id                = fields.Many2one( 'res.kecamatan.kelurahan', 'Kelurahan', 
                                                    domain   = "[('kecamatan_id','=',kecamatan_id)]",
                                                    ondelete = 'restrict',
                                                    related  = 'perusahaan_id.kelurahan_id',
                                                    copy     = False, 
                                                    tracking = True)
    
    state_id                    = fields.Many2one( 'res.country.state', 
                                                    string   = 'State', 
                                                    ondelete = 'restrict', 
                                                    domain   = "[('country_id', '=', country_id)]", 
                                                    related  = 'perusahaan_id.state_id',
                                                    tracking = True)
    
    country_id                  = fields.Many2one( 'res.country', 
                                                    string   = 'Country', 
                                                    ondelete = 'restrict', 
                                                    related  = 'perusahaan_id.country_id',
                                                    tracking = True)
    
    property_payment_term_id    = fields.Many2one( 'account.payment.term', company_dependent = True,
                                                    string  = 'Customer Payment Terms',
                                                    domain  ="[('company_id', 'in', [current_company_id, False])]",
                                                    related = 'perusahaan_id.property_payment_term_id')
    
    tanggal_pembuatan           = fields.Date(  string   = 'Created Date', 
                                                default  = fields.Date.today(),
                                                readonly = True,
                                                copy     = False,
                                                tracking = True)
    
    user_create                 = fields.Many2one(  'res.users', 
                                                    string   = 'Created By',
                                                    default  = lambda self: self.env.user, 
                                                    readonly = True, 
                                                    index    = True,
                                                    copy     = False,
                                                    tracking = True)
    
    jumlah_package_mcu          = fields.Integer(   string    = 'Jumlah Package MCU', 
                                                    readonly  = True,
                                                    tracking  = True,
                                                    copy      = False,
                                                    compute   = '_compute_jumlah_package')
    
    list_package_count          = fields.Integer(   string    = '# List Package',
                                                    copy      = False,
                                                    compute   = '_compute_list_package_count')
    
    list_package_line           = fields.One2many(  'list.package', 
                                                    'package_mcu_id', 
                                                    string    = 'List Package Lines', 
                                                    readonly  = True,
                                                    tracking  = True,
                                                    copy      = False)
    
    total_price_package         = fields.Float( compute  = '_compute_total_price_package', 
                                                string   = 'Total Price All Package',
                                                store    = True,
                                                tracking = True)
    
    # Punya Onsite
    team_member_line        = fields.One2many( 'config.team.member.line', 
                                                'onsite_id', 
                                                string      = 'Team Member Line',
                                                readonly    = True,
                                                copy        = False,
                                                states      = {'draft': [('readonly', False)]})

    equipment_status_line   = fields.One2many( 'config.equipment.list.line', 
                                                'onsite_id', 
                                                string      = 'Equipment Status Line',
                                                readonly    = True,
                                                copy        = False,
                                                states      = {'draft': [('readonly', False)]})
    
    transportasi_akomodasi_line = fields.One2many( 'config.transportasi.akomodasi.line', 
                                                    'onsite_id', 
                                                    string      = 'Transportasi / Akomodasi Line',
                                                    readonly    = True,
                                                    copy        = False,
                                                    states      = {'draft': [('readonly', False)]})
    
    total_price_team_member       = fields.Float( compute  = '_compute_total_price_team_member', 
                                            string   = 'Total Price Team Member',
                                            store    = True,
                                            tracking = True)
    
    total_fixed_price_team_member = fields.Float( compute  = '_compute_total_fixed_price_team_member', 
                                            string   = 'Total Fixed Price Team Member',
                                            store    = True,
                                            tracking = True)
    
    total_price_transportasi_akomodasi = fields.Float( compute  = '_compute_total_price_transportasi_akomodasi', 
                                                 string   = 'Total Price Transportasi & Akomodasi',
                                                 store    = True,
                                                 tracking = True)
    
    total_fixed_price_transportasi_akomodasi = fields.Float( compute  = '_compute_total_fixed_price_transportasi_akomodasi', 
                                                 string   = 'Total Fixed Price Transportasi & Akomodasi',
                                                 store    = True,
                                                 tracking = True)
    
    total_price_equipment_status = fields.Float( compute  = '_compute_total_price_equipment_status', 
                                                 string   = 'Total Price Equipment Status',
                                                 store    = True,
                                                 tracking = True)
    
    total_fixed_price_equipment_status = fields.Float( compute  = '_compute_total_fixed_price_equipment_status', 
                                                 string   = 'Total Fixed Price Equipment Status',
                                                 store    = True,
                                                 tracking = True)
    
    partner_ids             = fields.Many2many( 'res.partner', 
                                                compute = '_compute_partner')
    
    team_member_ids         = fields.Many2many( 'config.team.member', 
                                                compute = '_compute_team_member')
    
    equipment_status_ids    = fields.Many2many( 'config.equipment.list', 
                                                compute = '_compute_equipment_status')
    
    transportasi_akomodasi_ids    = fields.Many2many( 'config.transportasi.akomodasi', 
                                                compute = '_compute_transportasi_akomodasi')
    
    currency_id             = fields.Many2one( 'res.currency', 'Currency',
                                                default  = lambda self: self.env.company.currency_id.id,
                                                readonly = True)
    
    is_approval_2           = fields.Boolean( string  = 'Approval Level 2',
                                              default = False)
    
    def name_get(self):
        res = []
        for rec in self:
            res.append((rec.id, '%s - %s' % (rec.name, rec.keterangan)))
        return res
    
    # Sequence untuk Package MCU
    @api.model
    def create(self, vals):
        
        if vals['in_house'] == True:
            vals['name'] = self.env['ir.sequence'].next_by_code('package.mcu.house')
        if vals['onsite'] == True:
            vals['name'] = self.env['ir.sequence'].next_by_code('package.mcu.onsite')

        return super(PackageMCU, self).create(vals)
    
    # Button Action Confirm
    def action_confirm(self):
        for rec in self:
            if rec.list_package_line:
                return self.write({'state': 'waiting'})
            else:
                raise ValidationError("Tidak ada Paket pada Daftar ini !!!")
            
    # Button Action Approve
    def action_approve(self):
        for rec in self:
            profit = [data.profit for data in rec.list_package_line if rec.list_package_line]
            if any(data < 0.5 for data in profit):
                if self.env.user.has_group("asb_klinik_costing_team.group_master_costing_level_1"):
                    return self.write({'is_approval_2' : True})
                else:
                    raise ValidationError("Anda Tidak Memiliki Hak Akses untuk Approval pada Tingkat ini")
            else:
                if self.env.user.has_group("asb_klinik_costing_team.group_master_costing_level_1"): 
                    return self.write({'state' : 'client'})
                else:
                    raise ValidationError("Anda Tidak Memiliki Hak Akses untuk Approval pada Tingkat ini")
    
    def action_approve_2(self):
        for rec in self:
            if self.env.user.has_group("asb_klinik_costing_team.group_master_costing_level_2") and rec.is_approval_2:
                return self.write({'state': 'client'})
            else:
                raise ValidationError("Anda Tidak Memiliki Hak Akses untuk Approval pada Tingkat ini")
    
    # Button Action Reject
    def action_reject(self):
        return self.write({'state': 'rejected'})
    
    def action_reject_2(self):
        return self.write({'state': 'rejected'})
    
    def action_client_reject(self):
        return self.write({'state': 'rejected'})
    
    def action_client_approval(self):
        for rec in self:
            perusahaan_ids      = self.env['res.partner'].search([('status_perusahaan', '!=', 'rejected')]).filtered(lambda r: rec.perusahaan_id.id in r.ids)
            print("Hasil Perusahaan :", perusahaan_ids)
            for data in perusahaan_ids:
                if data.status_perusahaan == 'draft':
                    perusahaan_ids.write({'status_perusahaan': 'waiting'})
                else:
                    pass
        return self.write({'state': 'approved'})
    
    # Button Action Set to Draft
    def action_set_to_draft(self):
        return self.write({'state': 'draft', 'is_approval_2' : False})
    
    # Menghitung Jumlah Package yang tersedia
    def _compute_list_package_count(self):
        for rec in self:
            read_list_package_ids   = self.env['list.package'].search([]).filtered(lambda r: rec.id in r.package_mcu_id.ids)
            rec.list_package_count = len(read_list_package_ids.ids)
    
    # Menghitung Jumlah Package yang tersedia
    def _compute_jumlah_package(self):
        for rec in self:
            read_list_package_ids   = self.env['list.package'].search([]).filtered(lambda r: rec.id in r.package_mcu_id.ids)
            rec.jumlah_package_mcu = len(read_list_package_ids.ids)
    
    # Digunakan untuk Filter Data PIC berdasarkan Perusahaan terpilih
    @api.onchange('perusahaan_id')
    def compute_partner_id(self):
        for rec in self:
            rec.partner_id = False if not rec.perusahaan_id else rec.perusahaan_id.pic_perusahaan_line.ids
    
    # Digunakan untuk mengetahui status Package berdasarkan End Date
    @api.depends('end_date')
    def _get_status(self):
        tanggal_sekarang = datetime.date.today()
        for doc in self:
            doc.status = "Active" if tanggal_sekarang <= doc.end_date else "Expired"
    
    # Mendapatkan Total Price Paket dari Keseluruhan Package yang ada
    @api.depends('list_package_line.price_paket')
    def _compute_total_price_package(self):
        for rec in self:
            rec.total_price_package      = sum(rec.list_package_line.mapped('price_paket'))
    
    # Mendapatkan Total Price dari Transportasi dan Akomodasi
    @api.depends('transportasi_akomodasi_line.total_price')
    def _compute_total_price_transportasi_akomodasi(self):
        for rec in self:
            rec.total_price_transportasi_akomodasi = sum(rec.transportasi_akomodasi_line.mapped('total_price'))
    
    # Mendapatkan Harga untuk Transportasi dan Akomodasi yang sudah dibagi dengan Jumlah Pasien
    @api.depends('total_price_transportasi_akomodasi', 'total_patient')
    def _compute_total_fixed_price_transportasi_akomodasi(self):
        for rec in self:
            rec.total_patient      = 1 if rec.total_patient == 0 else rec.total_patient
            rec.total_fixed_price_transportasi_akomodasi = rec.total_price_transportasi_akomodasi / rec.total_patient
    
    # Mendapatkan Total Price dari Team Member
    @api.depends('team_member_line.total_price')
    def _compute_total_price_team_member(self):
        for rec in self:
            rec.total_price_team_member = sum(rec.team_member_line.mapped('total_price'))
    
    # Mendapatkan Harga untuk Team Member yang sudah dibagi dengan Jumlah Pasien
    @api.depends('total_price_team_member', 'total_patient')
    def _compute_total_fixed_price_team_member(self):
        for rec in self:
            rec.total_patient      = 1 if rec.total_patient == 0 else rec.total_patient
            rec.total_fixed_price_team_member = rec.total_price_team_member / rec.total_patient
    
    # Mendapatkan Total Price dari Equipment
    @api.depends('equipment_status_line.total_price')
    def _compute_total_price_equipment_status(self):
        for rec in self:
            rec.total_price_equipment_status = sum(rec.equipment_status_line.mapped('total_price'))
    
    # Mendapatkan Harga untuk Equipment yang sudah dibagi dengan Jumlah Pasien
    @api.depends('total_price_equipment_status', 'total_patient')
    def _compute_total_fixed_price_equipment_status(self):
        for rec in self:
            rec.total_patient      = 1 if rec.total_patient == 0 else rec.total_patient
            rec.total_fixed_price_equipment_status = rec.total_price_equipment_status / rec.total_patient

    # Digunakan untuk Filter Data PIC
    @api.depends('perusahaan_id')
    def _compute_partner(self):
        for data in self:
            domain = []
            if data.perusahaan_id:
                domain += [('parent_id', '=', data.perusahaan_id.id)]
            data.partner_ids = self.env['res.partner'].search(domain)
    
    # Digunakan untuk Tidak ada Duplicate pada Team Member
    @api.depends('team_member_line.team_member_id')
    def _compute_team_member(self):
        for data in self:
            domain = []
            if data.team_member_line:
                domain += [('id', 'not in', [line.team_member_id.id for line in data.team_member_line])]
            data.team_member_ids = self.env['config.team.member'].search(domain)
    
    # Digunakan untuk Tidak ada Duplicate pada Equipment
    @api.depends('equipment_status_line.equipment_list_id')
    def _compute_equipment_status(self):
        for data in self:
            domain = []
            if data.equipment_status_line:
                domain += [('id', 'not in', [line.equipment_list_id.id for line in data.equipment_status_line])]
            data.equipment_status_ids = self.env['config.equipment.list'].search(domain)
    
    # Digunakan untuk Tidak ada Duplicate pada Transportasi dan Akomodasi
    @api.depends('transportasi_akomodasi_line.transportasi_akomodasi_id')
    def _compute_transportasi_akomodasi(self):
        for data in self:
            domain = []
            if data.transportasi_akomodasi_line:
                domain += [('id', 'not in', [line.transportasi_akomodasi_id.id for line in data.transportasi_akomodasi_line])]
            data.transportasi_akomodasi_ids = self.env['config.transportasi.akomodasi'].search(domain)

class ConfigTeamMemberLine(models.Model):
    _inherit        = 'config.team.member.line'
    _description    = 'Config Team Member Line'
    
    onsite_id       = fields.Many2one( 'package.mcu', 
                                        string   = 'Package Onsite ID',
                                        index    = True,
                                        ondelete = 'cascade')

class ConfigEquipmentListLine(models.Model):
    _inherit        = 'config.equipment.list.line'
    _description    = 'Config Equipment List Line'
    
    onsite_id       = fields.Many2one( 'package.mcu', 
                                        string   = 'Package Onsite ID',
                                        index    = True,
                                        ondelete = 'cascade')
    
class ConfigTransportasiAkomodasiLine(models.Model):
    _inherit        = 'config.transportasi.akomodasi.line'
    _description    = 'Config Transportasi Akomodasi Line'
    
    onsite_id       = fields.Many2one( 'package.mcu', 
                                        string   = 'Package Onsite ID',
                                        index    = True,
                                        ondelete = 'cascade')