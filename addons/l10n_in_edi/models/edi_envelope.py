# -*- coding: utf-8 -*-
"""
Ocean ERP - Indian EDI Envelope Model
=====================================

EDI envelope management for kids clothing retail.
"""

from core_framework.orm import BaseModel, CharField, TextField, BooleanField, IntegerField, DateTimeField, Many2OneField, SelectionField, FloatField, One2ManyField
from core_framework.exceptions import ValidationError, UserError
from addons.core_base.models.base_mixins import KidsClothingMixin
import logging

_logger = logging.getLogger(__name__)


class EdiEnvelope(BaseModel, KidsClothingMixin):
    """Indian EDI Envelope Model for Ocean ERP"""
    
    _name = 'edi.envelope'
    _description = 'EDI Envelope'
    _order = 'sequence, name'
    _rec_name = 'name'

    name = CharField(
        string='Envelope Name',
        required=True,
        help='Name of the EDI envelope'
    )
    
    message_id = Many2OneField(
        'edi.message',
        string='Message',
        required=True,
        help='EDI message this envelope belongs to'
    )
    
    # EDI Specific Fields
    envelope_type = SelectionField(
        selection=[
            ('interchange', 'Interchange'),
            ('group', 'Group'),
            ('message', 'Message'),
            ('segment', 'Segment'),
            ('element', 'Element'),
            ('other', 'Other'),
        ],
        string='Envelope Type',
        required=True,
        help='Type of EDI envelope'
    )
    
    envelope_data = TextField(
        string='Envelope Data',
        help='Raw envelope data'
    )
    
    processed_data = TextField(
        string='Processed Data',
        help='Processed envelope data'
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
        help='Age group for this envelope'
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
        help='Size for this envelope'
    )
    
    season = SelectionField(
        selection=[
            ('summer', 'Summer'),
            ('winter', 'Winter'),
            ('monsoon', 'Monsoon'),
            ('all_season', 'All Season'),
        ],
        string='Season',
        help='Season for this envelope'
    )
    
    brand = CharField(
        string='Brand',
        help='Brand for this envelope'
    )
    
    color = CharField(
        string='Color',
        help='Color for this envelope'
    )
    
    # Envelope Configuration
    sequence = IntegerField(
        string='Sequence',
        default=10,
        help='Sequence for ordering'
    )
    
    active = BooleanField(
        string='Active',
        default=True,
        help='Whether the envelope is active'
    )
    
    # Company
    company_id = Many2OneField(
        'res.company',
        string='Company',
        help='Company this envelope belongs to'
    )
    
    # Additional Information
    notes = TextField(
        string='Notes',
        help='Additional notes for the envelope'
    )
    
    def create(self, vals):
        """Override create to set default values"""
        if not vals.get('company_id'):
            vals['company_id'] = self.env.context.get('default_company_id')
        
        return super(EdiEnvelope, self).create(vals)
    
    def get_kids_clothing_envelopes(self, age_group=None, size=None, season=None, brand=None, color=None):
        """Get envelopes filtered by kids clothing criteria"""
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