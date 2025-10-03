#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - POS Analytics Model
======================================

POS analytics and reporting for sales performance.
"""

import logging
from datetime import datetime, timedelta
from core_framework.orm import BaseModel, CharField, TextField, BooleanField, IntegerField, DateTimeField, Many2OneField, SelectionField, FloatField, One2ManyField, Many2ManyField
from core_framework.exceptions import ValidationError

logger = logging.getLogger(__name__)

class PosAnalytics(BaseModel):
    """POS analytics and performance metrics"""
    
    _name = 'pos.analytics'
    _description = 'POS Analytics'
    _table = 'pos_analytics'
    _order = 'date desc'
    
    # Basic Information
    name = CharField(
        string='Analytics Name',
        size=100,
        required=True,
        help='Name of the analytics record'
    )
    
    session_id = Many2OneField(
        'pos.session',
        string='POS Session',
        help='Related POS session'
    )
    
    config_id = Many2OneField(
        'pos.config',
        string='POS Configuration',
        help='Related POS configuration'
    )
    
    date = DateTimeField(
        string='Date',
        default=datetime.now,
        help='Date of analysis'
    )
    
    # Sales Metrics
    total_sales = FloatField(
        string='Total Sales',
        digits=(12, 2),
        default=0.0,
        help='Total sales amount'
    )
    
    total_orders = IntegerField(
        string='Total Orders',
        default=0,
        help='Total number of orders'
    )
    
    total_items = IntegerField(
        string='Total Items',
        default=0,
        help='Total number of items sold'
    )
    
    average_order_value = FloatField(
        string='Average Order Value',
        digits=(10, 2),
        default=0.0,
        help='Average order value'
    )
    
    # Payment Metrics
    cash_sales = FloatField(
        string='Cash Sales',
        digits=(12, 2),
        default=0.0,
        help='Total cash sales'
    )
    
    card_sales = FloatField(
        string='Card Sales',
        digits=(12, 2),
        default=0.0,
        help='Total card sales'
    )
    
    upi_sales = FloatField(
        string='UPI Sales',
        digits=(12, 2),
        default=0.0,
        help='Total UPI sales'
    )
    
    wallet_sales = FloatField(
        string='Wallet Sales',
        digits=(12, 2),
        default=0.0,
        help='Total wallet sales'
    )
    
    # Customer Metrics
    total_customers = IntegerField(
        string='Total Customers',
        default=0,
        help='Total number of customers'
    )
    
    new_customers = IntegerField(
        string='New Customers',
        default=0,
        help='Number of new customers'
    )
    
    returning_customers = IntegerField(
        string='Returning Customers',
        default=0,
        help='Number of returning customers'
    )
    
    customer_retention_rate = FloatField(
        string='Customer Retention Rate %',
        digits=(5, 2),
        default=0.0,
        help='Customer retention rate percentage'
    )
    
    # Product Metrics
    top_selling_products = TextField(
        string='Top Selling Products',
        help='Top selling products data'
    )
    
    top_selling_categories = TextField(
        string='Top Selling Categories',
        help='Top selling categories data'
    )
    
    # Age Group Analysis
    newborn_sales = FloatField(
        string='Newborn Sales',
        digits=(12, 2),
        default=0.0,
        help='Sales for newborn age group'
    )
    
    infant_sales = FloatField(
        string='Infant Sales',
        digits=(12, 2),
        default=0.0,
        help='Sales for infant age group'
    )
    
    toddler_sales = FloatField(
        string='Toddler Sales',
        digits=(12, 2),
        default=0.0,
        help='Sales for toddler age group'
    )
    
    preschool_sales = FloatField(
        string='Preschool Sales',
        digits=(12, 2),
        default=0.0,
        help='Sales for preschool age group'
    )
    
    school_sales = FloatField(
        string='School Sales',
        digits=(12, 2),
        default=0.0,
        help='Sales for school age group'
    )
    
    teen_sales = FloatField(
        string='Teen Sales',
        digits=(12, 2),
        default=0.0,
        help='Sales for teen age group'
    )
    
    # Gender Analysis
    boys_sales = FloatField(
        string='Boys Sales',
        digits=(12, 2),
        default=0.0,
        help='Sales for boys'
    )
    
    girls_sales = FloatField(
        string='Girls Sales',
        digits=(12, 2),
        default=0.0,
        help='Sales for girls'
    )
    
    unisex_sales = FloatField(
        string='Unisex Sales',
        digits=(12, 2),
        default=0.0,
        help='Sales for unisex items'
    )
    
    # Seasonal Analysis
    summer_sales = FloatField(
        string='Summer Sales',
        digits=(12, 2),
        default=0.0,
        help='Summer season sales'
    )
    
    winter_sales = FloatField(
        string='Winter Sales',
        digits=(12, 2),
        default=0.0,
        help='Winter season sales'
    )
    
    monsoon_sales = FloatField(
        string='Monsoon Sales',
        digits=(12, 2),
        default=0.0,
        help='Monsoon season sales'
    )
    
    # Loyalty Metrics
    loyalty_points_earned = IntegerField(
        string='Loyalty Points Earned',
        default=0,
        help='Total loyalty points earned'
    )
    
    loyalty_points_redeemed = IntegerField(
        string='Loyalty Points Redeemed',
        default=0,
        help='Total loyalty points redeemed'
    )
    
    loyalty_redemption_rate = FloatField(
        string='Loyalty Redemption Rate %',
        digits=(5, 2),
        default=0.0,
        help='Loyalty points redemption rate'
    )
    
    # Discount Metrics
    total_discounts = FloatField(
        string='Total Discounts',
        digits=(12, 2),
        default=0.0,
        help='Total discount amount given'
    )
    
    average_discount_percentage = FloatField(
        string='Average Discount %',
        digits=(5, 2),
        default=0.0,
        help='Average discount percentage'
    )
    
    discount_orders = IntegerField(
        string='Orders with Discount',
        default=0,
        help='Number of orders with discounts'
    )
    
    # Performance Metrics
    peak_hour = CharField(
        string='Peak Hour',
        size=10,
        help='Peak sales hour'
    )
    
    peak_day = CharField(
        string='Peak Day',
        size=20,
        help='Peak sales day'
    )
    
    conversion_rate = FloatField(
        string='Conversion Rate %',
        digits=(5, 2),
        default=0.0,
        help='Sales conversion rate'
    )
    
    # Status
    is_processed = BooleanField(
        string='Processed',
        default=False,
        help='Whether analytics has been processed'
    )
    
    # Timestamps
    create_date = DateTimeField(
        string='Created On',
        auto_now_add=True
    )
    
    write_date = DateTimeField(
        string='Updated On',
        auto_now=True
    )
    
    def create(self, vals):
        """Override create to calculate metrics"""
        result = super().create(vals)
        result._calculate_analytics()
        return result
    
    def write(self, vals):
        """Override write to recalculate metrics"""
        result = super().write(vals)
        if any(field in vals for field in ['session_id', 'config_id', 'date']):
            self._calculate_analytics()
        return result
    
    def _calculate_analytics(self):
        """Calculate analytics metrics"""
        for record in self:
            if not record.session_id and not record.config_id:
                continue
            
            # Get orders for analysis
            domain = []
            if record.session_id:
                domain.append(('session_id', '=', record.session_id.id))
            elif record.config_id:
                domain.append(('config_id', '=', record.config_id.id))
            
            orders = self.env['pos.order'].search(domain)
            
            # Calculate basic metrics
            record.total_orders = len(orders)
            record.total_sales = sum(order.amount_total for order in orders)
            record.total_items = sum(order.total_items for order in orders)
            record.average_order_value = record.total_sales / max(record.total_orders, 1)
            
            # Calculate payment metrics
            record.cash_sales = sum(order.cash_amount for order in orders)
            record.card_sales = sum(order.card_amount for order in orders)
            record.upi_sales = sum(order.upi_amount for order in orders)
            record.wallet_sales = sum(order.wallet_amount for order in orders)
            
            # Calculate customer metrics
            customers = set(order.partner_id.id for order in orders if order.partner_id)
            record.total_customers = len(customers)
            
            # Calculate age group sales
            record._calculate_age_group_sales(orders)
            
            # Calculate gender sales
            record._calculate_gender_sales(orders)
            
            # Calculate seasonal sales
            record._calculate_seasonal_sales(orders)
            
            # Calculate loyalty metrics
            record.loyalty_points_earned = sum(order.loyalty_points_earned for order in orders)
            record.loyalty_points_redeemed = sum(order.loyalty_points_redeemed for order in orders)
            
            # Calculate discount metrics
            record.total_discounts = sum(order.discount_amount for order in orders)
            record.discount_orders = len([order for order in orders if order.discount_amount > 0])
            if record.total_sales > 0:
                record.average_discount_percentage = (record.total_discounts / record.total_sales) * 100
            
            # Calculate performance metrics
            record._calculate_performance_metrics(orders)
            
            record.is_processed = True
    
    def _calculate_age_group_sales(self, orders):
        """Calculate age group sales"""
        for record in self:
            age_group_sales = {
                'newborn': 0.0,
                'infant': 0.0,
                'toddler': 0.0,
                'preschool': 0.0,
                'school': 0.0,
                'teen': 0.0
            }
            
            for order in orders:
                for line in order.order_line_ids:
                    if line.age_group in age_group_sales:
                        age_group_sales[line.age_group] += line.price_total
            
            record.newborn_sales = age_group_sales['newborn']
            record.infant_sales = age_group_sales['infant']
            record.toddler_sales = age_group_sales['toddler']
            record.preschool_sales = age_group_sales['preschool']
            record.school_sales = age_group_sales['school']
            record.teen_sales = age_group_sales['teen']
    
    def _calculate_gender_sales(self, orders):
        """Calculate gender sales"""
        for record in self:
            gender_sales = {
                'boys': 0.0,
                'girls': 0.0,
                'unisex': 0.0
            }
            
            for order in orders:
                for line in order.order_line_ids:
                    if line.gender in gender_sales:
                        gender_sales[line.gender] += line.price_total
            
            record.boys_sales = gender_sales['boys']
            record.girls_sales = gender_sales['girls']
            record.unisex_sales = gender_sales['unisex']
    
    def _calculate_seasonal_sales(self, orders):
        """Calculate seasonal sales"""
        for record in self:
            seasonal_sales = {
                'summer': 0.0,
                'winter': 0.0,
                'monsoon': 0.0
            }
            
            for order in orders:
                for line in order.order_line_ids:
                    if hasattr(line.product_id, 'season'):
                        season = line.product_id.season
                        if season in seasonal_sales:
                            seasonal_sales[season] += line.price_total
            
            record.summer_sales = seasonal_sales['summer']
            record.winter_sales = seasonal_sales['winter']
            record.monsoon_sales = seasonal_sales['monsoon']
    
    def _calculate_performance_metrics(self, orders):
        """Calculate performance metrics"""
        for record in self:
            # Calculate peak hour
            hour_sales = {}
            for order in orders:
                hour = order.create_date.hour
                hour_sales[hour] = hour_sales.get(hour, 0) + order.amount_total
            
            if hour_sales:
                record.peak_hour = f"{max(hour_sales, key=hour_sales.get)}:00"
            
            # Calculate peak day
            day_sales = {}
            for order in orders:
                day = order.create_date.strftime('%A')
                day_sales[day] = day_sales.get(day, 0) + order.amount_total
            
            if day_sales:
                record.peak_day = max(day_sales, key=day_sales.get)
    
    def get_analytics_summary(self):
        """Get analytics summary"""
        return {
            'sales_summary': {
                'total_sales': self.total_sales,
                'total_orders': self.total_orders,
                'total_items': self.total_items,
                'average_order_value': self.average_order_value
            },
            'payment_summary': {
                'cash_sales': self.cash_sales,
                'card_sales': self.card_sales,
                'upi_sales': self.upi_sales,
                'wallet_sales': self.wallet_sales
            },
            'customer_summary': {
                'total_customers': self.total_customers,
                'new_customers': self.new_customers,
                'returning_customers': self.returning_customers,
                'retention_rate': self.customer_retention_rate
            },
            'age_group_summary': {
                'newborn': self.newborn_sales,
                'infant': self.infant_sales,
                'toddler': self.toddler_sales,
                'preschool': self.preschool_sales,
                'school': self.school_sales,
                'teen': self.teen_sales
            },
            'gender_summary': {
                'boys': self.boys_sales,
                'girls': self.girls_sales,
                'unisex': self.unisex_sales
            },
            'seasonal_summary': {
                'summer': self.summer_sales,
                'winter': self.winter_sales,
                'monsoon': self.monsoon_sales
            },
            'loyalty_summary': {
                'points_earned': self.loyalty_points_earned,
                'points_redeemed': self.loyalty_points_redeemed,
                'redemption_rate': self.loyalty_redemption_rate
            },
            'discount_summary': {
                'total_discounts': self.total_discounts,
                'average_discount_percentage': self.average_discount_percentage,
                'discount_orders': self.discount_orders
            },
            'performance_summary': {
                'peak_hour': self.peak_hour,
                'peak_day': self.peak_day,
                'conversion_rate': self.conversion_rate
            }
        }
    
    def action_generate_report(self):
        """Generate detailed analytics report"""
        return {
            'type': 'ocean.actions.act_window',
            'name': f'Analytics Report - {self.name}',
            'res_model': 'pos.analytics',
            'view_mode': 'form',
            'res_id': self.id,
            'context': {'report_mode': True}
        }