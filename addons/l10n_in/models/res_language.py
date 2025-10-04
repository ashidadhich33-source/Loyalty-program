# -*- coding: utf-8 -*-
"""
Ocean ERP - Indian Language Model
=================================

Language model with Indian localization for kids clothing retail.
"""

from core_framework.orm import BaseModel, CharField, TextField, BooleanField, IntegerField, DateTimeField, Many2OneField, SelectionField, FloatField
from core_framework.exceptions import ValidationError, UserError
from addons.core_base.models.base_mixins import KidsClothingMixin
import logging

_logger = logging.getLogger(__name__)


class ResLanguage(BaseModel, KidsClothingMixin):
    """Indian Language Model for Ocean ERP"""
    
    _name = 'res.language'
    _description = 'Language'
    _order = 'name'
    _rec_name = 'name'

    name = CharField(
        string='Language Name',
        required=True,
        help='Name of the language'
    )
    
    code = CharField(
        string='Language Code',
        required=True,
        help='Code of the language'
    )
    
    # Indian Specific Fields
    language_type = SelectionField(
        selection=[
            ('official', 'Official Language'),
            ('regional', 'Regional Language'),
            ('local', 'Local Language'),
            ('foreign', 'Foreign Language'),
        ],
        string='Language Type',
        help='Type of language'
    )
    
    script = CharField(
        string='Script',
        help='Script used for the language'
    )
    
    direction = SelectionField(
        selection=[
            ('ltr', 'Left to Right'),
            ('rtl', 'Right to Left'),
        ],
        string='Direction',
        default='ltr',
        help='Text direction'
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
        help='Primary age group for the language'
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
        help='Primary size for the language'
    )
    
    season = SelectionField(
        selection=[
            ('summer', 'Summer'),
            ('winter', 'Winter'),
            ('monsoon', 'Monsoon'),
            ('all_season', 'All Season'),
        ],
        string='Season',
        help='Primary season for the language'
    )
    
    brand = CharField(
        string='Brand',
        help='Primary brand for the language'
    )
    
    color = CharField(
        string='Color',
        help='Primary color for the language'
    )
    
    # Additional Information
    description = TextField(
        string='Description',
        help='Description of the language'
    )
    
    # Status
    active = BooleanField(
        string='Active',
        default=True,
        help='Whether the language is active'
    )
    
    def create(self, vals):
        """Override create to set default values"""
        return super(ResLanguage, self).create(vals)
    
    def get_kids_clothing_languages(self, age_group=None, size=None, season=None, brand=None, color=None):
        """Get languages filtered by kids clothing criteria"""
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