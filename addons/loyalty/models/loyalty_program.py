# -*- coding: utf-8 -*-

from core_framework.orm import BaseModel, CharField, TextField, IntegerField, FloatField, BooleanField, DateField, DateTimeField, Many2oneField, One2manyField, SelectionField
from core_framework.exceptions import ValidationError


class LoyaltyProgram(BaseModel):
    """Loyalty Program Management"""
    
    _name = 'loyalty.program'
    _description = 'Loyalty Program'
    _order = 'name'
    
    name = CharField(string='Program Name', required=True, size=100)
    code = CharField(string='Program Code', required=True, size=20)
    description = TextField(string='Description')
    
    # Program Configuration
    is_active = BooleanField(string='Active', default=True)
    start_date = DateField(string='Start Date', required=True)
    end_date = DateField(string='End Date')
    
    # Points Configuration
    points_per_currency = FloatField(string='Points per Currency Unit', default=1.0, digits=(16, 2))
    currency_id = Many2oneField('res.currency', string='Currency', required=True)
    min_points_redemption = IntegerField(string='Minimum Points for Redemption', default=100)
    max_points_redemption = IntegerField(string='Maximum Points per Redemption', default=10000)
    
    # Expiry Configuration
    points_expiry_days = IntegerField(string='Points Expiry (Days)', default=365)
    expiry_notification_days = IntegerField(string='Expiry Notification (Days)', default=30)
    
    # Tier Configuration
    tier_based = BooleanField(string='Tier Based Program', default=False)
    tier_ids = One2manyField('loyalty.tier', 'program_id', string='Tiers')
    
    # Customer Configuration
    customer_ids = One2manyField('res.partner', 'loyalty_program_id', string='Customers')
    customer_count = IntegerField(string='Customer Count', compute='_compute_customer_count', store=True)
    
    # Analytics
    total_points_earned = IntegerField(string='Total Points Earned', compute='_compute_analytics', store=True)
    total_points_redeemed = IntegerField(string='Total Points Redeemed', compute='_compute_analytics', store=True)
    total_rewards_given = IntegerField(string='Total Rewards Given', compute='_compute_analytics', store=True)
    total_vouchers_issued = IntegerField(string='Total Vouchers Issued', compute='_compute_analytics', store=True)
    
    # Kids Clothing Specific
    age_group_focus = SelectionField([
        ('newborn', 'Newborn (0-6 months)'),
        ('infant', 'Infant (6-18 months)'),
        ('toddler', 'Toddler (18 months-3 years)'),
        ('preschool', 'Preschool (3-5 years)'),
        ('school', 'School (5-12 years)'),
        ('teen', 'Teen (12-18 years)'),
        ('all', 'All Age Groups'),
    ], string='Age Group Focus', default='all')
    
    gender_focus = SelectionField([
        ('boys', 'Boys'),
        ('girls', 'Girls'),
        ('unisex', 'Unisex'),
        ('all', 'All Genders'),
    ], string='Gender Focus', default='all')
    
    seasonal_focus = SelectionField([
        ('summer', 'Summer'),
        ('winter', 'Winter'),
        ('monsoon', 'Monsoon'),
        ('all', 'All Seasons'),
    ], string='Seasonal Focus', default='all')
    
    # Special Features
    birthday_offers = BooleanField(string='Birthday Offers', default=True)
    referral_program = BooleanField(string='Referral Program', default=False)
    referral_points = IntegerField(string='Referral Points', default=100)
    
    # System Fields
    create_date = DateTimeField(string='Created On', readonly=True)
    write_date = DateTimeField(string='Last Updated', readonly=True)
    create_uid = Many2oneField('res.users', string='Created By', readonly=True)
    write_uid = Many2oneField('res.users', string='Updated By', readonly=True)
    
    def _compute_customer_count(self):
        """Compute total customer count"""
        for record in self:
            record.customer_count = len(record.customer_ids)
    
    def _compute_analytics(self):
        """Compute loyalty program analytics"""
        for record in self:
            # This would be implemented with actual analytics computation
            record.total_points_earned = 0
            record.total_points_redeemed = 0
            record.total_rewards_given = 0
            record.total_vouchers_issued = 0
    
    def create(self, vals):
        """Create loyalty program with validation"""
        if 'code' in vals:
            # Check for duplicate codes
            existing = self.search([('code', '=', vals['code'])])
            if existing:
                raise ValidationError('Loyalty program code must be unique!')
        
        return super(LoyaltyProgram, self).create(vals)
    
    def write(self, vals):
        """Update loyalty program with validation"""
        if 'code' in vals:
            # Check for duplicate codes
            existing = self.search([('code', '=', vals['code']), ('id', '!=', self.id)])
            if existing:
                raise ValidationError('Loyalty program code must be unique!')
        
        return super(LoyaltyProgram, self).write(vals)
    
    def action_activate(self):
        """Activate loyalty program"""
        self.write({'is_active': True})
    
    def action_deactivate(self):
        """Deactivate loyalty program"""
        self.write({'is_active': False})
    
    def action_view_customers(self):
        """View program customers"""
        return {
            'type': 'ir.actions.act_window',
            'name': 'Program Customers',
            'res_model': 'res.partner',
            'view_mode': 'tree,form',
            'domain': [('loyalty_program_id', '=', self.id)],
        }
    
    def action_view_analytics(self):
        """View program analytics"""
        return {
            'type': 'ir.actions.act_window',
            'name': 'Program Analytics',
            'res_model': 'loyalty.analytics',
            'view_mode': 'tree,form',
            'domain': [('program_id', '=', self.id)],
        }