# -*- coding: utf-8 -*-

from core_framework.orm import BaseModel, CharField, TextField, IntegerField, FloatField, BooleanField, DateField, DateTimeField, Many2oneField, One2manyField, SelectionField
from core_framework.exceptions import ValidationError


class LoyaltyTier(BaseModel):
    """Loyalty Tier Management"""
    
    _name = 'loyalty.tier'
    _description = 'Loyalty Tier'
    _order = 'sequence, name'
    
    name = CharField(string='Tier Name', required=True, size=100)
    code = CharField(string='Tier Code', required=True, size=20)
    description = TextField(string='Description')
    
    # Tier Configuration
    program_id = Many2oneField('loyalty.program', string='Loyalty Program', required=True)
    sequence = IntegerField(string='Sequence', required=True, default=10)
    is_active = BooleanField(string='Active', default=True)
    
    # Tier Requirements
    min_points = IntegerField(string='Minimum Points', required=True, default=0)
    max_points = IntegerField(string='Maximum Points', default=0)  # 0 = unlimited
    min_purchases = IntegerField(string='Minimum Purchases', default=0)
    min_purchase_amount = FloatField(string='Minimum Purchase Amount', digits=(16, 2), default=0.0)
    min_purchase_frequency = IntegerField(string='Minimum Purchase Frequency (days)', default=0)
    
    # Tier Benefits
    points_multiplier = FloatField(string='Points Multiplier', default=1.0, digits=(16, 2))
    discount_percentage = FloatField(string='Discount Percentage', digits=(16, 2), default=0.0)
    free_shipping = BooleanField(string='Free Shipping', default=False)
    priority_support = BooleanField(string='Priority Support', default=False)
    exclusive_access = BooleanField(string='Exclusive Access', default=False)
    
    # Kids Clothing Specific Benefits
    birthday_bonus_points = IntegerField(string='Birthday Bonus Points', default=0)
    referral_bonus_points = IntegerField(string='Referral Bonus Points', default=0)
    seasonal_bonus_points = IntegerField(string='Seasonal Bonus Points', default=0)
    milestone_bonus_points = IntegerField(string='Milestone Bonus Points', default=0)
    
    # Age Group Benefits
    age_group_benefits = SelectionField([
        ('newborn', 'Newborn (0-6 months)'),
        ('infant', 'Infant (6-18 months)'),
        ('toddler', 'Toddler (18 months-3 years)'),
        ('preschool', 'Preschool (3-5 years)'),
        ('school', 'School (5-12 years)'),
        ('teen', 'Teen (12-18 years)'),
        ('all', 'All Age Groups'),
    ], string='Age Group Benefits', default='all')
    
    gender_benefits = SelectionField([
        ('boys', 'Boys'),
        ('girls', 'Girls'),
        ('unisex', 'Unisex'),
        ('all', 'All Genders'),
    ], string='Gender Benefits', default='all')
    
    seasonal_benefits = SelectionField([
        ('summer', 'Summer'),
        ('winter', 'Winter'),
        ('monsoon', 'Monsoon'),
        ('all', 'All Seasons'),
    ], string='Seasonal Benefits', default='all')
    
    # Tier Progression
    is_entry_tier = BooleanField(string='Entry Tier', default=False)
    is_highest_tier = BooleanField(string='Highest Tier', default=False)
    next_tier_id = Many2oneField('loyalty.tier', string='Next Tier')
    previous_tier_id = Many2oneField('loyalty.tier', string='Previous Tier')
    
    # Customer Tracking
    customer_ids = One2manyField('res.partner', 'loyalty_tier_id', string='Customers')
    customer_count = IntegerField(string='Customer Count', compute='_compute_customer_count', store=True)
    
    # Analytics
    total_points_earned = IntegerField(string='Total Points Earned', compute='_compute_analytics', store=True)
    total_purchases = IntegerField(string='Total Purchases', compute='_compute_analytics', store=True)
    total_purchase_amount = FloatField(string='Total Purchase Amount', compute='_compute_analytics', store=True)
    average_order_value = FloatField(string='Average Order Value', compute='_compute_analytics', store=True)
    
    # System Fields
    create_date = DateTimeField(string='Created On', readonly=True)
    write_date = DateTimeField(string='Last Updated', readonly=True)
    create_uid = Many2oneField('res.users', string='Created By', readonly=True)
    write_uid = Many2oneField('res.users', string='Updated By', readonly=True)
    
    def _compute_customer_count(self):
        """Compute customer count"""
        for record in self:
            record.customer_count = len(record.customer_ids)
    
    def _compute_analytics(self):
        """Compute tier analytics"""
        for record in self:
            # This would be implemented with actual analytics computation
            record.total_points_earned = 0
            record.total_purchases = 0
            record.total_purchase_amount = 0.0
            record.average_order_value = 0.0
    
    def create(self, vals):
        """Create loyalty tier with validation"""
        if 'min_points' in vals and 'max_points' in vals:
            if vals['max_points'] > 0 and vals['min_points'] > vals['max_points']:
                raise ValidationError('Minimum points cannot be greater than maximum points!')
        
        return super(LoyaltyTier, self).create(vals)
    
    def write(self, vals):
        """Update loyalty tier with validation"""
        if 'min_points' in vals and 'max_points' in vals:
            if vals['max_points'] > 0 and vals['min_points'] > vals['max_points']:
                raise ValidationError('Minimum points cannot be greater than maximum points!')
        
        return super(LoyaltyTier, self).write(vals)
    
    def action_view_customers(self):
        """View tier customers"""
        return {
            'type': 'ir.actions.act_window',
            'name': 'Tier Customers',
            'res_model': 'res.partner',
            'view_mode': 'tree,form',
            'domain': [('loyalty_tier_id', '=', self.id)],
        }
    
    def action_view_analytics(self):
        """View tier analytics"""
        return {
            'type': 'ir.actions.act_window',
            'name': 'Tier Analytics',
            'res_model': 'loyalty.tier.analytics',
            'view_mode': 'tree,form',
            'domain': [('tier_id', '=', self.id)],
        }


