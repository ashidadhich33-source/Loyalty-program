# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Company - Company Analytics
=============================================

Standalone version of the company analytics model.
"""

from core_framework.orm import BaseModel, CharField, TextField, BooleanField, IntegerField, DateTimeField, Many2OneField, SelectionField, FloatField, DateField
from core_framework.orm import Field
from typing import Dict, Any, Optional
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class CompanyAnalytics(BaseModel):
    """Company analytics model for Kids Clothing ERP"""
    
    _name = 'company.analytics'
    _description = 'Company Analytics'
    _table = 'company_analytics'
    
    # Basic fields
    name = CharField(
        string='Analytics Name',
        size=100,
        required=True,
        help='Name of the analytics record'
    )
    
    description = TextField(
        string='Description',
        help='Description of the analytics record'
    )
    
    # Company relationship
    company_id = IntegerField(
        string='Company ID',
        required=True,
        help='Company this analytics belongs to'
    )
    
    # Analytics period
    date_from = DateField(
        string='From Date',
        required=True,
        help='Start date of the analytics period'
    )
    
    date_to = DateField(
        string='To Date',
        required=True,
        help='End date of the analytics period'
    )
    
    # Analytics type
    analytics_type = SelectionField(
        string='Analytics Type',
        selection=[
            ('sales', 'Sales Analytics'),
            ('inventory', 'Inventory Analytics'),
            ('financial', 'Financial Analytics'),
            ('customer', 'Customer Analytics'),
            ('employee', 'Employee Analytics'),
            ('performance', 'Performance Analytics'),
            ('custom', 'Custom Analytics'),
        ],
        default='sales',
        help='Type of analytics'
    )
    
    # Analytics data
    total_sales = FloatField(
        string='Total Sales',
        default=0.0,
        help='Total sales for the period'
    )
    
    total_orders = IntegerField(
        string='Total Orders',
        default=0,
        help='Total orders for the period'
    )
    
    total_customers = IntegerField(
        string='Total Customers',
        default=0,
        help='Total customers for the period'
    )
    
    total_products = IntegerField(
        string='Total Products',
        default=0,
        help='Total products for the period'
    )
    
    total_users = IntegerField(
        string='Total Users',
        default=0,
        help='Total users for the period'
    )
    
    # Financial metrics
    revenue = FloatField(
        string='Revenue',
        default=0.0,
        help='Revenue for the period'
    )
    
    profit = FloatField(
        string='Profit',
        default=0.0,
        help='Profit for the period'
    )
    
    expenses = FloatField(
        string='Expenses',
        default=0.0,
        help='Expenses for the period'
    )
    
    # Performance metrics
    conversion_rate = FloatField(
        string='Conversion Rate (%)',
        default=0.0,
        help='Conversion rate percentage'
    )
    
    average_order_value = FloatField(
        string='Average Order Value',
        default=0.0,
        help='Average order value'
    )
    
    customer_satisfaction = FloatField(
        string='Customer Satisfaction (%)',
        default=0.0,
        help='Customer satisfaction percentage'
    )
    
    # Analytics status
    is_active = BooleanField(
        string='Active',
        default=True,
        help='Whether the analytics is active'
    )
    
    is_processed = BooleanField(
        string='Processed',
        default=False,
        help='Whether the analytics has been processed'
    )
    
    # Analytics metadata
    created_by = IntegerField(
        string='Created By',
        help='User who created this analytics'
    )
    
    created_date = DateTimeField(
        string='Created Date',
        default=datetime.now,
        help='Date when analytics was created'
    )
    
    processed_date = DateTimeField(
        string='Processed Date',
        help='Date when analytics was processed'
    )
    
    def create(self, vals: Dict[str, Any]):
        """Override create to set default values"""
        # Set created date
        if 'created_date' not in vals:
            vals['created_date'] = datetime.now()
        
        return super().create(vals)
    
    def write(self, vals: Dict[str, Any]):
        """Override write to handle analytics updates"""
        result = super().write(vals)
        
        # Log analytics updates
        for analytics in self:
            if vals:
                logger.info(f"Analytics {analytics.name} updated: {', '.join(vals.keys())}")
        
        return result
    
    def action_process(self):
        """Process analytics data"""
        self.ensure_one()
        
        # In standalone version, we'll do basic processing
        self.is_processed = True
        self.processed_date = datetime.now()
        
        logger.info(f"Analytics {self.name} processed")
        return True
    
    def get_analytics_summary(self):
        """Get analytics summary"""
        return {
            'total_sales': self.total_sales,
            'total_orders': self.total_orders,
            'total_customers': self.total_customers,
            'total_products': self.total_products,
            'total_users': self.total_users,
            'revenue': self.revenue,
            'profit': self.profit,
            'expenses': self.expenses,
            'conversion_rate': self.conversion_rate,
            'average_order_value': self.average_order_value,
            'customer_satisfaction': self.customer_satisfaction,
            'is_processed': self.is_processed,
            'date_from': self.date_from,
            'date_to': self.date_to,
        }
    
    @classmethod
    def get_analytics_by_company(cls, company_id: int, analytics_type: str = None):
        """Get analytics by company"""
        domain = [('company_id', '=', company_id), ('is_active', '=', True)]
        if analytics_type:
            domain.append(('analytics_type', '=', analytics_type))
        
        return cls.search(domain)
    
    @classmethod
    def get_analytics_by_period(cls, company_id: int, date_from: str, date_to: str):
        """Get analytics by period"""
        return cls.search([
            ('company_id', '=', company_id),
            ('date_from', '>=', date_from),
            ('date_to', '<=', date_to),
            ('is_active', '=', True),
        ])
    
    @classmethod
    def get_analytics_by_type(cls, analytics_type: str):
        """Get analytics by type"""
        return cls.search([
            ('analytics_type', '=', analytics_type),
            ('is_active', '=', True),
        ])
    
    @classmethod
    def get_processed_analytics(cls, company_id: int):
        """Get processed analytics for company"""
        return cls.search([
            ('company_id', '=', company_id),
            ('is_processed', '=', True),
            ('is_active', '=', True),
        ])
    
    @classmethod
    def get_analytics_summary_by_company(cls, company_id: int):
        """Get analytics summary for company"""
        analytics = cls.search([
            ('company_id', '=', company_id),
            ('is_active', '=', True),
        ])
        
        if not analytics:
            return {
                'total_sales': 0.0,
                'total_orders': 0,
                'total_customers': 0,
                'total_products': 0,
                'total_users': 0,
                'revenue': 0.0,
                'profit': 0.0,
                'expenses': 0.0,
                'conversion_rate': 0.0,
                'average_order_value': 0.0,
                'customer_satisfaction': 0.0,
            }
        
        # Calculate totals
        total_sales = sum(a.total_sales for a in analytics)
        total_orders = sum(a.total_orders for a in analytics)
        total_customers = sum(a.total_customers for a in analytics)
        total_products = sum(a.total_products for a in analytics)
        total_users = sum(a.total_users for a in analytics)
        revenue = sum(a.revenue for a in analytics)
        profit = sum(a.profit for a in analytics)
        expenses = sum(a.expenses for a in analytics)
        
        # Calculate averages
        conversion_rate = sum(a.conversion_rate for a in analytics) / len(analytics) if analytics else 0.0
        average_order_value = sum(a.average_order_value for a in analytics) / len(analytics) if analytics else 0.0
        customer_satisfaction = sum(a.customer_satisfaction for a in analytics) / len(analytics) if analytics else 0.0
        
        return {
            'total_sales': total_sales,
            'total_orders': total_orders,
            'total_customers': total_customers,
            'total_products': total_products,
            'total_users': total_users,
            'revenue': revenue,
            'profit': profit,
            'expenses': expenses,
            'conversion_rate': conversion_rate,
            'average_order_value': average_order_value,
            'customer_satisfaction': customer_satisfaction,
        }
    
    @classmethod
    def get_analytics_analytics(cls):
        """Get analytics analytics"""
        # In standalone version, we'll return mock data
        return {
            'total_analytics': 0,
            'active_analytics': 0,
            'processed_analytics': 0,
            'inactive_analytics': 0,
            'analytics_by_type': {},
        }
    
    def _check_dates(self):
        """Validate analytics dates"""
        if self.date_from and self.date_to:
            if self.date_from >= self.date_to:
                raise ValueError('From date must be before to date')
    
    def _check_analytics_type(self):
        """Validate analytics type"""
        valid_types = ['sales', 'inventory', 'financial', 'customer', 'employee', 'performance', 'custom']
        if self.analytics_type not in valid_types:
            raise ValueError(f'Invalid analytics type: {self.analytics_type}')
    
    def _check_metrics(self):
        """Validate metrics"""
        if self.conversion_rate < 0 or self.conversion_rate > 100:
            raise ValueError('Conversion rate must be between 0 and 100')
        
        if self.customer_satisfaction < 0 or self.customer_satisfaction > 100:
            raise ValueError('Customer satisfaction must be between 0 and 100')
    
    def action_duplicate(self):
        """Duplicate analytics"""
        self.ensure_one()
        
        new_analytics = self.copy({
            'name': f'{self.name} (Copy)',
            'is_processed': False,
            'processed_date': None,
        })
        
        return new_analytics
    
    def action_export_analytics(self):
        """Export analytics data"""
        self.ensure_one()
        
        return {
            'name': self.name,
            'description': self.description,
            'company_id': self.company_id,
            'date_from': self.date_from,
            'date_to': self.date_to,
            'analytics_type': self.analytics_type,
            'total_sales': self.total_sales,
            'total_orders': self.total_orders,
            'total_customers': self.total_customers,
            'total_products': self.total_products,
            'total_users': self.total_users,
            'revenue': self.revenue,
            'profit': self.profit,
            'expenses': self.expenses,
            'conversion_rate': self.conversion_rate,
            'average_order_value': self.average_order_value,
            'customer_satisfaction': self.customer_satisfaction,
        }
    
    def action_import_analytics(self, analytics_data: Dict[str, Any]):
        """Import analytics data"""
        self.ensure_one()
        
        self.write(analytics_data)
        return True