# -*- coding: utf-8 -*-

from core_framework.orm import BaseModel, CharField, TextField, FloatField, IntegerField, BooleanField, Many2OneField, Many2ManyField, SelectionField
from core_framework.orm import KidsClothingMixin, PriceMixin


class ProductCategoryTemplate(BaseModel, KidsClothingMixin, PriceMixin):
    """Product Category Template - Template for quick category creation"""
    
    _name = 'product.category.template'
    _description = 'Product Category Template'
    _order = 'name'

    # Basic Information
    name = CharField(string='Template Name', required=True, size=255)
    description = TextField(string='Description')
    active = BooleanField(string='Active', default=True)
    
    # Kids Clothing Specific Fields
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
        ('boys', 'Boys'),
        ('girls', 'Girls'),
        ('unisex', 'Unisex'),
    ], default='unisex')
    
    season = SelectionField(string='Season', selection=[
        ('summer', 'Summer'),
        ('winter', 'Winter'),
        ('monsoon', 'Monsoon'),
        ('all_season', 'All Season'),
    ], default='all_season')
    
    brand_type = SelectionField(string='Brand Type', selection=[
        ('premium', 'Premium'),
        ('mid_range', 'Mid Range'),
        ('budget', 'Budget'),
        ('all', 'All Brands'),
    ], default='all')
    
    style_type = SelectionField(string='Style Type', selection=[
        ('casual', 'Casual'),
        ('formal', 'Formal'),
        ('party', 'Party'),
        ('sports', 'Sports'),
        ('ethnic', 'Ethnic'),
        ('all', 'All Styles'),
    ], default='all')
    
    color_family = SelectionField(string='Color Family', selection=[
        ('primary', 'Primary Colors'),
        ('pastel', 'Pastel Colors'),
        ('neutral', 'Neutral Colors'),
        ('bright', 'Bright Colors'),
        ('all', 'All Colors'),
    ], default='all')
    
    size_range = SelectionField(string='Size Range', selection=[
        ('xs_s', 'XS-S'),
        ('m_l', 'M-L'),
        ('xl_xxl', 'XL-XXL'),
        ('xxxl_plus', 'XXXL+'),
        ('all', 'All Sizes'),
    ], default='all')
    
    # Business Rules
    min_age_months = IntegerField(string='Minimum Age (Months)')
    max_age_months = IntegerField(string='Maximum Age (Months)')
    min_height_cm = FloatField(string='Minimum Height (cm)', digits=(8, 2))
    max_height_cm = FloatField(string='Maximum Height (cm)', digits=(8, 2))
    min_weight_kg = FloatField(string='Minimum Weight (kg)', digits=(8, 2))
    max_weight_kg = FloatField(string='Maximum Weight (kg)', digits=(8, 2))
    
    # Pricing Rules
    default_margin = FloatField(string='Default Margin (%)', digits=(5, 2))
    min_margin = FloatField(string='Minimum Margin (%)', digits=(5, 2))
    max_margin = FloatField(string='Maximum Margin (%)', digits=(5, 2))
    
    # Template Usage
    usage_count = IntegerField(string='Usage Count', readonly=True)
    
    # Company
    company_id = Many2OneField('res.company', string='Company', default=lambda self: self.env.company)
    
    def _compute_usage_count(self):
        """Compute usage count for this template"""
        for template in self:
            categories = self.env['product.category'].search([
                ('template_id', '=', template.id)
            ])
            template.usage_count = len(categories)
    
    def _check_age_range(self):
        """Check age range validation"""
        for template in self:
            if template.min_age_months and template.max_age_months:
                if template.min_age_months >= template.max_age_months:
                    raise ValueError('Minimum age must be less than maximum age.')
    
    def _check_height_range(self):
        """Check height range validation"""
        for template in self:
            if template.min_height_cm and template.max_height_cm:
                if template.min_height_cm >= template.max_height_cm:
                    raise ValueError('Minimum height must be less than maximum height.')
    
    def _check_weight_range(self):
        """Check weight range validation"""
        for template in self:
            if template.min_weight_kg and template.max_weight_kg:
                if template.min_weight_kg >= template.max_weight_kg:
                    raise ValueError('Minimum weight must be less than maximum weight.')
    
    def _check_margin_range(self):
        """Check margin range validation"""
        for template in self:
            if template.min_margin and template.max_margin:
                if template.min_margin >= template.max_margin:
                    raise ValueError('Minimum margin must be less than maximum margin.')
    
    def create_category_from_template(self, name, parent_id=None):
        """Create a new category from this template"""
        vals = {
            'name': name,
            'parent_id': parent_id,
            'age_group': self.age_group,
            'gender': self.gender,
            'season': self.season,
            'brand_type': self.brand_type,
            'style_type': self.style_type,
            'color_family': self.color_family,
            'size_range': self.size_range,
            'min_age_months': self.min_age_months,
            'max_age_months': self.max_age_months,
            'min_height_cm': self.min_height_cm,
            'max_height_cm': self.max_height_cm,
            'min_weight_kg': self.min_weight_kg,
            'max_weight_kg': self.max_weight_kg,
            'default_margin': self.default_margin,
            'min_margin': self.min_margin,
            'max_margin': self.max_margin,
            'template_id': self.id,
        }
        return self.env['product.category'].create(vals)
    
    def apply_to_category(self, category):
        """Apply this template to an existing category"""
        category.write({
            'age_group': self.age_group,
            'gender': self.gender,
            'season': self.season,
            'brand_type': self.brand_type,
            'style_type': self.style_type,
            'color_family': self.color_family,
            'size_range': self.size_range,
            'min_age_months': self.min_age_months,
            'max_age_months': self.max_age_months,
            'min_height_cm': self.min_height_cm,
            'max_height_cm': self.max_height_cm,
            'min_weight_kg': self.min_weight_kg,
            'max_weight_kg': self.max_weight_kg,
            'default_margin': self.default_margin,
            'min_margin': self.min_margin,
            'max_margin': self.max_margin,
            'template_id': self.id,
        })
    
    def duplicate_template(self):
        """Duplicate this template"""
        copy_vals = {
            'name': f"{self.name} (Copy)",
            'description': self.description,
            'age_group': self.age_group,
            'gender': self.gender,
            'season': self.season,
            'brand_type': self.brand_type,
            'style_type': self.style_type,
            'color_family': self.color_family,
            'size_range': self.size_range,
            'min_age_months': self.min_age_months,
            'max_age_months': self.max_age_months,
            'min_height_cm': self.min_height_cm,
            'max_height_cm': self.max_height_cm,
            'min_weight_kg': self.min_weight_kg,
            'max_weight_kg': self.max_weight_kg,
            'default_margin': self.default_margin,
            'min_margin': self.min_margin,
            'max_margin': self.max_margin,
        }
        return self.create(copy_vals)


class ProductCategoryTag(BaseModel):
    """Product Category Tag - Flexible tagging system for categories"""
    
    _name = 'product.category.tag'
    _description = 'Product Category Tag'
    _order = 'name'

    # Basic Information
    name = CharField(string='Tag Name', required=True, size=255)
    color = IntegerField(string='Color')
    active = BooleanField(string='Active', default=True)
    
    # Usage
    category_count = IntegerField(string='Category Count', readonly=True)
    
    # Company
    company_id = Many2OneField('res.company', string='Company', default=lambda self: self.env.company)
    
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
        if other_tag = self.env['product.category.tag'].browse(other_tag)
        if other_tag == self:
            return
        
        # Move all categories from other tag to this tag
        categories = other_tag.get_categories()
        for category in categories:
            category.tag_ids = [(3, other_tag.id), (4, self.id)]
        
        # Archive the other tag
        other_tag.active = False