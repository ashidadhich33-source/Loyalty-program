# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Core Base - Base Mixins
==========================================

Standalone version of the base mixins for Kids Clothing ERP models.
"""

from core_framework.orm import BaseModel, CharField, TextField, BooleanField, IntegerField, DateTimeField, Many2OneField, SelectionField, FloatField
from core_framework.orm import Field
from typing import Dict, Any, Optional
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class KidsClothingMixin(BaseModel):
    """Base mixin for Kids Clothing ERP models"""
    
    _name = 'kids.clothing.mixin'
    _description = 'Kids Clothing Base Mixin'
    _abstract = True
    
    # Common fields for all models
    active = BooleanField(
        string='Active',
        default=True,
        help='Set to false to hide the record without removing it'
    )
    
    notes = TextField(
        string='Notes',
        help='Additional notes or comments'
    )
    
    created_by = IntegerField(
        string='Created By',
        default=1,  # Default to admin user
        help='User who created this record'
    )
    
    created_date = DateTimeField(
        string='Created Date',
        default=datetime.now,
        help='Date and time when this record was created'
    )
    
    updated_by = IntegerField(
        string='Updated By',
        help='User who last updated this record'
    )
    
    updated_date = DateTimeField(
        string='Updated Date',
        help='Date and time when this record was last updated'
    )
    
    def create(self, vals: Dict[str, Any]):
        """Override create to set created_by and created_date"""
        if 'created_by' not in vals:
            vals['created_by'] = 1  # Default to admin user
        if 'created_date' not in vals:
            vals['created_date'] = datetime.now()
        
        result = super().create(vals)
        return result
    
    def write(self, vals: Dict[str, Any]):
        """Override write to set updated_by and updated_date"""
        vals['updated_by'] = 1  # Default to admin user
        vals['updated_date'] = datetime.now()
        
        result = super().write(vals)
        return result
    
    def unlink(self):
        """Override unlink to add logging"""
        logger.info(f"Deleting {self._name} records: {self._ids}")
        return super().unlink()


class AgeGroupMixin(BaseModel):
    """Mixin for age group functionality"""
    
    _name = 'age.group.mixin'
    _description = 'Age Group Mixin'
    _abstract = True
    
    age_group = SelectionField(
        string='Age Group',
        selection=[
            ('newborn', 'Newborn (0-6 months)'),
            ('infant', 'Infant (6-12 months)'),
            ('toddler', 'Toddler (1-3 years)'),
            ('preschool', 'Preschool (3-5 years)'),
            ('school', 'School Age (5-12 years)'),
            ('teen', 'Teen (12-18 years)'),
        ],
        help='Age group for the product or customer'
    )
    
    min_age = IntegerField(
        string='Minimum Age (months)',
        help='Minimum age in months'
    )
    
    max_age = IntegerField(
        string='Maximum Age (months)',
        help='Maximum age in months'
    )
    
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
    
    def _check_age_range(self):
        """Validate age range"""
        if self.min_age and self.max_age and self.min_age >= self.max_age:
            raise ValueError('Minimum age must be less than maximum age')


class GenderMixin(BaseModel):
    """Mixin for gender functionality"""
    
    _name = 'gender.mixin'
    _description = 'Gender Mixin'
    _abstract = True
    
    gender = SelectionField(
        string='Gender',
        selection=[
            ('unisex', 'Unisex'),
            ('boys', 'Boys'),
            ('girls', 'Girls'),
        ],
        default='unisex',
        help='Gender category for the product'
    )
    
    def _check_gender(self):
        """Validate gender selection"""
        if not self.gender:
            raise ValueError('Gender must be selected')


class SeasonMixin(BaseModel):
    """Mixin for season functionality"""
    
    _name = 'season.mixin'
    _description = 'Season Mixin'
    _abstract = True
    
    season = SelectionField(
        string='Season',
        selection=[
            ('summer', 'Summer'),
            ('winter', 'Winter'),
            ('monsoon', 'Monsoon'),
            ('all_season', 'All Season'),
        ],
        default='all_season',
        help='Season for the product'
    )
    
    def _check_season(self):
        """Validate season selection"""
        if not self.season:
            raise ValueError('Season must be selected')


class SizeMixin(BaseModel):
    """Mixin for size functionality"""
    
    _name = 'size.mixin'
    _description = 'Size Mixin'
    _abstract = True
    
    size = SelectionField(
        string='Size',
        selection=[
            ('xs', 'XS'),
            ('s', 'S'),
            ('m', 'M'),
            ('l', 'L'),
            ('xl', 'XL'),
            ('xxl', 'XXL'),
            ('xxxl', 'XXXL'),
        ],
        help='Size of the product'
    )
    
    size_type = SelectionField(
        string='Size Type',
        selection=[
            ('age', 'Age-based'),
            ('standard', 'Standard'),
            ('custom', 'Custom'),
        ],
        default='age',
        help='Type of size measurement'
    )
    
    def _check_size(self):
        """Validate size selection"""
        if self.size_type == 'standard' and not self.size:
            raise ValueError('Size must be selected for standard size type')


class ColorMixin(BaseModel):
    """Mixin for color functionality"""
    
    _name = 'color.mixin'
    _description = 'Color Mixin'
    _abstract = True
    
    color = CharField(
        string='Color',
        size=100,
        help='Color of the product'
    )
    
    color_code = CharField(
        string='Color Code',
        size=10,
        help='Hex color code (e.g., #FF0000)'
    )
    
    def _check_color_code(self):
        """Validate color code format"""
        if self.color_code and not self.color_code.startswith('#'):
            raise ValueError('Color code must start with # (e.g., #FF0000)')


class BrandMixin(BaseModel):
    """Mixin for brand functionality"""
    
    _name = 'brand.mixin'
    _description = 'Brand Mixin'
    _abstract = True
    
    brand_id = IntegerField(
        string='Brand ID',
        help='Brand of the product'
    )
    
    brand_name = CharField(
        string='Brand Name',
        size=100,
        help='Name of the brand'
    )


class PriceMixin(BaseModel):
    """Mixin for price functionality"""
    
    _name = 'price.mixin'
    _description = 'Price Mixin'
    _abstract = True
    
    list_price = FloatField(
        string='List Price',
        help='List price of the product'
    )
    
    cost_price = FloatField(
        string='Cost Price',
        help='Cost price of the product'
    )
    
    margin = FloatField(
        string='Margin (%)',
        help='Profit margin percentage'
    )
    
    def _compute_margin(self):
        """Compute profit margin"""
        if self.list_price and self.cost_price:
            self.margin = ((self.list_price - self.cost_price) / self.list_price) * 100
        else:
            self.margin = 0.0
    
    def _check_prices(self):
        """Validate prices"""
        if self.list_price < 0 or self.cost_price < 0:
            raise ValueError('Prices cannot be negative')
        if self.cost_price > self.list_price:
            raise ValueError('Cost price cannot be higher than list price')