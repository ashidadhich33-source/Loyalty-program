# -*- coding: utf-8 -*-
"""
Ocean ERP - Indian HR Payslip Line Model
========================================

HR payslip line management for kids clothing retail.
"""

from core_framework.orm import BaseModel, CharField, TextField, BooleanField, IntegerField, DateTimeField, Many2OneField, SelectionField, FloatField, One2ManyField
from core_framework.exceptions import ValidationError, UserError
from addons.core_base.models.base_mixins import KidsClothingMixin
import logging

_logger = logging.getLogger(__name__)


class HrPayslipLine(BaseModel, KidsClothingMixin):
    """Indian HR Payslip Line Model for Ocean ERP"""
    
    _name = 'hr.payslip.line'
    _description = 'HR Payslip Line'
    _order = 'sequence, id'

    payslip_id = Many2OneField(
        'hr.payslip',
        string='Payslip',
        required=True,
        help='Payslip this line belongs to'
    )
    
    # Line Information
    name = CharField(
        string='Name',
        required=True,
        help='Name of the payslip line'
    )
    
    code = CharField(
        string='Code',
        required=True,
        help='Code of the payslip line'
    )
    
    category_id = Many2OneField(
        'hr.salary.rule.category',
        string='Category',
        help='Category of the payslip line'
    )
    
    sequence = IntegerField(
        string='Sequence',
        default=10,
        help='Sequence for ordering'
    )
    
    # Amount Information
    amount = FloatField(
        string='Amount',
        help='Amount of the payslip line'
    )
    
    quantity = FloatField(
        string='Quantity',
        default=1.0,
        help='Quantity for calculation'
    )
    
    rate = FloatField(
        string='Rate',
        help='Rate for calculation'
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
        help='Age group for this payslip line'
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
        help='Size for this payslip line'
    )
    
    season = SelectionField(
        selection=[
            ('summer', 'Summer'),
            ('winter', 'Winter'),
            ('monsoon', 'Monsoon'),
            ('all_season', 'All Season'),
        ],
        string='Season',
        help='Season for this payslip line'
    )
    
    brand = CharField(
        string='Brand',
        help='Brand for this payslip line'
    )
    
    color = CharField(
        string='Color',
        help='Color for this payslip line'
    )
    
    # Company
    company_id = Many2OneField(
        'res.company',
        string='Company',
        help='Company this payslip line belongs to'
    )
    
    def create(self, vals):
        """Override create to set default values"""
        if not vals.get('company_id'):
            vals['company_id'] = self.env.context.get('default_company_id')
        
        return super(HrPayslipLine, self).create(vals)
    
    def get_kids_clothing_payslip_lines(self, age_group=None, size=None, season=None, brand=None, color=None):
        """Get payslip lines filtered by kids clothing criteria"""
        domain = []
        
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