# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)


class KidsClothingMixin(models.AbstractModel):
    """Base mixin for Kids Clothing ERP models"""
    
    _name = 'kids.clothing.mixin'
    _description = 'Kids Clothing Base Mixin'
    
    # Common fields for all models
    active = fields.Boolean(
        string='Active',
        default=True,
        help='Set to false to hide the record without removing it'
    )
    
    notes = fields.Text(
        string='Notes',
        help='Additional notes or comments'
    )
    
    created_by = fields.Many2one(
        'res.users',
        string='Created By',
        default=lambda self: self.env.user,
        readonly=True,
        help='User who created this record'
    )
    
    created_date = fields.Datetime(
        string='Created Date',
        default=fields.Datetime.now,
        readonly=True,
        help='Date and time when this record was created'
    )
    
    updated_by = fields.Many2one(
        'res.users',
        string='Updated By',
        readonly=True,
        help='User who last updated this record'
    )
    
    updated_date = fields.Datetime(
        string='Updated Date',
        readonly=True,
        help='Date and time when this record was last updated'
    )
    
    @api.model
    def create(self, vals):
        """Override create to set created_by and created_date"""
        if 'created_by' not in vals:
            vals['created_by'] = self.env.user.id
        if 'created_date' not in vals:
            vals['created_date'] = fields.Datetime.now()
        
        result = super(KidsClothingMixin, self).create(vals)
        return result
    
    def write(self, vals):
        """Override write to set updated_by and updated_date"""
        vals['updated_by'] = self.env.user.id
        vals['updated_date'] = fields.Datetime.now()
        
        result = super(KidsClothingMixin, self).write(vals)
        return result
    
    def unlink(self):
        """Override unlink to add logging"""
        _logger.info(f"Deleting {self._name} records: {self.ids}")
        return super(KidsClothingMixin, self).unlink()


class AgeGroupMixin(models.AbstractModel):
    """Mixin for age group functionality"""
    
    _name = 'age.group.mixin'
    _description = 'Age Group Mixin'
    
    age_group = fields.Selection([
        ('newborn', 'Newborn (0-6 months)'),
        ('infant', 'Infant (6-12 months)'),
        ('toddler', 'Toddler (1-3 years)'),
        ('preschool', 'Preschool (3-5 years)'),
        ('school', 'School Age (5-12 years)'),
        ('teen', 'Teen (12-18 years)'),
    ], string='Age Group', help='Age group for the product or customer')
    
    min_age = fields.Integer(
        string='Minimum Age (months)',
        help='Minimum age in months'
    )
    
    max_age = fields.Integer(
        string='Maximum Age (months)',
        help='Maximum age in months'
    )
    
    @api.onchange('age_group')
    def _onchange_age_group(self):
        """Set min/max age based on age group selection"""
        age_mapping = {
            'newborn': (0, 6),
            'infant': (6, 12),
            'toddler': (12, 36),
            'preschool': (36, 60),
            'school': (60, 144),
            'teen': (144, 216),
        }
        
        if self.age_group in age_mapping:
            self.min_age, self.max_age = age_mapping[self.age_group]
    
    @api.constrains('min_age', 'max_age')
    def _check_age_range(self):
        """Validate age range"""
        for record in self:
            if record.min_age and record.max_age and record.min_age >= record.max_age:
                raise ValidationError(_('Minimum age must be less than maximum age'))


class GenderMixin(models.AbstractModel):
    """Mixin for gender functionality"""
    
    _name = 'gender.mixin'
    _description = 'Gender Mixin'
    
    gender = fields.Selection([
        ('unisex', 'Unisex'),
        ('boys', 'Boys'),
        ('girls', 'Girls'),
    ], string='Gender', default='unisex', help='Gender category for the product')
    
    @api.constrains('gender')
    def _check_gender(self):
        """Validate gender selection"""
        for record in self:
            if not record.gender:
                raise ValidationError(_('Gender must be selected'))


class SeasonMixin(models.AbstractModel):
    """Mixin for season functionality"""
    
    _name = 'season.mixin'
    _description = 'Season Mixin'
    
    season = fields.Selection([
        ('summer', 'Summer'),
        ('winter', 'Winter'),
        ('monsoon', 'Monsoon'),
        ('all_season', 'All Season'),
    ], string='Season', default='all_season', help='Season for the product')
    
    @api.constrains('season')
    def _check_season(self):
        """Validate season selection"""
        for record in self:
            if not record.season:
                raise ValidationError(_('Season must be selected'))


class SizeMixin(models.AbstractModel):
    """Mixin for size functionality"""
    
    _name = 'size.mixin'
    _description = 'Size Mixin'
    
    size = fields.Selection([
        ('xs', 'XS'),
        ('s', 'S'),
        ('m', 'M'),
        ('l', 'L'),
        ('xl', 'XL'),
        ('xxl', 'XXL'),
        ('xxxl', 'XXXL'),
    ], string='Size', help='Size of the product')
    
    size_type = fields.Selection([
        ('age', 'Age-based'),
        ('standard', 'Standard'),
        ('custom', 'Custom'),
    ], string='Size Type', default='age', help='Type of size measurement')
    
    @api.constrains('size', 'size_type')
    def _check_size(self):
        """Validate size selection"""
        for record in self:
            if record.size_type == 'standard' and not record.size:
                raise ValidationError(_('Size must be selected for standard size type'))


class ColorMixin(models.AbstractModel):
    """Mixin for color functionality"""
    
    _name = 'color.mixin'
    _description = 'Color Mixin'
    
    color = fields.Char(
        string='Color',
        help='Color of the product'
    )
    
    color_code = fields.Char(
        string='Color Code',
        help='Hex color code (e.g., #FF0000)'
    )
    
    @api.constrains('color_code')
    def _check_color_code(self):
        """Validate color code format"""
        for record in self:
            if record.color_code and not record.color_code.startswith('#'):
                raise ValidationError(_('Color code must start with # (e.g., #FF0000)'))


class BrandMixin(models.AbstractModel):
    """Mixin for brand functionality"""
    
    _name = 'brand.mixin'
    _description = 'Brand Mixin'
    
    brand_id = fields.Many2one(
        'product.brand',
        string='Brand',
        help='Brand of the product'
    )
    
    brand_name = fields.Char(
        related='brand_id.name',
        string='Brand Name',
        readonly=True,
        help='Name of the brand'
    )


class PriceMixin(models.AbstractModel):
    """Mixin for price functionality"""
    
    _name = 'price.mixin'
    _description = 'Price Mixin'
    
    list_price = fields.Float(
        string='List Price',
        digits='Product Price',
        help='List price of the product'
    )
    
    cost_price = fields.Float(
        string='Cost Price',
        digits='Product Price',
        help='Cost price of the product'
    )
    
    margin = fields.Float(
        string='Margin (%)',
        compute='_compute_margin',
        store=True,
        help='Profit margin percentage'
    )
    
    @api.depends('list_price', 'cost_price')
    def _compute_margin(self):
        """Compute profit margin"""
        for record in self:
            if record.list_price and record.cost_price:
                record.margin = ((record.list_price - record.cost_price) / record.list_price) * 100
            else:
                record.margin = 0.0
    
    @api.constrains('list_price', 'cost_price')
    def _check_prices(self):
        """Validate prices"""
        for record in self:
            if record.list_price < 0 or record.cost_price < 0:
                raise ValidationError(_('Prices cannot be negative'))
            if record.cost_price > record.list_price:
                raise ValidationError(_('Cost price cannot be higher than list price'))