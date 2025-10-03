# -*- coding: utf-8 -*-

from core_framework.orm import BaseModel, CharField, TextField, IntegerField, FloatField, BooleanField, DateField, DateTimeField, Many2oneField, One2manyField, SelectionField
from core_framework.exceptions import ValidationError


class LoyaltyOffer(BaseModel):
    """Loyalty Special Offers"""
    
    _name = 'loyalty.offer'
    _description = 'Loyalty Offer'
    _order = 'start_date desc, name'
    
    name = CharField(string='Offer Name', required=True, size=100)
    description = TextField(string='Description')
    
    # Offer Configuration
    is_active = BooleanField(string='Active', default=True)
    offer_type = SelectionField([
        ('birthday', 'Birthday Offer'),
        ('referral', 'Referral Offer'),
        ('seasonal', 'Seasonal Offer'),
        ('promotional', 'Promotional Offer'),
        ('tier_upgrade', 'Tier Upgrade Offer'),
        ('points_bonus', 'Points Bonus Offer'),
        ('first_purchase', 'First Purchase Offer'),
        ('loyalty_milestone', 'Loyalty Milestone Offer'),
    ], string='Offer Type', required=True, default='promotional')
    
    # Validity
    start_date = DateField(string='Start Date', required=True)
    end_date = DateField(string='End Date')
    is_permanent = BooleanField(string='Permanent Offer', default=False)
    
    # Offer Details
    offer_value = FloatField(string='Offer Value', digits=(16, 2))
    offer_currency_id = Many2oneField('res.currency', string='Offer Currency')
    min_purchase_amount = FloatField(string='Minimum Purchase Amount', digits=(16, 2))
    max_offer_amount = FloatField(string='Maximum Offer Amount', digits=(16, 2))
    
    # Points Configuration
    points_multiplier = FloatField(string='Points Multiplier', default=1.0, digits=(16, 2))
    bonus_points = IntegerField(string='Bonus Points', default=0)
    points_required = IntegerField(string='Points Required', default=0)
    
    # Product Configuration
    product_ids = One2manyField('loyalty.offer.product', 'offer_id', string='Products')
    category_ids = One2manyField('loyalty.offer.category', 'offer_id', string='Categories')
    
    # Customer Configuration
    customer_segment = SelectionField([
        ('all', 'All Customers'),
        ('new', 'New Customers'),
        ('existing', 'Existing Customers'),
        ('tier_based', 'Tier Based'),
        ('age_group', 'Age Group Based'),
        ('gender', 'Gender Based'),
        ('seasonal', 'Seasonal Based'),
    ], string='Customer Segment', default='all')
    
    tier_id = Many2oneField('loyalty.tier', string='Required Tier')
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
    
    # Usage Limits
    usage_limit = IntegerField(string='Usage Limit', default=0)  # 0 = unlimited
    usage_limit_per_customer = IntegerField(string='Usage Limit per Customer', default=1)
    
    # Kids Clothing Specific
    child_age_min = IntegerField(string='Minimum Child Age (months)', default=0)
    child_age_max = IntegerField(string='Maximum Child Age (months)', default=216)  # 18 years
    
    # Special Features
    is_automatic = BooleanField(string='Automatic Offer', default=False)
    is_notification_sent = BooleanField(string='Notification Sent', default=False)
    notification_template_id = Many2oneField('mail.template', string='Notification Template')
    
    # Analytics
    total_usage = IntegerField(string='Total Usage', default=0)
    total_customers = IntegerField(string='Total Customers', default=0)
    total_value = FloatField(string='Total Value', digits=(16, 2), default=0.0)
    
    # System Fields
    create_date = DateTimeField(string='Created On', readonly=True)
    write_date = DateTimeField(string='Last Updated', readonly=True)
    create_uid = Many2oneField('res.users', string='Created By', readonly=True)
    write_uid = Many2oneField('res.users', string='Updated By', readonly=True)
    
    def create(self, vals):
        """Create loyalty offer with validation"""
        if 'start_date' in vals and 'end_date' in vals:
            if vals['start_date'] > vals['end_date']:
                raise ValidationError('Start date cannot be after end date!')
        
        return super(LoyaltyOffer, self).create(vals)
    
    def write(self, vals):
        """Update loyalty offer with validation"""
        if 'start_date' in vals and 'end_date' in vals:
            if vals['start_date'] > vals['end_date']:
                raise ValidationError('Start date cannot be after end date!')
        
        return super(LoyaltyOffer, self).write(vals)
    
    def action_activate(self):
        """Activate offer"""
        self.write({'is_active': True})
    
    def action_deactivate(self):
        """Deactivate offer"""
        self.write({'is_active': False})
    
    def action_send_notification(self):
        """Send offer notification to eligible customers"""
        # This would implement notification logic
        self.write({'is_notification_sent': True})
    
    def action_view_usage(self):
        """View offer usage"""
        return {
            'type': 'ir.actions.act_window',
            'name': 'Offer Usage',
            'res_model': 'loyalty.offer.usage',
            'view_mode': 'tree,form',
            'domain': [('offer_id', '=', self.id)],
        }


class LoyaltyOfferProduct(BaseModel):
    """Loyalty Offer Products"""
    
    _name = 'loyalty.offer.product'
    _description = 'Loyalty Offer Product'
    _order = 'sequence, product_id'
    
    offer_id = Many2oneField('loyalty.offer', string='Offer', required=True)
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


class LoyaltyOfferCategory(BaseModel):
    """Loyalty Offer Categories"""
    
    _name = 'loyalty.offer.category'
    _description = 'Loyalty Offer Category'
    _order = 'sequence, category_id'
    
    offer_id = Many2oneField('loyalty.offer', string='Offer', required=True)
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


class LoyaltyOfferUsage(BaseModel):
    """Loyalty Offer Usage"""
    
    _name = 'loyalty.offer.usage'
    _description = 'Loyalty Offer Usage'
    _order = 'usage_date desc, id desc'
    
    name = CharField(string='Reference', required=True, size=64)
    offer_id = Many2oneField('loyalty.offer', string='Offer', required=True)
    partner_id = Many2oneField('res.partner', string='Customer', required=True)
    program_id = Many2oneField('loyalty.program', string='Loyalty Program', related='partner_id.loyalty_program_id', store=True)
    
    # Usage Details
    usage_date = DateTimeField(string='Usage Date', required=True, default=lambda self: self.env['datetime'].now())
    order_id = Many2oneField('sale.order', string='Sale Order')
    offer_value = FloatField(string='Offer Value', digits=(16, 2))
    points_earned = IntegerField(string='Points Earned', default=0)
    points_used = IntegerField(string='Points Used', default=0)
    
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