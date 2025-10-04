# -*- coding: utf-8 -*-
"""
Ocean ERP - Indian HR Salary Structure Model
===========================================

HR salary structure management for kids clothing retail.
"""

from core_framework.orm import BaseModel, CharField, TextField, BooleanField, IntegerField, DateTimeField, Many2OneField, SelectionField, FloatField, One2ManyField
from core_framework.exceptions import ValidationError, UserError
from addons.core_base.models.base_mixins import KidsClothingMixin
import logging

_logger = logging.getLogger(__name__)


class HrPayrollStructure(BaseModel, KidsClothingMixin):
    """Indian HR Payroll Structure Model for Ocean ERP"""
    
    _name = 'hr.payroll.structure'
    _description = 'HR Payroll Structure'
    _order = 'sequence, name'
    _rec_name = 'name'

    name = CharField(
        string='Structure Name',
        required=True,
        help='Name of the payroll structure'
    )
    
    # Structure Information
    code = CharField(
        string='Code',
        required=True,
        help='Code of the payroll structure'
    )
    
    sequence = IntegerField(
        string='Sequence',
        default=10,
        help='Sequence for ordering'
    )
    
    # Structure Configuration
    struct_type = SelectionField(
        selection=[
            ('regular', 'Regular'),
            ('contract', 'Contract'),
            ('intern', 'Intern'),
            ('consultant', 'Consultant'),
            ('other', 'Other'),
        ],
        string='Structure Type',
        required=True,
        help='Type of payroll structure'
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
        help='Age group for this structure'
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
        help='Size for this structure'
    )
    
    season = SelectionField(
        selection=[
            ('summer', 'Summer'),
            ('winter', 'Winter'),
            ('monsoon', 'Monsoon'),
            ('all_season', 'All Season'),
        ],
        string='Season',
        help='Season for this structure'
    )
    
    brand = CharField(
        string='Brand',
        help='Brand for this structure'
    )
    
    color = CharField(
        string='Color',
        help='Color for this structure'
    )
    
    # Structure Status
    active = BooleanField(
        string='Active',
        default=True,
        help='Whether the structure is active'
    )
    
    # Company
    company_id = Many2OneField(
        'res.company',
        string='Company',
        help='Company this structure belongs to'
    )
    
    # Salary Rules
    rule_ids = One2ManyField(
        'hr.salary.rule',
        'struct_id',
        string='Salary Rules',
        help='Salary rules in this structure'
    )
    
    # Additional Information
    description = TextField(
        string='Description',
        help='Description of the structure'
    )
    
    def create(self, vals):
        """Override create to set default values"""
        if not vals.get('company_id'):
            vals['company_id'] = self.env.context.get('default_company_id')
        
        return super(HrPayrollStructure, self).create(vals)
    
    def get_kids_clothing_structures(self, age_group=None, size=None, season=None, brand=None, color=None):
        """Get structures filtered by kids clothing criteria"""
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