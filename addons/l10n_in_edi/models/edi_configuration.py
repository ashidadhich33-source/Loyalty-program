# -*- coding: utf-8 -*-
"""
Ocean ERP - Indian EDI Configuration Model
=========================================

EDI configuration management for kids clothing retail.
"""

from core_framework.orm import BaseModel, CharField, TextField, BooleanField, IntegerField, DateTimeField, Many2OneField, SelectionField, FloatField, One2ManyField
from core_framework.exceptions import ValidationError, UserError
from addons.core_base.models.base_mixins import KidsClothingMixin
import logging

_logger = logging.getLogger(__name__)


class EdiConfiguration(BaseModel, KidsClothingMixin):
    """Indian EDI Configuration Model for Ocean ERP"""
    
    _name = 'edi.configuration'
    _description = 'EDI Configuration'
    _order = 'sequence, name'
    _rec_name = 'name'

    name = CharField(
        string='Configuration Name',
        required=True,
        help='Name of the EDI configuration'
    )
    
    # EDI Specific Fields
    configuration_type = SelectionField(
        selection=[
            ('connection', 'Connection Configuration'),
            ('mapping', 'Mapping Configuration'),
            ('validation', 'Validation Configuration'),
            ('transmission', 'Transmission Configuration'),
            ('format', 'Format Configuration'),
            ('other', 'Other'),
        ],
        string='Configuration Type',
        required=True,
        help='Type of EDI configuration'
    )
    
    edi_format = SelectionField(
        selection=[
            ('edifact', 'EDIFACT'),
            ('x12', 'X12'),
            ('xml', 'XML'),
            ('json', 'JSON'),
            ('csv', 'CSV'),
            ('custom', 'Custom'),
        ],
        string='EDI Format',
        required=True,
        help='Format of the EDI configuration'
    )
    
    edi_version = CharField(
        string='EDI Version',
        help='Version of the EDI standard'
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
        help='Age group for this configuration'
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
        help='Size for this configuration'
    )
    
    season = SelectionField(
        selection=[
            ('summer', 'Summer'),
            ('winter', 'Winter'),
            ('monsoon', 'Monsoon'),
            ('all_season', 'All Season'),
        ],
        string='Season',
        help='Season for this configuration'
    )
    
    brand = CharField(
        string='Brand',
        help='Brand for this configuration'
    )
    
    color = CharField(
        string='Color',
        help='Color for this configuration'
    )
    
    # Configuration Data
    configuration_data = TextField(
        string='Configuration Data',
        help='Configuration data in JSON format'
    )
    
    # Configuration Settings
    is_default = BooleanField(
        string='Is Default',
        default=False,
        help='Whether this is the default configuration'
    )
    
    is_active = BooleanField(
        string='Is Active',
        default=True,
        help='Whether this configuration is active'
    )
    
    # Configuration Configuration
    sequence = IntegerField(
        string='Sequence',
        default=10,
        help='Sequence for ordering'
    )
    
    # Company
    company_id = Many2OneField(
        'res.company',
        string='Company',
        help='Company this configuration belongs to'
    )
    
    # Partner
    partner_id = Many2OneField(
        'res.partner',
        string='Partner',
        help='Partner this configuration is for'
    )
    
    # Additional Information
    description = TextField(
        string='Description',
        help='Description of the configuration'
    )
    
    notes = TextField(
        string='Notes',
        help='Additional notes for the configuration'
    )
    
    def create(self, vals):
        """Override create to set default values"""
        if not vals.get('company_id'):
            vals['company_id'] = self.env.context.get('default_company_id')
        
        return super(EdiConfiguration, self).create(vals)
    
    def action_set_default(self):
        """Set this configuration as default"""
        for record in self:
            # Unset other default configurations
            self.search([('is_default', '=', True)]).write({'is_default': False})
            
            # Set this as default
            record.write({'is_default': True})
    
    def action_activate(self):
        """Activate this configuration"""
        for record in self:
            record.write({'is_active': True})
    
    def action_deactivate(self):
        """Deactivate this configuration"""
        for record in self:
            record.write({'is_active': False})
    
    def get_kids_clothing_configurations(self, age_group=None, size=None, season=None, brand=None, color=None):
        """Get configurations filtered by kids clothing criteria"""
        domain = [('is_active', '=', True)]
        
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