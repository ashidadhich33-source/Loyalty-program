#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Field Type Model
===================================

Field type management for custom field types.
"""

from core_framework.orm import (
    BaseModel, CharField, TextField, SelectionField, Many2OneField,
    BooleanField, One2ManyField, IntegerField, FloatField
)
from addons.core_base.models.base_mixins import KidsClothingMixin


class FieldType(BaseModel, KidsClothingMixin):
    """Field Type Model for Custom Field Types"""
    
    _name = 'custom.field.type'
    _description = 'Custom Field Type'
    _order = 'sequence, name'
    
    # Basic Information
    name = CharField('Field Type Name', required=True, size=200)
    technical_name = CharField('Technical Name', required=True, size=100)
    description = TextField('Description')
    
    # Field Type Configuration
    field_class = CharField('Field Class', required=True, size=100,
                          help='Python field class name')
    field_category = SelectionField([
        ('basic', 'Basic Fields'),
        ('text', 'Text Fields'),
        ('numeric', 'Numeric Fields'),
        ('date', 'Date Fields'),
        ('relational', 'Relational Fields'),
        ('selection', 'Selection Fields'),
        ('binary', 'Binary Fields'),
        ('custom', 'Custom Fields'),
    ], 'Field Category', required=True)
    
    # Field Type Properties
    has_size = BooleanField('Has Size Property', default=False)
    has_selection = BooleanField('Has Selection Property', default=False)
    has_comodel = BooleanField('Has Related Model', default=False)
    has_inverse = BooleanField('Has Inverse Field', default=False)
    has_digits = BooleanField('Has Digits Property', default=False)
    has_max_width = BooleanField('Has Max Width', default=False)
    has_max_height = BooleanField('Has Max Height', default=False)
    
    # Field Type Settings
    sequence = IntegerField('Sequence', default=10)
    active = BooleanField('Active', default=True)
    is_system = BooleanField('System Field Type', default=False)
    
    # Field Type Validation
    default_size = IntegerField('Default Size', default=255)
    min_size = IntegerField('Minimum Size', default=1)
    max_size = IntegerField('Maximum Size', default=10000)
    
    # Field Type Examples
    example_code = TextField('Example Code', 
                           help='Example field definition code')
    example_xml = TextField('Example XML', 
                          help='Example XML field definition')
    
    # Field Type Usage
    usage_count = IntegerField('Usage Count', default=0)
    field_ids = One2ManyField('custom.field', 'field_type_id', 'Fields')
    
    # Access Control
    user_id = Many2OneField('users.user', 'Created By', required=True)
    group_ids = One2ManyField('users.group', 'field_type_group_ids', 'Access Groups')
    
    def get_field_class(self):
        """Get field class for this field type"""
        return self.field_class
    
    def validate_field_config(self, field_config):
        """Validate field configuration for this field type"""
        errors = []
        
        # Check size if required
        if self.has_size and 'size' not in field_config:
            errors.append(f"Size is required for {self.name} field type")
        
        # Check selection if required
        if self.has_selection and 'selection' not in field_config:
            errors.append(f"Selection options are required for {self.name} field type")
        
        # Check comodel if required
        if self.has_comodel and 'comodel_name' not in field_config:
            errors.append(f"Related model is required for {self.name} field type")
        
        # Check inverse if required
        if self.has_inverse and 'inverse_name' not in field_config:
            errors.append(f"Inverse field is required for {self.name} field type")
        
        # Validate size range
        if 'size' in field_config:
            size = field_config['size']
            if size < self.min_size or size > self.max_size:
                errors.append(f"Size must be between {self.min_size} and {self.max_size}")
        
        return errors
    
    def generate_field_code(self, field_config):
        """Generate field code for this field type"""
        field_name = field_config.get('name', 'field_name')
        field_class = self.get_field_class()
        
        # Build field parameters
        params = []
        
        if field_config.get('string'):
            params.append(f"string='{field_config['string']}'")
        
        if field_config.get('required'):
            params.append("required=True")
        
        if field_config.get('readonly'):
            params.append("readonly=True")
        
        if field_config.get('invisible'):
            params.append("invisible=True")
        
        if field_config.get('default'):
            params.append(f"default={field_config['default']}")
        
        if field_config.get('help'):
            params.append(f"help='{field_config['help']}'")
        
        # Add type-specific parameters
        if self.has_size and 'size' in field_config:
            params.append(f"size={field_config['size']}")
        
        if self.has_selection and 'selection' in field_config:
            params.append(f"selection={field_config['selection']}")
        
        if self.has_comodel and 'comodel_name' in field_config:
            params.append(f"comodel_name='{field_config['comodel_name']}'")
        
        if self.has_inverse and 'inverse_name' in field_config:
            params.append(f"inverse_name='{field_config['inverse_name']}'")
        
        if self.has_digits and 'digits' in field_config:
            params.append(f"digits={field_config['digits']}")
        
        if self.has_max_width and 'max_width' in field_config:
            params.append(f"max_width={field_config['max_width']}")
        
        if self.has_max_height and 'max_height' in field_config:
            params.append(f"max_height={field_config['max_height']}")
        
        # Generate field definition
        params_str = ", ".join(params)
        return f"{field_name} = {field_class}({params_str})"
    
    def get_field_summary(self):
        """Get field type summary"""
        return {
            'id': self.id,
            'name': self.name,
            'technical_name': self.technical_name,
            'field_class': self.field_class,
            'field_category': self.field_category,
            'usage_count': self.usage_count,
            'is_system': self.is_system,
        }


class FieldTypeTemplate(BaseModel, KidsClothingMixin):
    """Field Type Template for Predefined Field Types"""
    
    _name = 'custom.field.type.template'
    _description = 'Field Type Template'
    
    field_type_id = Many2OneField('custom.field.type', 'Field Type', required=True)
    name = CharField('Template Name', required=True, size=200)
    description = TextField('Description')
    
    # Template Configuration
    template_config = TextField('Template Configuration', 
                               help='JSON configuration template')
    default_values = TextField('Default Values', 
                              help='Default field values')
    
    # Template Usage
    usage_count = IntegerField('Usage Count', default=0)
    is_public = BooleanField('Public Template', default=False)
    
    def apply_template(self, field_config):
        """Apply template to field configuration"""
        # Apply template configuration to field config
        # Implementation would merge template config with field config
        return field_config
    
    def get_template_summary(self):
        """Get template summary"""
        return {
            'id': self.id,
            'name': self.name,
            'field_type': self.field_type_id.name,
            'usage_count': self.usage_count,
            'is_public': self.is_public,
        }