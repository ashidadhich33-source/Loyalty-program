# -*- coding: utf-8 -*-

from core_framework.orm import BaseModel, CharField, TextField, FloatField, IntegerField, BooleanField, DateField, DateTimeField, Many2OneField, One2ManyField, Many2ManyField, SelectionField, ImageField, BinaryField
from core_framework.orm import KidsClothingMixin, PriceMixin


class ProductTemplate(BaseModel, KidsClothingMixin, PriceMixin):
    """Product Template - Main product definition"""
    
    _name = 'product.template'
    _description = 'Product Template'
    _order = 'name'
    
    # Basic Information
    name = CharField(string='Product Name', required=True, size=255)
    description = TextField(string='Description')
    short_description = CharField(string='Short Description', size=500)
    internal_reference = CharField(string='Internal Reference', size=64)
    barcode = CharField(string='Barcode', size=64)
    sku = CharField(string='SKU', size=64)
    
    # Product Type
    type = SelectionField(string='Product Type', selection=[
        ('consu', 'Consumable'),
        ('service', 'Service'),
        ('product', 'Stockable Product'),
    ], default='product', required=True)
    
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
    ], required=True)
    
    gender = SelectionField(string='Gender', selection=[
        ('unisex', 'Unisex'),
        ('boys', 'Boys'),
        ('girls', 'Girls'),
    ], default='unisex')
    
    season = SelectionField(string='Season', selection=[
        ('summer', 'Summer'),
        ('winter', 'Winter'),
        ('monsoon', 'Monsoon'),
        ('all_season', 'All Season'),
    ], default='all_season')
    
    # Product Details
    brand_id = Many2OneField('product.brand', string='Brand')
    category_id = Many2OneField('product.category', string='Category', required=True)
    sub_category_id = Many2OneField('product.category', string='Sub Category')
    tag_ids = Many2ManyField('product.tag', string='Tags')
    
    # GST Fields
    hsn_code = CharField(string='HSN Code', size=8)
    gst_tax_group_id = Many2OneField('account.tax.group', string='GST Tax Group')
    
    # Variants
    variant_ids = One2ManyField('product.variant', 'product_tmpl_id', string='Variants')
    has_variants = BooleanField(string='Has Variants', default=False)
    
    # Pricing
    list_price = FloatField(string='Sales Price', digits=(16, 2))
    standard_price = FloatField(string='Cost Price', digits=(16, 2))
    margin = FloatField(string='Margin', digits=(16, 2), readonly=True)
    margin_percent = FloatField(string='Margin %', digits=(16, 2), readonly=True)
    
    # Inventory
    sale_ok = BooleanField(string='Can be Sold', default=True)
    purchase_ok = BooleanField(string='Can be Purchased', default=True)
    track_service = BooleanField(string='Track Service', default=False)
    
    # Images
    image_1920 = ImageField(string='Image', max_width=1920, max_height=1920)
    image_1024 = ImageField(string='Image 1024', max_width=1024, max_height=1024)
    image_512 = ImageField(string='Image 512', max_width=512, max_height=512)
    image_256 = ImageField(string='Image 256', max_width=256, max_height=256)
    image_128 = ImageField(string='Image 128', max_width=128, max_height=128)
    
    # Status
    active = BooleanField(string='Active', default=True)
    state = SelectionField(string='State', selection=[
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('discontinued', 'Discontinued'),
    ], default='draft')
    
    # Analytics
    total_sales = FloatField(string='Total Sales', digits=(16, 2), readonly=True)
    total_quantity_sold = FloatField(string='Total Quantity Sold', digits=(16, 2), readonly=True)
    average_rating = FloatField(string='Average Rating', digits=(3, 2), readonly=True)
    review_count = IntegerField(string='Review Count', readonly=True)
    
    # Company
    company_id = Many2OneField('res.company', string='Company', required=True)
    
    # Timestamps
    create_date = DateTimeField(string='Created on', readonly=True)
    write_date = DateTimeField(string='Last Updated on', readonly=True)
    
    def _compute_margin(self):
        """Compute margin and margin percentage"""
        for record in self:
            if record.list_price and record.standard_price:
                record.margin = record.list_price - record.standard_price
                record.margin_percent = (record.margin / record.list_price) * 100
            else:
                record.margin = 0.0
                record.margin_percent = 0.0
    
    def _compute_total_sales(self):
        """Compute total sales amount"""
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
            record.review_count = 0
    
    def create_variant(self, variant_values):
        """Create a new product variant"""
        variant_data = {
            'product_tmpl_id': self.id,
            'name': variant_values.get('name', self.name),
            'default_code': variant_values.get('default_code', ''),
            'list_price': variant_values.get('list_price', self.list_price),
            'standard_price': variant_values.get('standard_price', self.standard_price),
        }
        return self.env['product.variant'].create(variant_data)
    
    def get_variants(self):
        """Get all variants for this product template"""
        return self.variant_ids
    
    def get_available_variants(self):
        """Get available variants (in stock)"""
        return self.variant_ids.filtered(lambda v: v.qty_available > 0)
    
    def get_product_analytics(self):
        """Get product analytics data"""
        return {
            'total_sales': self.total_sales,
            'total_quantity_sold': self.total_quantity_sold,
            'average_rating': self.average_rating,
            'review_count': self.review_count,
            'margin': self.margin,
            'margin_percent': self.margin_percent,
        }
    
    def get_product_summary(self):
        """Get product summary information"""
        return {
            'name': self.name,
            'age_group': self.age_group,
            'gender': self.gender,
            'season': self.season,
            'brand': self.brand_id.name if self.brand_id else '',
            'category': self.category_id.name if self.category_id else '',
            'list_price': self.list_price,
            'standard_price': self.standard_price,
            'has_variants': self.has_variants,
            'variant_count': len(self.variant_ids),
            'active': self.active,
            'state': self.state,
        }
    
    def activate_product(self):
        """Activate the product"""
        self.write({'state': 'active', 'active': True})
        return True
    
    def deactivate_product(self):
        """Deactivate the product"""
        self.write({'state': 'inactive', 'active': False})
        return True
    
    def discontinue_product(self):
        """Discontinue the product"""
        self.write({'state': 'discontinued', 'active': False})
        return True
    
    def get_product_variants_by_size(self, size):
        """Get variants filtered by size"""
        return self.variant_ids.filtered(lambda v: v.size == size)
    
    def get_product_variants_by_color(self, color):
        """Get variants filtered by color"""
        return self.variant_ids.filtered(lambda v: v.color == color)
    
    def get_product_variants_by_age_group(self, age_group):
        """Get variants filtered by age group"""
        return self.variant_ids.filtered(lambda v: v.age_group == age_group)
    
    def get_product_analytics_summary(self):
        """Get comprehensive product analytics summary"""
        return {
            'product_info': self.get_product_summary(),
            'analytics': self.get_product_analytics(),
            'variants': {
                'total_variants': len(self.variant_ids),
                'available_variants': len(self.get_available_variants()),
                'variant_details': [v.get_variant_summary() for v in self.variant_ids],
            },
            'performance': {
                'total_sales': self.total_sales,
                'total_quantity_sold': self.total_quantity_sold,
                'average_rating': self.average_rating,
                'review_count': self.review_count,
            },
        }