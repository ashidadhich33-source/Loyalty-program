# -*- coding: utf-8 -*-

from core_framework.orm import BaseModel, CharField, TextField, IntegerField, FloatField, BooleanField, DateField, DateTimeField, Many2oneField, One2manyField, SelectionField
from core_framework.exceptions import ValidationError


class DiscountProgram(BaseModel):
    """Discount Program Management"""
    
    _name = 'discount.program'
    _description = 'Discount Program'
    _order = 'name'
    
    name = CharField(string='Program Name', required=True, size=100)
    code = CharField(string='Program Code', required=True, size=20)
    description = TextField(string='Description')
    
    # Program Configuration
    is_active = BooleanField(string='Active', default=True)
    start_date = DateField(string='Start Date', required=True)
    end_date = DateField(string='End Date')
    is_permanent = BooleanField(string='Permanent Program', default=False)
    
    # Program Type
    program_type = SelectionField([
        ('seasonal', 'Seasonal Discount'),
        ('promotional', 'Promotional Discount'),
        ('loyalty', 'Loyalty Discount'),
        ('bulk', 'Bulk Discount'),
        ('first_purchase', 'First Purchase Discount'),
        ('referral', 'Referral Discount'),
        ('birthday', 'Birthday Discount'),
        ('anniversary', 'Anniversary Discount'),
        ('custom', 'Custom Discount'),
    ], string='Program Type', required=True, default='promotional')
    
    # Discount Configuration
    discount_type = SelectionField([
        ('percentage', 'Percentage'),
        ('fixed', 'Fixed Amount'),
        ('buy_x_get_y', 'Buy X Get Y'),
        ('free_shipping', 'Free Shipping'),
        ('loyalty_points', 'Loyalty Points'),
    ], string='Discount Type', required=True, default='percentage')
    
    discount_value = FloatField(string='Discount Value', digits=(16, 2))
    discount_currency_id = Many2oneField('res.currency', string='Discount Currency')
    min_purchase_amount = FloatField(string='Minimum Purchase Amount', digits=(16, 2), default=0.0)
    max_discount_amount = FloatField(string='Maximum Discount Amount', digits=(16, 2))
    
    # Buy X Get Y Configuration
    buy_quantity = IntegerField(string='Buy Quantity', default=1)
    get_quantity = IntegerField(string='Get Quantity', default=1)
    get_discount_percentage = FloatField(string='Get Discount Percentage', digits=(16, 2), default=100.0)
    
    # Usage Limits
    usage_limit = IntegerField(string='Usage Limit', default=0)  # 0 = unlimited
    usage_limit_per_customer = IntegerField(string='Usage Limit per Customer', default=1)
    usage_limit_per_day = IntegerField(string='Usage Limit per Day', default=0)  # 0 = unlimited
    
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
    
    # Product/Category Targeting
    product_ids = One2manyField('discount.program.product', 'program_id', string='Products')
    category_ids = One2manyField('discount.program.category', 'program_id', string='Categories')
    
    # Customer Targeting
    customer_segment = SelectionField([
        ('all', 'All Customers'),
        ('new', 'New Customers'),
        ('existing', 'Existing Customers'),
        ('loyalty_tier', 'Loyalty Tier Based'),
        ('age_group', 'Age Group Based'),
        ('gender', 'Gender Based'),
        ('seasonal', 'Seasonal Based'),
    ], string='Customer Segment', default='all')
    
    loyalty_tier_id = Many2oneField('loyalty.tier', string='Required Loyalty Tier')
    min_loyalty_points = IntegerField(string='Minimum Loyalty Points', default=0)
    
    # Approval Configuration
    requires_approval = BooleanField(string='Requires Approval', default=False)
    approval_workflow_id = Many2oneField('discount.approval.workflow', string='Approval Workflow')
    auto_approve = BooleanField(string='Auto Approve', default=True)
    
    # Coupon Configuration
    use_coupons = BooleanField(string='Use Coupons', default=False)
    coupon_template_id = Many2oneField('discount.coupon.template', string='Coupon Template')
    coupon_quantity = IntegerField(string='Coupon Quantity', default=0)  # 0 = unlimited
    
    # Analytics
    total_usage = IntegerField(string='Total Usage', default=0)
    total_customers = IntegerField(string='Total Customers', default=0)
    total_discount_amount = FloatField(string='Total Discount Amount', digits=(16, 2), default=0.0)
    average_discount_amount = FloatField(string='Average Discount Amount', digits=(16, 2), default=0.0)
    
    # System Fields
    create_date = DateTimeField(string='Created On', readonly=True)
    write_date = DateTimeField(string='Last Updated', readonly=True)
    create_uid = Many2oneField('res.users', string='Created By', readonly=True)
    write_uid = Many2oneField('res.users', string='Updated By', readonly=True)
    
    def create(self, vals):
        """Create discount program with validation"""
        if 'code' in vals:
            # Check for duplicate codes
            existing = self.search([('code', '=', vals['code'])])
            if existing:
                raise ValidationError('Discount program code must be unique!')
        
        if 'start_date' in vals and 'end_date' in vals:
            if vals['start_date'] > vals['end_date']:
                raise ValidationError('Start date cannot be after end date!')
        
        return super(DiscountProgram, self).create(vals)
    
    def write(self, vals):
        """Update discount program with validation"""
        if 'code' in vals:
            # Check for duplicate codes
            existing = self.search([('code', '=', vals['code']), ('id', '!=', self.id)])
            if existing:
                raise ValidationError('Discount program code must be unique!')
        
        if 'start_date' in vals and 'end_date' in vals:
            if vals['start_date'] > vals['end_date']:
                raise ValidationError('Start date cannot be after end date!')
        
        return super(DiscountProgram, self).write(vals)
    
    def action_activate(self):
        """Activate discount program"""
        self.write({'is_active': True})
    
    def action_deactivate(self):
        """Deactivate discount program"""
        self.write({'is_active': False})
    
    def action_generate_coupons(self):
        """Generate coupons for the program"""
        if not self.use_coupons or not self.coupon_template_id:
            raise ValidationError('Coupon template is required to generate coupons!')
        
        # Generate coupons logic would go here
        pass
    
    def action_view_analytics(self):
        """View program analytics"""
        return {
            'type': 'ir.actions.act_window',
            'name': 'Program Analytics',
            'res_model': 'discount.analytics',
            'view_mode': 'tree,form',
            'domain': [('program_id', '=', self.id)],
        }


