# -*- coding: utf-8 -*-
"""
Ocean ERP - Indian Partner Model
================================

Partner model with Indian localization for kids clothing retail.
"""

from core_framework.orm import BaseModel, CharField, TextField, BooleanField, IntegerField, DateTimeField, Many2OneField, SelectionField, FloatField
from core_framework.exceptions import ValidationError, UserError
from addons.core_base.models.base_mixins import KidsClothingMixin
import logging

_logger = logging.getLogger(__name__)


class ResPartner(BaseModel, KidsClothingMixin):
    """Indian Partner Model for Ocean ERP"""
    
    _name = 'res.partner'
    _description = 'Partner'
    _order = 'name'
    _rec_name = 'name'

    name = CharField(
        string='Name',
        required=True,
        help='Name of the partner'
    )
    
    # Partner Type
    is_company = BooleanField(
        string='Is Company',
        default=False,
        help='Whether this partner is a company'
    )
    
    partner_type = SelectionField(
        selection=[
            ('customer', 'Customer'),
            ('supplier', 'Supplier'),
            ('both', 'Customer & Supplier'),
            ('employee', 'Employee'),
            ('contact', 'Contact'),
        ],
        string='Partner Type',
        help='Type of partner'
    )
    
    # Indian Specific Fields
    pan = CharField(
        string='PAN',
        help='Permanent Account Number'
    )
    
    gstin = CharField(
        string='GSTIN',
        help='Goods and Services Tax Identification Number'
    )
    
    aadhar = CharField(
        string='Aadhar',
        help='Aadhar Number'
    )
    
    # Address Information
    street = CharField(
        string='Street',
        help='Street address'
    )
    
    street2 = CharField(
        string='Street 2',
        help='Additional street information'
    )
    
    city = CharField(
        string='City',
        help='City name'
    )
    
    state_id = Many2OneField(
        'res.country.state',
        string='State',
        help='State/Province'
    )
    
    district_id = Many2OneField(
        'res.country.district',
        string='District',
        help='District'
    )
    
    taluka_id = Many2OneField(
        'res.country.taluka',
        string='Taluka',
        help='Taluka/Tehsil'
    )
    
    village_id = Many2OneField(
        'res.country.village',
        string='Village',
        help='Village'
    )
    
    zip = CharField(
        string='ZIP',
        help='ZIP/Postal code'
    )
    
    country_id = Many2OneField(
        'res.country',
        string='Country',
        default=lambda self: self.env.ref('base.in'),
        help='Country'
    )
    
    # Contact Information
    phone = CharField(
        string='Phone',
        help='Phone number'
    )
    
    mobile = CharField(
        string='Mobile',
        help='Mobile number'
    )
    
    email = CharField(
        string='Email',
        help='Email address'
    )
    
    website = CharField(
        string='Website',
        help='Website URL'
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
        help='Primary age group for the partner'
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
        help='Primary size for the partner'
    )
    
    season = SelectionField(
        selection=[
            ('summer', 'Summer'),
            ('winter', 'Winter'),
            ('monsoon', 'Monsoon'),
            ('all_season', 'All Season'),
        ],
        string='Season',
        help='Primary season for the partner'
    )
    
    brand = CharField(
        string='Brand',
        help='Primary brand for the partner'
    )
    
    color = CharField(
        string='Color',
        help='Primary color for the partner'
    )
    
    # Business Information
    business_nature = SelectionField(
        selection=[
            ('manufacturing', 'Manufacturing'),
            ('trading', 'Trading'),
            ('service', 'Service'),
            ('retail', 'Retail'),
            ('wholesale', 'Wholesale'),
            ('ecommerce', 'E-commerce'),
            ('franchise', 'Franchise'),
        ],
        string='Nature of Business',
        help='Nature of business'
    )
    
    industry_type = SelectionField(
        selection=[
            ('textiles', 'Textiles'),
            ('garments', 'Garments'),
            ('kids_clothing', 'Kids Clothing'),
            ('fashion', 'Fashion'),
            ('retail', 'Retail'),
            ('wholesale', 'Wholesale'),
            ('ecommerce', 'E-commerce'),
            ('other', 'Other'),
        ],
        string='Industry Type',
        help='Type of industry'
    )
    
    # Credit Information
    credit_limit = FloatField(
        string='Credit Limit',
        help='Credit limit for this partner'
    )
    
    # Bank Information
    bank_ids = One2ManyField(
        'res.partner.bank',
        'partner_id',
        string='Bank Accounts',
        help='Bank accounts for this partner'
    )
    
    # Additional Information
    comment = TextField(
        string='Notes',
        help='Additional notes'
    )
    
    # Status
    active = BooleanField(
        string='Active',
        default=True,
        help='Whether the partner is active'
    )
    
    def create(self, vals):
        """Override create to set default values"""
        if not vals.get('country_id'):
            vals['country_id'] = self.env.ref('base.in').id
        
        return super(ResPartner, self).create(vals)
    
    def validate_pan(self, pan):
        """Validate PAN number format"""
        import re
        pan_pattern = r'^[A-Z]{5}[0-9]{4}[A-Z]{1}$'
        return re.match(pan_pattern, pan) is not None
    
    def validate_gstin(self, gstin):
        """Validate GSTIN format"""
        import re
        gstin_pattern = r'^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}[Z]{1}[0-9A-Z]{1}$'
        return re.match(gstin_pattern, gstin) is not None
    
    def validate_aadhar(self, aadhar):
        """Validate Aadhar number format"""
        import re
        aadhar_pattern = r'^[0-9]{12}$'
        return re.match(aadhar_pattern, aadhar) is not None
    
    def get_kids_clothing_partners(self, age_group=None, size=None, season=None, brand=None, color=None):
        """Get partners filtered by kids clothing criteria"""
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