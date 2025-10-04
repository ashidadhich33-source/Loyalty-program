# -*- coding: utf-8 -*-
"""
Ocean ERP - Indian GST Chart Template Model
===========================================

GST chart template management for kids clothing retail.
"""

from core_framework.orm import BaseModel, CharField, TextField, BooleanField, IntegerField, DateTimeField, Many2OneField, SelectionField, FloatField, One2ManyField
from core_framework.exceptions import ValidationError, UserError
from addons.core_base.models.base_mixins import KidsClothingMixin
import logging

_logger = logging.getLogger(__name__)


class AccountChartTemplate(BaseModel, KidsClothingMixin):
    """Indian GST Chart Template Model for Ocean ERP"""
    
    _name = 'account.chart.template'
    _description = 'Account Chart Template'
    _order = 'sequence, name'
    _rec_name = 'name'

    name = CharField(
        string='Chart Template Name',
        required=True,
        help='Name of the chart template'
    )
    
    # GST Specific Fields
    chart_type = SelectionField(
        selection=[
            ('standard', 'Standard Chart'),
            ('gst_compliant', 'GST Compliant Chart'),
            ('composition', 'Composition Scheme Chart'),
            ('export', 'Export Chart'),
            ('import', 'Import Chart'),
        ],
        string='Chart Type',
        required=True,
        help='Type of chart template'
    )
    
    gst_compliance = BooleanField(
        string='GST Compliant',
        default=True,
        help='Whether this chart is GST compliant'
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
        help='Age group for this chart template'
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
        help='Size for this chart template'
    )
    
    season = SelectionField(
        selection=[
            ('summer', 'Summer'),
            ('winter', 'Winter'),
            ('monsoon', 'Monsoon'),
            ('all_season', 'All Season'),
        ],
        string='Season',
        help='Season for this chart template'
    )
    
    brand = CharField(
        string='Brand',
        help='Brand for this chart template'
    )
    
    color = CharField(
        string='Color',
        help='Color for this chart template'
    )
    
    # Chart Template Configuration
    sequence = IntegerField(
        string='Sequence',
        default=10,
        help='Sequence for ordering'
    )
    
    active = BooleanField(
        string='Active',
        default=True,
        help='Whether the chart template is active'
    )
    
    # Company
    company_id = Many2OneField(
        'res.company',
        string='Company',
        help='Company this chart template belongs to'
    )
    
    # Additional Information
    description = TextField(
        string='Description',
        help='Description of the chart template'
    )
    
    def create(self, vals):
        """Override create to set default values"""
        if not vals.get('company_id'):
            vals['company_id'] = self.env.context.get('default_company_id')
        
        return super(AccountChartTemplate, self).create(vals)
    
    def get_kids_clothing_chart_templates(self, age_group=None, size=None, season=None, brand=None, color=None):
        """Get chart templates filtered by kids clothing criteria"""
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