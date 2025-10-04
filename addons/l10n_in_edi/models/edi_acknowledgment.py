# -*- coding: utf-8 -*-
"""
Ocean ERP - Indian EDI Acknowledgment Model
===========================================

EDI acknowledgment management for kids clothing retail.
"""

from core_framework.orm import BaseModel, CharField, TextField, BooleanField, IntegerField, DateTimeField, Many2OneField, SelectionField, FloatField, One2ManyField
from core_framework.exceptions import ValidationError, UserError
from addons.core_base.models.base_mixins import KidsClothingMixin
import logging

_logger = logging.getLogger(__name__)


class EdiAcknowledgment(BaseModel, KidsClothingMixin):
    """Indian EDI Acknowledgment Model for Ocean ERP"""
    
    _name = 'edi.acknowledgment'
    _description = 'EDI Acknowledgment'
    _order = 'acknowledgment_date desc, name'
    _rec_name = 'name'

    name = CharField(
        string='Acknowledgment Name',
        required=True,
        help='Name of the EDI acknowledgment'
    )
    
    transmission_id = Many2OneField(
        'edi.transmission',
        string='Transmission',
        required=True,
        help='EDI transmission this acknowledgment belongs to'
    )
    
    # EDI Specific Fields
    acknowledgment_type = SelectionField(
        selection=[
            ('ta', 'Technical Acknowledgment'),
            ('fa', 'Functional Acknowledgment'),
            ('ua', 'Usage Acknowledgment'),
            ('other', 'Other'),
        ],
        string='Acknowledgment Type',
        required=True,
        help='Type of EDI acknowledgment'
    )
    
    acknowledgment_code = CharField(
        string='Acknowledgment Code',
        help='Code of the acknowledgment'
    )
    
    acknowledgment_message = TextField(
        string='Acknowledgment Message',
        help='Message of the acknowledgment'
    )
    
    state = SelectionField(
        selection=[
            ('pending', 'Pending'),
            ('received', 'Received'),
            ('processed', 'Processed'),
            ('error', 'Error'),
        ],
        string='Status',
        default='pending',
        help='Status of the EDI acknowledgment'
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
        help='Age group for this acknowledgment'
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
        help='Size for this acknowledgment'
    )
    
    season = SelectionField(
        selection=[
            ('summer', 'Summer'),
            ('winter', 'Winter'),
            ('monsoon', 'Monsoon'),
            ('all_season', 'All Season'),
        ],
        string='Season',
        help='Season for this acknowledgment'
    )
    
    brand = CharField(
        string='Brand',
        help='Brand for this acknowledgment'
    )
    
    color = CharField(
        string='Color',
        help='Color for this acknowledgment'
    )
    
    # Dates
    acknowledgment_date = DateTimeField(
        string='Acknowledgment Date',
        help='Date of the acknowledgment'
    )
    
    receive_date = DateTimeField(
        string='Receive Date',
        help='Date when acknowledgment was received'
    )
    
    process_date = DateTimeField(
        string='Process Date',
        help='Date when acknowledgment was processed'
    )
    
    # Company
    company_id = Many2OneField(
        'res.company',
        string='Company',
        help='Company this acknowledgment belongs to'
    )
    
    # Additional Information
    notes = TextField(
        string='Notes',
        help='Additional notes for the acknowledgment'
    )
    
    def create(self, vals):
        """Override create to set default values"""
        if not vals.get('company_id'):
            vals['company_id'] = self.env.context.get('default_company_id')
        
        return super(EdiAcknowledgment, self).create(vals)
    
    def get_kids_clothing_acknowledgments(self, age_group=None, size=None, season=None, brand=None, color=None):
        """Get acknowledgments filtered by kids clothing criteria"""
        domain = [('state', '=', 'processed')]
        
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