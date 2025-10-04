# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
import logging
from datetime import datetime, timedelta

_logger = logging.getLogger(__name__)


class AccountPeriod(models.Model):
    _name = 'account.period'
    _description = 'Accounting Period'
    _order = 'date_start desc'
    _rec_name = 'name'

    name = fields.Char(
        string='Period Name',
        required=True,
        help='Name of the accounting period'
    )
    
    code = fields.Char(
        string='Period Code',
        required=True,
        help='Code for the accounting period'
    )
    
    date_start = fields.Date(
        string='Start Date',
        required=True,
        help='Start date of the period'
    )
    
    date_stop = fields.Date(
        string='End Date',
        required=True,
        help='End date of the period'
    )
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('open', 'Open'),
        ('closed', 'Closed'),
    ], string='State', default='draft', required=True, help='State of the period')
    
    # Kids Clothing Specific Fields
    age_group = fields.Selection([
        ('0-2', 'Baby (0-2 years)'),
        ('2-4', 'Toddler (2-4 years)'),
        ('4-6', 'Pre-school (4-6 years)'),
        ('6-8', 'Early School (6-8 years)'),
        ('8-10', 'Middle School (8-10 years)'),
        ('10-12', 'Late School (10-12 years)'),
        ('12-14', 'Teen (12-14 years)'),
        ('14-16', 'Young Adult (14-16 years)'),
        ('all', 'All Age Groups'),
    ], string='Age Group', help='Age group for this period')
    
    season = fields.Selection([
        ('summer', 'Summer'),
        ('winter', 'Winter'),
        ('monsoon', 'Monsoon'),
        ('all_season', 'All Season'),
    ], string='Season', help='Season for this period')
    
    brand = fields.Char(
        string='Brand',
        help='Brand for this period'
    )
    
    color = fields.Char(
        string='Color',
        help='Color for this period'
    )
    
    # Period Configuration
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self: self.env.company,
        help='Company this period belongs to'
    )
    
    fiscal_year_id = fields.Many2one(
        'account.fiscal.year',
        string='Fiscal Year',
        help='Fiscal year this period belongs to'
    )
    
    # Period Statistics
    total_entries = fields.Integer(
        string='Total Entries',
        compute='_compute_statistics',
        help='Total number of journal entries'
    )
    
    total_debit = fields.Float(
        string='Total Debit',
        compute='_compute_statistics',
        help='Total debit amount'
    )
    
    total_credit = fields.Float(
        string='Total Credit',
        compute='_compute_statistics',
        help='Total credit amount'
    )
    
    balance = fields.Float(
        string='Balance',
        compute='_compute_statistics',
        help='Balance of the period'
    )
    
    # Timestamps
    create_date = fields.Datetime(
        string='Created On',
        readonly=True,
        help='Date when the period was created'
    )
    
    opened_date = fields.Datetime(
        string='Opened On',
        readonly=True,
        help='Date when the period was opened'
    )
    
    closed_date = fields.Datetime(
        string='Closed On',
        readonly=True,
        help='Date when the period was closed'
    )
    
    created_by = fields.Many2one(
        'res.users',
        string='Created By',
        default=lambda self: self.env.user,
        readonly=True,
        help='User who created the period'
    )
    
    opened_by = fields.Many2one(
        'res.users',
        string='Opened By',
        readonly=True,
        help='User who opened the period'
    )
    
    closed_by = fields.Many2one(
        'res.users',
        string='Closed By',
        readonly=True,
        help='User who closed the period'
    )
    
    @api.depends('move_ids')
    def _compute_statistics(self):
        for record in self:
            moves = record.move_ids.filtered(lambda m: m.state == 'posted')
            record.total_entries = len(moves)
            record.total_debit = sum(moves.mapped('line_ids.debit'))
            record.total_credit = sum(moves.mapped('line_ids.credit'))
            record.balance = record.total_debit - record.total_credit
    
    @api.model
    def create(self, vals):
        """Override create to set default values"""
        if not vals.get('code'):
            # Generate code based on date
            date_start = vals.get('date_start')
            if date_start:
                date_obj = fields.Date.from_string(date_start)
                vals['code'] = date_obj.strftime('%Y%m')
        
        return super(AccountPeriod, self).create(vals)
    
    @api.constrains('date_start', 'date_stop')
    def _check_dates(self):
        for record in self:
            if record.date_start and record.date_stop:
                if record.date_start > record.date_stop:
                    raise ValidationError(_('Start date must be before end date.'))
    
    @api.constrains('code')
    def _check_code(self):
        for record in self:
            if record.code:
                # Check for duplicate codes
                duplicate = self.search([
                    ('code', '=', record.code),
                    ('id', '!=', record.id),
                    ('company_id', '=', record.company_id.id)
                ])
                if duplicate:
                    raise ValidationError(_('Period code must be unique within the company.'))
    
    def action_open(self):
        """Open the period"""
        for record in self:
            if record.state == 'draft':
                record.write({
                    'state': 'open',
                    'opened_date': fields.Datetime.now(),
                    'opened_by': self.env.user.id,
                })
    
    def action_close(self):
        """Close the period"""
        for record in self:
            if record.state == 'open':
                # Check if there are any draft entries
                draft_entries = record.move_ids.filtered(lambda m: m.state == 'draft')
                if draft_entries:
                    raise UserError(_('Cannot close period with draft journal entries.'))
                
                record.write({
                    'state': 'closed',
                    'closed_date': fields.Datetime.now(),
                    'closed_by': self.env.user.id,
                })
    
    def action_reopen(self):
        """Reopen the period"""
        for record in self:
            if record.state == 'closed':
                record.write({'state': 'open'})
    
    def action_view_entries(self):
        """View journal entries for this period"""
        return {
            'type': 'ir.actions.act_window',
            'name': _('Journal Entries'),
            'res_model': 'account.move',
            'view_mode': 'tree,form',
            'domain': [('period_id', '=', self.id)],
            'context': {'default_period_id': self.id},
        }
    
    def action_generate_report(self):
        """Generate period report"""
        return {
            'type': 'ir.actions.act_window',
            'name': _('Period Report'),
            'res_model': 'account.report',
            'view_mode': 'form',
            'context': {'default_period_id': self.id},
            'target': 'new',
        }
    
    @api.model
    def get_current_period(self):
        """Get current period"""
        today = fields.Date.today()
        return self.search([
            ('date_start', '<=', today),
            ('date_stop', '>=', today),
            ('state', '=', 'open'),
            ('company_id', '=', self.env.company.id)
        ], limit=1)
    
    @api.model
    def get_kids_clothing_periods(self, age_group=None, season=None, brand=None, color=None):
        """Get periods filtered by kids clothing criteria"""
        domain = [('state', '=', 'open')]
        
        if age_group:
            domain.append(('age_group', 'in', [age_group, 'all']))
        
        if season:
            domain.append(('season', 'in', [season, 'all_season']))
        
        if brand:
            domain.append(('brand', '=', brand))
        
        if color:
            domain.append(('color', '=', color))
        
        return self.search(domain)
    
    @api.model
    def create_kids_clothing_periods(self):
        """Create kids clothing specific periods"""
        # This method would create periods tailored for kids clothing business
        pass


