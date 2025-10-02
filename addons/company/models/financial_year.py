# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Company - Financial Year
=========================================

Standalone version of the financial year model.
"""

from core_framework.orm import BaseModel, CharField, TextField, BooleanField, IntegerField, DateTimeField, Many2OneField, SelectionField, DateField, FloatField, One2ManyField
from core_framework.orm import Field
from typing import Dict, Any, Optional
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class FinancialYear(BaseModel):
    """Financial year model for Kids Clothing ERP"""
    
    _name = 'financial.year'
    _description = 'Financial Year'
    _table = 'financial_year'
    
    # Basic fields
    name = CharField(
        string='Financial Year Name',
        size=100,
        required=True,
        help='Name of the financial year'
    )
    
    code = CharField(
        string='Financial Year Code',
        size=20,
        required=True,
        help='Unique code for the financial year'
    )
    
    description = TextField(
        string='Description',
        help='Description of the financial year'
    )
    
    # Company relationship
    company_id = IntegerField(
        string='Company ID',
        required=True,
        help='Company this financial year belongs to'
    )
    
    # Financial year dates
    date_start = DateField(
        string='Start Date',
        required=True,
        help='Start date of the financial year'
    )
    
    date_end = DateField(
        string='End Date',
        required=True,
        help='End date of the financial year'
    )
    
    # Financial year status
    state = SelectionField(
        string='State',
        selection=[
            ('draft', 'Draft'),
            ('active', 'Active'),
            ('closed', 'Closed'),
            ('cancelled', 'Cancelled'),
        ],
        default='draft',
        help='State of the financial year'
    )
    
    # Financial year settings
    is_active = BooleanField(
        string='Active',
        default=True,
        help='Whether the financial year is active'
    )
    
    is_default = BooleanField(
        string='Default Financial Year',
        default=False,
        help='Whether this is the default financial year'
    )
    
    # Financial year analytics
    total_transactions = IntegerField(
        string='Total Transactions',
        default=0,
        help='Total number of transactions in this financial year'
    )
    
    total_sales = FloatField(
        string='Total Sales',
        default=0.0,
        help='Total sales in this financial year'
    )
    
    total_purchases = FloatField(
        string='Total Purchases',
        default=0.0,
        help='Total purchases in this financial year'
    )
    
    # Financial year periods
    period_ids = One2ManyField(
        string='Periods',
        comodel_name='account.period',
        inverse_name='fiscalyear_id',
        help='Periods in this financial year'
    )
    
    def create(self, vals: Dict[str, Any]):
        """Override create to set default values"""
        # Set default dates if not provided
        if 'date_start' not in vals or 'date_end' not in vals:
            current_year = datetime.now().year
            vals['date_start'] = f'{current_year}-04-01'
            vals['date_end'] = f'{current_year + 1}-03-31'
        
        return super().create(vals)
    
    def write(self, vals: Dict[str, Any]):
        """Override write to handle financial year updates"""
        result = super().write(vals)
        
        # Log financial year updates
        for fy in self:
            if vals:
                logger.info(f"Financial year {fy.name} updated: {', '.join(vals.keys())}")
        
        return result
    
    def unlink(self):
        """Override unlink to prevent deletion of active financial years"""
        for fy in self:
            if fy.state == 'active':
                raise ValueError('Cannot delete active financial year')
            
            if fy.is_default:
                raise ValueError('Cannot delete default financial year')
        
        return super().unlink()
    
    def action_activate(self):
        """Activate financial year"""
        self.state = 'active'
        self.is_active = True
        return True
    
    def action_close(self):
        """Close financial year"""
        self.state = 'closed'
        return True
    
    def action_cancel(self):
        """Cancel financial year"""
        self.state = 'cancelled'
        return True
    
    def action_set_default(self):
        """Set as default financial year"""
        # Remove default from other financial years in same company
        other_fys = self.search([
            ('company_id', '=', self.company_id),
            ('is_default', '=', True),
        ])
        for fy in other_fys:
            fy.is_default = False
        
        # Set this financial year as default
        self.is_default = True
        return True
    
    def get_financial_year_analytics(self):
        """Get financial year analytics"""
        return {
            'total_transactions': self.total_transactions,
            'total_sales': self.total_sales,
            'total_purchases': self.total_purchases,
            'state': self.state,
            'is_active': self.is_active,
            'is_default': self.is_default,
            'date_start': self.date_start,
            'date_end': self.date_end,
        }
    
    @classmethod
    def get_financial_years_by_company(cls, company_id: int):
        """Get financial years by company"""
        return cls.search([
            ('company_id', '=', company_id),
            ('is_active', '=', True),
        ])
    
    @classmethod
    def get_active_financial_year(cls, company_id: int):
        """Get active financial year for company"""
        return cls.search([
            ('company_id', '=', company_id),
            ('state', '=', 'active'),
        ], limit=1)
    
    @classmethod
    def get_default_financial_year(cls, company_id: int):
        """Get default financial year for company"""
        return cls.search([
            ('company_id', '=', company_id),
            ('is_default', '=', True),
        ], limit=1)
    
    @classmethod
    def get_financial_year_analytics_summary(cls):
        """Get financial year analytics summary"""
        # In standalone version, we'll return mock data
        return {
            'total_financial_years': 0,
            'active_financial_years': 0,
            'closed_financial_years': 0,
            'default_financial_years': 0,
            'active_percentage': 0,
        }
    
    def _check_dates(self):
        """Validate financial year dates"""
        if self.date_start and self.date_end:
            if self.date_start >= self.date_end:
                raise ValueError('Start date must be before end date')
            
            # Check if financial year is 12 months
            start_date = datetime.strptime(self.date_start, '%Y-%m-%d').date()
            end_date = datetime.strptime(self.date_end, '%Y-%m-%d').date()
            diff_days = (end_date - start_date).days
            
            if diff_days < 365 or diff_days > 366:
                raise ValueError('Financial year must be 12 months')
    
    def _check_default_financial_year(self):
        """Validate default financial year"""
        if self.is_default:
            # Check if there's already a default financial year in same company
            existing_default = self.search([
                ('is_default', '=', True),
                ('company_id', '=', self.company_id),
                ('id', '!=', self.id),
            ])
            if existing_default:
                raise ValueError('Only one financial year can be set as default per company')
    
    def _check_state(self):
        """Validate financial year state"""
        valid_states = ['draft', 'active', 'closed', 'cancelled']
        if self.state not in valid_states:
            raise ValueError(f'Invalid state: {self.state}')
    
    def action_duplicate(self):
        """Duplicate financial year"""
        self.ensure_one()
        
        new_fy = self.copy({
            'name': f'{self.name} (Copy)',
            'code': f'{self.code}_copy',
            'is_default': False,
            'state': 'draft',
        })
        
        return new_fy
    
    def action_export_financial_year(self):
        """Export financial year data"""
        self.ensure_one()
        
        return {
            'name': self.name,
            'code': self.code,
            'company_id': self.company_id,
            'date_start': self.date_start,
            'date_end': self.date_end,
            'state': self.state,
            'is_active': self.is_active,
            'is_default': self.is_default,
        }
    
    def action_import_financial_year(self, fy_data: Dict[str, Any]):
        """Import financial year data"""
        self.ensure_one()
        
        self.write(fy_data)
        return True