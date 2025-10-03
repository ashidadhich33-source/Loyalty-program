# -*- coding: utf-8 -*-

from core_framework.orm import BaseModel, CharField, TextField, IntegerField, FloatField, BooleanField, DateField, DateTimeField, Many2oneField, One2manyField, SelectionField
from core_framework.exceptions import ValidationError


class LoyaltyVoucherTemplate(BaseModel):
    """Loyalty Voucher Template"""
    
    _name = 'loyalty.voucher.template'
    _description = 'Loyalty Voucher Template'
    _order = 'name'
    
    name = CharField(string='Template Name', required=True, size=100)
    code = CharField(string='Template Code', required=True, size=20)
    description = TextField(string='Description')
    
    # Template Configuration
    is_active = BooleanField(string='Active', default=True)
    voucher_type = SelectionField([
        ('discount', 'Discount Voucher'),
        ('product', 'Product Voucher'),
        ('points', 'Points Voucher'),
        ('cash', 'Cash Voucher'),
    ], string='Voucher Type', required=True, default='discount')
    
    # Discount Configuration
    discount_type = SelectionField([
        ('percentage', 'Percentage'),
        ('fixed', 'Fixed Amount'),
    ], string='Discount Type', default='percentage')
    discount_value = FloatField(string='Discount Value', digits=(16, 2))
    discount_currency_id = Many2oneField('res.currency', string='Discount Currency')
    min_purchase_amount = FloatField(string='Minimum Purchase Amount', digits=(16, 2))
    max_discount_amount = FloatField(string='Maximum Discount Amount', digits=(16, 2))
    
    # Product Configuration
    product_id = Many2oneField('product.template', string='Product')
    product_quantity = IntegerField(string='Product Quantity', default=1)
    
    # Points Configuration
    points_value = IntegerField(string='Points Value', default=0)
    
    # Cash Configuration
    cash_value = FloatField(string='Cash Value', digits=(16, 2))
    cash_currency_id = Many2oneField('res.currency', string='Cash Currency')
    
    # Validity
    validity_days = IntegerField(string='Validity (Days)', default=30)
    expiry_date = DateField(string='Expiry Date')
    
    # Usage Limits
    usage_limit = IntegerField(string='Usage Limit', default=1)
    usage_limit_per_customer = IntegerField(string='Usage Limit per Customer', default=1)
    
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
    is_birthday_voucher = BooleanField(string='Birthday Voucher', default=False)
    is_referral_voucher = BooleanField(string='Referral Voucher', default=False)
    is_tier_exclusive = BooleanField(string='Tier Exclusive', default=False)
    tier_id = Many2oneField('loyalty.tier', string='Required Tier')
    
    # Voucher Generation
    voucher_ids = One2manyField('loyalty.voucher', 'template_id', string='Generated Vouchers')
    voucher_count = IntegerField(string='Voucher Count', compute='_compute_voucher_count', store=True)
    
    # System Fields
    create_date = DateTimeField(string='Created On', readonly=True)
    write_date = DateTimeField(string='Last Updated', readonly=True)
    create_uid = Many2oneField('res.users', string='Created By', readonly=True)
    write_uid = Many2oneField('res.users', string='Updated By', readonly=True)
    
    def _compute_voucher_count(self):
        """Compute voucher count"""
        for record in self:
            record.voucher_count = len(record.voucher_ids)
    
    def create(self, vals):
        """Create voucher template with validation"""
        if 'code' in vals:
            # Check for duplicate codes
            existing = self.search([('code', '=', vals['code'])])
            if existing:
                raise ValidationError('Voucher template code must be unique!')
        
        return super(LoyaltyVoucherTemplate, self).create(vals)
    
    def write(self, vals):
        """Update voucher template with validation"""
        if 'code' in vals:
            # Check for duplicate codes
            existing = self.search([('code', '=', vals['code']), ('id', '!=', self.id)])
            if existing:
                raise ValidationError('Voucher template code must be unique!')
        
        return super(LoyaltyVoucherTemplate, self).write(vals)
    
    def action_generate_vouchers(self, quantity, partner_id=None):
        """Generate vouchers from template"""
        vouchers = []
        for i in range(quantity):
            voucher_vals = {
                'template_id': self.id,
                'partner_id': partner_id,
                'voucher_type': self.voucher_type,
                'discount_type': self.discount_type,
                'discount_value': self.discount_value,
                'discount_currency_id': self.discount_currency_id.id if self.discount_currency_id else False,
                'min_purchase_amount': self.min_purchase_amount,
                'max_discount_amount': self.max_discount_amount,
                'product_id': self.product_id.id if self.product_id else False,
                'product_quantity': self.product_quantity,
                'points_value': self.points_value,
                'cash_value': self.cash_value,
                'cash_currency_id': self.cash_currency_id.id if self.cash_currency_id else False,
                'validity_days': self.validity_days,
                'expiry_date': self.expiry_date,
                'usage_limit': self.usage_limit,
                'usage_limit_per_customer': self.usage_limit_per_customer,
                'age_group': self.age_group,
                'gender': self.gender,
                'season': self.season,
                'is_birthday_voucher': self.is_birthday_voucher,
                'is_referral_voucher': self.is_referral_voucher,
                'is_tier_exclusive': self.is_tier_exclusive,
                'tier_id': self.tier_id.id if self.tier_id else False,
            }
            vouchers.append(self.env['loyalty.voucher'].create(voucher_vals))
        
        return vouchers


