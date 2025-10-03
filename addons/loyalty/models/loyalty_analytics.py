# -*- coding: utf-8 -*-

from core_framework.orm import BaseModel, CharField, TextField, IntegerField, FloatField, BooleanField, DateField, DateTimeField, Many2oneField, SelectionField
from core_framework.exceptions import ValidationError


class LoyaltyAnalytics(BaseModel):
    """Loyalty Program Analytics"""
    
    _name = 'loyalty.analytics'
    _description = 'Loyalty Analytics'
    _order = 'date desc, program_id'
    
    name = CharField(string='Reference', required=True, size=64)
    program_id = Many2oneField('loyalty.program', string='Loyalty Program', required=True)
    
    # Analytics Period
    date = DateField(string='Date', required=True)
    period_type = SelectionField([
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
    ], string='Period Type', required=True, default='daily')
    
    # Customer Metrics
    total_customers = IntegerField(string='Total Customers', default=0)
    active_customers = IntegerField(string='Active Customers', default=0)
    new_customers = IntegerField(string='New Customers', default=0)
    churned_customers = IntegerField(string='Churned Customers', default=0)
    customer_retention_rate = FloatField(string='Customer Retention Rate', digits=(16, 2), default=0.0)
    
    # Purchase Metrics
    total_purchases = IntegerField(string='Total Purchases', default=0)
    total_purchase_amount = FloatField(string='Total Purchase Amount', digits=(16, 2), default=0.0)
    average_order_value = FloatField(string='Average Order Value', digits=(16, 2), default=0.0)
    average_purchase_frequency = FloatField(string='Average Purchase Frequency (days)', digits=(16, 2), default=0.0)
    
    # Points Metrics
    total_points_earned = IntegerField(string='Total Points Earned', default=0)
    total_points_redeemed = IntegerField(string='Total Points Redeemed', default=0)
    total_points_expired = IntegerField(string='Total Points Expired', default=0)
    points_redemption_rate = FloatField(string='Points Redemption Rate', digits=(16, 2), default=0.0)
    points_expiry_rate = FloatField(string='Points Expiry Rate', digits=(16, 2), default=0.0)
    
    # Rewards Metrics
    total_rewards_given = IntegerField(string='Total Rewards Given', default=0)
    total_reward_value = FloatField(string='Total Reward Value', digits=(16, 2), default=0.0)
    average_reward_value = FloatField(string='Average Reward Value', digits=(16, 2), default=0.0)
    
    # Voucher Metrics
    total_vouchers_issued = IntegerField(string='Total Vouchers Issued', default=0)
    total_vouchers_used = IntegerField(string='Total Vouchers Used', default=0)
    total_vouchers_expired = IntegerField(string='Total Vouchers Expired', default=0)
    voucher_usage_rate = FloatField(string='Voucher Usage Rate', digits=(16, 2), default=0.0)
    voucher_expiry_rate = FloatField(string='Voucher Expiry Rate', digits=(16, 2), default=0.0)
    
    # Offer Metrics
    total_offers_active = IntegerField(string='Total Active Offers', default=0)
    total_offer_usage = IntegerField(string='Total Offer Usage', default=0)
    total_offer_value = FloatField(string='Total Offer Value', digits=(16, 2), default=0.0)
    average_offer_value = FloatField(string='Average Offer Value', digits=(16, 2), default=0.0)
    
    # Tier Metrics
    tier_distribution = TextField(string='Tier Distribution')
    tier_upgrades = IntegerField(string='Tier Upgrades', default=0)
    tier_downgrades = IntegerField(string='Tier Downgrades', default=0)
    tier_retention_rate = FloatField(string='Tier Retention Rate', digits=(16, 2), default=0.0)
    
    # Kids Clothing Metrics
    age_group_breakdown = TextField(string='Age Group Breakdown')
    gender_breakdown = TextField(string='Gender Breakdown')
    seasonal_breakdown = TextField(string='Seasonal Breakdown')
    
    # Special Metrics
    birthday_offers_sent = IntegerField(string='Birthday Offers Sent', default=0)
    birthday_offers_used = IntegerField(string='Birthday Offers Used', default=0)
    referral_signups = IntegerField(string='Referral Signups', default=0)
    referral_rewards_given = IntegerField(string='Referral Rewards Given', default=0)
    
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
        """Create loyalty analytics with validation"""
        if 'date' in vals and 'program_id' in vals:
            # Check for duplicate analytics
            existing = self.search([
                ('date', '=', vals['date']),
                ('program_id', '=', vals['program_id']),
                ('period_type', '=', vals.get('period_type', 'daily')),
            ])
            if existing:
                raise ValidationError('Analytics already exists for this date and program!')
        
        return super(LoyaltyAnalytics, self).create(vals)
    
    def action_generate_analytics(self):
        """Generate analytics for the period"""
        # This would implement analytics generation logic
        pass
    
    def action_export_analytics(self):
        """Export analytics data"""
        # This would implement analytics export logic
        pass


class LoyaltyCustomerAnalytics(BaseModel):
    """Loyalty Customer Analytics"""
    
    _name = 'loyalty.customer.analytics'
    _description = 'Loyalty Customer Analytics'
    _order = 'partner_id, date desc'
    
    name = CharField(string='Reference', required=True, size=64)
    partner_id = Many2oneField('res.partner', string='Customer', required=True)
    program_id = Many2oneField('loyalty.program', string='Loyalty Program', related='partner_id.loyalty_program_id', store=True)
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
    
    # Points Metrics
    total_points_earned = IntegerField(string='Total Points Earned', default=0)
    total_points_redeemed = IntegerField(string='Total Points Redeemed', default=0)
    total_points_expired = IntegerField(string='Total Points Expired', default=0)
    current_points_balance = IntegerField(string='Current Points Balance', default=0)
    points_redemption_rate = FloatField(string='Points Redemption Rate', digits=(16, 2), default=0.0)
    
    # Rewards Metrics
    total_rewards_redeemed = IntegerField(string='Total Rewards Redeemed', default=0)
    total_reward_value = FloatField(string='Total Reward Value', digits=(16, 2), default=0.0)
    average_reward_value = FloatField(string='Average Reward Value', digits=(16, 2), default=0.0)
    
    # Voucher Metrics
    total_vouchers_received = IntegerField(string='Total Vouchers Received', default=0)
    total_vouchers_used = IntegerField(string='Total Vouchers Used', default=0)
    total_vouchers_expired = IntegerField(string='Total Vouchers Expired', default=0)
    voucher_usage_rate = FloatField(string='Voucher Usage Rate', digits=(16, 2), default=0.0)
    
    # Offer Metrics
    total_offers_used = IntegerField(string='Total Offers Used', default=0)
    total_offer_value = FloatField(string='Total Offer Value', digits=(16, 2), default=0.0)
    average_offer_value = FloatField(string='Average Offer Value', digits=(16, 2), default=0.0)
    
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
    birthday_offers_received = IntegerField(string='Birthday Offers Received', default=0)
    birthday_offers_used = IntegerField(string='Birthday Offers Used', default=0)
    referral_count = IntegerField(string='Referral Count', default=0)
    referral_rewards_earned = IntegerField(string='Referral Rewards Earned', default=0)
    
    # System Fields
    create_date = DateTimeField(string='Created On', readonly=True)
    write_date = DateTimeField(string='Last Updated', readonly=True)
    create_uid = Many2oneField('res.users', string='Created By', readonly=True)
    write_uid = Many2oneField('res.users', string='Updated By', readonly=True)