# -*- coding: utf-8 -*-

from core_framework.orm import BaseModel, CharField, TextField, IntegerField, FloatField, BooleanField, DateField, DateTimeField, Many2oneField, One2manyField, SelectionField
from core_framework.exceptions import ValidationError


class DiscountCouponTemplate(BaseModel):
    """Discount Coupon Template"""
    
    _name = 'discount.coupon.template'
    _description = 'Discount Coupon Template'
    _order = 'name'
    
    name = CharField(string='Template Name', required=True, size=100)
    code = CharField(string='Template Code', required=True, size=20)
    description = TextField(string='Description')
    
    # Template Configuration
    is_active = BooleanField(string='Active', default=True)
    program_id = Many2oneField('discount.program', string='Discount Program', required=True)
    
    # Coupon Configuration
    coupon_type = SelectionField([
        ('percentage', 'Percentage'),
        ('fixed', 'Fixed Amount'),
        ('buy_x_get_y', 'Buy X Get Y'),
        ('free_shipping', 'Free Shipping'),
        ('loyalty_points', 'Loyalty Points'),
    ], string='Coupon Type', required=True, default='percentage')
    
    discount_value = FloatField(string='Discount Value', digits=(16, 2))
    discount_currency_id = Many2oneField('res.currency', string='Discount Currency')
    min_purchase_amount = FloatField(string='Minimum Purchase Amount', digits=(16, 2), default=0.0)
    max_discount_amount = FloatField(string='Maximum Discount Amount', digits=(16, 2))
    
    # Buy X Get Y Configuration
    buy_quantity = IntegerField(string='Buy Quantity', default=1)
    get_quantity = IntegerField(string='Get Quantity', default=1)
    get_discount_percentage = FloatField(string='Get Discount Percentage', digits=(16, 2), default=100.0)
    
    # Validity
    validity_days = IntegerField(string='Validity (Days)', default=30)
    expiry_date = DateField(string='Expiry Date')
    
    # Usage Limits
    usage_limit = IntegerField(string='Usage Limit', default=1)
    usage_limit_per_customer = IntegerField(string='Usage Limit per Customer', default=1)
    
    # Kids Clothing Specific
    age_group_target = SelectionField([
        ('newborn', 'Newborn (0-6 months)'),
        ('infant', 'Infant (6-18 months)'),
        ('toddler', 'Toddler (18 months-3 years)'),
        ('preschool', 'Preschool (3-5 years)'),
        ('school', 'School (5-12 years)'),
        ('teen', 'Teen (12-18 years)'),
        ('all', 'All Age Groups'),
    ], string='Age Group Target', default='all')
    
    gender_target = SelectionField([
        ('boys', 'Boys'),
        ('girls', 'Girls'),
        ('unisex', 'Unisex'),
        ('all', 'All Genders'),
    ], string='Gender Target', default='all')
    
    season_target = SelectionField([
        ('summer', 'Summer'),
        ('winter', 'Winter'),
        ('monsoon', 'Monsoon'),
        ('all', 'All Seasons'),
    ], string='Season Target', default='all')
    
    # Special Features
    is_birthday_coupon = BooleanField(string='Birthday Coupon', default=False)
    is_referral_coupon = BooleanField(string='Referral Coupon', default=False)
    is_tier_exclusive = BooleanField(string='Tier Exclusive', default=False)
    tier_id = Many2oneField('loyalty.tier', string='Required Tier')
    
    # Coupon Generation
    coupon_ids = One2manyField('discount.coupon', 'template_id', string='Generated Coupons')
    coupon_count = IntegerField(string='Coupon Count', compute='_compute_coupon_count', store=True)
    
    # System Fields
    create_date = DateTimeField(string='Created On', readonly=True)
    write_date = DateTimeField(string='Last Updated', readonly=True)
    create_uid = Many2oneField('res.users', string='Created By', readonly=True)
    write_uid = Many2oneField('res.users', string='Updated By', readonly=True)
    
    def _compute_coupon_count(self):
        """Compute coupon count"""
        for record in self:
            record.coupon_count = len(record.coupon_ids)
    
    def create(self, vals):
        """Create coupon template with validation"""
        if 'code' in vals:
            # Check for duplicate codes
            existing = self.search([('code', '=', vals['code'])])
            if existing:
                raise ValidationError('Coupon template code must be unique!')
        
        return super(DiscountCouponTemplate, self).create(vals)
    
    def write(self, vals):
        """Update coupon template with validation"""
        if 'code' in vals:
            # Check for duplicate codes
            existing = self.search([('code', '=', vals['code']), ('id', '!=', self.id)])
            if existing:
                raise ValidationError('Coupon template code must be unique!')
        
        return super(DiscountCouponTemplate, self).write(vals)
    
    def action_generate_coupons(self, quantity, partner_id=None):
        """Generate coupons from template"""
        coupons = []
        for i in range(quantity):
            coupon_vals = {
                'template_id': self.id,
                'partner_id': partner_id,
                'program_id': self.program_id.id,
                'coupon_type': self.coupon_type,
                'discount_value': self.discount_value,
                'discount_currency_id': self.discount_currency_id.id if self.discount_currency_id else False,
                'min_purchase_amount': self.min_purchase_amount,
                'max_discount_amount': self.max_discount_amount,
                'buy_quantity': self.buy_quantity,
                'get_quantity': self.get_quantity,
                'get_discount_percentage': self.get_discount_percentage,
                'validity_days': self.validity_days,
                'expiry_date': self.expiry_date,
                'usage_limit': self.usage_limit,
                'usage_limit_per_customer': self.usage_limit_per_customer,
                'age_group_target': self.age_group_target,
                'gender_target': self.gender_target,
                'season_target': self.season_target,
                'is_birthday_coupon': self.is_birthday_coupon,
                'is_referral_coupon': self.is_referral_coupon,
                'is_tier_exclusive': self.is_tier_exclusive,
                'tier_id': self.tier_id.id if self.tier_id else False,
            }
            coupons.append(self.env['discount.coupon'].create(coupon_vals))
        
        return coupons


