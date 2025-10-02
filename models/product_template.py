# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    # Kids Clothing specific fields
    is_kids_clothing = fields.Boolean(
        string='Kids Clothing Product',
        help='Check if this is a kids clothing product'
    )
    
    age_range = fields.Char(
        string='Age Range',
        help='Age range for the clothing (e.g., 2-4 years)'
    )
    
    gender = fields.Selection([
        ('unisex', 'Unisex'),
        ('boys', 'Boys'),
        ('girls', 'Girls'),
    ], string='Gender', default='unisex')
    
    season = fields.Selection([
        ('spring', 'Spring'),
        ('summer', 'Summer'),
        ('fall', 'Fall'),
        ('winter', 'Winter'),
        ('all_season', 'All Season'),
    ], string='Season', default='all_season')
    
    clothing_type = fields.Selection([
        ('shirt', 'Shirt'),
        ('pants', 'Pants'),
        ('dress', 'Dress'),
        ('shorts', 'Shorts'),
        ('jacket', 'Jacket'),
        ('sweater', 'Sweater'),
        ('shoes', 'Shoes'),
        ('accessories', 'Accessories'),
    ], string='Clothing Type')
    
    brand = fields.Char(
        string='Brand',
        help='Clothing brand'
    )
    
    material = fields.Char(
        string='Material',
        help='Fabric/material composition'
    )
    
    care_instructions = fields.Text(
        string='Care Instructions',
        help='Washing and care instructions'
    )
    
    # Size variants
    size_variants = fields.One2many(
        'product.template.size.variant',
        'product_tmpl_id',
        string='Size Variants'
    )
    
    # Color_variants
    color_variants = fields.One2many(
        'product.template.color.variant',
        'product_tmpl_id',
        string='Color Variants'
    )
    
    # Product attributes
    product_attributes = fields.One2many(
        'product.template.attribute',
        'product_tmpl_id',
        string='Product Attributes'
    )
    
    # Safety information
    safety_certification = fields.Char(
        string='Safety Certification',
        help='Safety certification (e.g., CPSC, CE)'
    )
    
    choking_hazard = fields.Boolean(
        string='Choking Hazard',
        help='Contains small parts that may pose choking hazard'
    )
    
    # Inventory management
    min_stock_level = fields.Float(
        string='Minimum Stock Level',
        help='Minimum stock level before reorder'
    )
    
    reorder_qty = fields.Float(
        string='Reorder Quantity',
        help='Quantity to reorder when stock is low'
    )
    
    # Pricing
    wholesale_price = fields.Float(
        string='Wholesale Price',
        help='Wholesale price for bulk purchases'
    )
    
    retail_price = fields.Float(
        string='Retail Price',
        help='Retail price for individual sales'
    )
    
    @api.model
    def create(self, vals):
        """Override create to set default values for kids clothing products"""
        if vals.get('is_kids_clothing'):
            vals.setdefault('type', 'product')
            vals.setdefault('sale_ok', True)
            vals.setdefault('purchase_ok', True)
        return super().create(vals)
    
    def action_view_stock(self):
        """Action to view product stock levels"""
        action = self.env.ref('stock.action_product_stock_tree').read()[0]
        action['domain'] = [('product_id.product_tmpl_id', '=', self.id)]
        return action


class ProductTemplateSizeVariant(models.Model):
    _name = 'product.template.size.variant'
    _description = 'Product Size Variant'
    
    product_tmpl_id = fields.Many2one(
        'product.template',
        string='Product Template',
        required=True
    )
    
    size = fields.Char(
        string='Size',
        required=True,
        help='Size designation (e.g., XS, S, M, L, XL)'
    )
    
    age_range = fields.Char(
        string='Age Range',
        help='Age range for this size'
    )
    
    chest_measurement = fields.Float(
        string='Chest Measurement (inches)',
        help='Chest measurement in inches'
    )
    
    waist_measurement = fields.Float(
        string='Waist Measurement (inches)',
        help='Waist measurement in inches'
    )
    
    length_measurement = fields.Float(
        string='Length Measurement (inches)',
        help='Length measurement in inches'
    )


class ProductTemplateColorVariant(models.Model):
    _name = 'product.template.color.variant'
    _description = 'Product Color Variant'
    
    product_tmpl_id = fields.Many2one(
        'product.template',
        string='Product Template',
        required=True
    )
    
    color_name = fields.Char(
        string='Color Name',
        required=True,
        help='Color name (e.g., Red, Blue, Green)'
    )
    
    color_code = fields.Char(
        string='Color Code',
        help='Color code (e.g., #FF0000)'
    )
    
    image = fields.Binary(
        string='Color Image',
        help='Image showing the color'
    )


class ProductTemplateAttribute(models.Model):
    _name = 'product.template.attribute'
    _description = 'Product Template Attribute'
    
    product_tmpl_id = fields.Many2one(
        'product.template',
        string='Product Template',
        required=True
    )
    
    attribute_name = fields.Char(
        string='Attribute Name',
        required=True,
        help='Name of the attribute (e.g., Pattern, Style)'
    )
    
    attribute_value = fields.Char(
        string='Attribute Value',
        required=True,
        help='Value of the attribute (e.g., Striped, Solid)'
    )