# -*- coding: utf-8 -*-

from core_framework.orm import BaseModel, CharField, TextField, IntegerField, FloatField, BooleanField, DateField, DateTimeField, Many2oneField, One2manyField, SelectionField
from core_framework.exceptions import ValidationError


class LoyaltyReward(BaseModel):
    """Loyalty Rewards Catalog"""
    
    _name = 'loyalty.reward'
    _description = 'Loyalty Reward'
    _order = 'points_required, name'
    
    name = CharField(string='Reward Name', required=True, size=100)
    description = TextField(string='Description')
    
    # Reward Configuration
    is_active = BooleanField(string='Active', default=True)
    points_required = IntegerField(string='Points Required', required=True)
    reward_type = SelectionField([
        ('product', 'Product'),
        ('discount', 'Discount'),
        ('voucher', 'Voucher'),
        ('service', 'Service'),
        ('experience', 'Experience'),
    ], string='Reward Type', required=True, default='product')
    
    # Product Reward
    product_id = Many2oneField('product.template', string='Product')
    product_quantity = IntegerField(string='Product Quantity', default=1)
    
    # Discount Reward
    discount_type = SelectionField([
        ('percentage', 'Percentage'),
        ('fixed', 'Fixed Amount'),
    ], string='Discount Type', default='percentage')
    discount_value = FloatField(string='Discount Value', digits=(16, 2))
    discount_currency_id = Many2oneField('res.currency', string='Discount Currency')
    
    # Voucher Reward
    voucher_template_id = Many2oneField('loyalty.voucher.template', string='Voucher Template')
    
    # Availability
    total_quantity = IntegerField(string='Total Quantity', default=0)
    available_quantity = IntegerField(string='Available Quantity', compute='_compute_available_quantity', store=True)
    redeemed_quantity = IntegerField(string='Redeemed Quantity', default=0)
    
    # Kids Clothing Specific
    age_group = SelectionField([
        ('newborn', 'Newborn (0-6 months)'),
        ('infant', 'Infant (6-18 months)'),
        ('toddler', 'Toddler (18 months-3 years)'),
        ('preschool', 'Preschool (3-5 years)'),
        ('school', 'School (5-12 years)'),
        ('teen', 'Teen (12-18 years)'),
        ('all', 'All Age Groups'),
    ], string='Age Group', default='all')
    
    gender = SelectionField([
        ('boys', 'Boys'),
        ('girls', 'Girls'),
        ('unisex', 'Unisex'),
        ('all', 'All Genders'),
    ], string='Gender', default='all')
    
    season = SelectionField([
        ('summer', 'Summer'),
        ('winter', 'Winter'),
        ('monsoon', 'Monsoon'),
        ('all', 'All Seasons'),
    ], string='Season', default='all')
    
    # Special Features
    is_birthday_reward = BooleanField(string='Birthday Reward', default=False)
    is_referral_reward = BooleanField(string='Referral Reward', default=False)
    is_tier_exclusive = BooleanField(string='Tier Exclusive', default=False)
    tier_id = Many2oneField('loyalty.tier', string='Required Tier')
    
    # Redemption Tracking
    redemption_ids = One2manyField('loyalty.redemption', 'reward_id', string='Redemptions')
    redemption_count = IntegerField(string='Redemption Count', compute='_compute_redemption_count', store=True)
    
    # System Fields
    create_date = DateTimeField(string='Created On', readonly=True)
    write_date = DateTimeField(string='Last Updated', readonly=True)
    create_uid = Many2oneField('res.users', string='Created By', readonly=True)
    write_uid = Many2oneField('res.users', string='Updated By', readonly=True)
    
    def _compute_available_quantity(self):
        """Compute available quantity"""
        for record in self:
            if record.total_quantity > 0:
                record.available_quantity = record.total_quantity - record.redeemed_quantity
            else:
                record.available_quantity = -1  # Unlimited
    
    def _compute_redemption_count(self):
        """Compute redemption count"""
        for record in self:
            record.redemption_count = len(record.redemption_ids)
    
    def create(self, vals):
        """Create loyalty reward with validation"""
        if 'points_required' in vals and vals['points_required'] <= 0:
            raise ValidationError('Points required must be greater than zero!')
        
        return super(LoyaltyReward, self).create(vals)
    
    def write(self, vals):
        """Update loyalty reward with validation"""
        if 'points_required' in vals and vals['points_required'] <= 0:
            raise ValidationError('Points required must be greater than zero!')
        
        return super(LoyaltyReward, self).write(vals)
    
    def action_redeem(self, partner_id, quantity=1):
        """Redeem reward for customer"""
        if not self.is_active:
            raise ValidationError('Reward is not active!')
        
        if self.available_quantity >= 0 and self.available_quantity < quantity:
            raise ValidationError('Insufficient reward quantity available!')
        
        # Create redemption record
        redemption = self.env['loyalty.redemption'].create({
            'partner_id': partner_id,
            'reward_id': self.id,
            'quantity': quantity,
            'points_used': self.points_required * quantity,
        })
        
        # Update redeemed quantity
        self.write({'redeemed_quantity': self.redeemed_quantity + quantity})
        
        return redemption


class LoyaltyRedemption(BaseModel):
    """Loyalty Reward Redemption"""
    
    _name = 'loyalty.redemption'
    _description = 'Loyalty Redemption'
    _order = 'date desc, id desc'
    
    name = CharField(string='Reference', required=True, size=64)
    partner_id = Many2oneField('res.partner', string='Customer', required=True)
    reward_id = Many2oneField('loyalty.reward', string='Reward', required=True)
    program_id = Many2oneField('loyalty.program', string='Loyalty Program', related='partner_id.loyalty_program_id', store=True)
    
    # Redemption Details
    quantity = IntegerField(string='Quantity', required=True, default=1)
    points_used = IntegerField(string='Points Used', required=True)
    points_per_unit = IntegerField(string='Points per Unit', compute='_compute_points_per_unit', store=True)
    
    # Status
    state = SelectionField([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('fulfilled', 'Fulfilled'),
        ('cancelled', 'Cancelled'),
    ], string='State', default='draft', required=True)
    
    # Fulfillment
    fulfillment_date = DateField(string='Fulfillment Date')
    fulfillment_note = TextField(string='Fulfillment Note')
    
    # Kids Clothing Context
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
    
    # Additional Information
    description = TextField(string='Description')
    note = TextField(string='Internal Note')
    
    # System Fields
    date = DateTimeField(string='Date', required=True, default=lambda self: self.env['datetime'].now())
    create_date = DateTimeField(string='Created On', readonly=True)
    write_date = DateTimeField(string='Last Updated', readonly=True)
    create_uid = Many2oneField('res.users', string='Created By', readonly=True)
    write_uid = Many2oneField('res.users', string='Updated By', readonly=True)
    
    def _compute_points_per_unit(self):
        """Compute points per unit"""
        for record in self:
            if record.quantity > 0:
                record.points_per_unit = record.points_used / record.quantity
            else:
                record.points_per_unit = 0
    
    def action_confirm(self):
        """Confirm redemption"""
        self.write({'state': 'confirmed'})
    
    def action_fulfill(self):
        """Mark redemption as fulfilled"""
        self.write({
            'state': 'fulfilled',
            'fulfillment_date': self.env['datetime'].now().date(),
        })
    
    def action_cancel(self):
        """Cancel redemption"""
        self.write({'state': 'cancelled'})