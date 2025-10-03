# -*- coding: utf-8 -*-

from core_framework.orm import BaseModel, CharField, TextField, IntegerField, FloatField, BooleanField, DateField, DateTimeField, Many2oneField, One2manyField, SelectionField
from core_framework.exceptions import ValidationError


class DiscountCampaign(BaseModel):
    """Discount Campaign Management"""
    
    _name = 'discount.campaign'
    _description = 'Discount Campaign'
    _order = 'start_date desc, name'
    
    name = CharField(string='Campaign Name', required=True, size=100)
    code = CharField(string='Campaign Code', required=True, size=20)
    description = TextField(string='Description')
    
    # Campaign Configuration
    is_active = BooleanField(string='Active', default=True)
    campaign_type = SelectionField([
        ('seasonal', 'Seasonal Campaign'),
        ('promotional', 'Promotional Campaign'),
        ('loyalty', 'Loyalty Campaign'),
        ('birthday', 'Birthday Campaign'),
        ('referral', 'Referral Campaign'),
        ('anniversary', 'Anniversary Campaign'),
        ('custom', 'Custom Campaign'),
    ], string='Campaign Type', required=True, default='promotional')
    
    # Campaign Period
    start_date = DateField(string='Start Date', required=True)
    end_date = DateField(string='End Date')
    is_permanent = BooleanField(string='Permanent Campaign', default=False)
    
    # Campaign Settings
    program_id = Many2oneField('discount.program', string='Discount Program', required=True)
    workflow_id = Many2oneField('discount.approval.workflow', string='Approval Workflow')
    coupon_template_id = Many2oneField('discount.coupon.template', string='Coupon Template')
    
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
    product_ids = One2manyField('discount.campaign.product', 'campaign_id', string='Products')
    category_ids = One2manyField('discount.campaign.category', 'campaign_id', string='Categories')
    
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
    
    # Campaign Rules
    rule_ids = One2manyField('discount.campaign.rule', 'campaign_id', string='Campaign Rules')
    rule_count = IntegerField(string='Rule Count', compute='_compute_rule_count', store=True)
    
    # Special Features
    is_automatic = BooleanField(string='Automatic Campaign', default=False)
    is_notification_sent = BooleanField(string='Notification Sent', default=False)
    notification_template_id = Many2oneField('mail.template', string='Notification Template')
    
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
    
    def _compute_rule_count(self):
        """Compute rule count"""
        for record in self:
            record.rule_count = len(record.rule_ids)
    
    def create(self, vals):
        """Create discount campaign with validation"""
        if 'code' in vals:
            # Check for duplicate codes
            existing = self.search([('code', '=', vals['code'])])
            if existing:
                raise ValidationError('Discount campaign code must be unique!')
        
        if 'start_date' in vals and 'end_date' in vals:
            if vals['start_date'] > vals['end_date']:
                raise ValidationError('Start date cannot be after end date!')
        
        return super(DiscountCampaign, self).create(vals)
    
    def write(self, vals):
        """Update discount campaign with validation"""
        if 'code' in vals:
            # Check for duplicate codes
            existing = self.search([('code', '=', vals['code']), ('id', '!=', self.id)])
            if existing:
                raise ValidationError('Discount campaign code must be unique!')
        
        if 'start_date' in vals and 'end_date' in vals:
            if vals['start_date'] > vals['end_date']:
                raise ValidationError('Start date cannot be after end date!')
        
        return super(DiscountCampaign, self).write(vals)
    
    def action_activate(self):
        """Activate discount campaign"""
        self.write({'is_active': True})
    
    def action_deactivate(self):
        """Deactivate discount campaign"""
        self.write({'is_active': False})
    
    def action_send_notification(self):
        """Send campaign notification to eligible customers"""
        # This would implement notification logic
        self.write({'is_notification_sent': True})
    
    def action_view_analytics(self):
        """View campaign analytics"""
        return {
            'type': 'ir.actions.act_window',
            'name': 'Campaign Analytics',
            'res_model': 'discount.analytics',
            'view_mode': 'tree,form',
            'domain': [('campaign_id', '=', self.id)],
        }


class DiscountCampaignProduct(BaseModel):
    """Discount Campaign Products"""
    
    _name = 'discount.campaign.product'
    _description = 'Discount Campaign Product'
    _order = 'sequence, product_id'
    
    campaign_id = Many2oneField('discount.campaign', string='Campaign', required=True)
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


class DiscountCampaignCategory(BaseModel):
    """Discount Campaign Categories"""
    
    _name = 'discount.campaign.category'
    _description = 'Discount Campaign Category'
    _order = 'sequence, category_id'
    
    campaign_id = Many2oneField('discount.campaign', string='Campaign', required=True)
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


class DiscountCampaignRule(BaseModel):
    """Discount Campaign Rules"""
    
    _name = 'discount.campaign.rule'
    _description = 'Discount Campaign Rule'
    _order = 'sequence, name'
    
    name = CharField(string='Rule Name', required=True, size=100)
    campaign_id = Many2oneField('discount.campaign', string='Campaign', required=True)
    sequence = IntegerField(string='Sequence', default=10)
    is_active = BooleanField(string='Active', default=True)
    
    # Rule Configuration
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
    condition_field = CharField(string='Condition Field', required=True, size=100)
    condition_operator = SelectionField([
        ('equals', 'Equals'),
        ('not_equals', 'Not Equals'),
        ('greater_than', 'Greater Than'),
        ('less_than', 'Less Than'),
        ('contains', 'Contains'),
        ('not_contains', 'Not Contains'),
    ], string='Condition Operator', required=True, default='equals')
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
    
    # Usage Limits
    usage_limit = IntegerField(string='Usage Limit', default=0)  # 0 = unlimited
    usage_limit_per_customer = IntegerField(string='Usage Limit per Customer', default=1)
    usage_limit_per_day = IntegerField(string='Usage Limit per Day', default=0)  # 0 = unlimited
    
    # System Fields
    create_date = DateTimeField(string='Created On', readonly=True)
    write_date = DateTimeField(string='Last Updated', readonly=True)
    create_uid = Many2oneField('res.users', string='Created By', readonly=True)
    write_uid = Many2oneField('res.users', string='Updated By', readonly=True)