class AccountFiscalYear(models.Model):
    _name = 'account.fiscal.year'
    _description = 'Fiscal Year'
    _order = 'date_start desc'
    _rec_name = 'name'

    name = fields.Char(
        string='Fiscal Year Name',
        required=True,
        help='Name of the fiscal year'
    )
    
    code = fields.Char(
        string='Fiscal Year Code',
        required=True,
        help='Code for the fiscal year'
    )
    
    date_start = fields.Date(
        string='Start Date',
        required=True,
        help='Start date of the fiscal year'
    )
    
    date_stop = fields.Date(
        string='End Date',
        required=True,
        help='End date of the fiscal year'
    )
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('open', 'Open'),
        ('closed', 'Closed'),
    ], string='State', default='draft', required=True, help='State of the fiscal year')
    
    # Kids Clothing Specific Fields
    age_group = fields.Selection([
        ('0-2', 'Baby (0-2 years)'),
        ('2-4', 'Toddler (2-4 years)'),
        ('4-6', 'Pre-school (4-6 years)'),
        ('6-8', 'Early School (6-8 years)'),
        ('8-10', 'Middle School (8-10 years)'),
        ('10-12', 'Late School (10-12 years)'),
        ('12-14', 'Teen (12-14 years)'),
        ('14-16', 'Young Adult (14-16 years)'),
        ('all', 'All Age Groups'),
    ], string='Age Group', help='Age group for this fiscal year')
    
    season = fields.Selection([
        ('summer', 'Summer'),
        ('winter', 'Winter'),
        ('monsoon', 'Monsoon'),
        ('all_season', 'All Season'),
    ], string='Season', help='Season for this fiscal year')
    
    brand = fields.Char(
        string='Brand',
        help='Brand for this fiscal year'
    )
    
    color = fields.Char(
        string='Color',
        help='Color for this fiscal year'
    )
    
    # Fiscal Year Configuration
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self: self.env.company,
        help='Company this fiscal year belongs to'
    )
    
    # Fiscal Year Periods
    period_ids = fields.One2many(
        'account.period',
        'fiscal_year_id',
        string='Periods',
        help='Periods in this fiscal year'
    )
    
    # Fiscal Year Statistics
    total_periods = fields.Integer(
        string='Total Periods',
        compute='_compute_statistics',
        help='Total number of periods'
    )
    
    total_entries = fields.Integer(
        string='Total Entries',
        compute='_compute_statistics',
        help='Total number of journal entries'
    )
    
    total_debit = fields.Float(
        string='Total Debit',
        compute='_compute_statistics',
        help='Total debit amount'
    )
    
    total_credit = fields.Float(
        string='Total Credit',
        compute='_compute_statistics',
        help='Total credit amount'
    )
    
    balance = fields.Float(
        string='Balance',
        compute='_compute_statistics',
        help='Balance of the fiscal year'
    )
    
    # Timestamps
    create_date = fields.Datetime(
        string='Created On',
        readonly=True,
        help='Date when the fiscal year was created'
    )
    
    opened_date = fields.Datetime(
        string='Opened On',
        readonly=True,
        help='Date when the fiscal year was opened'
    )
    
    closed_date = fields.Datetime(
        string='Closed On',
        readonly=True,
        help='Date when the fiscal year was closed'
    )
    
    created_by = fields.Many2one(
        'res.users',
        string='Created By',
        default=lambda self: self.env.user,
        readonly=True,
        help='User who created the fiscal year'
    )
    
    opened_by = fields.Many2one(
        'res.users',
        string='Opened By',
        readonly=True,
        help='User who opened the fiscal year'
    )
    
    closed_by = fields.Many2one(
        'res.users',
        string='Closed By',
        readonly=True,
        help='User who closed the fiscal year'
    )
    
    @api.depends('period_ids')
    def _compute_statistics(self):
        for record in self:
            periods = record.period_ids
            record.total_periods = len(periods)
            
            moves = periods.mapped('move_ids').filtered(lambda m: m.state == 'posted')
            record.total_entries = len(moves)
            record.total_debit = sum(moves.mapped('line_ids.debit'))
            record.total_credit = sum(moves.mapped('line_ids.credit'))
            record.balance = record.total_debit - record.total_credit
    
    @api.model
    def create(self, vals):
        """Override create to set default values"""
        if not vals.get('code'):
            # Generate code based on start date
            date_start = vals.get('date_start')
            if date_start:
                date_obj = fields.Date.from_string(date_start)
                vals['code'] = date_obj.strftime('%Y')
        
        return super(AccountFiscalYear, self).create(vals)
    
    @api.constrains('date_start', 'date_stop')
    def _check_dates(self):
        for record in self:
            if record.date_start and record.date_stop:
                if record.date_start > record.date_stop:
                    raise ValidationError(_('Start date must be before end date.'))
    
    @api.constrains('code')
    def _check_code(self):
        for record in self:
            if record.code:
                # Check for duplicate codes
                duplicate = self.search([
                    ('code', '=', record.code),
                    ('id', '!=', record.id),
                    ('company_id', '=', record.company_id.id)
                ])
                if duplicate:
                    raise ValidationError(_('Fiscal year code must be unique within the company.'))
    
    def action_open(self):
        """Open the fiscal year"""
        for record in self:
            if record.state == 'draft':
                record.write({
                    'state': 'open',
                    'opened_date': fields.Datetime.now(),
                    'opened_by': self.env.user.id,
                })
    
    def action_close(self):
        """Close the fiscal year"""
        for record in self:
            if record.state == 'open':
                # Check if there are any open periods
                open_periods = record.period_ids.filtered(lambda p: p.state == 'open')
                if open_periods:
                    raise UserError(_('Cannot close fiscal year with open periods.'))
                
                record.write({
                    'state': 'closed',
                    'closed_date': fields.Datetime.now(),
                    'closed_by': self.env.user.id,
                })
    
    def action_reopen(self):
        """Reopen the fiscal year"""
        for record in self:
            if record.state == 'closed':
                record.write({'state': 'open'})
    
    def action_view_periods(self):
        """View periods for this fiscal year"""
        return {
            'type': 'ir.actions.act_window',
            'name': _('Periods'),
            'res_model': 'account.period',
            'view_mode': 'tree,form',
            'domain': [('fiscal_year_id', '=', self.id)],
            'context': {'default_fiscal_year_id': self.id},
        }
    
    def action_generate_report(self):
        """Generate fiscal year report"""
        return {
            'type': 'ir.actions.act_window',
            'name': _('Fiscal Year Report'),
            'res_model': 'account.report',
            'view_mode': 'form',
            'context': {'default_fiscal_year_id': self.id},
            'target': 'new',
        }
    
    @api.model
    def get_current_fiscal_year(self):
        """Get current fiscal year"""
        today = fields.Date.today()
        return self.search([
            ('date_start', '<=', today),
            ('date_stop', '>=', today),
            ('state', '=', 'open'),
            ('company_id', '=', self.env.company.id)
        ], limit=1)
    
    @api.model
    def get_kids_clothing_fiscal_years(self, age_group=None, season=None, brand=None, color=None):
        """Get fiscal years filtered by kids clothing criteria"""
        domain = [('state', '=', 'open')]
        
        if age_group:
            domain.append(('age_group', 'in', [age_group, 'all']))
        
        if season:
            domain.append(('season', 'in', [season, 'all_season']))
        
        if brand:
            domain.append(('brand', '=', brand))
        
        if color:
            domain.append(('color', '=', color))
        
        return self.search(domain)
    
    @api.model
    def create_kids_clothing_fiscal_years(self):
        """Create kids clothing specific fiscal years"""
        # This method would create fiscal years tailored for kids clothing business
        pass