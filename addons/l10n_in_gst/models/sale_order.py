# -*- coding: utf-8 -*-
"""
Ocean ERP - Indian GST Sale Order Model
=======================================

GST sale order management for kids clothing retail.
"""

from core_framework.orm import BaseModel, CharField, TextField, BooleanField, IntegerField, DateTimeField, Many2OneField, SelectionField, FloatField, One2ManyField
from core_framework.exceptions import ValidationError, UserError
from addons.core_base.models.base_mixins import KidsClothingMixin
import logging

_logger = logging.getLogger(__name__)


class SaleOrder(BaseModel, KidsClothingMixin):
    """Indian GST Sale Order Model for Ocean ERP"""
    
    _name = 'sale.order'
    _description = 'Sale Order'
    _order = 'date_order desc, name'
    _rec_name = 'name'

    name = CharField(
        string='Order Reference',
        required=True,
        help='Order reference number'
    )
    
    # GST Specific Fields
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
        help='GST treatment for this order'
    )
    
    fiscal_position_id = Many2OneField(
        'account.fiscal.position',
        string='Fiscal Position',
        help='Fiscal position for this order'
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
        help='Age group for this order'
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
        help='Size for this order'
    )
    
    season = SelectionField(
        selection=[
            ('summer', 'Summer'),
            ('winter', 'Winter'),
            ('monsoon', 'Monsoon'),
            ('all_season', 'All Season'),
        ],
        string='Season',
        help='Season for this order'
    )
    
    brand = CharField(
        string='Brand',
        help='Brand for this order'
    )
    
    color = CharField(
        string='Color',
        help='Color for this order'
    )
    
    # Order Configuration
    date_order = DateTimeField(
        string='Order Date',
        required=True,
        help='Date of the order'
    )
    
    state = SelectionField(
        selection=[
            ('draft', 'Draft'),
            ('sent', 'Sent'),
            ('sale', 'Sale Order'),
            ('done', 'Done'),
            ('cancel', 'Cancelled'),
        ],
        string='Status',
        default='draft',
        help='Status of the order'
    )
    
    # Company
    company_id = Many2OneField(
        'res.company',
        string='Company',
        help='Company this order belongs to'
    )
    
    # Additional Information
    notes = TextField(
        string='Notes',
        help='Additional notes for the order'
    )
    
    def create(self, vals):
        """Override create to set default values"""
        if not vals.get('company_id'):
            vals['company_id'] = self.env.context.get('default_company_id')
        
        return super(SaleOrder, self).create(vals)
    
    def get_kids_clothing_orders(self, age_group=None, size=None, season=None, brand=None, color=None):
        """Get orders filtered by kids clothing criteria"""
        domain = [('state', '=', 'sale')]
        
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