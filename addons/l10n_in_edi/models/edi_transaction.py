# -*- coding: utf-8 -*-
"""
Ocean ERP - Indian EDI Transaction Model
=========================================

EDI transaction management for kids clothing retail.
"""

from core_framework.orm import BaseModel, CharField, TextField, BooleanField, IntegerField, DateTimeField, Many2OneField, SelectionField, FloatField, One2ManyField
from core_framework.exceptions import ValidationError, UserError
from addons.core_base.models.base_mixins import KidsClothingMixin
import logging

_logger = logging.getLogger(__name__)


class EdiTransaction(BaseModel, KidsClothingMixin):
    """Indian EDI Transaction Model for Ocean ERP"""
    
    _name = 'edi.transaction'
    _description = 'EDI Transaction'
    _order = 'sequence, name'
    _rec_name = 'name'

    name = CharField(
        string='Transaction Name',
        required=True,
        help='Name of the EDI transaction'
    )
    
    document_id = Many2OneField(
        'edi.document',
        string='Document',
        required=True,
        help='EDI document this transaction belongs to'
    )
    
    # EDI Specific Fields
    transaction_type = SelectionField(
        selection=[
            ('line_item', 'Line Item'),
            ('header', 'Header'),
            ('footer', 'Footer'),
            ('summary', 'Summary'),
            ('detail', 'Detail'),
            ('other', 'Other'),
        ],
        string='Transaction Type',
        required=True,
        help='Type of EDI transaction'
    )
    
    segment_type = CharField(
        string='Segment Type',
        help='EDI segment type'
    )
    
    segment_data = TextField(
        string='Segment Data',
        help='Raw segment data'
    )
    
    processed_data = TextField(
        string='Processed Data',
        help='Processed segment data'
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
        help='Age group for this transaction'
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
        help='Size for this transaction'
    )
    
    season = SelectionField(
        selection=[
            ('summer', 'Summer'),
            ('winter', 'Winter'),
            ('monsoon', 'Monsoon'),
            ('all_season', 'All Season'),
        ],
        string='Season',
        help='Season for this transaction'
    )
    
    brand = CharField(
        string='Brand',
        help='Brand for this transaction'
    )
    
    color = CharField(
        string='Color',
        help='Color for this transaction'
    )
    
    # Transaction Configuration
    sequence = IntegerField(
        string='Sequence',
        default=10,
        help='Sequence for ordering'
    )
    
    active = BooleanField(
        string='Active',
        default=True,
        help='Whether the transaction is active'
    )
    
    # Company
    company_id = Many2OneField(
        'res.company',
        string='Company',
        help='Company this transaction belongs to'
    )
    
    # Additional Information
    notes = TextField(
        string='Notes',
        help='Additional notes for the transaction'
    )
    
    def create(self, vals):
        """Override create to set default values"""
        if not vals.get('company_id'):
            vals['company_id'] = self.env.context.get('default_company_id')
        
        return super(EdiTransaction, self).create(vals)
    
    def get_kids_clothing_transactions(self, age_group=None, size=None, season=None, brand=None, color=None):
        """Get transactions filtered by kids clothing criteria"""
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