class LoyaltyVoucher(BaseModel):
    """Loyalty Voucher"""
    
    _name = 'loyalty.voucher'
    _description = 'Loyalty Voucher'
    _order = 'expiry_date, name'
    
    name = CharField(string='Voucher Code', required=True, size=64)
    template_id = Many2oneField('loyalty.voucher.template', string='Template', required=True)
    partner_id = Many2oneField('res.partner', string='Customer')
    program_id = Many2oneField('loyalty.program', string='Loyalty Program', related='partner_id.loyalty_program_id', store=True)
    
    # Voucher Configuration
    voucher_type = SelectionField([
        ('discount', 'Discount Voucher'),
        ('product', 'Product Voucher'),
        ('points', 'Points Voucher'),
        ('cash', 'Cash Voucher'),
    ], string='Voucher Type', required=True, default='discount')
    
    # Discount Configuration
    discount_type = SelectionField([
        ('percentage', 'Percentage'),
        ('fixed', 'Fixed Amount'),
    ], string='Discount Type', default='percentage')
    discount_value = FloatField(string='Discount Value', digits=(16, 2))
    discount_currency_id = Many2oneField('res.currency', string='Discount Currency')
    min_purchase_amount = FloatField(string='Minimum Purchase Amount', digits=(16, 2))
    max_discount_amount = FloatField(string='Maximum Discount Amount', digits=(16, 2))
    
    # Product Configuration
    product_id = Many2oneField('product.template', string='Product')
    product_quantity = IntegerField(string='Product Quantity', default=1)
    
    # Points Configuration
    points_value = IntegerField(string='Points Value', default=0)
    
    # Cash Configuration
    cash_value = FloatField(string='Cash Value', digits=(16, 2))
    cash_currency_id = Many2oneField('res.currency', string='Cash Currency')
    
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
    
    # Special Features
    is_birthday_voucher = BooleanField(string='Birthday Voucher', default=False)
    is_referral_voucher = BooleanField(string='Referral Voucher', default=False)
    is_tier_exclusive = BooleanField(string='Tier Exclusive', default=False)
    tier_id = Many2oneField('loyalty.tier', string='Required Tier')
    
    # Usage History
    usage_ids = One2manyField('loyalty.voucher.usage', 'voucher_id', string='Usage History')
    
    # System Fields
    create_date = DateTimeField(string='Created On', readonly=True)
    write_date = DateTimeField(string='Last Updated', readonly=True)
    create_uid = Many2oneField('res.users', string='Created By', readonly=True)
    write_uid = Many2oneField('res.users', string='Updated By', readonly=True)
    
    def _compute_is_expired(self):
        """Compute if voucher is expired"""
        for record in self:
            if record.expiry_date:
                from datetime import date
                record.is_expired = record.expiry_date < date.today()
            else:
                record.is_expired = False
    
    def _compute_is_used(self):
        """Compute if voucher is used"""
        for record in self:
            record.is_used = record.usage_count >= record.usage_limit
    
    def create(self, vals):
        """Create voucher with validation"""
        if 'name' not in vals:
            # Generate unique voucher code
            vals['name'] = self._generate_voucher_code()
        
        return super(LoyaltyVoucher, self).create(vals)
    
    def _generate_voucher_code(self):
        """Generate unique voucher code"""
        import random
        import string
        
        while True:
            code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
            if not self.search([('name', '=', code)]):
                return code
    
    def action_activate(self):
        """Activate voucher"""
        self.write({'state': 'active'})
    
    def action_use(self, partner_id=None):
        """Use voucher"""
        if self.state != 'active':
            raise ValidationError('Voucher is not active!')
        
        if self.is_expired:
            raise ValidationError('Voucher has expired!')
        
        if self.is_used:
            raise ValidationError('Voucher has already been used!')
        
        # Create usage record
        usage = self.env['loyalty.voucher.usage'].create({
            'voucher_id': self.id,
            'partner_id': partner_id or self.partner_id.id,
            'usage_date': self.env['datetime'].now(),
        })
        
        # Update usage count
        self.write({'usage_count': self.usage_count + 1})
        
        if self.usage_count >= self.usage_limit:
            self.write({'state': 'used'})
        
        return usage
    
    def action_cancel(self):
        """Cancel voucher"""
        self.write({'state': 'cancelled'})
    
    def action_expire(self):
        """Mark voucher as expired"""
        self.write({'state': 'expired'})


class LoyaltyVoucherUsage(BaseModel):
    """Loyalty Voucher Usage"""
    
    _name = 'loyalty.voucher.usage'
    _description = 'Loyalty Voucher Usage'
    _order = 'usage_date desc, id desc'
    
    name = CharField(string='Reference', required=True, size=64)
    voucher_id = Many2oneField('loyalty.voucher', string='Voucher', required=True)
    partner_id = Many2oneField('res.partner', string='Customer', required=True)
    program_id = Many2oneField('loyalty.program', string='Loyalty Program', related='partner_id.loyalty_program_id', store=True)
    
    # Usage Details
    usage_date = DateTimeField(string='Usage Date', required=True, default=lambda self: self.env['datetime'].now())
    order_id = Many2oneField('sale.order', string='Sale Order')
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