# -*- coding: utf-8 -*-
"""
Ocean ERP - Indian GST Fiscal Position Model
=============================================

GST fiscal position management for kids clothing retail.
"""

from core_framework.orm import BaseModel, CharField, TextField, BooleanField, IntegerField, DateTimeField, Many2OneField, SelectionField, FloatField, One2ManyField
from core_framework.exceptions import ValidationError, UserError
from addons.core_base.models.base_mixins import KidsClothingMixin
import logging

_logger = logging.getLogger(__name__)


class AccountFiscalPosition(BaseModel, KidsClothingMixin):
    """Indian GST Fiscal Position Model for Ocean ERP"""
    
    _name = 'account.fiscal.position'
    _description = 'Account Fiscal Position'
    _order = 'sequence, name'
    _rec_name = 'name'

    name = CharField(
        string='Fiscal Position Name',
        required=True,
        help='Name of the fiscal position'
    )
    
    # GST Specific Fields
    fiscal_position_type = SelectionField(
        selection=[
            ('inter_state', 'Inter State'),
            ('intra_state', 'Intra State'),
            ('export', 'Export'),
            ('import', 'Import'),
            ('sez', 'SEZ'),
            ('deemed_export', 'Deemed Export'),
        ],
        string='Fiscal Position Type',
        required=True,
        help='Type of fiscal position'
    )
    
    gst_treatment = SelectionField(
        selection=[
            ('regular', 'Regular'),
            ('composition', 'Composition'),
            ('unregistered', 'Unregistered'),
            ('consumer', 'Consumer'),
            ('overseas', 'Overseas'),
            ('special_economic_zone', 'Special Economic Zone'),
            ('deemed_export', 'Deemed Export'),
        ],
        string='GST Treatment',
        help='GST treatment for this fiscal position'
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
        help='Age group for this fiscal position'
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
        help='Size for this fiscal position'
    )
    
    season = SelectionField(
        selection=[
            ('summer', 'Summer'),
            ('winter', 'Winter'),
            ('monsoon', 'Monsoon'),
            ('all_season', 'All Season'),
        ],
        string='Season',
        help='Season for this fiscal position'
    )
    
    brand = CharField(
        string='Brand',
        help='Brand for this fiscal position'
    )
    
    color = CharField(
        string='Color',
        help='Color for this fiscal position'
    )
    
    # Fiscal Position Configuration
    sequence = IntegerField(
        string='Sequence',
        default=10,
        help='Sequence for ordering'
    )
    
    active = BooleanField(
        string='Active',
        default=True,
        help='Whether the fiscal position is active'
    )
    
    # Tax Mappings
    tax_ids = One2ManyField(
        'account.fiscal.position.tax',
        'fiscal_position_id',
        string='Tax Mappings',
        help='Tax mappings for this fiscal position'
    )
    
    # Company
    company_id = Many2OneField(
        'res.company',
        string='Company',
        help='Company this fiscal position belongs to'
    )
    
    # Additional Information
    description = TextField(
        string='Description',
        help='Description of the fiscal position'
    )
    
    def create(self, vals):
        """Override create to set default values"""
        if not vals.get('company_id'):
            vals['company_id'] = self.env.context.get('default_company_id')
        
        return super(AccountFiscalPosition, self).create(vals)
    
    def get_kids_clothing_fiscal_positions(self, age_group=None, size=None, season=None, brand=None, color=None):
        """Get fiscal positions filtered by kids clothing criteria"""
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
    
    def get_gst_tax_mapping(self, tax_id):
        """Get GST tax mapping for the given tax"""
        tax_mapping = self.tax_ids.filtered(lambda t: t.tax_src_id.id == tax_id)
        if tax_mapping:
            return tax_mapping[0].tax_dest_id
        return tax_id


class AccountFiscalPositionTax(BaseModel, KidsClothingMixin):
    """Indian GST Fiscal Position Tax Model for Ocean ERP"""
    
    _name = 'account.fiscal.position.tax'
    _description = 'Account Fiscal Position Tax'
    _order = 'sequence, id'

    fiscal_position_id = Many2OneField(
        'account.fiscal.position',
        string='Fiscal Position',
        required=True,
        help='Fiscal position this tax mapping belongs to'
    )
    
    tax_src_id = Many2OneField(
        'account.tax',
        string='Source Tax',
        required=True,
        help='Source tax'
    )
    
    tax_dest_id = Many2OneField(
        'account.tax',
        string='Destination Tax',
        help='Destination tax'
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
        help='Age group for this tax mapping'
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
        help='Size for this tax mapping'
    )
    
    season = SelectionField(
        selection=[
            ('summer', 'Summer'),
            ('winter', 'Winter'),
            ('monsoon', 'Monsoon'),
            ('all_season', 'All Season'),
        ],
        string='Season',
        help='Season for this tax mapping'
    )
    
    brand = CharField(
        string='Brand',
        help='Brand for this tax mapping'
    )
    
    color = CharField(
        string='Color',
        help='Color for this tax mapping'
    )
    
    # Tax Mapping Configuration
    sequence = IntegerField(
        string='Sequence',
        default=10,
        help='Sequence for ordering'
    )
    
    active = BooleanField(
        string='Active',
        default=True,
        help='Whether the tax mapping is active'
    )
    
    # Company
    company_id = Many2OneField(
        'res.company',
        string='Company',
        help='Company this tax mapping belongs to'
    )
    
    def create(self, vals):
        """Override create to set default values"""
        if not vals.get('company_id'):
            vals['company_id'] = self.env.context.get('default_company_id')
        
        return super(AccountFiscalPositionTax, self).create(vals)
    
    def get_kids_clothing_tax_mappings(self, age_group=None, size=None, season=None, brand=None, color=None):
        """Get tax mappings filtered by kids clothing criteria"""
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