class DiscountCoupon(BaseModel):
    """Discount Coupon"""
    
    _name = 'discount.coupon'
    _description = 'Discount Coupon'
    _order = 'expiry_date, name'
    
    name = CharField(string='Coupon Code', required=True, size=64)
    template_id = Many2oneField('discount.coupon.template', string='Template', required=True)
    partner_id = Many2oneField('res.partner', string='Customer')
    program_id = Many2oneField('discount.program', string='Discount Program', related='template_id.program_id', store=True)
    
    # Coupon Configuration
    coupon_type = SelectionField([
        ('percentage', 'Percentage'),
        ('fixed', 'Fixed Amount'),
        ('buy_x_get_y', 'Buy X Get Y'),
        ('free_shipping', 'Free Shipping'),
        ('loyalty_points', 'Loyalty Points'),
    ], string='Coupon Type', required=True, default='percentage')
    
    discount_value = FloatField(string='Discount Value', digits=(16, 2))
    discount_currency_id = Many2oneField('res.currency', string='Discount Currency')
    min_purchase_amount = FloatField(string='Minimum Purchase Amount', digits=(16, 2), default=0.0)
    max_discount_amount = FloatField(string='Maximum Discount Amount', digits=(16, 2))
    
    # Buy X Get Y Configuration
    buy_quantity = IntegerField(string='Buy Quantity', default=1)
    get_quantity = IntegerField(string='Get Quantity', default=1)
    get_discount_percentage = FloatField(string='Get Discount Percentage', digits=(16, 2), default=100.0)
    
    # Validity
    validity_days = IntegerField(string='Validity (Days)', default=30)
    expiry_date = DateField(string='Expiry Date', required=True)
    is_expired = BooleanField(string='Expired', compute='_compute_is_expired', store=True)
    
    # Usage Tracking
    usage_count = IntegerField(string='Usage Count', default=0)
    usage_limit = IntegerField(string='Usage Limit', default=1)
    usage_limit_per_customer = IntegerField(string='Usage Limit per Customer', default=1)
    is_used = BooleanField(string='Used', compute='_compute_is_used', store=True)
    
    # Status
    state = SelectionField([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('used', 'Used'),
        ('expired', 'Expired'),
        ('cancelled', 'Cancelled'),
    ], string='State', default='draft', required=True)
    
    # Kids Clothing Context
    age_group_target = SelectionField([
        ('newborn', 'Newborn (0-6 months)'),
        ('infant', 'Infant (6-18 months)'),
        ('toddler', 'Toddler (18 months-3 years)'),
        ('preschool', 'Preschool (3-5 years)'),
        ('school', 'School (5-12 years)'),
        ('teen', 'Teen (12-18 years)'),
    ], string='Age Group Target')
    
    gender_target = SelectionField([
        ('boys', 'Boys'),
        ('girls', 'Girls'),
        ('unisex', 'Unisex'),
    ], string='Gender Target')
    
    season_target = SelectionField([
        ('summer', 'Summer'),
        ('winter', 'Winter'),
        ('monsoon', 'Monsoon'),
    ], string='Season Target')
    
    # Special Features
    is_birthday_coupon = BooleanField(string='Birthday Coupon', default=False)
    is_referral_coupon = BooleanField(string='Referral Coupon', default=False)
    is_tier_exclusive = BooleanField(string='Tier Exclusive', default=False)
    tier_id = Many2oneField('loyalty.tier', string='Required Tier')
    
    # Usage History
    usage_ids = One2manyField('discount.coupon.usage', 'coupon_id', string='Usage History')
    
    # System Fields
    create_date = DateTimeField(string='Created On', readonly=True)
    write_date = DateTimeField(string='Last Updated', readonly=True)
    create_uid = Many2oneField('res.users', string='Created By', readonly=True)
    write_uid = Many2oneField('res.users', string='Updated By', readonly=True)
    
    def _compute_is_expired(self):
        """Compute if coupon is expired"""
        for record in self:
            if record.expiry_date:
                from datetime import date
                record.is_expired = record.expiry_date < date.today()
            else:
                record.is_expired = False
    
    def _compute_is_used(self):
        """Compute if coupon is used"""
        for record in self:
            record.is_used = record.usage_count >= record.usage_limit
    
    def create(self, vals):
        """Create coupon with validation"""
        if 'name' not in vals:
            # Generate unique coupon code
            vals['name'] = self._generate_coupon_code()
        
        return super(DiscountCoupon, self).create(vals)
    
    def _generate_coupon_code(self):
        """Generate unique coupon code"""
        import random
        import string
        
        while True:
            code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
            if not self.search([('name', '=', code)]):
                return code
    
    def action_activate(self):
        """Activate coupon"""
        self.write({'state': 'active'})
    
    def action_use(self, partner_id=None, order_id=None):
        """Use coupon"""
        if self.state != 'active':
            raise ValidationError('Coupon is not active!')
        
        if self.is_expired:
            raise ValidationError('Coupon has expired!')
        
        if self.is_used:
            raise ValidationError('Coupon has already been used!')
        
        # Create usage record
        usage = self.env['discount.coupon.usage'].create({
            'coupon_id': self.id,
            'partner_id': partner_id or self.partner_id.id,
            'order_id': order_id,
            'usage_date': self.env['datetime'].now(),
        })
        
        # Update usage count
        self.write({'usage_count': self.usage_count + 1})
        
        if self.usage_count >= self.usage_limit:
            self.write({'state': 'used'})
        
        return usage
    
    def action_cancel(self):
        """Cancel coupon"""
        self.write({'state': 'cancelled'})
    
    def action_expire(self):
        """Mark coupon as expired"""
        self.write({'state': 'expired'})


class DiscountCouponUsage(BaseModel):
    """Discount Coupon Usage"""
    
    _name = 'discount.coupon.usage'
    _description = 'Discount Coupon Usage'
    _order = 'usage_date desc, id desc'
    
    name = CharField(string='Reference', required=True, size=64)
    coupon_id = Many2oneField('discount.coupon', string='Coupon', required=True)
    partner_id = Many2oneField('res.partner', string='Customer', required=True)
    program_id = Many2oneField('discount.program', string='Discount Program', related='coupon_id.program_id', store=True)
    
    # Usage Details
    usage_date = DateTimeField(string='Usage Date', required=True, default=lambda self: self.env['datetime'].now())
    order_id = Many2oneField('sale.order', string='Sale Order')
    discount_amount = FloatField(string='Discount Amount', digits=(16, 2))
    points_earned = IntegerField(string='Points Earned', default=0)
    
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
    create_date = DateTimeField(string='Created On', readonly=True)
    write_date = DateTimeField(string='Last Updated', readonly=True)
    create_uid = Many2oneField('res.users', string='Created By', readonly=True)
    write_uid = Many2oneField('res.users', string='Updated By', readonly=True)