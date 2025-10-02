# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class ProductCategory(models.Model):
    _name = 'product.category'
    _description = 'Product Category'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'sequence, name'
    _parent_name = 'parent_id'
    _parent_store = True
    _parent_order = 'name'
    _rec_name = 'complete_name'

    name = fields.Char(
        string='Category Name',
        required=True,
        translate=True,
        tracking=True,
        help="Category name for kids clothing products"
    )
    
    complete_name = fields.Char(
        string='Complete Name',
        compute='_compute_complete_name',
        store=True,
        help="Full category path including parent categories"
    )
    
    parent_id = fields.Many2one(
        'product.category',
        string='Parent Category',
        index=True,
        ondelete='cascade',
        help="Parent category in the hierarchy"
    )
    
    parent_path = fields.Char(
        string='Parent Path',
        index=True,
        help="Parent path for hierarchical queries"
    )
    
    child_id = fields.One2many(
        'product.category',
        'parent_id',
        string='Child Categories',
        help="Child categories under this category"
    )
    
    sequence = fields.Integer(
        string='Sequence',
        default=10,
        help="Order of categories in the list"
    )
    
    # Kids Clothing Specific Fields
    age_group = fields.Selection([
        ('0-2', '0-2 Years (Baby)'),
        ('2-4', '2-4 Years (Toddler)'),
        ('4-6', '4-6 Years (Pre-school)'),
        ('6-8', '6-8 Years (Early School)'),
        ('8-10', '8-10 Years (Middle School)'),
        ('10-12', '10-12 Years (Pre-teen)'),
        ('12-14', '12-14 Years (Teen)'),
        ('14-16', '14-16 Years (Young Adult)'),
        ('all', 'All Ages'),
    ], string='Age Group', required=True, default='all',
       help="Target age group for this category")
    
    gender = fields.Selection([
        ('boys', 'Boys'),
        ('girls', 'Girls'),
        ('unisex', 'Unisex'),
    ], string='Gender', required=True, default='unisex',
       help="Target gender for this category")
    
    season = fields.Selection([
        ('summer', 'Summer'),
        ('winter', 'Winter'),
        ('monsoon', 'Monsoon'),
        ('all_season', 'All Season'),
    ], string='Season', required=True, default='all_season',
       help="Season for this category")
    
    brand_type = fields.Selection([
        ('premium', 'Premium'),
        ('mid_range', 'Mid Range'),
        ('budget', 'Budget'),
        ('all', 'All Brands'),
    ], string='Brand Type', required=True, default='all',
       help="Brand type for this category")
    
    # Category Properties
    is_active = fields.Boolean(
        string='Active',
        default=True,
        tracking=True,
        help="Whether this category is active"
    )
    
    description = fields.Text(
        string='Description',
        translate=True,
        help="Detailed description of the category"
    )
    
    image = fields.Binary(
        string='Category Image',
        help="Image representing this category"
    )
    
    image_medium = fields.Binary(
        string='Medium Image',
        compute='_compute_image_medium',
        store=True,
        help="Medium-sized image for this category"
    )
    
    image_small = fields.Binary(
        string='Small Image',
        compute='_compute_image_small',
        store=True,
        help="Small-sized image for this category"
    )
    
    icon = fields.Char(
        string='Icon',
        help="Icon class for this category (e.g., 'fa fa-baby')"
    )
    
    color = fields.Char(
        string='Color',
        default='#007bff',
        help="Color code for this category"
    )
    
    # Business Rules
    min_price = fields.Float(
        string='Minimum Price',
        digits='Product Price',
        help="Minimum price for products in this category"
    )
    
    max_price = fields.Float(
        string='Maximum Price',
        digits='Product Price',
        help="Maximum price for products in this category"
    )
    
    default_margin = fields.Float(
        string='Default Margin (%)',
        digits='Product Price',
        default=30.0,
        help="Default margin percentage for products in this category"
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
        digits='Product Price',
        help="Total sales amount for this category"
    )
    
    avg_rating = fields.Float(
        string='Average Rating',
        compute='_compute_avg_rating',
        digits=(3, 2),
        help="Average rating of products in this category"
    )
    
    # Company and Multi-company
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self: self.env.company,
        help="Company this category belongs to"
    )
    
    # Product Relations
    product_ids = fields.One2many(
        'product.template',
        'categ_id',
        string='Products',
        help="Products in this category"
    )
    
    # Category Attributes
    attribute_ids = fields.One2many(
        'category.attribute',
        'category_id',
        string='Category Attributes',
        help="Attributes specific to this category"
    )
    
    # Category Rules
    rule_ids = fields.One2many(
        'category.rule',
        'category_id',
        string='Category Rules',
        help="Business rules for this category"
    )
    
    @api.depends('name', 'parent_id.complete_name')
    def _compute_complete_name(self):
        for category in self:
            if category.parent_id:
                category.complete_name = f"{category.parent_id.complete_name} / {category.name}"
            else:
                category.complete_name = category.name
    
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
    
    @api.depends('product_ids')
    def _compute_product_count(self):
        for category in self:
            category.product_count = len(category.product_ids)
    
    @api.depends('product_ids', 'product_ids.sales_count')
    def _compute_total_sales(self):
        for category in self:
            total = 0.0
            for product in category.product_ids:
                total += product.sales_count or 0.0
            category.total_sales = total
    
    @api.depends('product_ids', 'product_ids.rating_avg')
    def _compute_avg_rating(self):
        for category in self:
            if category.product_ids:
                ratings = [p.rating_avg for p in category.product_ids if p.rating_avg > 0]
                category.avg_rating = sum(ratings) / len(ratings) if ratings else 0.0
            else:
                category.avg_rating = 0.0
    
    @api.constrains('parent_id')
    def _check_parent_recursion(self):
        if not self._check_recursion():
            raise ValidationError(_('You cannot create recursive categories.'))
    
    @api.constrains('min_price', 'max_price')
    def _check_price_range(self):
        for category in self:
            if category.min_price and category.max_price:
                if category.min_price > category.max_price:
                    raise ValidationError(_('Minimum price cannot be greater than maximum price.'))
    
    def name_get(self):
        result = []
        for category in self:
            result.append((category.id, category.complete_name))
        return result
    
    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        args = args or []
        if name:
            categories = self.search([('complete_name', operator, name)] + args, limit=limit)
        else:
            categories = self.search(args, limit=limit)
        return categories.name_get()
    
    def action_view_products(self):
        """Action to view products in this category"""
        action = self.env.ref('products.action_product_template').read()[0]
        action['domain'] = [('categ_id', '=', self.id)]
        action['context'] = {'default_categ_id': self.id}
        return action
    
    def action_view_analytics(self):
        """Action to view category analytics"""
        action = self.env.ref('categories.action_category_analytics').read()[0]
        action['domain'] = [('category_id', '=', self.id)]
        return action