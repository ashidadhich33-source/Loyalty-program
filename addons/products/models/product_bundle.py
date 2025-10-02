# -*- coding: utf-8 -*-

from core_framework.orm import BaseModel, CharField, TextField, FloatField, IntegerField, BooleanField, DateField, DateTimeField, Many2OneField, One2ManyField, Many2ManyField, SelectionField, ImageField, BinaryField


class ProductBundle(BaseModel):
    """Product Bundle - Product bundles and sets"""
    
    _name = 'product.bundle'
    _description = 'Product Bundle'
    _order = 'name'
    
    # Basic Information
    name = CharField(string='Bundle Name', required=True, size=255)
    description = TextField(string='Description')
    code = CharField(string='Bundle Code', size=64)
    
    # Bundle Type
    bundle_type = SelectionField(string='Bundle Type', selection=[
        ('set', 'Product Set'),
        ('combo', 'Combo Offer'),
        ('gift', 'Gift Set'),
        ('seasonal', 'Seasonal Bundle'),
        ('age_group', 'Age Group Bundle'),
        ('other', 'Other'),
    ], default='set')
    
    # Kids Clothing Specific
    age_group = SelectionField(string='Age Group', selection=[
        ('0-2', '0-2 Years (Baby)'),
        ('2-4', '2-4 Years (Toddler)'),
        ('4-6', '4-6 Years (Pre-school)'),
        ('6-8', '6-8 Years (Early School)'),
        ('8-10', '8-10 Years (School)'),
        ('10-12', '10-12 Years (Pre-teen)'),
        ('12-14', '12-14 Years (Teen)'),
        ('14-16', '14-16 Years (Young Adult)'),
        ('all', 'All Ages'),
    ], default='all')
    
    gender = SelectionField(string='Gender', selection=[
        ('unisex', 'Unisex'),
        ('boys', 'Boys'),
        ('girls', 'Girls'),
        ('all', 'All Genders'),
    ], default='all')
    
    # Bundle Items
    bundle_item_ids = One2ManyField('product.bundle.item', 'bundle_id', string='Bundle Items')
    item_count = IntegerField(string='Item Count', readonly=True)
    
    # Pricing
    bundle_price = FloatField(string='Bundle Price', digits=(16, 2))
    individual_price = FloatField(string='Individual Price', digits=(16, 2), readonly=True)
    discount_amount = FloatField(string='Discount Amount', digits=(16, 2), readonly=True)
    discount_percent = FloatField(string='Discount %', digits=(16, 2), readonly=True)
    
    # Status
    active = BooleanField(string='Active', default=True)
    state = SelectionField(string='State', selection=[
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('discontinued', 'Discontinued'),
    ], default='draft')
    
    # Images
    image_1920 = ImageField(string='Bundle Image', max_width=1920, max_height=1920)
    image_1024 = ImageField(string='Image 1024', max_width=1024, max_height=1024)
    image_512 = ImageField(string='Image 512', max_width=512, max_height=512)
    image_256 = ImageField(string='Image 256', max_width=256, max_height=256)
    image_128 = ImageField(string='Image 128', max_width=128, max_height=128)
    
    # Analytics
    total_sales = FloatField(string='Total Sales', digits=(16, 2), readonly=True)
    total_quantity_sold = FloatField(string='Total Quantity Sold', digits=(16, 2), readonly=True)
    average_rating = FloatField(string='Average Rating', digits=(3, 2), readonly=True)
    
    # Company
    company_id = Many2OneField('res.company', string='Company', required=True)
    
    # Timestamps
    create_date = DateTimeField(string='Created on', readonly=True)
    write_date = DateTimeField(string='Last Updated on', readonly=True)
    
    def _compute_item_count(self):
        """Compute total item count"""
        for record in self:
            record.item_count = len(record.bundle_item_ids)
    
    def _compute_individual_price(self):
        """Compute individual price (sum of all item prices)"""
        for record in self:
            total_price = 0.0
            for item in record.bundle_item_ids:
                total_price += item.product_id.list_price * item.quantity
            record.individual_price = total_price
    
    def _compute_discount_amount(self):
        """Compute discount amount"""
        for record in self:
            if record.individual_price and record.bundle_price:
                record.discount_amount = record.individual_price - record.bundle_price
            else:
                record.discount_amount = 0.0
    
    def _compute_discount_percent(self):
        """Compute discount percentage"""
        for record in self:
            if record.individual_price and record.discount_amount:
                record.discount_percent = (record.discount_amount / record.individual_price) * 100
            else:
                record.discount_percent = 0.0
    
    def _compute_total_sales(self):
        """Compute total sales for this bundle"""
        for record in self:
            # This would be computed from actual sales data
            record.total_sales = 0.0
    
    def _compute_total_quantity_sold(self):
        """Compute total quantity sold"""
        for record in self:
            # This would be computed from actual sales data
            record.total_quantity_sold = 0.0
    
    def _compute_average_rating(self):
        """Compute average rating"""
        for record in self:
            # This would be computed from actual review data
            record.average_rating = 0.0
    
    def get_bundle_summary(self):
        """Get bundle summary information"""
        return {
            'name': self.name,
            'description': self.description,
            'code': self.code,
            'bundle_type': self.bundle_type,
            'age_group': self.age_group,
            'gender': self.gender,
            'item_count': self.item_count,
            'bundle_price': self.bundle_price,
            'individual_price': self.individual_price,
            'discount_amount': self.discount_amount,
            'discount_percent': self.discount_percent,
            'active': self.active,
            'state': self.state,
        }
    
    def get_bundle_items(self):
        """Get all bundle items"""
        return self.bundle_item_ids
    
    def get_bundle_analytics(self):
        """Get bundle analytics data"""
        return {
            'total_sales': self.total_sales,
            'total_quantity_sold': self.total_quantity_sold,
            'average_rating': self.average_rating,
            'item_count': self.item_count,
        }
    
    def activate_bundle(self):
        """Activate the bundle"""
        self.write({'state': 'active', 'active': True})
        return True
    
    def deactivate_bundle(self):
        """Deactivate the bundle"""
        self.write({'state': 'inactive', 'active': False})
        return True
    
    def discontinue_bundle(self):
        """Discontinue the bundle"""
        self.write({'state': 'discontinued', 'active': False})
        return True
    
    def get_bundle_analytics_summary(self):
        """Get comprehensive bundle analytics summary"""
        return {
            'bundle_info': self.get_bundle_summary(),
            'analytics': self.get_bundle_analytics(),
            'items': [item.get_item_summary() for item in self.bundle_item_ids],
            'performance': {
                'total_sales': self.total_sales,
                'total_quantity_sold': self.total_quantity_sold,
                'average_rating': self.average_rating,
            },
        }


