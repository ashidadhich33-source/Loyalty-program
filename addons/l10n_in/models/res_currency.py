# -*- coding: utf-8 -*-
"""
Ocean ERP - Indian Currency Model
=================================

Currency model with Indian localization for kids clothing retail.
"""

from core_framework.orm import BaseModel, CharField, TextField, BooleanField, IntegerField, DateTimeField, Many2OneField, SelectionField, FloatField
from core_framework.exceptions import ValidationError, UserError
from addons.core_base.models.base_mixins import KidsClothingMixin
import logging

_logger = logging.getLogger(__name__)


class ResCurrency(BaseModel, KidsClothingMixin):
    """Indian Currency Model for Ocean ERP"""
    
    _name = 'res.currency'
    _description = 'Currency'
    _order = 'name'
    _rec_name = 'name'

    name = CharField(
        string='Currency Name',
        required=True,
        help='Name of the currency'
    )
    
    symbol = CharField(
        string='Symbol',
        required=True,
        help='Symbol of the currency'
    )
    
    code = CharField(
        string='Code',
        required=True,
        help='Code of the currency'
    )
    
    # Indian Specific Fields
    currency_type = SelectionField(
        selection=[
            ('fiat', 'Fiat Currency'),
            ('digital', 'Digital Currency'),
            ('commodity', 'Commodity Currency'),
        ],
        string='Currency Type',
        help='Type of currency'
    )
    
    decimal_places = IntegerField(
        string='Decimal Places',
        default=2,
        help='Number of decimal places'
    )
    
    rounding = FloatField(
        string='Rounding Factor',
        default=0.01,
        help='Rounding factor for currency'
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
        help='Primary age group for the currency'
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
        help='Primary size for the currency'
    )
    
    season = SelectionField(
        selection=[
            ('summer', 'Summer'),
            ('winter', 'Winter'),
            ('monsoon', 'Monsoon'),
            ('all_season', 'All Season'),
        ],
        string='Season',
        help='Primary season for the currency'
    )
    
    brand = CharField(
        string='Brand',
        help='Primary brand for the currency'
    )
    
    color = CharField(
        string='Color',
        help='Primary color for the currency'
    )
    
    # Additional Information
    description = TextField(
        string='Description',
        help='Description of the currency'
    )
    
    # Status
    active = BooleanField(
        string='Active',
        default=True,
        help='Whether the currency is active'
    )
    
    def create(self, vals):
        """Override create to set default values"""
        return super(ResCurrency, self).create(vals)
    
    def get_kids_clothing_currencies(self, age_group=None, size=None, season=None, brand=None, color=None):
        """Get currencies filtered by kids clothing criteria"""
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