# -*- coding: utf-8 -*-

from core_framework.orm import BaseModel, CharField, TextField, FloatField, IntegerField, BooleanField, DateField, DateTimeField, Many2OneField, One2ManyField, Many2ManyField, SelectionField, ImageField, BinaryField


class ProductAnalytics(BaseModel):
    """Product Analytics - Business intelligence for products"""
    
    _name = 'product.analytics'
    _description = 'Product Analytics'
    _order = 'name'
    
    # Basic Information
    name = CharField(string='Analytics Name', required=True, size=255)
    description = TextField(string='Description')
    
    # Analytics Type
    analytics_type = SelectionField(string='Analytics Type', selection=[
        ('sales', 'Sales Analytics'),
        ('inventory', 'Inventory Analytics'),
        ('performance', 'Performance Analytics'),
        ('trends', 'Trend Analytics'),
        ('customer', 'Customer Analytics'),
        ('other', 'Other'),
    ], required=True)
    
    # Product
    product_id = Many2OneField('product.template', string='Product')
    product_variant_id = Many2OneField('product.variant', string='Product Variant')
    category_id = Many2OneField('product.category', string='Category')
    
    # Time Period
    period_start = DateField(string='Period Start')
    period_end = DateField(string='Period End')
    
    # Sales Analytics
    total_sales = FloatField(string='Total Sales', digits=(16, 2))
    total_quantity_sold = FloatField(string='Total Quantity Sold', digits=(16, 2))
    average_order_value = FloatField(string='Average Order Value', digits=(16, 2))
    total_orders = IntegerField(string='Total Orders')
    
    # Inventory Analytics
    current_stock = FloatField(string='Current Stock', digits=(16, 2))
    stock_turnover = FloatField(string='Stock Turnover', digits=(16, 2))
    days_in_stock = FloatField(string='Days in Stock', digits=(16, 2))
    stock_velocity = FloatField(string='Stock Velocity', digits=(16, 2))
    
    # Performance Analytics
    conversion_rate = FloatField(string='Conversion Rate', digits=(5, 2))
    click_through_rate = FloatField(string='Click Through Rate', digits=(5, 2))
    bounce_rate = FloatField(string='Bounce Rate', digits=(5, 2))
    engagement_rate = FloatField(string='Engagement Rate', digits=(5, 2))
    
    # Customer Analytics
    total_customers = IntegerField(string='Total Customers')
    repeat_customers = IntegerField(string='Repeat Customers')
    new_customers = IntegerField(string='New Customers')
    customer_retention_rate = FloatField(string='Customer Retention Rate', digits=(5, 2))
    
    # Trend Analytics
    sales_growth = FloatField(string='Sales Growth %', digits=(5, 2))
    quantity_growth = FloatField(string='Quantity Growth %', digits=(5, 2))
    customer_growth = FloatField(string='Customer Growth %', digits=(5, 2))
    market_share = FloatField(string='Market Share %', digits=(5, 2))
    
    # Rating and Reviews
    average_rating = FloatField(string='Average Rating', digits=(3, 2))
    total_reviews = IntegerField(string='Total Reviews')
    positive_reviews = IntegerField(string='Positive Reviews')
    negative_reviews = IntegerField(string='Negative Reviews')
    neutral_reviews = IntegerField(string='Neutral Reviews')
    
    # Status
    active = BooleanField(string='Active', default=True)
    state = SelectionField(string='State', selection=[
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ], default='draft')
    
    # Company
    company_id = Many2OneField('res.company', string='Company', required=True)
    
    # Timestamps
    create_date = DateTimeField(string='Created on', readonly=True)
    write_date = DateTimeField(string='Last Updated on', readonly=True)
    
    def get_analytics_summary(self):
        """Get analytics summary information"""
        return {
            'name': self.name,
            'description': self.description,
            'analytics_type': self.analytics_type,
            'product': self.product_id.name if self.product_id else '',
            'product_variant': self.product_variant_id.name if self.product_variant_id else '',
            'category': self.category_id.name if self.category_id else '',
            'period_start': self.period_start,
            'period_end': self.period_end,
            'active': self.active,
            'state': self.state,
        }
    
    def get_sales_analytics(self):
        """Get sales analytics data"""
        return {
            'total_sales': self.total_sales,
            'total_quantity_sold': self.total_quantity_sold,
            'average_order_value': self.average_order_value,
            'total_orders': self.total_orders,
        }
    
    def get_inventory_analytics(self):
        """Get inventory analytics data"""
        return {
            'current_stock': self.current_stock,
            'stock_turnover': self.stock_turnover,
            'days_in_stock': self.days_in_stock,
            'stock_velocity': self.stock_velocity,
        }
    
    def get_performance_analytics(self):
        """Get performance analytics data"""
        return {
            'conversion_rate': self.conversion_rate,
            'click_through_rate': self.click_through_rate,
            'bounce_rate': self.bounce_rate,
            'engagement_rate': self.engagement_rate,
        }
    
    def get_customer_analytics(self):
        """Get customer analytics data"""
        return {
            'total_customers': self.total_customers,
            'repeat_customers': self.repeat_customers,
            'new_customers': self.new_customers,
            'customer_retention_rate': self.customer_retention_rate,
        }
    
    def get_trend_analytics(self):
        """Get trend analytics data"""
        return {
            'sales_growth': self.sales_growth,
            'quantity_growth': self.quantity_growth,
            'customer_growth': self.customer_growth,
            'market_share': self.market_share,
        }
    
    def get_rating_analytics(self):
        """Get rating and review analytics data"""
        return {
            'average_rating': self.average_rating,
            'total_reviews': self.total_reviews,
            'positive_reviews': self.positive_reviews,
            'negative_reviews': self.negative_reviews,
            'neutral_reviews': self.neutral_reviews,
        }
    
    def get_comprehensive_analytics(self):
        """Get comprehensive analytics data"""
        return {
            'analytics_info': self.get_analytics_summary(),
            'sales': self.get_sales_analytics(),
            'inventory': self.get_inventory_analytics(),
            'performance': self.get_performance_analytics(),
            'customer': self.get_customer_analytics(),
            'trends': self.get_trend_analytics(),
            'ratings': self.get_rating_analytics(),
        }
    
    def activate_analytics(self):
        """Activate the analytics"""
        self.write({'state': 'active', 'active': True})
        return True
    
    def deactivate_analytics(self):
        """Deactivate the analytics"""
        self.write({'state': 'inactive', 'active': False})
        return True
    
    def get_analytics_analytics_summary(self):
        """Get comprehensive analytics analytics summary"""
        return {
            'analytics_info': self.get_analytics_summary(),
            'comprehensive_data': self.get_comprehensive_analytics(),
            'performance': {
                'active': self.active,
                'state': self.state,
            },
        }