# -*- coding: utf-8 -*-

from core_framework.orm import BaseModel, CharField, TextField, IntegerField, FloatField, BooleanField, DateField, DateTimeField, Many2oneField, SelectionField
from core_framework.exceptions import ValidationError


class DiscountAnalytics(BaseModel):
    """Discount Analytics"""
    
    _name = 'discount.analytics'
    _description = 'Discount Analytics'
    _order = 'date desc, program_id'
    
    name = CharField(string='Reference', required=True, size=64)
    program_id = Many2oneField('discount.program', string='Discount Program', required=True)
    rule_id = Many2oneField('discount.rule', string='Discount Rule')
    campaign_id = Many2oneField('discount.campaign', string='Discount Campaign')
    
    # Analytics Period
    date = DateField(string='Date', required=True)
    period_type = SelectionField([
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
    ], string='Period Type', required=True, default='daily')
    
    # Program Metrics
    total_programs = IntegerField(string='Total Programs', default=0)
    active_programs = IntegerField(string='Active Programs', default=0)
    total_rules = IntegerField(string='Total Rules', default=0)
    active_rules = IntegerField(string='Active Rules', default=0)
    total_campaigns = IntegerField(string='Total Campaigns', default=0)
    active_campaigns = IntegerField(string='Active Campaigns', default=0)
    
    # Usage Metrics
    total_usage = IntegerField(string='Total Usage', default=0)
    total_customers = IntegerField(string='Total Customers', default=0)
    total_orders = IntegerField(string='Total Orders', default=0)
    total_order_amount = FloatField(string='Total Order Amount', digits=(16, 2), default=0.0)
    average_order_value = FloatField(string='Average Order Value', digits=(16, 2), default=0.0)
    
    # Discount Metrics
    total_discount_amount = FloatField(string='Total Discount Amount', digits=(16, 2), default=0.0)
    average_discount_amount = FloatField(string='Average Discount Amount', digits=(16, 2), default=0.0)
    discount_percentage = FloatField(string='Discount Percentage', digits=(16, 2), default=0.0)
    discount_per_order = FloatField(string='Discount per Order', digits=(16, 2), default=0.0)
    
    # Coupon Metrics
    total_coupons_issued = IntegerField(string='Total Coupons Issued', default=0)
    total_coupons_used = IntegerField(string='Total Coupons Used', default=0)
    total_coupons_expired = IntegerField(string='Total Coupons Expired', default=0)
    coupon_usage_rate = FloatField(string='Coupon Usage Rate', digits=(16, 2), default=0.0)
    coupon_expiry_rate = FloatField(string='Coupon Expiry Rate', digits=(16, 2), default=0.0)
    
    # Approval Metrics
    total_requests = IntegerField(string='Total Requests', default=0)
    approved_requests = IntegerField(string='Approved Requests', default=0)
    rejected_requests = IntegerField(string='Rejected Requests', default=0)
    pending_requests = IntegerField(string='Pending Requests', default=0)
    approval_rate = FloatField(string='Approval Rate', digits=(16, 2), default=0.0)
    average_approval_time = FloatField(string='Average Approval Time (hours)', digits=(16, 2), default=0.0)
    
    # Campaign Metrics
    total_campaigns_active = IntegerField(string='Total Active Campaigns', default=0)
    total_campaign_usage = IntegerField(string='Total Campaign Usage', default=0)
    total_campaign_value = FloatField(string='Total Campaign Value', digits=(16, 2), default=0.0)
    average_campaign_value = FloatField(string='Average Campaign Value', digits=(16, 2), default=0.0)
    
    # Kids Clothing Metrics
    age_group_breakdown = TextField(string='Age Group Breakdown')
    gender_breakdown = TextField(string='Gender Breakdown')
    seasonal_breakdown = TextField(string='Seasonal Breakdown')
    
    # Special Metrics
    birthday_discounts = IntegerField(string='Birthday Discounts', default=0)
    referral_discounts = IntegerField(string='Referral Discounts', default=0)
    loyalty_discounts = IntegerField(string='Loyalty Discounts', default=0)
    seasonal_discounts = IntegerField(string='Seasonal Discounts', default=0)
    
    # Financial Metrics
    program_cost = FloatField(string='Program Cost', digits=(16, 2), default=0.0)
    program_revenue = FloatField(string='Program Revenue', digits=(16, 2), default=0.0)
    program_roi = FloatField(string='Program ROI', digits=(16, 2), default=0.0)
    cost_per_customer = FloatField(string='Cost per Customer', digits=(16, 2), default=0.0)
    revenue_per_customer = FloatField(string='Revenue per Customer', digits=(16, 2), default=0.0)
    
    # System Fields
    create_date = DateTimeField(string='Created On', readonly=True)
    write_date = DateTimeField(string='Last Updated', readonly=True)
    create_uid = Many2oneField('res.users', string='Created By', readonly=True)
    write_uid = Many2oneField('res.users', string='Updated By', readonly=True)
    
    def create(self, vals):
        """Create discount analytics with validation"""
        if 'date' in vals and 'program_id' in vals:
            # Check for duplicate analytics
            existing = self.search([
                ('date', '=', vals['date']),
                ('program_id', '=', vals['program_id']),
                ('period_type', '=', vals.get('period_type', 'daily')),
            ])
            if existing:
                raise ValidationError('Analytics already exists for this date and program!')
        
        return super(DiscountAnalytics, self).create(vals)
    
    def action_generate_analytics(self):
        """Generate analytics for the period"""
        # This would implement analytics generation logic
        pass
    
    def action_export_analytics(self):
        """Export analytics data"""
        # This would implement analytics export logic
        pass


