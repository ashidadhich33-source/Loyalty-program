# -*- coding: utf-8 -*-
"""
Ocean ERP - Indian Bank Model
=============================

Bank model with Indian localization for kids clothing retail.
"""

from core_framework.orm import BaseModel, CharField, TextField, BooleanField, IntegerField, DateTimeField, Many2OneField, SelectionField, FloatField, One2ManyField
from core_framework.exceptions import ValidationError, UserError
from addons.core_base.models.base_mixins import KidsClothingMixin
import logging

_logger = logging.getLogger(__name__)


class ResBank(BaseModel, KidsClothingMixin):
    """Indian Bank Model for Ocean ERP"""
    
    _name = 'res.bank'
    _description = 'Bank'
    _order = 'name'
    _rec_name = 'name'

    name = CharField(
        string='Bank Name',
        required=True,
        help='Name of the bank'
    )
    
    code = CharField(
        string='Bank Code',
        required=True,
        help='Code of the bank'
    )
    
    # Indian Specific Fields
    bank_type = SelectionField(
        selection=[
            ('public', 'Public Sector Bank'),
            ('private', 'Private Sector Bank'),
            ('foreign', 'Foreign Bank'),
            ('cooperative', 'Cooperative Bank'),
            ('payment', 'Payment Bank'),
            ('small_finance', 'Small Finance Bank'),
        ],
        string='Bank Type',
        help='Type of bank'
    )
    
    ifsc_code = CharField(
        string='IFSC Code',
        help='Indian Financial System Code'
    )
    
    micr_code = CharField(
        string='MICR Code',
        help='Magnetic Ink Character Recognition Code'
    )
    
    swift_code = CharField(
        string='SWIFT Code',
        help='Society for Worldwide Interbank Financial Telecommunication Code'
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
        help='Primary age group for the bank'
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
        help='Primary size for the bank'
    )
    
    season = SelectionField(
        selection=[
            ('summer', 'Summer'),
            ('winter', 'Winter'),
            ('monsoon', 'Monsoon'),
            ('all_season', 'All Season'),
        ],
        string='Season',
        help='Primary season for the bank'
    )
    
    brand = CharField(
        string='Brand',
        help='Primary brand for the bank'
    )
    
    color = CharField(
        string='Color',
        help='Primary color for the bank'
    )
    
    # Bank Branches
    branch_ids = One2ManyField(
        'res.bank.branch',
        'bank_id',
        string='Branches',
        help='Branches of this bank'
    )
    
    # Additional Information
    description = TextField(
        string='Description',
        help='Description of the bank'
    )
    
    # Status
    active = BooleanField(
        string='Active',
        default=True,
        help='Whether the bank is active'
    )
    
    def create(self, vals):
        """Override create to set default values"""
        if not vals.get('country_id'):
            vals['country_id'] = self.env.ref('base.in').id
        
        return super(ResBank, self).create(vals)
    
    def validate_ifsc(self, ifsc):
        """Validate IFSC code format"""
        import re
        ifsc_pattern = r'^[A-Z]{4}0[A-Z0-9]{6}$'
        return re.match(ifsc_pattern, ifsc) is not None
    
    def validate_micr(self, micr):
        """Validate MICR code format"""
        import re
        micr_pattern = r'^[0-9]{9}$'
        return re.match(micr_pattern, micr) is not None
    
    def get_kids_clothing_banks(self, age_group=None, size=None, season=None, brand=None, color=None):
        """Get banks filtered by kids clothing criteria"""
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