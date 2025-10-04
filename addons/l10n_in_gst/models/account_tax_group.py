# -*- coding: utf-8 -*-
"""
Ocean ERP - Indian GST Tax Group Model
======================================

GST tax group management for kids clothing retail.
"""

from core_framework.orm import BaseModel, CharField, TextField, BooleanField, IntegerField, DateTimeField, Many2OneField, SelectionField, FloatField, One2ManyField
from core_framework.exceptions import ValidationError, UserError
from addons.core_base.models.base_mixins import KidsClothingMixin
import logging

_logger = logging.getLogger(__name__)


class AccountTaxGroup(BaseModel, KidsClothingMixin):
    """Indian GST Tax Group Model for Ocean ERP"""
    
    _name = 'account.tax.group'
    _description = 'Account Tax Group'
    _order = 'sequence, name'
    _rec_name = 'name'

    name = CharField(
        string='Tax Group Name',
        required=True,
        help='Name of the tax group'
    )
    
    # GST Specific Fields
    gst_group_type = SelectionField(
        selection=[
            ('gst_0', 'GST 0%'),
            ('gst_5', 'GST 5%'),
            ('gst_12', 'GST 12%'),
            ('gst_18', 'GST 18%'),
            ('gst_28', 'GST 28%'),
            ('exempt', 'Exempt'),
            ('nil_rated', 'Nil Rated'),
            ('non_gst', 'Non-GST'),
        ],
        string='GST Group Type',
        help='GST group type'
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
        help='Age group for this tax group'
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
        help='Size for this tax group'
    )
    
    season = SelectionField(
        selection=[
            ('summer', 'Summer'),
            ('winter', 'Winter'),
            ('monsoon', 'Monsoon'),
            ('all_season', 'All Season'),
        ],
        string='Season',
        help='Season for this tax group'
    )
    
    brand = CharField(
        string='Brand',
        help='Brand for this tax group'
    )
    
    color = CharField(
        string='Color',
        help='Color for this tax group'
    )
    
    # Tax Group Configuration
    sequence = IntegerField(
        string='Sequence',
        default=10,
        help='Sequence for ordering'
    )
    
    active = BooleanField(
        string='Active',
        default=True,
        help='Whether the tax group is active'
    )
    
    # Company
    company_id = Many2OneField(
        'res.company',
        string='Company',
        help='Company this tax group belongs to'
    )
    
    # Additional Information
    description = TextField(
        string='Description',
        help='Description of the tax group'
    )
    
    def create(self, vals):
        """Override create to set default values"""
        if not vals.get('company_id'):
            vals['company_id'] = self.env.context.get('default_company_id')
        
        return super(AccountTaxGroup, self).create(vals)
    
    def get_kids_clothing_tax_groups(self, age_group=None, size=None, season=None, brand=None, color=None):
        """Get tax groups filtered by kids clothing criteria"""
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