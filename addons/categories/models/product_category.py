# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Categories - Product Category Management
==========================================================

Standalone version of the product category management model.
"""

from core_framework.orm import BaseModel, CharField, TextField, FloatField, IntegerField, BooleanField, DateField, DateTimeField, Many2OneField, One2ManyField, Many2ManyField, SelectionField, ImageField, BinaryField
from core_framework.orm import KidsClothingMixin, PriceMixin
from typing import Dict, Any, Optional, List
import logging
from datetime import datetime, date

logger = logging.getLogger(__name__)


class ProductCategory(BaseModel, KidsClothingMixin, PriceMixin):
    """Product Category - Hierarchical category management for kids clothing"""
    
    _name = 'product.category'
    _description = 'Product Category'
    _table = 'product_category'
    _order = 'sequence, name'
    _parent_name = 'parent_id'
    _parent_store = True
    _parent_order = 'name'
    _rec_name = 'complete_name'

    # Basic Information
    name = CharField(
        string='Category Name',
        size=255,
        required=True,
        help='Category name for kids clothing products'
    )
    complete_name = CharField(
        string='Complete Name',
        size=500,
        readonly=True,
        help='Full category path'
    )
    parent_id = Many2OneField(
        'product.category',
        string='Parent Category',
        help='Parent category in the hierarchy'
    )
    child_id = One2ManyField(
        'product.category',
        string='Child Categories',
        help='Child categories'
    )
    parent_path = CharField(
        string='Parent Path',
        size=500,
        help='Parent path for hierarchical queries'
    )
    sequence = IntegerField(
        string='Sequence',
        default=10,
        help='Order of categories in the list'
    )
    active = BooleanField(
        string='Active',
        default=True,
        help='Whether this category is active'
    )
    
    # Kids Clothing Specific Fields
    age_group = SelectionField(
        string='Age Group',
        selection=[
            ('0-2', '0-2 Years (Baby)'),
            ('2-4', '2-4 Years (Toddler)'),
            ('4-6', '4-6 Years (Pre-school)'),
            ('6-8', '6-8 Years (Early School)'),
            ('8-10', '8-10 Years (School)'),
            ('10-12', '10-12 Years (Pre-teen)'),
            ('12-14', '12-14 Years (Teen)'),
            ('14-16', '14-16 Years (Young Adult)'),
            ('all', 'All Ages'),
        ],
        default='all',
        help='Target age group for this category'
    )
    
    gender = SelectionField(
        string='Gender',
        selection=[
            ('boys', 'Boys'),
            ('girls', 'Girls'),
            ('unisex', 'Unisex'),
        ],
        default='unisex',
        help='Target gender for this category'
    )
    
    season = SelectionField(
        string='Season',
        selection=[
            ('summer', 'Summer'),
            ('winter', 'Winter'),
            ('monsoon', 'Monsoon'),
            ('all_season', 'All Season'),
        ],
        default='all_season',
        help='Season for this category'
    )
    
    brand_type = SelectionField(
        string='Brand Type',
        selection=[
            ('premium', 'Premium'),
            ('mid_range', 'Mid Range'),
            ('budget', 'Budget'),
            ('all', 'All Brands'),
        ],
        default='all',
        help='Brand type for this category'
    )
    
    style_type = SelectionField(
        string='Style Type',
        selection=[
            ('casual', 'Casual'),
            ('formal', 'Formal'),
            ('party', 'Party'),
            ('sports', 'Sports'),
            ('ethnic', 'Ethnic'),
            ('all', 'All Styles'),
        ],
        default='all',
        help='Style type for this category'
    )
    
    color_family = SelectionField(
        string='Color Family',
        selection=[
            ('primary', 'Primary Colors'),
            ('pastel', 'Pastel Colors'),
            ('neutral', 'Neutral Colors'),
            ('bright', 'Bright Colors'),
            ('all', 'All Colors'),
        ],
        default='all',
        help='Color family for this category'
    )
    
    size_range = SelectionField(
        string='Size Range',
        selection=[
            ('xs_s', 'XS-S'),
            ('m_l', 'M-L'),
            ('xl_xxl', 'XL-XXL'),
            ('xxxl_plus', 'XXXL+'),
            ('all', 'All Sizes'),
        ],
        default='all',
        help='Size range for this category'
    )
    
    # Category Properties
    is_main_category = BooleanField(
        string='Main Category',
        default=False,
        help='Whether this is a main category'
    )
    is_leaf_category = BooleanField(
        string='Leaf Category',
        readonly=True,
        help='Whether this category has no children'
    )
    category_code = CharField(
        string='Category Code',
        size=10,
        help='Short code for this category'
    )
    description = TextField(
        string='Description',
        help='Detailed description of this category'
    )
    image = ImageField(
        string='Category Image',
        help='Image representing this category'
    )
    image_medium = ImageField(
        string='Medium Image',
        readonly=True,
        help='Medium sized image'
    )
    image_small = ImageField(
        string='Small Image',
        readonly=True,
        help='Small sized image'
    )
    
    # Business Rules
    min_age_months = IntegerField(
        string='Minimum Age (Months)',
        help='Minimum age in months for this category'
    )
    max_age_months = IntegerField(
        string='Maximum Age (Months)',
        help='Maximum age in months for this category'
    )
    min_height_cm = FloatField(
        string='Minimum Height (cm)',
        digits=(8, 2),
        help='Minimum height in cm for this category'
    )
    max_height_cm = FloatField(
        string='Maximum Height (cm)',
        digits=(8, 2),
        help='Maximum height in cm for this category'
    )
    min_weight_kg = FloatField(
        string='Minimum Weight (kg)',
        digits=(8, 2),
        help='Minimum weight in kg for this category'
    )
    max_weight_kg = FloatField(
        string='Maximum Weight (kg)',
        digits=(8, 2),
        help='Maximum weight in kg for this category'
    )
    
    # Pricing Rules
    default_margin = FloatField(
        string='Default Margin (%)',
        digits=(5, 2),
        help='Default margin percentage for products in this category'
    )
    min_margin = FloatField(
        string='Minimum Margin (%)',
        digits=(5, 2),
        help='Minimum margin percentage allowed'
    )
    max_margin = FloatField(
        string='Maximum Margin (%)',
        digits=(5, 2),
        help='Maximum margin percentage allowed'
    )
    
    # Analytics Fields
    product_count = IntegerField(
        string='Product Count',
        readonly=True,
        help='Number of products in this category'
    )
    total_sales = FloatField(
        string='Total Sales',
        digits=(12, 2),
        readonly=True,
        help='Total sales amount for this category'
    )
    avg_rating = FloatField(
        string='Average Rating',
        digits=(3, 2),
        readonly=True,
        help='Average rating of products in this category'
    )
    
    # Company and Multi-company
    company_id = Many2OneField(
        'res.company',
        string='Company',
        default=lambda self: self.env.company,
        help='Company this category belongs to'
    )
    
    # Tags and Classification
    tag_ids = Many2ManyField(
        'product.category.tag',
        string='Tags',
        help='Tags for this category'
    )
    
    # SEO Fields
    meta_title = CharField(
        string='Meta Title',
        size=255,
        help='SEO meta title'
    )
    meta_description = TextField(
        string='Meta Description',
        help='SEO meta description'
    )
    meta_keywords = CharField(
        string='Meta Keywords',
        size=500,
        help='SEO meta keywords'
    )
    
    # Display Properties
    display_type = SelectionField(
        string='Display Type',
        selection=[
            ('normal', 'Normal'),
            ('page', 'Page'),
            ('group', 'Group'),
        ],
        default='normal',
        help='Display type for this category'
    )
    
    def _compute_complete_name(self):
        """Compute complete name with parent path"""
        for record in self:
            if record.parent_id:
                record.complete_name = f"{record.parent_id.complete_name} / {record.name}"
            else:
                record.complete_name = record.name
    
    def _compute_is_leaf(self):
        """Compute if category is leaf (no children)"""
        for record in self:
            record.is_leaf_category = not bool(record.child_id)
    
    def _compute_image_medium(self):
        """Compute medium image from main image"""
        for record in self:
            if record.image:
                # In a real implementation, you would resize the image here
                record.image_medium = record.image
            else:
                record.image_medium = False
    
    def _compute_image_small(self):
        """Compute small image from main image"""
        for record in self:
            if record.image:
                # In a real implementation, you would resize the image here
                record.image_small = record.image
            else:
                record.image_small = False
    
    def _compute_product_count(self):
        """Compute product count for this category and its children"""
        for record in self:
            # Count products in this category and all its children
            all_categories = self._get_all_children(record)
            all_categories.append(record.id)
            
            products = self.env['product.template'].search([
                ('categ_id', 'in', all_categories)
            ])
            record.product_count = len(products)
    
    def _compute_total_sales(self):
        """Compute total sales for this category"""
        for record in self:
            # This would be computed from actual sales data
            record.total_sales = 0.0
    
    def _compute_avg_rating(self):
        """Compute average rating for this category"""
        for record in self:
            # This would be computed from product ratings
            record.avg_rating = 0.0
    
    def _get_all_children(self, category):
        """Get all child category IDs recursively"""
        children = []
        for child in category.child_id:
            children.append(child.id)
            children.extend(self._get_all_children(child))
        return children
    
    def _check_parent_recursion(self):
        """Check for parent recursion"""
        if not self._check_recursion():
            raise ValueError('You cannot create recursive categories.')
    
    def _check_age_range(self):
        """Check age range validation"""
        for record in self:
            if record.min_age_months and record.max_age_months:
                if record.min_age_months >= record.max_age_months:
                    raise ValueError('Minimum age must be less than maximum age.')
    
    def _check_height_range(self):
        """Check height range validation"""
        for record in self:
            if record.min_height_cm and record.max_height_cm:
                if record.min_height_cm >= record.max_height_cm:
                    raise ValueError('Minimum height must be less than maximum height.')
    
    def _check_weight_range(self):
        """Check weight range validation"""
        for record in self:
            if record.min_weight_kg and record.max_weight_kg:
                if record.min_weight_kg >= record.max_weight_kg:
                    raise ValueError('Minimum weight must be less than maximum weight.')
    
    def _check_margin_range(self):
        """Check margin range validation"""
        for record in self:
            if record.min_margin and record.max_margin:
                if record.min_margin >= record.max_margin:
                    raise ValueError('Minimum margin must be less than maximum margin.')
    
    def name_get(self):
        """Return the display name for the category"""
        result = []
        for category in self:
            name = category.complete_name
            result.append((category.id, name))
        return result
    
    def name_search(self, name, args=None, operator='ilike', limit=100):
        """Search categories by name"""
        args = args or []
        if name:
            categories = self.search([('name', operator, name)] + args, limit=limit)
        else:
            categories = self.search(args, limit=limit)
        return categories.name_get()
    
    def get_products(self):
        """Get all products in this category and its children"""
        all_categories = self._get_all_children(self)
        all_categories.append(self.id)
        
        return self.env['product.template'].search([
            ('categ_id', 'in', all_categories)
        ])
    
    def get_category_path(self):
        """Get the full path of this category"""
        path = []
        current = self
        while current:
            path.insert(0, current.name)
            current = current.parent_id
        return ' / '.join(path)
    
    def get_children_recursive(self):
        """Get all children recursively"""
        children = []
        for child in self.child_id:
            children.append(child)
            children.extend(child.get_children_recursive())
        return children
    
    def get_parents(self):
        """Get all parent categories"""
        parents = []
        current = self.parent_id
        while current:
            parents.append(current)
            current = current.parent_id
        return parents
    
    def is_child_of(self, parent_category):
        """Check if this category is a child of the given parent"""
        return parent_category in self.get_parents()
    
    def get_siblings(self):
        """Get all sibling categories"""
        if not self.parent_id:
            return self.env['product.category']
        return self.parent_id.child_id - self
    
    def move_to_parent(self, new_parent):
        """Move this category to a new parent"""
        if new_parent and new_parent.is_child_of(self):
            raise ValueError('Cannot move category to its own child.')
        self.parent_id = new_parent
    
    def archive(self):
        """Archive this category and all its children"""
        for child in self.child_id:
            child.archive()
        self.active = False
    
    def unarchive(self):
        """Unarchive this category"""
        self.active = True
    
    def duplicate(self):
        """Duplicate this category"""
        copy_vals = {
            'name': f"{self.name} (Copy)",
            'parent_id': self.parent_id.id if self.parent_id else False,
            'age_group': self.age_group,
            'gender': self.gender,
            'season': self.season,
            'brand_type': self.brand_type,
            'style_type': self.style_type,
            'color_family': self.color_family,
            'size_range': self.size_range,
            'description': self.description,
            'default_margin': self.default_margin,
            'min_margin': self.min_margin,
            'max_margin': self.max_margin,
        }
        return self.create(copy_vals)


class ProductCategoryTag(BaseModel):
    """Product Category Tag - Flexible tagging system for categories"""
    
    _name = 'product.category.tag'
    _description = 'Product Category Tag'
    _table = 'product_category_tag'
    _order = 'name'

    # Basic Information
    name = CharField(
        string='Tag Name',
        size=255,
        required=True,
        help='Name of the tag'
    )
    color = IntegerField(
        string='Color',
        help='Color for the tag'
    )
    active = BooleanField(
        string='Active',
        default=True,
        help='Whether this tag is active'
    )
    
    # Usage
    category_count = IntegerField(
        string='Category Count',
        readonly=True,
        help='Number of categories using this tag'
    )
    
    # Company
    company_id = Many2OneField(
        'res.company',
        string='Company',
        default=lambda self: self.env.company,
        help='Company this tag belongs to'
    )
    
    def _compute_category_count(self):
        """Compute category count for this tag"""
        for tag in self:
            categories = self.env['product.category'].search([
                ('tag_ids', 'in', tag.id)
            ])
            tag.category_count = len(categories)
    
    def get_categories(self):
        """Get all categories using this tag"""
        return self.env['product.category'].search([
            ('tag_ids', 'in', self.id)
        ])
    
    def merge_with(self, other_tag):
        """Merge this tag with another tag"""
        other_tag = self.env['product.category.tag'].browse(other_tag)
        if other_tag == self:
            return
        
        # Move all categories from other tag to this tag
        categories = other_tag.get_categories()
        for category in categories:
            category.tag_ids = [(3, other_tag.id), (4, self.id)]
        
        # Archive the other tag
        other_tag.active = False