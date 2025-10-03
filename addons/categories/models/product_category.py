# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)


class ProductCategory(models.Model):
    _name = 'product.category'
    _description = 'Product Category'
    _order = 'sequence, name'
    _parent_name = 'parent_id'
    _parent_store = True
    _parent_order = 'name'
    _rec_name = 'complete_name'

    name = fields.Char(
        string='Category Name',
        required=True,
        translate=True,
        help="Category name for kids clothing products"
    )
    complete_name = fields.Char(
        string='Complete Name',
        compute='_compute_complete_name',
        store=True,
        help="Full category path"
    )
    parent_id = fields.Many2one(
        'product.category',
        string='Parent Category',
        index=True,
        ondelete='cascade',
        help="Parent category in the hierarchy"
    )
    child_id = fields.One2many(
        'product.category',
        'parent_id',
        string='Child Categories',
        help="Child categories"
    )
    parent_path = fields.Char(
        index=True,
        help="Parent path for hierarchical queries"
    )
    sequence = fields.Integer(
        string='Sequence',
        default=10,
        help="Order of categories in the list"
    )
    active = fields.Boolean(
        string='Active',
        default=True,
        help="Whether this category is active"
    )
    
    # Kids Clothing Specific Fields
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
    ], string='Age Group', help="Target age group for this category")
    
    gender = fields.Selection([
        ('boys', 'Boys'),
        ('girls', 'Girls'),
        ('unisex', 'Unisex'),
    ], string='Gender', help="Target gender for this category")
    
    season = fields.Selection([
        ('summer', 'Summer'),
        ('winter', 'Winter'),
        ('monsoon', 'Monsoon'),
        ('all_season', 'All Season'),
    ], string='Season', help="Season for this category")
    
    brand_type = fields.Selection([
        ('premium', 'Premium'),
        ('mid_range', 'Mid Range'),
        ('budget', 'Budget'),
        ('all', 'All Brands'),
    ], string='Brand Type', help="Brand type for this category")
    
    style_type = fields.Selection([
        ('casual', 'Casual'),
        ('formal', 'Formal'),
        ('party', 'Party'),
        ('sports', 'Sports'),
        ('ethnic', 'Ethnic'),
        ('all', 'All Styles'),
    ], string='Style Type', help="Style type for this category")
    
    color_family = fields.Selection([
        ('primary', 'Primary Colors'),
        ('pastel', 'Pastel Colors'),
        ('neutral', 'Neutral Colors'),
        ('bright', 'Bright Colors'),
        ('all', 'All Colors'),
    ], string='Color Family', help="Color family for this category")
    
    size_range = fields.Selection([
        ('xs_s', 'XS-S'),
        ('m_l', 'M-L'),
        ('xl_xxl', 'XL-XXL'),
        ('xxxl_plus', 'XXXL+'),
        ('all', 'All Sizes'),
    ], string='Size Range', help="Size range for this category")
    
    # Category Properties
    is_main_category = fields.Boolean(
        string='Main Category',
        default=False,
        help="Whether this is a main category"
    )
    is_leaf_category = fields.Boolean(
        string='Leaf Category',
        compute='_compute_is_leaf',
        store=True,
        help="Whether this category has no children"
    )
    category_code = fields.Char(
        string='Category Code',
        size=10,
        help="Short code for this category"
    )
    description = fields.Text(
        string='Description',
        translate=True,
        help="Detailed description of this category"
    )
    image = fields.Binary(
        string='Category Image',
        help="Image representing this category"
    )
    image_medium = fields.Binary(
        string='Medium Image',
        compute='_compute_image_medium',
        store=True,
        help="Medium sized image"
    )
    image_small = fields.Binary(
        string='Small Image',
        compute='_compute_image_small',
        store=True,
        help="Small sized image"
    )
    
    # Business Rules
    min_age_months = fields.Integer(
        string='Minimum Age (Months)',
        help="Minimum age in months for this category"
    )
    max_age_months = fields.Integer(
        string='Maximum Age (Months)',
        help="Maximum age in months for this category"
    )
    min_height_cm = fields.Float(
        string='Minimum Height (cm)',
        digits=(8, 2),
        help="Minimum height in cm for this category"
    )
    max_height_cm = fields.Float(
        string='Maximum Height (cm)',
        digits=(8, 2),
        help="Maximum height in cm for this category"
    )
    min_weight_kg = fields.Float(
        string='Minimum Weight (kg)',
        digits=(8, 2),
        help="Minimum weight in kg for this category"
    )
    max_weight_kg = fields.Float(
        string='Maximum Weight (kg)',
        digits=(8, 2),
        help="Maximum weight in kg for this category"
    )
    
    # Pricing Rules
    default_margin = fields.Float(
        string='Default Margin (%)',
        digits=(5, 2),
        help="Default margin percentage for products in this category"
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
    
    # Analytics Fields
    product_count = fields.Integer(
        string='Product Count',
        compute='_compute_product_count',
        help="Number of products in this category"
    )
    total_sales = fields.Float(
        string='Total Sales',
        compute='_compute_total_sales',
        digits=(12, 2),
        help="Total sales amount for this category"
    )
    avg_rating = fields.Float(
        string='Average Rating',
        digits=(3, 2),
        compute='_compute_avg_rating',
        help="Average rating of products in this category"
    )
    
    # Company and Multi-company
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self: self.env.company,
        help="Company this category belongs to"
    )
    
    # Tags and Classification
    tag_ids = fields.Many2many(
        'product.category.tag',
        'product_category_tag_rel',
        'category_id',
        'tag_id',
        string='Tags',
        help="Tags for this category"
    )
    
    # SEO Fields
    meta_title = fields.Char(
        string='Meta Title',
        translate=True,
        help="SEO meta title"
    )
    meta_description = fields.Text(
        string='Meta Description',
        translate=True,
        help="SEO meta description"
    )
    meta_keywords = fields.Char(
        string='Meta Keywords',
        translate=True,
        help="SEO meta keywords"
    )
    
    # Display Properties
    display_type = fields.Selection([
        ('normal', 'Normal'),
        ('page', 'Page'),
        ('group', 'Group'),
    ], string='Display Type', default='normal', help="Display type for this category")
    
    # Computed Fields
    @api.depends('name', 'parent_id.complete_name')
    def _compute_complete_name(self):
        for category in self:
            if category.parent_id:
                category.complete_name = f"{category.parent_id.complete_name} / {category.name}"
            else:
                category.complete_name = category.name
    
    @api.depends('child_id')
    def _compute_is_leaf(self):
        for category in self:
            category.is_leaf_category = not bool(category.child_id)
    
    @api.depends('image')
    def _compute_image_medium(self):
        for category in self:
            if category.image:
                # In a real implementation, you would resize the image here
                category.image_medium = category.image
            else:
                category.image_medium = False
    
    @api.depends('image')
    def _compute_image_small(self):
        for category in self:
            if category.image:
                # In a real implementation, you would resize the image here
                category.image_small = category.image
            else:
                category.image_small = False
    
    @api.depends('child_id')
    def _compute_product_count(self):
        for category in self:
            # Count products in this category and all its children
            all_categories = self._get_all_children(category)
            all_categories.append(category.id)
            
            products = self.env['product.template'].search([
                ('categ_id', 'in', all_categories)
            ])
            category.product_count = len(products)
    
    def _compute_total_sales(self):
        for category in self:
            # This would be computed from actual sales data
            category.total_sales = 0.0
    
    def _compute_avg_rating(self):
        for category in self:
            # This would be computed from product ratings
            category.avg_rating = 0.0
    
    def _get_all_children(self, category):
        """Get all child category IDs recursively"""
        children = []
        for child in category.child_id:
            children.append(child.id)
            children.extend(self._get_all_children(child))
        return children
    
    # Constraints
    @api.constrains('parent_id')
    def _check_parent_recursion(self):
        if not self._check_recursion():
            raise ValidationError(_('You cannot create recursive categories.'))
    
    @api.constrains('min_age_months', 'max_age_months')
    def _check_age_range(self):
        for category in self:
            if category.min_age_months and category.max_age_months:
                if category.min_age_months >= category.max_age_months:
                    raise ValidationError(_('Minimum age must be less than maximum age.'))
    
    @api.constrains('min_height_cm', 'max_height_cm')
    def _check_height_range(self):
        for category in self:
            if category.min_height_cm and category.max_height_cm:
                if category.min_height_cm >= category.max_height_cm:
                    raise ValidationError(_('Minimum height must be less than maximum height.'))
    
    @api.constrains('min_weight_kg', 'max_weight_kg')
    def _check_weight_range(self):
        for category in self:
            if category.min_weight_kg and category.max_weight_kg:
                if category.min_weight_kg >= category.max_weight_kg:
                    raise ValidationError(_('Minimum weight must be less than maximum weight.'))
    
    @api.constrains('min_margin', 'max_margin')
    def _check_margin_range(self):
        for category in self:
            if category.min_margin and category.max_margin:
                if category.min_margin >= category.max_margin:
                    raise ValidationError(_('Minimum margin must be less than maximum margin.'))
    
    # Methods
    def name_get(self):
        """Return the display name for the category"""
        result = []
        for category in self:
            name = category.complete_name
            result.append((category.id, name))
        return result
    
    @api.model
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
            raise ValidationError(_('Cannot move category to its own child.'))
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
            'parent_id': self.parent_id.id,
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