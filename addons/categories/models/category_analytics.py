# -*- coding: utf-8 -*-

from core_framework.orm import BaseModel, CharField, TextField, FloatField, IntegerField, BooleanField, DateField, DateTimeField, Many2OneField, SelectionField
from datetime import datetime, timedelta


class ProductCategoryAnalytics(BaseModel):
    """Product Category Analytics - Performance tracking and reporting"""
    
    _name = 'product.category.analytics'
    _description = 'Product Category Analytics'
    _order = 'date desc'
    _rec_name = 'display_name'

    # Basic Fields
    category_id = Many2OneField('product.category', string='Category', required=True)
    date = DateField(string='Date', required=True, default=lambda self: self.env.today())
    period_type = SelectionField(string='Period Type', selection=[
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('yearly', 'Yearly'),
    ], required=True, default='daily')
    
    # Sales Analytics
    total_sales = FloatField(string='Total Sales', digits=(12, 2))
    total_quantity = FloatField(string='Total Quantity', digits=(12, 2))
    average_order_value = FloatField(string='Average Order Value', digits=(12, 2), readonly=True)
    total_orders = IntegerField(string='Total Orders')
    
    # Product Analytics
    total_products = IntegerField(string='Total Products')
    active_products = IntegerField(string='Active Products')
    new_products = IntegerField(string='New Products')
    discontinued_products = IntegerField(string='Discontinued Products')
    
    # Performance Metrics
    conversion_rate = FloatField(string='Conversion Rate (%)', digits=(5, 2))
    return_rate = FloatField(string='Return Rate (%)', digits=(5, 2))
    average_rating = FloatField(string='Average Rating', digits=(3, 2))
    total_reviews = IntegerField(string='Total Reviews')
    
    # Inventory Analytics
    total_stock_value = FloatField(string='Total Stock Value', digits=(12, 2))
    total_stock_quantity = FloatField(string='Total Stock Quantity', digits=(12, 2))
    stock_turnover = FloatField(string='Stock Turnover', digits=(5, 2))
    stock_velocity = FloatField(string='Stock Velocity', digits=(5, 2))
    
    # Customer Analytics
    total_customers = IntegerField(string='Total Customers')
    new_customers = IntegerField(string='New Customers')
    returning_customers = IntegerField(string='Returning Customers')
    customer_retention_rate = FloatField(string='Customer Retention Rate (%)', digits=(5, 2))
    
    # Financial Analytics
    total_cost = FloatField(string='Total Cost', digits=(12, 2))
    total_margin = FloatField(string='Total Margin', digits=(12, 2))
    margin_percentage = FloatField(string='Margin Percentage (%)', digits=(5, 2), readonly=True)
    profit_margin = FloatField(string='Profit Margin (%)', digits=(5, 2))
    
    # Growth Analytics
    sales_growth = FloatField(string='Sales Growth (%)', digits=(5, 2))
    quantity_growth = FloatField(string='Quantity Growth (%)', digits=(5, 2))
    customer_growth = FloatField(string='Customer Growth (%)', digits=(5, 2))
    product_growth = FloatField(string='Product Growth (%)', digits=(5, 2))
    
    # Seasonal Analytics
    seasonal_index = FloatField(string='Seasonal Index', digits=(5, 2))
    peak_period = CharField(string='Peak Period', size=255)
    low_period = CharField(string='Low Period', size=255)
    
    # Company
    company_id = Many2OneField('res.company', string='Company', default=lambda self: self.env.company)
    
    # Computed Fields
    display_name = CharField(string='Display Name', readonly=True)
    
    def _compute_display_name(self):
        """Compute display name for this analytics record"""
        for record in self:
            record.display_name = f"{record.category_id.name} - {record.date} ({record.period_type})"
    
    def _compute_average_order_value(self):
        """Compute average order value"""
        for record in self:
            if record.total_orders > 0:
                record.average_order_value = record.total_sales / record.total_orders
            else:
                record.average_order_value = 0.0
    
    def _compute_margin_percentage(self):
        """Compute margin percentage"""
        for record in self:
            if record.total_sales > 0:
                record.margin_percentage = (record.total_margin / record.total_sales) * 100
            else:
                record.margin_percentage = 0.0
    
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
        
        date_from = self.env.today() - timedelta(days=period_days)
        date_to = self.env.today()
        
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
        date_from = self.env.today() - timedelta(days=period_days)
        date_to = self.env.today()
        
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
            year = self.env.today().year
        
        date_from = self.env.today().replace(year=year, month=1, day=1)
        date_to = self.env.today().replace(year=year, month=12, day=31)
        
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