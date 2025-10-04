# -*- coding: utf-8 -*-
"""
Ocean ERP - Indian EDI Validation Model
=======================================

EDI validation management for kids clothing retail.
"""

from core_framework.orm import BaseModel, CharField, TextField, BooleanField, IntegerField, DateTimeField, Many2OneField, SelectionField, FloatField, One2ManyField
from core_framework.exceptions import ValidationError, UserError
from addons.core_base.models.base_mixins import KidsClothingMixin
import logging

_logger = logging.getLogger(__name__)


class EdiValidation(BaseModel, KidsClothingMixin):
    """Indian EDI Validation Model for Ocean ERP"""
    
    _name = 'edi.validation'
    _description = 'EDI Validation'
    _order = 'validation_date desc, name'
    _rec_name = 'name'

    name = CharField(
        string='Validation Name',
        required=True,
        help='Name of the EDI validation'
    )
    
    # EDI Specific Fields
    validation_type = SelectionField(
        selection=[
            ('syntax', 'Syntax Validation'),
            ('semantic', 'Semantic Validation'),
            ('business', 'Business Validation'),
            ('compliance', 'Compliance Validation'),
            ('format', 'Format Validation'),
            ('other', 'Other'),
        ],
        string='Validation Type',
        required=True,
        help='Type of EDI validation'
    )
    
    validation_status = SelectionField(
        selection=[
            ('pending', 'Pending'),
            ('running', 'Running'),
            ('passed', 'Passed'),
            ('failed', 'Failed'),
            ('warning', 'Warning'),
            ('error', 'Error'),
        ],
        string='Validation Status',
        default='pending',
        help='Status of the validation'
    )
    
    validation_rules = TextField(
        string='Validation Rules',
        help='Rules used for validation'
    )
    
    validation_results = TextField(
        string='Validation Results',
        help='Results of the validation'
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
        help='Age group for this validation'
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
        help='Size for this validation'
    )
    
    season = SelectionField(
        selection=[
            ('summer', 'Summer'),
            ('winter', 'Winter'),
            ('monsoon', 'Monsoon'),
            ('all_season', 'All Season'),
        ],
        string='Season',
        help='Season for this validation'
    )
    
    brand = CharField(
        string='Brand',
        help='Brand for this validation'
    )
    
    color = CharField(
        string='Color',
        help='Color for this validation'
    )
    
    # Validation Configuration
    validation_date = DateTimeField(
        string='Validation Date',
        help='Date of the validation'
    )
    
    start_time = DateTimeField(
        string='Start Time',
        help='Time when validation started'
    )
    
    end_time = DateTimeField(
        string='End Time',
        help='Time when validation ended'
    )
    
    # Company
    company_id = Many2OneField(
        'res.company',
        string='Company',
        help='Company this validation belongs to'
    )
    
    # Document
    document_id = Many2OneField(
        'edi.document',
        string='Document',
        help='EDI document being validated'
    )
    
    # Additional Information
    notes = TextField(
        string='Notes',
        help='Additional notes for the validation'
    )
    
    def create(self, vals):
        """Override create to set default values"""
        if not vals.get('company_id'):
            vals['company_id'] = self.env.context.get('default_company_id')
        
        return super(EdiValidation, self).create(vals)
    
    def action_run_validation(self):
        """Run the EDI validation"""
        for record in self:
            if record.validation_status != 'pending':
                raise UserError('Only pending validations can be run.')
            
            record.write({
                'validation_status': 'running',
                'start_time': self.env.context.get('start_time'),
            })
            
            # Run validation logic
            validation_results = self._run_validation_logic(record)
            
            record.write({
                'validation_status': 'passed' if validation_results['passed'] else 'failed',
                'end_time': self.env.context.get('end_time'),
                'validation_results': validation_results['results'],
            })
    
    def _run_validation_logic(self, record):
        """Run the actual validation logic"""
        # This would run the actual validation
        return {
            'passed': True,
            'results': '{}'
        }
    
    def get_kids_clothing_validations(self, age_group=None, size=None, season=None, brand=None, color=None):
        """Get validations filtered by kids clothing criteria"""
        domain = [('validation_status', '=', 'passed')]
        
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