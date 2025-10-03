# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)


class ProductCategoryTemplate(models.Model):
    _name = 'product.category.template'
    _description = 'Product Category Template'
    _order = 'name'

    name = fields.Char(
        string='Template Name',
        required=True,
        help="Name of the category template"
    )
    description = fields.Text(
        string='Description',
        help="Description of this template"
    )
    active = fields.Boolean(
        string='Active',
        default=True,
        help="Whether this template is active"
    )
    
    # Template Properties
    age_group = fields.Selection([
        ('0-2', '0-2 Years (Baby)'),
        ('2-4', '2-4 Years (Toddler)'),
        ('4-6', '4-6 Years (Pre-school)'),
        ('6-8', '6-8 Years (Early School)'),
        ('8-10', '8-10 Years (School)'),
        ('10-12', '10-12 Years (Pre-teen)'),
        ('12-14', '12-14 Years (Teen)'),
        ('14-16', '14-16 Years (Young Adult)'),
        ('all', 'All Ages'),
    ], string='Age Group', help="Target age group for this template")
    
    gender = fields.Selection([
        ('boys', 'Boys'),
        ('girls', 'Girls'),
        ('unisex', 'Unisex'),
    ], string='Gender', help="Target gender for this template")
    
    season = fields.Selection([
        ('summer', 'Summer'),
        ('winter', 'Winter'),
        ('monsoon', 'Monsoon'),
        ('all_season', 'All Season'),
    ], string='Season', help="Season for this template")
    
    brand_type = fields.Selection([
        ('premium', 'Premium'),
        ('mid_range', 'Mid Range'),
        ('budget', 'Budget'),
        ('all', 'All Brands'),
    ], string='Brand Type', help="Brand type for this template")
    
    style_type = fields.Selection([
        ('casual', 'Casual'),
        ('formal', 'Formal'),
        ('party', 'Party'),
        ('sports', 'Sports'),
        ('ethnic', 'Ethnic'),
        ('all', 'All Styles'),
    ], string='Style Type', help="Style type for this template")
    
    color_family = fields.Selection([
        ('primary', 'Primary Colors'),
        ('pastel', 'Pastel Colors'),
        ('neutral', 'Neutral Colors'),
        ('bright', 'Bright Colors'),
        ('all', 'All Colors'),
    ], string='Color Family', help="Color family for this template")
    
    size_range = fields.Selection([
        ('xs_s', 'XS-S'),
        ('m_l', 'M-L'),
        ('xl_xxl', 'XL-XXL'),
        ('xxxl_plus', 'XXXL+'),
        ('all', 'All Sizes'),
    ], string='Size Range', help="Size range for this template")
    
    # Business Rules
    min_age_months = fields.Integer(
        string='Minimum Age (Months)',
        help="Minimum age in months for this template"
    )
    max_age_months = fields.Integer(
        string='Maximum Age (Months)',
        help="Maximum age in months for this template"
    )
    min_height_cm = fields.Float(
        string='Minimum Height (cm)',
        digits=(8, 2),
        help="Minimum height in cm for this template"
    )
    max_height_cm = fields.Float(
        string='Maximum Height (cm)',
        digits=(8, 2),
        help="Maximum height in cm for this template"
    )
    min_weight_kg = fields.Float(
        string='Minimum Weight (kg)',
        digits=(8, 2),
        help="Minimum weight in kg for this template"
    )
    max_weight_kg = fields.Float(
        string='Maximum Weight (kg)',
        digits=(8, 2),
        help="Maximum weight in kg for this template"
    )
    
    # Pricing Rules
    default_margin = fields.Float(
        string='Default Margin (%)',
        digits=(5, 2),
        help="Default margin percentage for this template"
    )
    min_margin = fields.Float(
        string='Minimum Margin (%)',
        digits=(5, 2),
        help="Minimum margin percentage allowed"
    )
    max_margin = fields.Float(
        string='Maximum Margin (%)',
        digits=(5, 2),
        help="Maximum margin percentage allowed"
    )
    
    # Template Usage
    usage_count = fields.Integer(
        string='Usage Count',
        compute='_compute_usage_count',
        help="Number of categories using this template"
    )
    
    # Company
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self: self.env.company,
        help="Company this template belongs to"
    )
    
    # Computed Fields
    @api.depends('name')
    def _compute_usage_count(self):
        for template in self:
            categories = self.env['product.category'].search([
                ('template_id', '=', template.id)
            ])
            template.usage_count = len(categories)
    
    # Constraints
    @api.constrains('min_age_months', 'max_age_months')
    def _check_age_range(self):
        for template in self:
            if template.min_age_months and template.max_age_months:
                if template.min_age_months >= template.max_age_months:
                    raise ValidationError(_('Minimum age must be less than maximum age.'))
    
    @api.constrains('min_height_cm', 'max_height_cm')
    def _check_height_range(self):
        for template in self:
            if template.min_height_cm and template.max_height_cm:
                if template.min_height_cm >= template.max_height_cm:
                    raise ValidationError(_('Minimum height must be less than maximum height.'))
    
    @api.constrains('min_weight_kg', 'max_weight_kg')
    def _check_weight_range(self):
        for template in self:
            if template.min_weight_kg and template.max_weight_kg:
                if template.min_weight_kg >= template.max_weight_kg:
                    raise ValidationError(_('Minimum weight must be less than maximum weight.'))
    
    @api.constrains('min_margin', 'max_margin')
    def _check_margin_range(self):
        for template in self:
            if template.min_margin and template.max_margin:
                if template.min_margin >= template.max_margin:
                    raise ValidationError(_('Minimum margin must be less than maximum margin.'))
    
    # Methods
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


class ProductCategoryTag(models.Model):
    _name = 'product.category.tag'
    _description = 'Product Category Tag'
    _order = 'name'

    name = fields.Char(
        string='Tag Name',
        required=True,
        help="Name of the tag"
    )
    color = fields.Integer(
        string='Color',
        help="Color for the tag"
    )
    active = fields.Boolean(
        string='Active',
        default=True,
        help="Whether this tag is active"
    )
    
    # Usage
    category_count = fields.Integer(
        string='Category Count',
        compute='_compute_category_count',
        help="Number of categories using this tag"
    )
    
    # Company
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self: self.env.company,
        help="Company this tag belongs to"
    )
    
    # Computed Fields
    @api.depends('name')
    def _compute_category_count(self):
        for tag in self:
            categories = self.env['product.category'].search([
                ('tag_ids', 'in', tag.id)
            ])
            tag.category_count = len(categories)
    
    # Methods
    def get_categories(self):
        """Get all categories using this tag"""
        return self.env['product.category'].search([
            ('tag_ids', 'in', self.id)
        ])
    
    def merge_with(self, other_tag):
        """Merge this tag with another tag"""
        if other_tag == self:
            return
        
        # Move all categories from other tag to this tag
        categories = other_tag.get_categories()
        for category in categories:
            category.tag_ids = [(3, other_tag.id), (4, self.id)]
        
        # Archive the other tag
        other_tag.active = False