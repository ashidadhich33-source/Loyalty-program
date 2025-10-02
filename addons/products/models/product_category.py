# -*- coding: utf-8 -*-

from core_framework.orm import BaseModel, CharField, TextField, FloatField, IntegerField, BooleanField, DateField, DateTimeField, Many2OneField, One2ManyField, Many2ManyField, SelectionField, ImageField, BinaryField


class ProductCategory(BaseModel):
    """Product Category - Hierarchical product categorization"""
    
    _name = 'product.category'
    _description = 'Product Category'
    _order = 'name'
    
    # Basic Information
    name = CharField(string='Category Name', required=True, size=255)
    description = TextField(string='Description')
    code = CharField(string='Category Code', size=64)
    
    # Hierarchy
    parent_id = Many2OneField('product.category', string='Parent Category')
    child_ids = One2ManyField('product.category', 'parent_id', string='Child Categories')
    level = IntegerField(string='Level', readonly=True)
    
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
    
    season = SelectionField(string='Season', selection=[
        ('summer', 'Summer'),
        ('winter', 'Winter'),
        ('monsoon', 'Monsoon'),
        ('all_season', 'All Season'),
    ], default='all_season')
    
    # Category Type
    category_type = SelectionField(string='Category Type', selection=[
        ('clothing', 'Clothing'),
        ('accessories', 'Accessories'),
        ('shoes', 'Shoes'),
        ('toys', 'Toys'),
        ('books', 'Books'),
        ('other', 'Other'),
    ], default='clothing')
    
    # Products
    product_ids = One2ManyField('product.template', 'category_id', string='Products')
    product_count = IntegerField(string='Product Count', readonly=True)
    
    # Status
    active = BooleanField(string='Active', default=True)
    state = SelectionField(string='State', selection=[
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ], default='draft')
    
    # Images
    image_1920 = ImageField(string='Category Image', max_width=1920, max_height=1920)
    image_1024 = ImageField(string='Image 1024', max_width=1024, max_height=1024)
    image_512 = ImageField(string='Image 512', max_width=512, max_height=512)
    image_256 = ImageField(string='Image 256', max_width=256, max_height=256)
    image_128 = ImageField(string='Image 128', max_width=128, max_height=128)
    
    # Analytics
    total_sales = FloatField(string='Total Sales', digits=(16, 2), readonly=True)
    total_products = IntegerField(string='Total Products', readonly=True)
    average_rating = FloatField(string='Average Rating', digits=(3, 2), readonly=True)
    
    # Company
    company_id = Many2OneField('res.company', string='Company', required=True)
    
    # Timestamps
    create_date = DateTimeField(string='Created on', readonly=True)
    write_date = DateTimeField(string='Last Updated on', readonly=True)
    
    def _compute_level(self):
        """Compute category level in hierarchy"""
        for record in self:
            level = 0
            parent = record.parent_id
            while parent:
                level += 1
                parent = parent.parent_id
            record.level = level
    
    def _compute_product_count(self):
        """Compute total product count including child categories"""
        for record in self:
            count = len(record.product_ids)
            # Add products from child categories
            for child in record.child_ids:
                count += len(child.product_ids)
            record.product_count = count
    
    def _compute_total_sales(self):
        """Compute total sales for this category"""
        for record in self:
            # This would be computed from actual sales data
            record.total_sales = 0.0
    
    def _compute_total_products(self):
        """Compute total products in this category"""
        for record in self:
            record.total_products = len(record.product_ids)
    
    def _compute_average_rating(self):
        """Compute average rating for products in this category"""
        for record in self:
            # This would be computed from actual product ratings
            record.average_rating = 0.0
    
    def get_category_summary(self):
        """Get category summary information"""
        return {
            'name': self.name,
            'description': self.description,
            'code': self.code,
            'parent': self.parent_id.name if self.parent_id else '',
            'level': self.level,
            'age_group': self.age_group,
            'gender': self.gender,
            'season': self.season,
            'category_type': self.category_type,
            'product_count': self.product_count,
            'active': self.active,
            'state': self.state,
        }
    
    def get_category_analytics(self):
        """Get category analytics data"""
        return {
            'total_sales': self.total_sales,
            'total_products': self.total_products,
            'average_rating': self.average_rating,
            'product_count': self.product_count,
        }
    
    def get_child_categories(self):
        """Get all child categories"""
        return self.child_ids
    
    def get_all_products(self):
        """Get all products in this category and child categories"""
        products = self.product_ids
        for child in self.child_ids:
            products += child.get_all_products()
        return products
    
    def get_category_hierarchy(self):
        """Get full category hierarchy"""
        hierarchy = {
            'category': self.get_category_summary(),
            'children': [child.get_category_hierarchy() for child in self.child_ids],
        }
        return hierarchy
    
    def get_products_by_age_group(self, age_group):
        """Get products filtered by age group"""
        return self.product_ids.filtered(lambda p: p.age_group == age_group)
    
    def get_products_by_gender(self, gender):
        """Get products filtered by gender"""
        return self.product_ids.filtered(lambda p: p.gender == gender)
    
    def get_products_by_season(self, season):
        """Get products filtered by season"""
        return self.product_ids.filtered(lambda p: p.season == season)
    
    def activate_category(self):
        """Activate the category"""
        self.write({'state': 'active', 'active': True})
        return True
    
    def deactivate_category(self):
        """Deactivate the category"""
        self.write({'state': 'inactive', 'active': False})
        return True
    
    def get_category_analytics_summary(self):
        """Get comprehensive category analytics summary"""
        return {
            'category_info': self.get_category_summary(),
            'analytics': self.get_category_analytics(),
            'hierarchy': self.get_category_hierarchy(),
            'performance': {
                'total_sales': self.total_sales,
                'total_products': self.total_products,
                'average_rating': self.average_rating,
            },
        }