class ProductBundleItem(BaseModel):
    """Product Bundle Item - Individual items in a bundle"""
    
    _name = 'product.bundle.item'
    _description = 'Product Bundle Item'
    _order = 'sequence'
    
    # Basic Information
    name = CharField(string='Item Name', size=255)
    sequence = IntegerField(string='Sequence', default=10)
    
    # Bundle
    bundle_id = Many2OneField('product.bundle', string='Bundle', required=True, ondelete='cascade')
    
    # Product
    product_id = Many2OneField('product.template', string='Product', required=True)
    product_variant_id = Many2OneField('product.variant', string='Product Variant')
    
    # Quantity
    quantity = FloatField(string='Quantity', digits=(16, 2), default=1.0)
    
    # Pricing
    unit_price = FloatField(string='Unit Price', digits=(16, 2), readonly=True)
    total_price = FloatField(string='Total Price', digits=(16, 2), readonly=True)
    
    # Status
    active = BooleanField(string='Active', default=True)
    
    # Company
    company_id = Many2OneField('res.company', string='Company', required=True)
    
    # Timestamps
    create_date = DateTimeField(string='Created on', readonly=True)
    write_date = DateTimeField(string='Last Updated on', readonly=True)
    
    def _compute_unit_price(self):
        """Compute unit price from product"""
        for record in self:
            if record.product_id:
                record.unit_price = record.product_id.list_price
            else:
                record.unit_price = 0.0
    
    def _compute_total_price(self):
        """Compute total price (unit price * quantity)"""
        for record in self:
            record.total_price = record.unit_price * record.quantity
    
    def get_item_summary(self):
        """Get item summary information"""
        return {
            'name': self.name,
            'sequence': self.sequence,
            'product': self.product_id.name if self.product_id else '',
            'product_variant': self.product_variant_id.name if self.product_variant_id else '',
            'quantity': self.quantity,
            'unit_price': self.unit_price,
            'total_price': self.total_price,
            'active': self.active,
        }
    
    def get_item_analytics_summary(self):
        """Get comprehensive item analytics summary"""
        return {
            'item_info': self.get_item_summary(),
            'performance': {
                'unit_price': self.unit_price,
                'total_price': self.total_price,
                'quantity': self.quantity,
            },
        }