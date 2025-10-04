# -*- coding: utf-8 -*-
"""
Ocean ERP - Indian GST Account Invoice Model
===========================================

GST account invoice management for kids clothing retail.
"""

from core_framework.orm import BaseModel, CharField, TextField, BooleanField, IntegerField, DateTimeField, Many2OneField, SelectionField, FloatField, One2ManyField
from core_framework.exceptions import ValidationError, UserError
from addons.core_base.models.base_mixins import KidsClothingMixin
import logging

_logger = logging.getLogger(__name__)


class AccountInvoice(BaseModel, KidsClothingMixin):
    """Indian GST Account Invoice Model for Ocean ERP"""
    
    _name = 'account.invoice'
    _description = 'Account Invoice'
    _order = 'date_invoice desc, name'
    _rec_name = 'name'

    name = CharField(
        string='Invoice Number',
        required=True,
        help='Invoice number'
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
        help='GST treatment for this invoice'
    )
    
    fiscal_position_id = Many2OneField(
        'account.fiscal.position',
        string='Fiscal Position',
        help='Fiscal position for this invoice'
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
        help='Age group for this invoice'
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
        help='Size for this invoice'
    )
    
    season = SelectionField(
        selection=[
            ('summer', 'Summer'),
            ('winter', 'Winter'),
            ('monsoon', 'Monsoon'),
            ('all_season', 'All Season'),
        ],
        string='Season',
        help='Season for this invoice'
    )
    
    brand = CharField(
        string='Brand',
        help='Brand for this invoice'
    )
    
    color = CharField(
        string='Color',
        help='Color for this invoice'
    )
    
    # Invoice Configuration
    date_invoice = DateTimeField(
        string='Invoice Date',
        required=True,
        help='Date of the invoice'
    )
    
    state = SelectionField(
        selection=[
            ('draft', 'Draft'),
            ('open', 'Open'),
            ('paid', 'Paid'),
            ('cancelled', 'Cancelled'),
        ],
        string='Status',
        default='draft',
        help='Status of the invoice'
    )
    
    # Company
    company_id = Many2OneField(
        'res.company',
        string='Company',
        help='Company this invoice belongs to'
    )
    
    # Additional Information
    notes = TextField(
        string='Notes',
        help='Additional notes for the invoice'
    )
    
    def create(self, vals):
        """Override create to set default values"""
        if not vals.get('company_id'):
            vals['company_id'] = self.env.context.get('default_company_id')
        
        return super(AccountInvoice, self).create(vals)
    
    def get_kids_clothing_invoices(self, age_group=None, size=None, season=None, brand=None, color=None):
        """Get invoices filtered by kids clothing criteria"""
        domain = [('state', '=', 'open')]
        
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