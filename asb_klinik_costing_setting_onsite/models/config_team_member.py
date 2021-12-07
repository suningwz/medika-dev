from odoo import _, api, fields, models
from odoo.exceptions import UserError

class ConfigTeamMember(models.Model):
    _name               = 'config.team.member'
    _description        = 'Config Team Member'
    _inherit            = ['mail.thread', 'mail.activity.mixin']
    
    name                = fields.Char(  string   = "Team Member's Name", 
                                        index    = True,
                                        required = True,
                                        tracking = True)
    
    internal_cost       = fields.Float( string   = 'Internal Cost (IDR)',
                                        digits   = (10,2),
                                        default  = 0.0,
                                        required = True,
                                        tracking = True)
    
    external_cost       = fields.Float( string   = 'External Cost (IDR)',
                                        digits   = (10,2),
                                        default  = 0.0,
                                        required = True,
                                        tracking = True)
    
    updated_date        = fields.Date(  string       = 'Updated Date', 
                                        default      = fields.Date.today(),
                                        readonly     = True,
                                        tracking     = True)
    
    updated_user        = fields.Many2one( 'res.users', 
                                            string    = 'Updated By',
                                            default   = lambda self: self.env.user, 
                                            readonly  = True, 
                                            index     = True,
                                            tracking  = True)
    
    # Check Team Member sebelum dihapus
    def unlink(self):
        team_member_ids          = self.env['config.team.member.line'].search([('team_member_id', '=' , self.ids)])
        if team_member_ids:
            raise UserError(_('Kamu tidak bisa menghapus Data karena Data terhubung dengan Package MCU yang ada')) 
        res = super(ConfigTeamMember, self).unlink()
        return res
    
class ConfigTeamMemberLine(models.Model):
    _name               = 'config.team.member.line'
    _description        = 'Config Team Member Line'
    _inherit            = ['mail.thread', 'mail.activity.mixin']
    
    team_member_id      = fields.Many2one(  'config.team.member', 
                                            string     = 'Team Member', 
                                            index      = True, 
                                            required   = True,
                                            store      = True,
                                            ondelete   = 'cascade',
                                            tracking   = True)
    
    internal_cost       = fields.Float( string   = 'Internal Cost (IDR)',
                                        digits   = (10,2),
                                        related  = 'team_member_id.internal_cost',
                                        tracking = True,
                                        store    = True)
    
    external_cost       = fields.Float( string   = 'External Cost (IDR)',
                                        digits   = (10,2),
                                        related  = 'team_member_id.external_cost',
                                        tracking = True,
                                        store    = True)
    
    name                = fields.Char(  string   = "Team Member's Name", 
                                        index    = True,
                                        store    = True,
                                        related  = 'team_member_id.name',
                                        tracking = True)
    
    days                = fields.Integer( string    = 'Days', 
                                          required  = True)
    
    internal_quantity   = fields.Integer ( string   = 'Internal',
                                           default  = 0,
                                           required = True,
                                           tracking = True)
    
    external_quantity   = fields.Integer( string    = 'External',
                                          default   = 0,
                                          required  = True,
                                          tracking  = True)
    
    total_price         = fields.Float( string   = 'Total Price (IDR)', 
                                        compute  = '_compute_total_price',
                                        store    = True,
                                        tracking = True)
    
    updated_date        = fields.Date(  string       = 'Updated Date', 
                                        default      = fields.Date.today(),
                                        readonly     = True,
                                        tracking     = True)
    
    updated_user        = fields.Many2one( 'res.users', 
                                            string    = 'Updated By',
                                            default   = lambda self: self.env.user, 
                                            readonly  = True, 
                                            index     = True,
                                            tracking  = True)
    
    # Mendapatkan Total Price dari Team Member
    @api.depends('internal_quantity', 'external_quantity', 'internal_cost', 'external_cost', 'days')
    def _compute_total_price(self):
        for rec in self:
            rec.total_price = ((rec.internal_quantity * rec.internal_cost) + (rec.external_quantity * rec.external_cost)) * rec.days