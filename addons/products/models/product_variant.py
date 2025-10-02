# -*- coding: utf-8 -*-

from core_framework.orm import BaseModel, CharField, TextField, FloatField, IntegerField, BooleanField, DateField, DateTimeField, Many2OneField, One2ManyField, Many2ManyField, SelectionField, ImageField, BinaryField
from core_framework.orm import KidsClothingMixin, PriceMixin


class ProductVariant(BaseModel, KidsClothingMixin, PriceMixin):
    """Product Variant - Specific product variations"""
    
    _name = 'product.variant'
    _description = 'Product Variant'
    _order = 'name'
    
    # Basic Information
    name = CharField(string='Variant Name', required=True, size=255)
    default_code = CharField(string='Internal Reference', size=64)
    barcode = CharField(string='Barcode', size=64)
    sku = CharField(string='SKU', size=64)
    
    # Product Template
    product_tmpl_id = Many2OneField('product.template', string='Product Template', required=True, ondelete='cascade')
    
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
    
    size = SelectionField(string='Size', selection=[
        ('XS', 'XS (Extra Small)'),
        ('S', 'S (Small)'),
        ('M', 'M (Medium)'),
        ('L', 'L (Large)'),
        ('XL', 'XL (Extra Large)'),
        ('XXL', 'XXL (Double Extra Large)'),
        ('XXXL', 'XXXL (Triple Extra Large)'),
    ], required=True)
    
    color = CharField(string='Color', size=64)
    fabric = CharField(string='Fabric', size=64)
    style = CharField(string='Style', size=64)
    
    # Pricing
    list_price = FloatField(string='Sales Price', digits=(16, 2))
    standard_price = FloatField(string='Cost Price', digits=(16, 2))
    margin = FloatField(string='Margin', digits=(16, 2), readonly=True)
    margin_percent = FloatField(string='Margin %', digits=(16, 2), readonly=True)
    
    # Inventory
    qty_available = FloatField(string='Quantity On Hand', digits=(16, 2), readonly=True)
    qty_reserved = FloatField(string='Quantity Reserved', digits=(16, 2), readonly=True)
    qty_free = FloatField(string='Free Quantity', digits=(16, 2), readonly=True)
    qty_incoming = FloatField(string='Incoming Quantity', digits=(16, 2), readonly=True)
    qty_outgoing = FloatField(string='Outgoing Quantity', digits=(16, 2), readonly=True)
    
    # Status
    active = BooleanField(string='Active', default=True)
    state = SelectionField(string='State', selection=[
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('discontinued', 'Discontinued'),
    ], default='draft')
    
    # Images
    image_1920 = ImageField(string='Image', max_width=1920, max_height=1920)
    image_1024 = ImageField(string='Image 1024', max_width=1024, max_height=1024)
    image_512 = ImageField(string='Image 512', max_width=512, max_height=512)
    image_256 = ImageField(string='Image 256', max_width=256, max_height=256)
    image_128 = ImageField(string='Image 128', max_width=128, max_height=128)
    
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
    
    def _compute_qty_free(self):
        """Compute free quantity (available - reserved)"""
        for record in self:
            record.qty_free = record.qty_available - record.qty_reserved
    
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
    
    def get_variant_summary(self):
        """Get variant summary information"""
        return {
            'name': self.name,
            'default_code': self.default_code,
            'barcode': self.barcode,
            'sku': self.sku,
            'age_group': self.age_group,
            'gender': self.gender,
            'size': self.size,
            'color': self.color,
            'fabric': self.fabric,
            'style': self.style,
            'list_price': self.list_price,
            'standard_price': self.standard_price,
            'margin': self.margin,
            'margin_percent': self.margin_percent,
            'qty_available': self.qty_available,
            'qty_reserved': self.qty_reserved,
            'qty_free': self.qty_free,
            'active': self.active,
            'state': self.state,
        }
    
    def get_variant_analytics(self):
        """Get variant analytics data"""
        return {
            'total_sales': self.total_sales,
            'total_quantity_sold': self.total_quantity_sold,
            'average_rating': self.average_rating,
            'review_count': self.review_count,
            'margin': self.margin,
            'margin_percent': self.margin_percent,
        }
    
    def get_inventory_summary(self):
        """Get inventory summary"""
        return {
            'qty_available': self.qty_available,
            'qty_reserved': self.qty_reserved,
            'qty_free': self.qty_free,
            'qty_incoming': self.qty_incoming,
            'qty_outgoing': self.qty_outgoing,
            'is_in_stock': self.qty_available > 0,
            'is_low_stock': self.qty_available < 10,  # Assuming 10 is low stock threshold
        }
    
    def activate_variant(self):
        """Activate the variant"""
        self.write({'state': 'active', 'active': True})
        return True
    
    def deactivate_variant(self):
        """Deactivate the variant"""
        self.write({'state': 'inactive', 'active': False})
        return True
    
    def discontinue_variant(self):
        """Discontinue the variant"""
        self.write({'state': 'discontinued', 'active': False})
        return True
    
    def get_variant_by_attributes(self, size=None, color=None, age_group=None):
        """Get variant by specific attributes"""
        domain = [('product_tmpl_id', '=', self.product_tmpl_id.id)]
        if size:
            domain.append(('size', '=', size))
        if color:
            domain.append(('color', '=', color))
        if age_group:
            domain.append(('age_group', '=', age_group))
        
        return self.env['product.variant'].search(domain)
    
    def get_variant_analytics_summary(self):
        """Get comprehensive variant analytics summary"""
        return {
            'variant_info': self.get_variant_summary(),
            'analytics': self.get_variant_analytics(),
            'inventory': self.get_inventory_summary(),
            'performance': {
                'total_sales': self.total_sales,
                'total_quantity_sold': self.total_quantity_sold,
                'average_rating': self.average_rating,
                'review_count': self.review_count,
            },
        }