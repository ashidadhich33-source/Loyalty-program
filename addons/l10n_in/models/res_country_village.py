# -*- coding: utf-8 -*-
"""
Ocean ERP - Indian Village Model
================================

Village model with Indian localization for kids clothing retail.
"""

from core_framework.orm import BaseModel, CharField, TextField, BooleanField, IntegerField, DateTimeField, Many2OneField, SelectionField, FloatField
from core_framework.exceptions import ValidationError, UserError
from addons.core_base.models.base_mixins import KidsClothingMixin
import logging

_logger = logging.getLogger(__name__)


class ResCountryVillage(BaseModel, KidsClothingMixin):
    """Indian Village Model for Ocean ERP"""
    
    _name = 'res.country.village'
    _description = 'Village'
    _order = 'name'
    _rec_name = 'name'

    name = CharField(
        string='Village Name',
        required=True,
        help='Name of the village'
    )
    
    code = CharField(
        string='Village Code',
        required=True,
        help='Code of the village'
    )
    
    taluka_id = Many2OneField(
        'res.country.taluka',
        string='Taluka',
        required=True,
        help='Taluka this village belongs to'
    )
    
    district_id = Many2OneField(
        'res.country.district',
        string='District',
        required=True,
        help='District this village belongs to'
    )
    
    state_id = Many2OneField(
        'res.country.state',
        string='State',
        required=True,
        help='State this village belongs to'
    )
    
    country_id = Many2OneField(
        'res.country',
        string='Country',
        required=True,
        default=lambda self: self.env.ref('base.in'),
        help='Country this village belongs to'
    )
    
    # Indian Specific Fields
    village_type = SelectionField(
        selection=[
            ('village', 'Village'),
            ('town', 'Town'),
            ('city', 'City'),
            ('municipality', 'Municipality'),
        ],
        string='Village Type',
        help='Type of village'
    )
    
    population = IntegerField(
        string='Population',
        help='Population of the village'
    )
    
    area = FloatField(
        string='Area (sq km)',
        help='Area of the village in square kilometers'
    )
    
    pincode = CharField(
        string='Pincode',
        help='Pincode of the village'
    )
    
    # Kids Clothing Specific Fields
    age_group = SelectionField(
        selection=[
            ('0-2', 'Baby (0-2 years)'),
            ('2-4', 'Toddler (2-4 years)'),
            ('4-6', 'Pre-school (4-6 years)'),
            ('6-8', 'Early School (6-8 years)'),
            ('8-10', 'Middle School (8-10 years)'),
            ('10-12', 'Late School (10-12 years)'),
            ('12-14', 'Teen (12-14 years)'),
            ('14-16', 'Young Adult (14-16 years)'),
            ('all', 'All Age Groups'),
        ],
        string='Age Group',
        help='Primary age group for the village'
    )
    
    size = SelectionField(
        selection=[
            ('xs', 'XS'),
            ('s', 'S'),
            ('m', 'M'),
            ('l', 'L'),
            ('xl', 'XL'),
            ('xxl', 'XXL'),
            ('xxxl', 'XXXL'),
            ('all', 'All Sizes'),
        ],
        string='Size',
        help='Primary size for the village'
    )
    
    season = SelectionField(
        selection=[
            ('summer', 'Summer'),
            ('winter', 'Winter'),
            ('monsoon', 'Monsoon'),
            ('all_season', 'All Season'),
        ],
        string='Season',
        help='Primary season for the village'
    )
    
    brand = CharField(
        string='Brand',
        help='Primary brand for the village'
    )
    
    color = CharField(
        string='Color',
        help='Primary color for the village'
    )
    
    # Additional Information
    description = TextField(
        string='Description',
        help='Description of the village'
    )
    
    # Status
    active = BooleanField(
        string='Active',
        default=True,
        help='Whether the village is active'
    )
    
    def create(self, vals):
        """Override create to set default values"""
        if not vals.get('country_id'):
            vals['country_id'] = self.env.ref('base.in').id
        
        return super(ResCountryVillage, self).create(vals)
    
    def get_kids_clothing_villages(self, age_group=None, size=None, season=None, brand=None, color=None):
        """Get villages filtered by kids clothing criteria"""
        domain = [('active', '=', True)]
        
        if age_group:
            domain.append(('age_group', 'in', [age_group, 'all']))
        
        if size:
            domain.append(('size', 'in', [size, 'all']))
        
        if season:
            domain.append(('season', 'in', [season, 'all_season']))
        
        if brand:
            domain.append(('brand', '=', brand))
        
        if color:
            domain.append(('color', '=', color))
        
        return self.search(domain)