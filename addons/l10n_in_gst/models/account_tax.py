# -*- coding: utf-8 -*-
"""
Ocean ERP - Indian GST Tax Model
================================

GST tax management for kids clothing retail.
"""

from core_framework.orm import BaseModel, CharField, TextField, BooleanField, IntegerField, DateTimeField, Many2OneField, SelectionField, FloatField
from core_framework.exceptions import ValidationError, UserError
from addons.core_base.models.base_mixins import KidsClothingMixin
import logging

_logger = logging.getLogger(__name__)


class AccountTax(BaseModel, KidsClothingMixin):
    """Indian GST Tax Model for Ocean ERP"""
    
    _name = 'account.tax'
    _description = 'Account Tax'
    _order = 'sequence, name'
    _rec_name = 'name'

    name = CharField(
        string='Tax Name',
        required=True,
        help='Name of the tax'
    )
    
    # GST Specific Fields
    tax_type = SelectionField(
        selection=[
            ('gst', 'GST'),
            ('cgst', 'CGST'),
            ('sgst', 'SGST'),
            ('igst', 'IGST'),
            ('cess', 'CESS'),
            ('other', 'Other'),
        ],
        string='Tax Type',
        required=True,
        help='Type of tax'
    )
    
    gst_type = SelectionField(
        selection=[
            ('cgst', 'CGST'),
            ('sgst', 'SGST'),
            ('igst', 'IGST'),
            ('cess', 'CESS'),
        ],
        string='GST Type',
        help='GST tax type'
    )
    
    amount = FloatField(
        string='Amount',
        required=True,
        help='Tax amount'
    )
    
    amount_type = SelectionField(
        selection=[
            ('percent', 'Percentage'),
            ('fixed', 'Fixed Amount'),
        ],
        string='Amount Type',
        required=True,
        help='Type of tax amount'
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
        help='Age group for this tax'
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
        help='Size for this tax'
    )
    
    season = SelectionField(
        selection=[
            ('summer', 'Summer'),
            ('winter', 'Winter'),
            ('monsoon', 'Monsoon'),
            ('all_season', 'All Season'),
        ],
        string='Season',
        help='Season for this tax'
    )
    
    brand = CharField(
        string='Brand',
        help='Brand for this tax'
    )
    
    color = CharField(
        string='Color',
        help='Color for this tax'
    )
    
    # Tax Configuration
    sequence = IntegerField(
        string='Sequence',
        default=10,
        help='Sequence for ordering'
    )
    
    active = BooleanField(
        string='Active',
        default=True,
        help='Whether the tax is active'
    )
    
    # GST Specific Configuration
    gst_rate = FloatField(
        string='GST Rate (%)',
        help='GST rate percentage'
    )
    
    hsn_code = CharField(
        string='HSN Code',
        help='Harmonized System of Nomenclature code'
    )
    
    sac_code = CharField(
        string='SAC Code',
        help='Service Accounting Code'
    )
    
    # Tax Group
    tax_group_id = Many2OneField(
        'account.tax.group',
        string='Tax Group',
        help='Tax group this tax belongs to'
    )
    
    # Company
    company_id = Many2OneField(
        'res.company',
        string='Company',
        help='Company this tax belongs to'
    )
    
    # Additional Information
    description = TextField(
        string='Description',
        help='Description of the tax'
    )
    
    def create(self, vals):
        """Override create to set default values"""
        if not vals.get('company_id'):
            vals['company_id'] = self.env.context.get('default_company_id')
        
        return super(AccountTax, self).create(vals)
    
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
    
    def get_kids_clothing_taxes(self, age_group=None, size=None, season=None, brand=None, color=None):
        """Get taxes filtered by kids clothing criteria"""
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
    
    def compute_gst_amount(self, base_amount):
        """Compute GST amount from base amount"""
        if self.amount_type == 'percent':
            return base_amount * (self.amount / 100)
        else:
            return self.amount
    
    def get_gst_breakdown(self, base_amount):
        """Get GST breakdown for the given amount"""
        total_tax = self.compute_gst_amount(base_amount)
        
        if self.gst_type == 'igst':
            return {
                'igst': total_tax,
                'cgst': 0,
                'sgst': 0,
                'cess': 0,
                'total': total_tax
            }
        elif self.gst_type == 'cgst':
            return {
                'igst': 0,
                'cgst': total_tax,
                'sgst': total_tax,
                'cess': 0,
                'total': total_tax * 2
            }
        elif self.gst_type == 'sgst':
            return {
                'igst': 0,
                'cgst': total_tax,
                'sgst': total_tax,
                'cess': 0,
                'total': total_tax * 2
            }
        elif self.gst_type == 'cess':
            return {
                'igst': 0,
                'cgst': 0,
                'sgst': 0,
                'cess': total_tax,
                'total': total_tax
            }
        else:
            return {
                'igst': 0,
                'cgst': 0,
                'sgst': 0,
                'cess': 0,
                'total': total_tax
            }


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