class LoyaltyTierAnalytics(BaseModel):
    """Loyalty Tier Analytics"""
    
    _name = 'loyalty.tier.analytics'
    _description = 'Loyalty Tier Analytics'
    _order = 'date desc, tier_id'
    
    name = CharField(string='Reference', required=True, size=64)
    tier_id = Many2oneField('loyalty.tier', string='Tier', required=True)
    program_id = Many2oneField('loyalty.program', string='Loyalty Program', related='tier_id.program_id', store=True)
    
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
    new_customers = IntegerField(string='New Customers', default=0)
    upgraded_customers = IntegerField(string='Upgraded Customers', default=0)
    downgraded_customers = IntegerField(string='Downgraded Customers', default=0)
    
    # Purchase Metrics
    total_purchases = IntegerField(string='Total Purchases', default=0)
    total_purchase_amount = FloatField(string='Total Purchase Amount', digits=(16, 2), default=0.0)
    average_order_value = FloatField(string='Average Order Value', digits=(16, 2), default=0.0)
    average_purchase_frequency = FloatField(string='Average Purchase Frequency (days)', digits=(16, 2), default=0.0)
    
    # Points Metrics
    total_points_earned = IntegerField(string='Total Points Earned', default=0)
    total_points_redeemed = IntegerField(string='Total Points Redeemed', default=0)
    points_redemption_rate = FloatField(string='Points Redemption Rate', digits=(16, 2), default=0.0)
    
    # Kids Clothing Metrics
    age_group_breakdown = TextField(string='Age Group Breakdown')
    gender_breakdown = TextField(string='Gender Breakdown')
    seasonal_breakdown = TextField(string='Seasonal Breakdown')
    
    # System Fields
    create_date = DateTimeField(string='Created On', readonly=True)
    write_date = DateTimeField(string='Last Updated', readonly=True)
    create_uid = Many2oneField('res.users', string='Created By', readonly=True)
    write_uid = Many2oneField('res.users', string='Updated By', readonly=True)