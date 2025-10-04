# -*- coding: utf-8 -*-
"""
Ocean ERP - Indian EDI Error Model
==================================

EDI error management for kids clothing retail.
"""

from core_framework.orm import BaseModel, CharField, TextField, BooleanField, IntegerField, DateTimeField, Many2OneField, SelectionField, FloatField, One2ManyField
from core_framework.exceptions import ValidationError, UserError
from addons.core_base.models.base_mixins import KidsClothingMixin
import logging

_logger = logging.getLogger(__name__)


class EdiError(BaseModel, KidsClothingMixin):
    """Indian EDI Error Model for Ocean ERP"""
    
    _name = 'edi.error'
    _description = 'EDI Error'
    _order = 'error_date desc, name'
    _rec_name = 'name'

    name = CharField(
        string='Error Name',
        required=True,
        help='Name of the EDI error'
    )
    
    # EDI Specific Fields
    error_type = SelectionField(
        selection=[
            ('syntax', 'Syntax Error'),
            ('semantic', 'Semantic Error'),
            ('business', 'Business Error'),
            ('compliance', 'Compliance Error'),
            ('format', 'Format Error'),
            ('transmission', 'Transmission Error'),
            ('validation', 'Validation Error'),
            ('other', 'Other'),
        ],
        string='Error Type',
        required=True,
        help='Type of EDI error'
    )
    
    error_code = CharField(
        string='Error Code',
        help='Code of the error'
    )
    
    error_message = TextField(
        string='Error Message',
        help='Message of the error'
    )
    
    error_details = TextField(
        string='Error Details',
        help='Detailed information about the error'
    )
    
    severity = SelectionField(
        selection=[
            ('low', 'Low'),
            ('medium', 'Medium'),
            ('high', 'High'),
            ('critical', 'Critical'),
        ],
        string='Severity',
        default='medium',
        help='Severity of the error'
    )
    
    state = SelectionField(
        selection=[
            ('new', 'New'),
            ('acknowledged', 'Acknowledged'),
            ('resolved', 'Resolved'),
            ('ignored', 'Ignored'),
        ],
        string='Status',
        default='new',
        help='Status of the error'
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
        help='Age group for this error'
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
        help='Size for this error'
    )
    
    season = SelectionField(
        selection=[
            ('summer', 'Summer'),
            ('winter', 'Winter'),
            ('monsoon', 'Monsoon'),
            ('all_season', 'All Season'),
        ],
        string='Season',
        help='Season for this error'
    )
    
    brand = CharField(
        string='Brand',
        help='Brand for this error'
    )
    
    color = CharField(
        string='Color',
        help='Color for this error'
    )
    
    # Error Configuration
    error_date = DateTimeField(
        string='Error Date',
        help='Date of the error'
    )
    
    resolved_date = DateTimeField(
        string='Resolved Date',
        help='Date when error was resolved'
    )
    
    resolved_by = Many2OneField(
        'res.users',
        string='Resolved By',
        help='User who resolved the error'
    )
    
    # Company
    company_id = Many2OneField(
        'res.company',
        string='Company',
        help='Company this error belongs to'
    )
    
    # Document
    document_id = Many2OneField(
        'edi.document',
        string='Document',
        help='EDI document that caused the error'
    )
    
    # Additional Information
    notes = TextField(
        string='Notes',
        help='Additional notes for the error'
    )
    
    def create(self, vals):
        """Override create to set default values"""
        if not vals.get('company_id'):
            vals['company_id'] = self.env.context.get('default_company_id')
        
        return super(EdiError, self).create(vals)
    
    def action_acknowledge(self):
        """Acknowledge the error"""
        for record in self:
            if record.state != 'new':
                raise UserError('Only new errors can be acknowledged.')
            
            record.write({
                'state': 'acknowledged',
            })
    
    def action_resolve(self):
        """Resolve the error"""
        for record in self:
            if record.state not in ['new', 'acknowledged']:
                raise UserError('Only new or acknowledged errors can be resolved.')
            
            record.write({
                'state': 'resolved',
                'resolved_date': self.env.context.get('resolved_date'),
                'resolved_by': self.env.context.get('resolved_by'),
            })
    
    def action_ignore(self):
        """Ignore the error"""
        for record in self:
            if record.state != 'new':
                raise UserError('Only new errors can be ignored.')
            
            record.write({
                'state': 'ignored',
            })
    
    def get_kids_clothing_errors(self, age_group=None, size=None, season=None, brand=None, color=None):
        """Get errors filtered by kids clothing criteria"""
        domain = [('state', '=', 'resolved')]
        
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