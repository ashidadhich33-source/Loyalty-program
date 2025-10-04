# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Advanced Accounting - Fiscal Year Management
==============================================================

Fiscal year management for kids clothing retail business.
"""

from ocean import models, fields, api, _
from ocean.exceptions import ValidationError, UserError
from datetime import datetime, date
import logging

_logger = logging.getLogger(__name__)


class AccountFiscalYear(models.Model):
    """Fiscal Year"""
    
    _name = 'account.fiscal.year'
    _description = 'Fiscal Year'
    _order = 'date_from desc'
    
    # Basic Information
    name = fields.Char(
        string='Fiscal Year Name',
        required=True,
        help='Fiscal year name'
    )
    
    # Dates
    date_from = fields.Date(
        string='Start Date',
        required=True,
        help='Fiscal year start date'
    )
    
    date_to = fields.Date(
        string='End Date',
        required=True,
        help='Fiscal year end date'
    )
    
    # Company Information
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self: self.env.company,
        required=True,
        help='Company this fiscal year belongs to'
    )
    
    # Currency
    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        default=lambda self: self.env.company.currency_id,
        help='Fiscal year currency'
    )
    
    # Status
    state = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('closed', 'Closed'),
    ], string='Status', default='draft', help='Fiscal year status')
    
    # Kids Clothing Specific Fields
    age_group_focus = fields.Selection([
        ('infant', 'Infant (0-2 years)'),
        ('toddler', 'Toddler (2-4 years)'),
        ('preschool', 'Preschool (4-6 years)'),
        ('school_age', 'School Age (6-12 years)'),
        ('teen', 'Teen (12+ years)'),
        ('all', 'All Age Groups'),
    ], string='Age Group Focus', help='Primary age group for this fiscal year')
    
    season_specialization = fields.Selection([
        ('summer', 'Summer'),
        ('winter', 'Winter'),
        ('monsoon', 'Monsoon'),
        ('festival', 'Festival'),
        ('all_seasons', 'All Seasons'),
    ], string='Season Specialization', help='Season specialization for this fiscal year')
    
    brand_focus = fields.Char(
        string='Brand Focus',
        help='Specific brands this fiscal year relates to'
    )
    
    product_category = fields.Selection([
        ('clothing', 'Clothing'),
        ('accessories', 'Accessories'),
        ('shoes', 'Shoes'),
        ('toys', 'Toys'),
        ('books', 'Books'),
        ('general', 'General'),
    ], string='Product Category', help='Product category for this fiscal year')
    
    # Analytics
    total_revenue = fields.Float(
        string='Total Revenue',
        compute='_compute_analytics',
        store=True,
        help='Total revenue for this fiscal year'
    )
    
    total_expenses = fields.Float(
        string='Total Expenses',
        compute='_compute_analytics',
        store=True,
        help='Total expenses for this fiscal year'
    )
    
    net_profit = fields.Float(
        string='Net Profit',
        compute='_compute_analytics',
        store=True,
        help='Net profit for this fiscal year'
    )
    
    # Notes
    notes = fields.Text(
        string='Notes',
        help='Additional notes about this fiscal year'
    )
    
    @api.depends('date_from', 'date_to')
    def _compute_analytics(self):
        """Compute analytics"""
        for fiscal_year in self:
            # This would be computed from journal entries
            # For now, setting to 0
            fiscal_year.total_revenue = 0.0
            fiscal_year.total_expenses = 0.0
            fiscal_year.net_profit = 0.0
    
    @api.constrains('date_from', 'date_to')
    def _check_dates(self):
        """Validate dates"""
        for fiscal_year in self:
            if fiscal_year.date_from >= fiscal_year.date_to:
                raise ValidationError(_('Start date must be before end date.'))
    
    @api.constrains('date_from', 'date_to', 'company_id')
    def _check_overlap(self):
        """Check for overlapping fiscal years"""
        for fiscal_year in self:
            overlapping = self.search([
                ('company_id', '=', fiscal_year.company_id.id),
                ('id', '!=', fiscal_year.id),
                '|',
                '&', ('date_from', '<=', fiscal_year.date_from), ('date_to', '>=', fiscal_year.date_from),
                '&', ('date_from', '<=', fiscal_year.date_to), ('date_to', '>=', fiscal_year.date_to),
            ])
            if overlapping:
                raise ValidationError(_('Fiscal years cannot overlap.'))
    
    def action_activate(self):
        """Activate fiscal year"""
        for fiscal_year in self:
            if fiscal_year.state != 'draft':
                raise UserError(_('Only draft fiscal years can be activated.'))
            
            # Deactivate other active fiscal years
            self.search([
                ('company_id', '=', fiscal_year.company_id.id),
                ('state', '=', 'active')
            ]).write({'state': 'draft'})
            
            fiscal_year.state = 'active'
    
    def action_close(self):
        """Close fiscal year"""
        for fiscal_year in self:
            if fiscal_year.state != 'active':
                raise UserError(_('Only active fiscal years can be closed.'))
            
            fiscal_year.state = 'closed'
    
    def action_draft(self):
        """Set to draft"""
        for fiscal_year in self:
            if fiscal_year.state == 'closed':
                raise UserError(_('Closed fiscal years cannot be set to draft.'))
            
            fiscal_year.state = 'draft'
    
    def get_fiscal_year_analytics(self):
        """Get fiscal year analytics"""
        self.ensure_one()
        return {
            'total_revenue': self.total_revenue,
            'total_expenses': self.total_expenses,
            'net_profit': self.net_profit,
        }
    
    @api.model
    def get_current_fiscal_year(self):
        """Get current fiscal year"""
        today = fields.Date.context_today(self)
        fiscal_year = self.search([
            ('company_id', '=', self.env.company.id),
            ('date_from', '<=', today),
            ('date_to', '>=', today),
            ('state', '=', 'active')
        ], limit=1)
        return fiscal_year