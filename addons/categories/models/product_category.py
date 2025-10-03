#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Product Category Model
=========================================

Product category management for kids clothing retail.
"""

import logging
from core_framework.orm import BaseModel, CharField, TextField, BooleanField, IntegerField, DateTimeField, Many2OneField, SelectionField, FloatField, One2ManyField, Many2ManyField
from core_framework.exceptions import ValidationError

logger = logging.getLogger(__name__)

class ProductCategory(BaseModel):
    """Product categories for kids clothing"""
    
    _name = 'product.category'
    _description = 'Product Category'
    _table = 'product_category'
    _order = 'sequence, name'
    
    # Basic Information
    name = CharField(
        string='Category Name',
        size=100,
        required=True,
        help='Name of the product category'
    )
    
    code = CharField(
        string='Category Code',
        size=20,
        help='Short code for the category'
    )
    
    description = TextField(
        string='Description',
        help='Detailed description of the category'
    )
    
    # Hierarchy
    parent_id = Many2OneField(
        'product.category',
        string='Parent Category',
        help='Parent category in hierarchy'
    )
    
    child_ids = One2ManyField(
        string='Child Categories',
        comodel_name='product.category',
        inverse_name='parent_id',
        help='Child categories in hierarchy'
    )
    
    # Category Type
    category_type = SelectionField(
        string='Category Type',
        selection=[
            ('age_based', 'Age Based'),
            ('seasonal', 'Seasonal'),
            ('brand', 'Brand'),
            ('gender', 'Gender'),
            ('size', 'Size'),
            ('style', 'Style'),
            ('other', 'Other')
        ],
        default='age_based',
        help='Type of category classification'
    )
    
    # Age-based categories
    age_group = SelectionField(
        string='Age Group',
        selection=[
            ('newborn', 'Newborn (0-6 months)'),
            ('infant', 'Infant (6-12 months)'),
            ('toddler', 'Toddler (1-3 years)'),
            ('preschool', 'Preschool (3-5 years)'),
            ('school', 'School (5-12 years)'),
            ('teen', 'Teen (12+ years)'),
            ('all', 'All Ages')
        ],
        help='Target age group for this category'
    )
    
    # Gender categories
    gender = SelectionField(
        string='Gender',
        selection=[
            ('boys', 'Boys'),
            ('girls', 'Girls'),
            ('unisex', 'Unisex'),
            ('all', 'All Genders')
        ],
        default='all',
        help='Target gender for this category'
    )
    
    # Seasonal categories
    season = SelectionField(
        string='Season',
        selection=[
            ('summer', 'Summer'),
            ('winter', 'Winter'),
            ('monsoon', 'Monsoon'),
            ('all_season', 'All Season'),
            ('festive', 'Festive'),
            ('party', 'Party Wear')
        ],
        help='Seasonal classification'
    )
    
    # Category Properties
    is_active = BooleanField(
        string='Active',
        default=True,
        help='Whether this category is active'
    )
    
    sequence = IntegerField(
        string='Sequence',
        default=10,
        help='Display order'
    )
    
    # Visual Properties
    color = IntegerField(
        string='Color',
        help='Color for category display'
    )
    
    icon = CharField(
        string='Icon',
        size=50,
        help='Icon class for category display'
    )
    
    # Analytics
    product_count = IntegerField(
        string='Product Count',
        default=0,
        help='Number of products in this category'
    )
    
    # Business Rules
    margin_percentage = FloatField(
        string='Margin %',
        digits=(5, 2),
        help='Default margin percentage for this category'
    )
    
    discount_percentage = FloatField(
        string='Discount %',
        digits=(5, 2),
        help='Default discount percentage for this category'
    )
    
    # Timestamps
    create_date = DateTimeField(
        string='Created On',
        auto_now_add=True
    )
    
    write_date = DateTimeField(
        string='Updated On',
        auto_now=True
    )
    
    def create(self, vals):
        """Override create to set defaults"""
        if 'code' not in vals and 'name' in vals:
            vals['code'] = vals['name'].upper().replace(' ', '_')
        
        return super().create(vals)
    
    def write(self, vals):
        """Override write to update product counts"""
        result = super().write(vals)
        
        # Update product count if category changed
        if 'name' in vals or 'parent_id' in vals:
            self._update_product_count()
        
        return result
    
    def _update_product_count(self):
        """Update product count for this category"""
        for record in self:
            # Count products in this category
            product_count = self.env['product.template'].search_count([
                ('categ_id', '=', record.id)
            ])
            record.product_count = product_count
    
    def get_category_hierarchy(self):
        """Get full category hierarchy path"""
        hierarchy = []
        current = self
        
        while current:
            hierarchy.insert(0, current.name)
            current = current.parent_id
        
        return ' > '.join(hierarchy)
    
    def get_child_categories(self):
        """Get all child categories recursively"""
        children = []
        
        for child in self.child_ids:
            children.append(child)
            children.extend(child.get_child_categories())
        
        return children
    
    def validate_category_rules(self):
        """Validate category business rules"""
        errors = []
        
        # Check for circular references
        if self.parent_id:
            if self in self.parent_id.get_child_categories():
                errors.append("Circular reference detected in category hierarchy")
        
        # Validate age group and gender combination
        if self.category_type == 'age_based':
            if not self.age_group:
                errors.append("Age group is required for age-based categories")
        
        if errors:
            raise ValidationError('\n'.join(errors))
    
    def action_view_products(self):
        """Action to view products in this category"""
        return {
            'type': 'ocean.actions.act_window',
            'name': f'Products in {self.name}',
            'res_model': 'product.template',
            'view_mode': 'tree,form',
            'domain': [('categ_id', '=', self.id)],
            'context': {'default_categ_id': self.id}
        }
    
    def action_analyze_category(self):
        """Action to analyze category performance"""
        return {
            'type': 'ocean.actions.act_window',
            'name': f'Category Analytics - {self.name}',
            'res_model': 'category.analytics',
            'view_mode': 'form',
            'domain': [('category_id', '=', self.id)],
            'context': {'default_category_id': self.id}
        }