class DiscountProgramProduct(BaseModel):
    """Discount Program Products"""
    
    _name = 'discount.program.product'
    _description = 'Discount Program Product'
    _order = 'sequence, product_id'
    
    program_id = Many2oneField('discount.program', string='Program', required=True)
    product_id = Many2oneField('product.template', string='Product', required=True)
    sequence = IntegerField(string='Sequence', default=10)
    
    # Product Configuration
    is_required = BooleanField(string='Required Product', default=False)
    min_quantity = IntegerField(string='Minimum Quantity', default=1)
    max_quantity = IntegerField(string='Maximum Quantity', default=0)  # 0 = unlimited
    discount_percentage = FloatField(string='Discount Percentage', digits=(16, 2))
    discount_amount = FloatField(string='Discount Amount', digits=(16, 2))
    
    # System Fields
    create_date = DateTimeField(string='Created On', readonly=True)
    write_date = DateTimeField(string='Last Updated', readonly=True)
    create_uid = Many2oneField('res.users', string='Created By', readonly=True)
    write_uid = Many2oneField('res.users', string='Updated By', readonly=True)


class DiscountProgramCategory(BaseModel):
    """Discount Program Categories"""
    
    _name = 'discount.program.category'
    _description = 'Discount Program Category'
    _order = 'sequence, category_id'
    
    program_id = Many2oneField('discount.program', string='Program', required=True)
    category_id = Many2oneField('product.category', string='Category', required=True)
    sequence = IntegerField(string='Sequence', default=10)
    
    # Category Configuration
    is_required = BooleanField(string='Required Category', default=False)
    min_quantity = IntegerField(string='Minimum Quantity', default=1)
    max_quantity = IntegerField(string='Maximum Quantity', default=0)  # 0 = unlimited
    discount_percentage = FloatField(string='Discount Percentage', digits=(16, 2))
    discount_amount = FloatField(string='Discount Amount', digits=(16, 2))
    
    # System Fields
    create_date = DateTimeField(string='Created On', readonly=True)
    write_date = DateTimeField(string='Last Updated', readonly=True)
    create_uid = Many2oneField('res.users', string='Created By', readonly=True)
    write_uid = Many2oneField('res.users', string='Updated By', readonly=True)