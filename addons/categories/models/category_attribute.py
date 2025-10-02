# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class CategoryAttribute(models.Model):
    _name = 'category.attribute'
    _description = 'Category Attribute'
    _order = 'sequence, name'
    _rec_name = 'name'

    name = fields.Char(
        string='Attribute Name',
        required=True,
        translate=True,
        help="Name of the attribute for this category"
    )
    
    category_id = fields.Many2one(
        'product.category',
        string='Category',
        required=True,
        ondelete='cascade',
        help="Category this attribute belongs to"
    )
    
    sequence = fields.Integer(
        string='Sequence',
        default=10,
        help="Order of attributes in the category"
    )
    
    attribute_type = fields.Selection([
        ('text', 'Text'),
        ('number', 'Number'),
        ('boolean', 'Boolean'),
        ('selection', 'Selection'),
        ('date', 'Date'),
        ('datetime', 'DateTime'),
        ('float', 'Float'),
        ('integer', 'Integer'),
    ], string='Attribute Type', required=True, default='text',
       help="Type of the attribute")
    
    required = fields.Boolean(
        string='Required',
        default=False,
        help="Whether this attribute is required for products in this category"
    )
    
    default_value = fields.Char(
        string='Default Value',
        help="Default value for this attribute"
    )
    
    # Selection Options (for selection type)
    selection_options = fields.Text(
        string='Selection Options',
        help="Options for selection type attributes (one per line)"
    )
    
    # Validation Rules
    min_value = fields.Float(
        string='Minimum Value',
        help="Minimum value for numeric attributes"
    )
    
    max_value = fields.Float(
        string='Maximum Value',
        help="Maximum value for numeric attributes"
    )
    
    min_length = fields.Integer(
        string='Minimum Length',
        help="Minimum length for text attributes"
    )
    
    max_length = fields.Integer(
        string='Maximum Length',
        help="Maximum length for text attributes"
    )
    
    # Display Options
    display_type = fields.Selection([
        ('text', 'Text'),
        ('radio', 'Radio Buttons'),
        ('checkbox', 'Checkboxes'),
        ('select', 'Dropdown'),
        ('multiselect', 'Multi-select'),
    ], string='Display Type', default='text',
       help="How to display this attribute in forms")
    
    help_text = fields.Text(
        string='Help Text',
        translate=True,
        help="Help text to display with this attribute"
    )
    
    # Kids Clothing Specific
    is_kids_specific = fields.Boolean(
        string='Kids Specific',
        default=False,
        help="Whether this attribute is specific to kids clothing"
    )
    
    age_group_filter = fields.Selection([
        ('0-2', '0-2 Years (Baby)'),
        ('2-4', '2-4 Years (Toddler)'),
        ('4-6', '4-6 Years (Pre-school)'),
        ('6-8', '6-8 Years (Early School)'),
        ('8-10', '8-10 Years (Middle School)'),
        ('10-12', '10-12 Years (Pre-teen)'),
        ('12-14', '12-14 Years (Teen)'),
        ('14-16', '14-16 Years (Young Adult)'),
        ('all', 'All Ages'),
    ], string='Age Group Filter', default='all',
       help="Age group this attribute applies to")
    
    gender_filter = fields.Selection([
        ('boys', 'Boys'),
        ('girls', 'Girls'),
        ('unisex', 'Unisex'),
    ], string='Gender Filter', default='unisex',
       help="Gender this attribute applies to")
    
    # Company and Multi-company
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self: self.env.company,
        help="Company this attribute belongs to"
    )
    
    # Product Relations
    product_attribute_ids = fields.One2many(
        'product.attribute.value',
        'category_attribute_id',
        string='Product Attribute Values',
        help="Product attribute values for this category attribute"
    )
    
    @api.constrains('min_value', 'max_value')
    def _check_value_range(self):
        for attribute in self:
            if attribute.min_value and attribute.max_value:
                if attribute.min_value > attribute.max_value:
                    raise ValidationError(_('Minimum value cannot be greater than maximum value.'))
    
    @api.constrains('min_length', 'max_length')
    def _check_length_range(self):
        for attribute in self:
            if attribute.min_length and attribute.max_length:
                if attribute.min_length > attribute.max_length:
                    raise ValidationError(_('Minimum length cannot be greater than maximum length.'))
    
    @api.constrains('attribute_type', 'selection_options')
    def _check_selection_options(self):
        for attribute in self:
            if attribute.attribute_type == 'selection' and not attribute.selection_options:
                raise ValidationError(_('Selection options are required for selection type attributes.'))
    
    def get_selection_options(self):
        """Get selection options as a list of tuples"""
        if self.attribute_type == 'selection' and self.selection_options:
            options = []
            for line in self.selection_options.split('\n'):
                line = line.strip()
                if line:
                    options.append((line, line))
            return options
        return []
    
    def validate_value(self, value):
        """Validate a value against this attribute's rules"""
        if self.required and not value:
            raise ValidationError(_('Value is required for attribute %s') % self.name)
        
        if not value:
            return True
        
        if self.attribute_type == 'number' or self.attribute_type == 'float':
            try:
                num_value = float(value)
                if self.min_value and num_value < self.min_value:
                    raise ValidationError(_('Value must be at least %s for attribute %s') % (self.min_value, self.name))
                if self.max_value and num_value > self.max_value:
                    raise ValidationError(_('Value must be at most %s for attribute %s') % (self.max_value, self.name))
            except ValueError:
                raise ValidationError(_('Invalid numeric value for attribute %s') % self.name)
        
        elif self.attribute_type == 'text':
            if self.min_length and len(str(value)) < self.min_length:
                raise ValidationError(_('Value must be at least %s characters for attribute %s') % (self.min_length, self.name))
            if self.max_length and len(str(value)) > self.max_length:
                raise ValidationError(_('Value must be at most %s characters for attribute %s') % (self.max_length, self.name))
        
        elif self.attribute_type == 'selection':
            valid_options = [opt[0] for opt in self.get_selection_options()]
            if value not in valid_options:
                raise ValidationError(_('Invalid selection value for attribute %s') % self.name)
        
        return True