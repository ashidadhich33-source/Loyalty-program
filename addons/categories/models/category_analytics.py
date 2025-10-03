# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging
from datetime import datetime, timedelta

_logger = logging.getLogger(__name__)


class ProductCategoryAnalytics(models.Model):
    _name = 'product.category.analytics'
    _description = 'Product Category Analytics'
    _order = 'date desc'
    _rec_name = 'display_name'

    # Basic Fields
    category_id = fields.Many2one(
        'product.category',
        string='Category',
        required=True,
        ondelete='cascade',
        help="Category this analytics record belongs to"
    )
    date = fields.Date(
        string='Date',
        required=True,
        default=fields.Date.today,
        help="Date of the analytics record"
    )
    period_type = fields.Selection([
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('yearly', 'Yearly'),
    ], string='Period Type', required=True, default='daily', help="Type of period for this analytics")
    
    # Sales Analytics
    total_sales = fields.Float(
        string='Total Sales',
        digits=(12, 2),
        help="Total sales amount for this category"
    )
    total_quantity = fields.Float(
        string='Total Quantity',
        digits=(12, 2),
        help="Total quantity sold for this category"
    )
    average_order_value = fields.Float(
        string='Average Order Value',
        digits=(12, 2),
        compute='_compute_average_order_value',
        help="Average order value for this category"
    )
    total_orders = fields.Integer(
        string='Total Orders',
        help="Total number of orders for this category"
    )
    
    # Product Analytics
    total_products = fields.Integer(
        string='Total Products',
        help="Total number of products in this category"
    )
    active_products = fields.Integer(
        string='Active Products',
        help="Number of active products in this category"
    )
    new_products = fields.Integer(
        string='New Products',
        help="Number of new products added in this period"
    )
    discontinued_products = fields.Integer(
        string='Discontinued Products',
        help="Number of products discontinued in this period"
    )
    
    # Performance Metrics
    conversion_rate = fields.Float(
        string='Conversion Rate (%)',
        digits=(5, 2),
        help="Conversion rate for this category"
    )
    return_rate = fields.Float(
        string='Return Rate (%)',
        digits=(5, 2),
        help="Return rate for this category"
    )
    average_rating = fields.Float(
        string='Average Rating',
        digits=(3, 2),
        help="Average rating of products in this category"
    )
    total_reviews = fields.Integer(
        string='Total Reviews',
        help="Total number of reviews for this category"
    )
    
    # Inventory Analytics
    total_stock_value = fields.Float(
        string='Total Stock Value',
        digits=(12, 2),
        help="Total value of stock for this category"
    )
    total_stock_quantity = fields.Float(
        string='Total Stock Quantity',
        digits=(12, 2),
        help="Total quantity of stock for this category"
    )
    stock_turnover = fields.Float(
        string='Stock Turnover',
        digits=(5, 2),
        help="Stock turnover ratio for this category"
    )
    stock_velocity = fields.Float(
        string='Stock Velocity',
        digits=(5, 2),
        help="Stock velocity for this category"
    )
    
    # Customer Analytics
    total_customers = fields.Integer(
        string='Total Customers',
        help="Total number of customers for this category"
    )
    new_customers = fields.Integer(
        string='New Customers',
        help="Number of new customers for this category"
    )
    returning_customers = fields.Integer(
        string='Returning Customers',
        help="Number of returning customers for this category"
    )
    customer_retention_rate = fields.Float(
        string='Customer Retention Rate (%)',
        digits=(5, 2),
        help="Customer retention rate for this category"
    )
    
    # Financial Analytics
    total_cost = fields.Float(
        string='Total Cost',
        digits=(12, 2),
        help="Total cost for this category"
    )
    total_margin = fields.Float(
        string='Total Margin',
        digits=(12, 2),
        help="Total margin for this category"
    )
    margin_percentage = fields.Float(
        string='Margin Percentage (%)',
        digits=(5, 2),
        compute='_compute_margin_percentage',
        help="Margin percentage for this category"
    )
    profit_margin = fields.Float(
        string='Profit Margin (%)',
        digits=(5, 2),
        help="Profit margin for this category"
    )
    
    # Growth Analytics
    sales_growth = fields.Float(
        string='Sales Growth (%)',
        digits=(5, 2),
        help="Sales growth percentage compared to previous period"
    )
    quantity_growth = fields.Float(
        string='Quantity Growth (%)',
        digits=(5, 2),
        help="Quantity growth percentage compared to previous period"
    )
    customer_growth = fields.Float(
        string='Customer Growth (%)',
        digits=(5, 2),
        help="Customer growth percentage compared to previous period"
    )
    product_growth = fields.Float(
        string='Product Growth (%)',
        digits=(5, 2),
        help="Product growth percentage compared to previous period"
    )
    
    # Seasonal Analytics
    seasonal_index = fields.Float(
        string='Seasonal Index',
        digits=(5, 2),
        help="Seasonal index for this category"
    )
    peak_period = fields.Char(
        string='Peak Period',
        help="Peak period for this category"
    )
    low_period = fields.Char(
        string='Low Period',
        help="Low period for this category"
    )
    
    # Company
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self: self.env.company,
        help="Company this analytics record belongs to"
    )
    
    # Computed Fields
    display_name = fields.Char(
        string='Display Name',
        compute='_compute_display_name',
        store=True,
        help="Display name for this analytics record"
    )
    
    @api.depends('category_id', 'date', 'period_type')
    def _compute_display_name(self):
        for record in self:
            record.display_name = f"{record.category_id.name} - {record.date} ({record.period_type})"
    
    @api.depends('total_sales', 'total_orders')
    def _compute_average_order_value(self):
        for record in self:
            if record.total_orders > 0:
                record.average_order_value = record.total_sales / record.total_orders
            else:
                record.average_order_value = 0.0
    
    @api.depends('total_margin', 'total_sales')
    def _compute_margin_percentage(self):
        for record in self:
            if record.total_sales > 0:
                record.margin_percentage = (record.total_margin / record.total_sales) * 100
            else:
                record.margin_percentage = 0.0
    
    # Methods
    def generate_analytics(self, category_id, date_from, date_to, period_type='daily'):
        """Generate analytics for a category for a specific period"""
        category = self.env['product.category'].browse(category_id)
        if not category:
            return False
        
        # Get all products in this category and its children
        all_categories = category._get_all_children(category)
        all_categories.append(category.id)
        
        # Calculate date range
        if period_type == 'daily':
            dates = [(date_from + timedelta(days=i)) for i in range((date_to - date_from).days + 1)]
        elif period_type == 'weekly':
            dates = [(date_from + timedelta(weeks=i)) for i in range(((date_to - date_from).days // 7) + 1)]
        elif period_type == 'monthly':
            dates = [(date_from + timedelta(days=30*i)) for i in range(((date_to - date_from).days // 30) + 1)]
        else:
            dates = [date_from, date_to]
        
        analytics_records = []
        for date in dates:
            # Check if analytics already exists for this date
            existing = self.search([
                ('category_id', '=', category_id),
                ('date', '=', date),
                ('period_type', '=', period_type)
            ])
            if existing:
                continue
            
            # Generate analytics for this date
            analytics_data = self._calculate_analytics(category, date, period_type)
            analytics_data.update({
                'category_id': category_id,
                'date': date,
                'period_type': period_type,
            })
            
            record = self.create(analytics_data)
            analytics_records.append(record)
        
        return analytics_records
    
    def _calculate_analytics(self, category, date, period_type):
        """Calculate analytics data for a specific category and date"""
        # This would contain the actual calculation logic
        # For now, returning sample data
        return {
            'total_sales': 0.0,
            'total_quantity': 0.0,
            'total_orders': 0,
            'total_products': 0,
            'active_products': 0,
            'new_products': 0,
            'discontinued_products': 0,
            'conversion_rate': 0.0,
            'return_rate': 0.0,
            'average_rating': 0.0,
            'total_reviews': 0,
            'total_stock_value': 0.0,
            'total_stock_quantity': 0.0,
            'stock_turnover': 0.0,
            'stock_velocity': 0.0,
            'total_customers': 0,
            'new_customers': 0,
            'returning_customers': 0,
            'customer_retention_rate': 0.0,
            'total_cost': 0.0,
            'total_margin': 0.0,
            'profit_margin': 0.0,
            'sales_growth': 0.0,
            'quantity_growth': 0.0,
            'customer_growth': 0.0,
            'product_growth': 0.0,
            'seasonal_index': 0.0,
            'peak_period': '',
            'low_period': '',
        }
    
    def get_category_performance(self, category_id, period_days=30):
        """Get performance metrics for a category"""
        category = self.env['product.category'].browse(category_id)
        if not category:
            return {}
        
        date_from = fields.Date.today() - timedelta(days=period_days)
        date_to = fields.Date.today()
        
        analytics = self.search([
            ('category_id', '=', category_id),
            ('date', '>=', date_from),
            ('date', '<=', date_to)
        ])
        
        if not analytics:
            return {}
        
        # Calculate aggregated metrics
        total_sales = sum(analytics.mapped('total_sales'))
        total_quantity = sum(analytics.mapped('total_quantity'))
        total_orders = sum(analytics.mapped('total_orders'))
        total_products = sum(analytics.mapped('total_products'))
        total_customers = sum(analytics.mapped('total_customers'))
        
        return {
            'total_sales': total_sales,
            'total_quantity': total_quantity,
            'total_orders': total_orders,
            'total_products': total_products,
            'total_customers': total_customers,
            'average_order_value': total_sales / total_orders if total_orders > 0 else 0,
            'sales_growth': self._calculate_growth_rate(analytics, 'total_sales'),
            'quantity_growth': self._calculate_growth_rate(analytics, 'total_quantity'),
            'customer_growth': self._calculate_growth_rate(analytics, 'total_customers'),
        }
    
    def _calculate_growth_rate(self, analytics, field):
        """Calculate growth rate for a field"""
        if len(analytics) < 2:
            return 0.0
        
        # Sort by date
        sorted_analytics = analytics.sorted('date')
        first_value = getattr(sorted_analytics[0], field)
        last_value = getattr(sorted_analytics[-1], field)
        
        if first_value == 0:
            return 0.0
        
        return ((last_value - first_value) / first_value) * 100
    
    def get_top_categories(self, limit=10, period_days=30):
        """Get top performing categories"""
        date_from = fields.Date.today() - timedelta(days=period_days)
        date_to = fields.Date.today()
        
        analytics = self.search([
            ('date', '>=', date_from),
            ('date', '<=', date_to)
        ])
        
        if not analytics:
            return []
        
        # Group by category and sum sales
        category_sales = {}
        for record in analytics:
            category_id = record.category_id.id
            if category_id not in category_sales:
                category_sales[category_id] = {
                    'category': record.category_id,
                    'total_sales': 0,
                    'total_quantity': 0,
                    'total_orders': 0,
                }
            category_sales[category_id]['total_sales'] += record.total_sales
            category_sales[category_id]['total_quantity'] += record.total_quantity
            category_sales[category_id]['total_orders'] += record.total_orders
        
        # Sort by total sales and return top categories
        sorted_categories = sorted(
            category_sales.values(),
            key=lambda x: x['total_sales'],
            reverse=True
        )
        
        return sorted_categories[:limit]
    
    def get_seasonal_analysis(self, category_id, year=None):
        """Get seasonal analysis for a category"""
        if not year:
            year = fields.Date.today().year
        
        date_from = fields.Date.today().replace(year=year, month=1, day=1)
        date_to = fields.Date.today().replace(year=year, month=12, day=31)
        
        analytics = self.search([
            ('category_id', '=', category_id),
            ('date', '>=', date_from),
            ('date', '<=', date_to)
        ])
        
        if not analytics:
            return {}
        
        # Group by month
        monthly_data = {}
        for record in analytics:
            month = record.date.month
            if month not in monthly_data:
                monthly_data[month] = {
                    'total_sales': 0,
                    'total_quantity': 0,
                    'total_orders': 0,
                }
            monthly_data[month]['total_sales'] += record.total_sales
            monthly_data[month]['total_quantity'] += record.total_quantity
            monthly_data[month]['total_orders'] += record.total_orders
        
        return monthly_data