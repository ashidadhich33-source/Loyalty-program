# -*- coding: utf-8 -*-

from core_framework.orm import BaseModel, CharField, TextField, FloatField, IntegerField, BooleanField, DateField, DateTimeField, Many2OneField, One2ManyField, Many2ManyField, SelectionField, ImageField, BinaryField


class ProductTag(BaseModel):
    """Product Tag - Flexible tagging system for products"""
    
    _name = 'product.tag'
    _description = 'Product Tag'
    _order = 'name'
    
    # Basic Information
    name = CharField(string='Tag Name', required=True, size=255)
    description = TextField(string='Description')
    code = CharField(string='Tag Code', size=64)
    color = CharField(string='Tag Color', size=7, default='#007bff')  # Hex color code
    
    # Tag Type
    tag_type = SelectionField(string='Tag Type', selection=[
        ('feature', 'Feature'),
        ('season', 'Season'),
        ('trend', 'Trend'),
        ('sale', 'Sale'),
        ('new', 'New'),
        ('popular', 'Popular'),
        ('recommended', 'Recommended'),
        ('other', 'Other'),
    ], default='other')
    
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
    
    # Products
    product_ids = Many2ManyField('product.template', string='Products')
    product_count = IntegerField(string='Product Count', readonly=True)
    
    # Status
    active = BooleanField(string='Active', default=True)
    state = SelectionField(string='State', selection=[
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ], default='draft')
    
    # Company
    company_id = Many2OneField('res.company', string='Company', required=True)
    
    # Timestamps
    create_date = DateTimeField(string='Created on', readonly=True)
    write_date = DateTimeField(string='Last Updated on', readonly=True)
    
    def _compute_product_count(self):
        """Compute total product count"""
        for record in self:
            record.product_count = len(record.product_ids)
    
    def get_tag_summary(self):
        """Get tag summary information"""
        return {
            'name': self.name,
            'description': self.description,
            'code': self.code,
            'color': self.color,
            'tag_type': self.tag_type,
            'age_group': self.age_group,
            'gender': self.gender,
            'product_count': self.product_count,
            'active': self.active,
            'state': self.state,
        }
    
    def get_tagged_products(self):
        """Get all products with this tag"""
        return self.product_ids
    
    def get_products_by_age_group(self, age_group):
        """Get tagged products filtered by age group"""
        return self.product_ids.filtered(lambda p: p.age_group == age_group)
    
    def get_products_by_gender(self, gender):
        """Get tagged products filtered by gender"""
        return self.product_ids.filtered(lambda p: p.gender == gender)
    
    def get_products_by_tag_type(self, tag_type):
        """Get products filtered by tag type"""
        if self.tag_type == tag_type:
            return self.product_ids
        return self.env['product.template']
    
    def activate_tag(self):
        """Activate the tag"""
        self.write({'state': 'active', 'active': True})
        return True
    
    def deactivate_tag(self):
        """Deactivate the tag"""
        self.write({'state': 'inactive', 'active': False})
        return True
    
    def get_tag_analytics_summary(self):
        """Get comprehensive tag analytics summary"""
        return {
            'tag_info': self.get_tag_summary(),
            'products': [p.get_product_summary() for p in self.product_ids],
            'performance': {
                'product_count': self.product_count,
                'active_products': len(self.product_ids.filtered(lambda p: p.active)),
            },
        }