from odoo import _, api, fields, models
import math

class ListPackage(models.Model):
    _name                       = 'list.package'
    _description                = 'List Package'
    _rec_name                   = 'nama_paket'
    _order                      = 'name'
    _inherit                    = ['mail.thread', 'mail.activity.mixin']
    
    @api.model
    def _get_default_direct_cost(self):
        direct_cost     = 0.0
        cost            = self.env['master.cost.allocation'].search([], limit=1)
        for data in cost:
            direct_cost = data.direct_cost_allocation
        return direct_cost
    
    @api.model
    def _get_default_fixed_cost(self):
        fixed_cost      = 0.0
        cost            = self.env['master.cost.allocation'].search([], limit=1)
        for data in cost:
            fixed_cost  = data.fixed_cost_allocation
        return fixed_cost
    
    name                        = fields.Char( string   = 'Package ID', 
                                               readonly = True, 
                                               default  = '-',
                                               copy     = False)
    
    nama_paket                  = fields.Char( string   = 'Nama Paket', 
                                               required = True,
                                               copy     = False,
                                               tracking = True)
    
    certificate_ids             = fields.Many2many( 'config.certificate.list', 
                                                    string      = 'Certificate',
                                                    copy        = False,
                                                    store       = True,
                                                    tracking    = True)
    
    package_mcu_id              = fields.Many2one( 'package.mcu', 
                                                   string       = 'Package MCU ID',
                                                   index        = True,
                                                   ondelete     = 'cascade',
                                                   tracking     = True)
    
    perusahaan_id               = fields.Many2one( 'res.partner', 
                                                    string   = 'Perusahaan', 
                                                    domain   = [('is_company', '=', True)], 
                                                    readonly = True,
                                                    ondelete = 'restrict', 
                                                    related  = 'package_mcu_id.perusahaan_id',
                                                    tracking = True)
    
    bahasa_hasil                = fields.Selection( string   = 'Bahasa Hasil', 
                                                    readonly = True, 
                                                    tracking = True,
                                                    related  = 'package_mcu_id.bahasa_hasil')
    
    in_house                    = fields.Boolean(   string   = 'In House',
                                                    readonly = True,
                                                    related  = 'package_mcu_id.in_house')
    
    onsite                      = fields.Boolean(   string    = 'Onsite', 
                                                    readonly  = True,
                                                    related   = 'package_mcu_id.onsite')
    
    fixed_costing_line          = fields.One2many(  'config.fixed.costing.line', 
                                                    'package_id', 
                                                    string   = 'Fixed Costing',
                                                    compute  = '_get_fixed_costing',
                                                    readonly = True,
                                                    store    = True,
                                                    copy     = False,
                                                    tracking = True)
    
    examination_list_ids        = fields.Many2many( 'config.examination.list', 
                                                    string   = 'Examination List',
                                                    store    = True,
                                                    tracking = True)
    
    sampling_list_ids           = fields.Many2many('master.sampling', 
                                                    string   ='Sampling List',
                                                    compute  = '_get_sampling_list',
                                                    readonly = True,
                                                    store    = True,
                                                    copy     = False)
    
    direct_cost                 = fields.Float( string   = 'Direct Cost Allocation', 
                                                default  = _get_default_direct_cost,
                                                store    = True,
                                                readonly = True,
                                                tracking = True)
    
    fixed_cost                  = fields.Float( string   = 'Fixed Cost Allocation', 
                                                default  = _get_default_fixed_cost,
                                                readonly = True,
                                                store    = True,
                                                tracking = True)
    
    profit                      = fields.Float( string   = 'Profit', 
                                                tracking = True)
    
    manual_fee                  = fields.Float( string   = 'Manual Fee (IDR)',
                                                digits   = (10,2),
                                                tracking = True)
    
    total_cost_examination_list = fields.Float( string   = 'Total Cost Examination List (IDR)',
                                                store    = True,
                                                tracking = True,
                                                compute  = '_compute_total_cost_examination_list')
    
    total_cost_certificate      = fields.Float( string   = 'Total Cost Certificate (IDR)', 
                                                store    = True,
                                                tracking = True, 
                                                compute  = '_compute_total_cost_certificate')
    
    total_cost_sampling         = fields.Float( string   = 'Total Cost Sampling (IDR)', 
                                                store    = True,
                                                tracking = True, 
                                                compute  = '_compute_total_cost_sampling')
    
    total_cost_fixed_costing    = fields.Float( string   = 'Total Cost Fixed Costing (IDR)', 
                                                store    = True,
                                                tracking = True,
                                                compute  = '_compute_total_cost_fixed_costing') 
    
    total_direct_cost           = fields.Float( string   = 'Direct Cost Allocation',
                                                store    = True,
                                                tracking = True,
                                                compute  = '_compute_total_direct_cost')
    
    total_fixed_cost            = fields.Float( string   = 'Fixed Cost Allocation',
                                                store    = True,
                                                tracking = True,
                                                compute  = '_compute_total_fixed_cost')
    
    total_cost                  = fields.Float( string   = 'Total Cost (IDR)', 
                                                store    = True,
                                                tracking = True,
                                                compute  = '_compute_total_cost')
    
    profit_rupiah               = fields.Float( string   = 'Profit (IDR)', 
                                                store    = True,
                                                tracking = True,
                                                compute  = '_compute_profit_rupiah')
    
    price_paket                 = fields.Float( string   = 'Price (IDR)',
                                                    store    = True,
                                                    tracking = True,
                                                    compute  = '_compute_price_paket')
    
    # Punya Onsite
    total_patient               = fields.Integer(   string   = 'Total Pasien',
                                                    store    = True,
                                                    tracking = True,
                                                    related  = 'package_mcu_id.total_patient')
    
    total_fixed_price_team_member     = fields.Float( string   = 'Total Price Team Member',
                                                      store    = True,
                                                      tracking = True,
                                                      related  = 'package_mcu_id.total_fixed_price_team_member')
    
    total_fixed_price_transportasi_akomodasi = fields.Float( string   = 'Total Price Transportasi & Akomodasi',
                                                             store    = True,
                                                             tracking = True,
                                                             related  = 'package_mcu_id.total_fixed_price_transportasi_akomodasi')
    
    total_fixed_price_equipment_status = fields.Float( string   = 'Total Price Equipment Status',
                                                       store    = True,
                                                       tracking = True,
                                                       related  = 'package_mcu_id.total_fixed_price_equipment_status')
    
    option                      = fields.Boolean( string  = 'Option - Copy Data',
                                                  default = False)
    
    data_perusahaan_id          = fields.Many2one( 'res.partner', 
                                                    string   = 'Pilih Perusahaan', 
                                                    domain   = [('is_company', '=', True)],
                                                    ondelete = 'restrict', 
                                                    tracking = True)
    
    list_package_id             = fields.Many2one( 'list.package', 
                                                   string   = 'Pilih Paket',
                                                   copy     = False)
    
    list_package_ids            = fields.Many2many( 'list.package', 
                                                    compute = '_compute_list_package')
    
    currency_id                 = fields.Many2one( 'res.currency', 'Currency',
                                                   default  = lambda self: self.env.company.currency_id.id,
                                                   readonly = True)
    
    # Sequence untuk List Package MCU
    @api.model
    def create(self, values):
        if values['in_house'] == True:
            values['name'] = self.env['ir.sequence'].next_by_code('list.package.house')
        if values['onsite'] == True:
            values['name'] = self.env['ir.sequence'].next_by_code('list.package.onsite')
        res = super(ListPackage, self).create(values)
        return res
    
    # Digunakan untuk menghapus Data Perusahaan apabila Option bernilai False
    @api.onchange('option')
    def compute_option(self):
        for rec in self:
            if not rec.option:
                rec.data_perusahaan_id = False
    
    # Digunakan untuk menghapus List Package yang ingin dicopy apabila Data Perusahaan False
    @api.onchange('data_perusahaan_id')
    def compute_list_package_id(self):
        for rec in self:
            if not rec.data_perusahaan_id:
                rec.list_package_id = False
            else:
                rec.list_package_id = self.env['list.package'].search([('perusahaan_id', '=', rec.data_perusahaan_id.id)]).ids
    
    # Mengisi Examination List dan Certificate List dari Reference List Package
    @api.onchange('list_package_id')
    def _onchange_list_package_id(self):
        for rec in self:
            rec.certificate_ids         = rec.list_package_id.certificate_ids
            rec.examination_list_ids    = rec.list_package_id.examination_list_ids
    
    # Menampilkan List Package yang tersedia dari Perusahaan yang dipilih untuk dicopy
    @api.depends('data_perusahaan_id')
    def _compute_list_package(self):
        for data in self:
            domain = []
            if data.in_house:
                domain += [('in_house', '=', True)]
            if data.onsite:
                domain += [('onsite', '=', True)]
            if data.data_perusahaan_id:
                domain += [('perusahaan_id', '=', data.data_perusahaan_id.id)]
            data.list_package_ids = self.env['list.package'].search(domain)
    
    # Digunakan untuk mengisi Sampling yang digunakan berdasarkan Examination List yang dipilih
    @api.depends('examination_list_ids')
    def _get_sampling_list(self):
        for record in self:
            val = []
            data_tindakan = [data for data in record.examination_list_ids.master_tindakan_id.ids 
                             if record.examination_list_ids]
            for rec in data_tindakan:
                val += [data.id for data in self.env['master.sampling'].search([
                    ]).filtered(lambda r: rec in r.master_action_ids.ids)]
            record.sampling_list_ids = [(6, 0, val)]
    
    # Menampilan Fixed Costing berdasarkan Package Onsite atau In House
    @api.depends('in_house', 'onsite')
    def _get_fixed_costing(self):
        for record in self:
            values, result = [], [(5, 0, 0)]
            fixed_costing_line_ids = self.env['costing.setting.general'].search([]).fixed_costing_line
            if record.in_house:     
                values = [{
                            'fixed_costing_id'  : data.id,
                            'name'              : data.name,
                            'cost_in_house'     : data.cost_in_house,
                } for data in fixed_costing_line_ids if data.cost_in_house > 0.0]
                for data in values: result.append((0, 0, data))
            if record.onsite:
                values = [{
                            'fixed_costing_id'  : data.id,
                            'name'              : data.name,
                            'cost_onsite'       : data.cost_onsite,
                } for data in fixed_costing_line_ids if data.cost_onsite > 0.0]
                for data in values: result.append((0, 0, data))
            record.fixed_costing_line = result
    
    # Total dari Sampling
    @api.depends('sampling_list_ids.total_cost')
    def _compute_total_cost_sampling(self):
        for rec in self:
            rec.total_cost_sampling  = sum(rec.sampling_list_ids.mapped('total_cost'))
    
    # Total dari List Certificate
    @api.depends('certificate_ids.cost')
    def _compute_total_cost_certificate(self):
        for rec in self:
            rec.total_cost_certificate  = sum(rec.certificate_ids.mapped('cost'))
    
    # Total dari Examination List
    @api.depends('examination_list_ids.total_beban_langsung')
    def _compute_total_cost_examination_list(self):
        for rec in self:
            rec.total_cost_examination_list  = sum(rec.examination_list_ids.mapped('total_beban_langsung'))
    
    # Total dari Fixed Costing in House dan Onsite
    @api.depends('fixed_costing_line.cost_in_house', 'fixed_costing_line.cost_onsite', 'in_house', 'onsite')
    def _compute_total_cost_fixed_costing(self):
        for rec in self:
            if rec.in_house:
                rec.total_cost_fixed_costing  = sum(rec.fixed_costing_line.mapped('cost_in_house'))
            elif rec.onsite:
                rec.total_cost_fixed_costing  = sum(rec.fixed_costing_line.mapped('cost_onsite'))
    
    # Total dari Direct Cost in House
    @api.depends('total_cost_examination_list', 'total_cost_certificate', 'total_cost_fixed_costing', 'total_fixed_price_team_member', 'total_fixed_price_transportasi_akomodasi', 'total_fixed_price_equipment_status', 'total_cost_sampling', 'in_house', 'onsite')
    def _compute_total_direct_cost(self):
        for rec in self:
            if rec.in_house:
                rec.total_direct_cost  = rec.total_cost_fixed_costing + rec.total_cost_certificate + rec.total_cost_examination_list + rec.total_cost_sampling
            elif rec.onsite:
                rec.total_direct_cost  = rec.total_cost_examination_list + rec.total_cost_certificate + rec.total_cost_fixed_costing + rec.total_fixed_price_team_member + rec.total_fixed_price_transportasi_akomodasi + rec.total_fixed_price_equipment_status + rec.total_cost_sampling
            
    # Total dari Fixed Cost in House
    @api.depends('total_direct_cost', 'direct_cost', 'fixed_cost', 'in_house', 'onsite')
    def _compute_total_fixed_cost(self):
        for rec in self:
            rec.direct_cost           = 1.0 if rec.direct_cost == 0.0 else rec.direct_cost
            if rec.in_house:
                rec.total_fixed_cost  = (rec.total_direct_cost / rec.direct_cost) * rec.fixed_cost
            elif rec.onsite:
                rec.total_fixed_cost  = (rec.total_direct_cost / rec.direct_cost) * rec.fixed_cost
            
    # Total Cost in House
    @api.depends('total_direct_cost', 'total_fixed_cost', 'in_house', 'onsite')
    def _compute_total_cost(self):
        for rec in self:
            if rec.in_house:
                rec.total_cost      = rec.total_direct_cost + rec.total_fixed_cost
            elif rec.onsite:
                rec.total_cost      = rec.total_direct_cost + rec.total_fixed_cost
                
    # Nilai Rupiah Profit in House
    @api.depends('profit', 'total_cost', 'in_house', 'onsite')
    def _compute_profit_rupiah(self):
        for rec in self:
            if rec.in_house:
                rec.profit_rupiah   = rec.profit * rec.total_cost
            elif rec.onsite:
                rec.profit_rupiah   = rec.profit * rec.total_cost
    
    # Total dari Price Paket House
    @api.depends('profit_rupiah', 'manual_fee', 'total_cost', 'in_house', 'onsite')
    def _compute_price_paket(self):
        for rec in self:
            total_fixed_cost      = 0.0
            if rec.in_house:
                total_fixed_cost  = round((math.ceil(rec.profit_rupiah + rec.total_cost + rec.manual_fee) + 50), -2)
                rec.price_paket   = total_fixed_cost
            elif rec.onsite:
                total_fixed_cost  = round((math.ceil(rec.profit_rupiah + rec.total_cost + rec.manual_fee) + 50), -2)
                rec.price_paket   = total_fixed_cost

class ConfigFixedCostingLine(models.Model):
    _inherit        = 'config.fixed.costing.line'
    _description    = 'Config Fixed Costing Line'
    
    package_id      = fields.Many2one( 'list.package', 
                                        string   = 'List Package ID',
                                        index    = True,
                                        ondelete = 'cascade')
    
    
    
    
   
    
    