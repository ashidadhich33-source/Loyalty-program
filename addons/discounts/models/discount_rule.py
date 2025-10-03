# -*- coding: utf-8 -*-

from core_framework.orm import BaseModel, CharField, TextField, IntegerField, FloatField, BooleanField, DateField, DateTimeField, Many2oneField, One2manyField, SelectionField
from core_framework.exceptions import ValidationError


class DiscountRule(BaseModel):
    """Discount Rules Management"""
    
    _name = 'discount.rule'
    _description = 'Discount Rule'
    _order = 'sequence, name'
    
    name = CharField(string='Rule Name', required=True, size=100)
    code = CharField(string='Rule Code', required=True, size=20)
    description = TextField(string='Description')
    
    # Rule Configuration
    program_id = Many2oneField('discount.program', string='Discount Program', required=True)
    sequence = IntegerField(string='Sequence', required=True, default=10)
    is_active = BooleanField(string='Active', default=True)
    
    # Rule Type
    rule_type = SelectionField([
        ('product', 'Product Based'),
        ('category', 'Category Based'),
        ('customer', 'Customer Based'),
        ('order', 'Order Based'),
        ('time', 'Time Based'),
        ('loyalty', 'Loyalty Based'),
        ('age_group', 'Age Group Based'),
        ('gender', 'Gender Based'),
        ('seasonal', 'Seasonal Based'),
    ], string='Rule Type', required=True, default='product')
    
    # Rule Conditions
    condition_type = SelectionField([
        ('equals', 'Equals'),
        ('not_equals', 'Not Equals'),
        ('greater_than', 'Greater Than'),
        ('less_than', 'Less Than'),
        ('greater_equal', 'Greater or Equal'),
        ('less_equal', 'Less or Equal'),
        ('contains', 'Contains'),
        ('not_contains', 'Not Contains'),
        ('in', 'In'),
        ('not_in', 'Not In'),
    ], string='Condition Type', required=True, default='equals')
    
    condition_field = CharField(string='Condition Field', required=True, size=100)
    condition_value = TextField(string='Condition Value')
    
    # Discount Application
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
    product_ids = One2manyField('discount.rule.product', 'rule_id', string='Products')
    category_ids = One2manyField('discount.rule.category', 'rule_id', string='Categories')
    
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
    
    # Usage Limits
    usage_limit = IntegerField(string='Usage Limit', default=0)  # 0 = unlimited
    usage_limit_per_customer = IntegerField(string='Usage Limit per Customer', default=1)
    usage_limit_per_day = IntegerField(string='Usage Limit per Day', default=0)  # 0 = unlimited
    
    # Time Based Rules
    time_condition = SelectionField([
        ('always', 'Always'),
        ('business_hours', 'Business Hours'),
        ('weekdays', 'Weekdays'),
        ('weekends', 'Weekends'),
        ('specific_days', 'Specific Days'),
        ('specific_hours', 'Specific Hours'),
    ], string='Time Condition', default='always')
    
    specific_days = CharField(string='Specific Days', size=100)  # Comma separated days
    specific_hours = CharField(string='Specific Hours', size=100)  # Comma separated hours
    
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
        """Create discount rule with validation"""
        if 'code' in vals:
            # Check for duplicate codes
            existing = self.search([('code', '=', vals['code'])])
            if existing:
                raise ValidationError('Discount rule code must be unique!')
        
        return super(DiscountRule, self).create(vals)
    
    def write(self, vals):
        """Update discount rule with validation"""
        if 'code' in vals:
            # Check for duplicate codes
            existing = self.search([('code', '=', vals['code']), ('id', '!=', self.id)])
            if existing:
                raise ValidationError('Discount rule code must be unique!')
        
        return super(DiscountRule, self).write(vals)
    
    def action_activate(self):
        """Activate discount rule"""
        self.write({'is_active': True})
    
    def action_deactivate(self):
        """Deactivate discount rule"""
        self.write({'is_active': False})
    
    def action_test_rule(self, order_data):
        """Test rule against order data"""
        # Rule testing logic would go here
        pass
    
    def action_view_analytics(self):
        """View rule analytics"""
        return {
            'type': 'ir.actions.act_window',
            'name': 'Rule Analytics',
            'res_model': 'discount.analytics',
            'view_mode': 'tree,form',
            'domain': [('rule_id', '=', self.id)],
        }


class DiscountRuleProduct(BaseModel):
    """Discount Rule Products"""
    
    _name = 'discount.rule.product'
    _description = 'Discount Rule Product'
    _order = 'sequence, product_id'
    
    rule_id = Many2oneField('discount.rule', string='Rule', required=True)
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


class DiscountRuleCategory(BaseModel):
    """Discount Rule Categories"""
    
    _name = 'discount.rule.category'
    _description = 'Discount Rule Category'
    _order = 'sequence, category_id'
    
    rule_id = Many2oneField('discount.rule', string='Rule', required=True)
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