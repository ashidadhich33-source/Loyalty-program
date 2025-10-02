# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging
from datetime import datetime, timedelta

_logger = logging.getLogger(__name__)


class FinancialYear(models.Model):
    """Financial year model for Kids Clothing ERP"""
    
    _name = 'financial.year'
    _description = 'Financial Year'
    _order = 'date_start desc'
    
    # Basic fields
    name = fields.Char(
        string='Financial Year',
        required=True,
        help='Name of the financial year'
    )
    
    code = fields.Char(
        string='Code',
        required=True,
        help='Unique code for the financial year'
    )
    
    # Company relationship
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        required=True,
        help='Company this financial year belongs to'
    )
    
    # Date fields
    date_start = fields.Date(
        string='Start Date',
        required=True,
        help='Start date of the financial year'
    )
    
    date_end = fields.Date(
        string='End Date',
        required=True,
        help='End date of the financial year'
    )
    
    # Financial year status
    state = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('closed', 'Closed'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft', help='Status of the financial year')
    
    # Financial year settings
    is_default = fields.Boolean(
        string='Default Financial Year',
        default=False,
        help='Whether this is the default financial year'
    )
    
    is_active = fields.Boolean(
        string='Active',
        default=True,
        help='Whether the financial year is active'
    )
    
    # Financial year analytics
    total_sales = fields.Float(
        string='Total Sales',
        compute='_compute_total_sales',
        store=True,
        help='Total sales for this financial year'
    )
    
    total_purchase = fields.Float(
        string='Total Purchase',
        compute='_compute_total_purchase',
        store=True,
        help='Total purchase for this financial year'
    )
    
    total_profit = fields.Float(
        string='Total Profit',
        compute='_compute_total_profit',
        store=True,
        help='Total profit for this financial year'
    )
    
    total_orders = fields.Integer(
        string='Total Orders',
        compute='_compute_total_orders',
        store=True,
        help='Total orders for this financial year'
    )
    
    # Financial year periods
    period_ids = fields.One2many(
        'financial.period',
        'financial_year_id',
        string='Periods',
        help='Periods in this financial year'
    )
    
    # Financial year documents
    document_ids = fields.One2many(
        'financial.document',
        'financial_year_id',
        string='Documents',
        help='Documents for this financial year'
    )
    
    @api.depends('period_ids')
    def _compute_total_sales(self):
        """Compute total sales for this financial year"""
        for fy in self:
            # This would need actual implementation based on sales data
            fy.total_sales = 0.0
    
    @api.depends('period_ids')
    def _compute_total_purchase(self):
        """Compute total purchase for this financial year"""
        for fy in self:
            # This would need actual implementation based on purchase data
            fy.total_purchase = 0.0
    
    @api.depends('total_sales', 'total_purchase')
    def _compute_total_profit(self):
        """Compute total profit for this financial year"""
        for fy in self:
            fy.total_profit = fy.total_sales - fy.total_purchase
    
    @api.depends('period_ids')
    def _compute_total_orders(self):
        """Compute total orders for this financial year"""
        for fy in self:
            # This would need actual implementation based on order data
            fy.total_orders = 0
    
    @api.model
    def create(self, vals):
        """Override create to set default values"""
        # Generate code if not provided
        if 'code' not in vals and 'name' in vals:
            vals['code'] = vals['name'].lower().replace(' ', '_').replace('-', '_')
        
        # Set default dates if not provided
        if 'date_start' not in vals:
            current_year = datetime.now().year
            vals['date_start'] = f'{current_year}-04-01'
            vals['date_end'] = f'{current_year + 1}-03-31'
        
        return super(FinancialYear, self).create(vals)
    
    def write(self, vals):
        """Override write to handle financial year updates"""
        result = super(FinancialYear, self).write(vals)
        
        # Update periods if dates changed
        if 'date_start' in vals or 'date_end' in vals:
            for fy in self:
                fy._update_periods()
        
        return result
    
    def _update_periods(self):
        """Update periods for this financial year"""
        # This would need actual implementation to create/update periods
        pass
    
    def unlink(self):
        """Override unlink to prevent deletion of active financial years"""
        for fy in self:
            if fy.state == 'active':
                raise ValidationError(_('Cannot delete active financial year'))
            
            if fy.period_ids:
                raise ValidationError(_('Cannot delete financial year with periods. Please delete periods first.'))
        
        return super(FinancialYear, self).unlink()
    
    def action_activate(self):
        """Activate financial year"""
        self.ensure_one()
        
        # Close other active financial years in same company
        self.search([
            ('company_id', '=', self.company_id.id),
            ('state', '=', 'active'),
        ]).write({'state': 'closed'})
        
        # Activate this financial year
        self.state = 'active'
        return True
    
    def action_close(self):
        """Close financial year"""
        self.ensure_one()
        
        if self.state != 'active':
            raise ValidationError(_('Only active financial years can be closed'))
        
        self.state = 'closed'
        return True
    
    def action_cancel(self):
        """Cancel financial year"""
        self.ensure_one()
        
        if self.state == 'active':
            raise ValidationError(_('Active financial years cannot be cancelled'))
        
        self.state = 'cancelled'
        return True
    
    def action_set_default(self):
        """Set as default financial year"""
        # Remove default from other financial years in same company
        self.search([
            ('company_id', '=', self.company_id.id),
            ('is_default', '=', True),
        ]).write({'is_default': False})
        
        # Set this financial year as default
        self.is_default = True
        return True
    
    def get_financial_year_periods(self):
        """Get all periods in this financial year"""
        return self.period_ids
    
    def get_financial_year_documents(self):
        """Get all documents for this financial year"""
        return self.document_ids
    
    def get_financial_year_analytics(self):
        """Get financial year analytics"""
        return {
            'total_sales': self.total_sales,
            'total_purchase': self.total_purchase,
            'total_profit': self.total_profit,
            'total_orders': self.total_orders,
            'state': self.state,
            'is_default': self.is_default,
            'is_active': self.is_active,
            'date_start': self.date_start,
            'date_end': self.date_end,
        }
    
    @api.model
    def get_financial_years_by_company(self, company_id):
        """Get financial years by company"""
        return self.search([
            ('company_id', '=', company_id),
            ('is_active', '=', True),
        ])
    
    @api.model
    def get_active_financial_year(self, company_id):
        """Get active financial year for company"""
        return self.search([
            ('company_id', '=', company_id),
            ('state', '=', 'active'),
        ], limit=1)
    
    @api.model
    def get_default_financial_year(self, company_id):
        """Get default financial year for company"""
        return self.search([
            ('company_id', '=', company_id),
            ('is_default', '=', True),
        ], limit=1)
    
    @api.model
    def get_financial_year_analytics_summary(self):
        """Get financial year analytics summary"""
        total_financial_years = self.search_count([])
        active_financial_years = self.search_count([('state', '=', 'active')])
        closed_financial_years = self.search_count([('state', '=', 'closed')])
        default_financial_years = self.search_count([('is_default', '=', True)])
        
        return {
            'total_financial_years': total_financial_years,
            'active_financial_years': active_financial_years,
            'closed_financial_years': closed_financial_years,
            'default_financial_years': default_financial_years,
            'cancelled_financial_years': total_financial_years - active_financial_years - closed_financial_years,
        }
    
    @api.constrains('code')
    def _check_code(self):
        """Validate financial year code"""
        for fy in self:
            if fy.code:
                # Check for duplicate codes in same company
                existing = self.search([
                    ('code', '=', fy.code),
                    ('company_id', '=', fy.company_id.id),
                    ('id', '!=', fy.id),
                ])
                if existing:
                    raise ValidationError(_('Financial year code must be unique within company'))
    
    @api.constrains('date_start', 'date_end')
    def _check_dates(self):
        """Validate financial year dates"""
        for fy in self:
            if fy.date_start and fy.date_end:
                if fy.date_start >= fy.date_end:
                    raise ValidationError(_('Start date must be before end date'))
                
                # Check if financial year is 12 months
                start_date = fields.Date.from_string(fy.date_start)
                end_date = fields.Date.from_string(fy.date_end)
                diff_days = (end_date - start_date).days
                
                if diff_days < 365 or diff_days > 366:
                    raise ValidationError(_('Financial year must be 12 months'))
    
    @api.constrains('state')
    def _check_state(self):
        """Validate financial year state"""
        for fy in self:
            if fy.state == 'active':
                # Check if there's already an active financial year in same company
                existing_active = self.search([
                    ('state', '=', 'active'),
                    ('company_id', '=', fy.company_id.id),
                    ('id', '!=', fy.id),
                ])
                if existing_active:
                    raise ValidationError(_('Only one financial year can be active per company'))
    
    @api.constrains('is_default')
    def _check_default_financial_year(self):
        """Validate default financial year"""
        for fy in self:
            if fy.is_default:
                # Check if there's already a default financial year in same company
                existing_default = self.search([
                    ('is_default', '=', True),
                    ('company_id', '=', fy.company_id.id),
                    ('id', '!=', fy.id),
                ])
                if existing_default:
                    raise ValidationError(_('Only one financial year can be set as default per company'))
    
    def action_duplicate(self):
        """Duplicate financial year"""
        self.ensure_one()
        
        new_fy = self.copy({
            'name': f'{self.name} (Copy)',
            'code': f'{self.code}_copy',
            'is_default': False,
            'state': 'draft',
        })
        
        return {
            'type': 'ir.actions.act_window',
            'name': 'Duplicated Financial Year',
            'res_model': 'financial.year',
            'res_id': new_fy.id,
            'view_mode': 'form',
            'target': 'current',
        }
    
    def action_export_financial_year(self):
        """Export financial year data"""
        self.ensure_one()
        
        return {
            'name': self.name,
            'code': self.code,
            'company_id': self.company_id.id,
            'date_start': self.date_start,
            'date_end': self.date_end,
            'state': self.state,
            'is_default': self.is_default,
            'is_active': self.is_active,
        }
    
    def action_import_financial_year(self, fy_data):
        """Import financial year data"""
        self.ensure_one()
        
        self.write(fy_data)
        return True