class DiscountCustomerAnalytics(BaseModel):
    """Discount Customer Analytics"""
    
    _name = 'discount.customer.analytics'
    _description = 'Discount Customer Analytics'
    _order = 'partner_id, date desc'
    
    name = CharField(string='Reference', required=True, size=64)
    partner_id = Many2oneField('res.partner', string='Customer', required=True)
    program_id = Many2oneField('discount.program', string='Discount Program', required=True)
    tier_id = Many2oneField('loyalty.tier', string='Current Tier', related='partner_id.loyalty_tier_id', store=True)
    
    # Analytics Period
    date = DateField(string='Date', required=True)
    period_type = SelectionField([
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
    ], string='Period Type', required=True, default='daily')
    
    # Customer Metrics
    is_active = BooleanField(string='Active Customer', default=True)
    days_since_last_purchase = IntegerField(string='Days Since Last Purchase', default=0)
    total_purchases = IntegerField(string='Total Purchases', default=0)
    total_purchase_amount = FloatField(string='Total Purchase Amount', digits=(16, 2), default=0.0)
    average_order_value = FloatField(string='Average Order Value', digits=(16, 2), default=0.0)
    purchase_frequency = FloatField(string='Purchase Frequency (days)', digits=(16, 2), default=0.0)
    
    # Discount Metrics
    total_discounts_used = IntegerField(string='Total Discounts Used', default=0)
    total_discount_amount = FloatField(string='Total Discount Amount', digits=(16, 2), default=0.0)
    average_discount_amount = FloatField(string='Average Discount Amount', digits=(16, 2), default=0.0)
    discount_savings_percentage = FloatField(string='Discount Savings Percentage', digits=(16, 2), default=0.0)
    
    # Coupon Metrics
    total_coupons_received = IntegerField(string='Total Coupons Received', default=0)
    total_coupons_used = IntegerField(string='Total Coupons Used', default=0)
    total_coupons_expired = IntegerField(string='Total Coupons Expired', default=0)
    coupon_usage_rate = FloatField(string='Coupon Usage Rate', digits=(16, 2), default=0.0)
    
    # Campaign Metrics
    total_campaigns_used = IntegerField(string='Total Campaigns Used', default=0)
    total_campaign_value = FloatField(string='Total Campaign Value', digits=(16, 2), default=0.0)
    average_campaign_value = FloatField(string='Average Campaign Value', digits=(16, 2), default=0.0)
    
    # Kids Clothing Metrics
    age_group = SelectionField([
        ('newborn', 'Newborn (0-6 months)'),
        ('infant', 'Infant (6-18 months)'),
        ('toddler', 'Toddler (18 months-3 years)'),
        ('preschool', 'Preschool (3-5 years)'),
        ('school', 'School (5-12 years)'),
        ('teen', 'Teen (12-18 years)'),
    ], string='Age Group')
    
    gender = SelectionField([
        ('boys', 'Boys'),
        ('girls', 'Girls'),
        ('unisex', 'Unisex'),
    ], string='Gender')
    
    season = SelectionField([
        ('summer', 'Summer'),
        ('winter', 'Winter'),
        ('monsoon', 'Monsoon'),
    ], string='Season')
    
    # Special Metrics
    birthday_discounts_used = IntegerField(string='Birthday Discounts Used', default=0)
    referral_discounts_used = IntegerField(string='Referral Discounts Used', default=0)
    loyalty_discounts_used = IntegerField(string='Loyalty Discounts Used', default=0)
    seasonal_discounts_used = IntegerField(string='Seasonal Discounts Used', default=0)
    
    # System Fields
    create_date = DateTimeField(string='Created On', readonly=True)
    write_date = DateTimeField(string='Last Updated', readonly=True)
    create_uid = Many2oneField('res.users', string='Created By', readonly=True)
    write_uid = Many2oneField('res.users', string='Updated By', readonly=True)