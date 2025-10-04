# -*- coding: utf-8 -*-
"""
Ocean ERP - Indian GST Product Template Model
=============================================

GST product template management for kids clothing retail.
"""

from core_framework.orm import BaseModel, CharField, TextField, BooleanField, IntegerField, DateTimeField, Many2OneField, SelectionField, FloatField, One2ManyField
from core_framework.exceptions import ValidationError, UserError
from addons.core_base.models.base_mixins import KidsClothingMixin
import logging

_logger = logging.getLogger(__name__)


class ProductTemplate(BaseModel, KidsClothingMixin):
    """Indian GST Product Template Model for Ocean ERP"""
    
    _name = 'product.template'
    _description = 'Product Template'
    _order = 'sequence, name'
    _rec_name = 'name'

    name = CharField(
        string='Product Name',
        required=True,
        help='Name of the product'
    )
    
    # GST Specific Fields
    hsn_code = CharField(
        string='HSN Code',
        help='Harmonized System of Nomenclature code'
    )
    
    sac_code = CharField(
        string='SAC Code',
        help='Service Accounting Code'
    )
    
    gst_tax_group_id = Many2OneField(
        'account.tax.group',
        string='GST Tax Group',
        help='GST tax group for this product'
    )
    
    gst_rate = FloatField(
        string='GST Rate (%)',
        help='GST rate percentage'
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
        help='Age group for this product'
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
        help='Size for this product'
    )
    
    season = SelectionField(
        selection=[
            ('summer', 'Summer'),
            ('winter', 'Winter'),
            ('monsoon', 'Monsoon'),
            ('all_season', 'All Season'),
        ],
        string='Season',
        help='Season for this product'
    )
    
    brand = CharField(
        string='Brand',
        help='Brand for this product'
    )
    
    color = CharField(
        string='Color',
        help='Color for this product'
    )
    
    # Product Configuration
    sequence = IntegerField(
        string='Sequence',
        default=10,
        help='Sequence for ordering'
    )
    
    active = BooleanField(
        string='Active',
        default=True,
        help='Whether the product is active'
    )
    
    # Company
    company_id = Many2OneField(
        'res.company',
        string='Company',
        help='Company this product belongs to'
    )
    
    # Additional Information
    description = TextField(
        string='Description',
        help='Description of the product'
    )
    
    def create(self, vals):
        """Override create to set default values"""
        if not vals.get('company_id'):
            vals['company_id'] = self.env.context.get('default_company_id')
        
        return super(ProductTemplate, self).create(vals)
    
    def validate_hsn_code(self, hsn_code):
        """Validate HSN code format"""
        import re
        hsn_pattern = r'^[0-9]{4,8}$'
        return re.match(hsn_pattern, hsn_code) is not None
    
    def validate_sac_code(self, sac_code):
        """Validate SAC code format"""
        import re
        sac_pattern = r'^[0-9]{6}$'
        return re.match(sac_pattern, sac_code) is not None
    
    def get_kids_clothing_products(self, age_group=None, size=None, season=None, brand=None, color=None):
        """Get products filtered by kids clothing criteria"""
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