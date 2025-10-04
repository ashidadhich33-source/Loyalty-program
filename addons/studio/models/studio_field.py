#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Studio Field
===============================

Studio field management for custom field creation.
"""

from core_framework.orm import (
    BaseModel, CharField, TextField, SelectionField, Many2OneField,
    BooleanField, One2ManyField, IntegerField, FloatField
)
from addons.core_base.models.base_mixins import KidsClothingMixin


class StudioField(BaseModel, KidsClothingMixin):
    """Studio Field for Custom Field Creation"""
    
    _name = 'studio.field'
    _description = 'Studio Field'
    _order = 'sequence, name'
    
    # Basic Information
    name = CharField('Field Name', required=True, size=200)
    technical_name = CharField('Technical Name', required=True, size=100)
    label = CharField('Field Label', required=True, size=200)
    help_text = TextField('Help Text')
    
    # Field Configuration
    model_id = Many2OneField('studio.model', 'Model', required=True)
    field_type = SelectionField([
        ('char', 'Text'),
        ('text', 'Long Text'),
        ('integer', 'Integer'),
        ('float', 'Float'),
        ('boolean', 'Boolean'),
        ('date', 'Date'),
        ('datetime', 'DateTime'),
        ('selection', 'Selection'),
        ('many2one', 'Many2One'),
        ('one2many', 'One2Many'),
        ('many2many', 'Many2Many'),
        ('binary', 'Binary'),
        ('image', 'Image'),
    ], 'Field Type', required=True)
    
    # Field Properties
    required = BooleanField('Required', default=False)
    readonly = BooleanField('Readonly', default=False)
    invisible = BooleanField('Invisible', default=False)
    default_value = TextField('Default Value')
    
    # Field Settings
    sequence = IntegerField('Sequence', default=10)
    active = BooleanField('Active', default=True)
    
    # Field Validation
    min_value = FloatField('Minimum Value')
    max_value = FloatField('Maximum Value')
    min_length = IntegerField('Minimum Length')
    max_length = IntegerField('Maximum Length')
    size = IntegerField('Size', default=255)
    
    # Selection Options
    selection_options = TextField('Selection Options', 
                                help='Format: [("value", "Label"), ("value2", "Label2")]')
    
    # Relationship Fields
    comodel_name = CharField('Related Model', size=100)
    inverse_name = CharField('Inverse Field', size=100)
    
    # Field Dependencies
    depends_on_ids = One2ManyField('studio.field.dependency', 'field_id', 'Dependencies')
    
    def generate_field_code(self):
        """Generate Python field code"""
        field_type = self.field_type
        field_name = self.technical_name
        
        # Base field parameters
        params = []
        
        if self.label:
            params.append(f"string='{self.label}'")
        
        if self.required:
            params.append("required=True")
        
        if self.readonly:
            params.append("readonly=True")
        
        if self.invisible:
            params.append("invisible=True")
        
        if self.default_value:
            params.append(f"default={self.default_value}")
        
        if self.help_text:
            params.append(f"help='{self.help_text}'")
        
        # Field-specific parameters
        if field_type == 'char':
            if self.size:
                params.append(f"size={self.size}")
        elif field_type == 'selection':
            if self.selection_options:
                params.append(f"selection={self.selection_options}")
        elif field_type == 'many2one':
            if self.comodel_name:
                params.append(f"comodel_name='{self.comodel_name}'")
        elif field_type == 'one2many':
            if self.comodel_name and self.inverse_name:
                params.append(f"comodel_name='{self.comodel_name}'")
                params.append(f"inverse_name='{self.inverse_name}'")
        elif field_type == 'many2many':
            if self.comodel_name:
                params.append(f"comodel_name='{self.comodel_name}'")
        
        # Generate field definition
        field_class = self._get_field_class()
        params_str = ", ".join(params)
        
        return f"{field_name} = {field_class}({params_str})"
    
    def _get_field_class(self):
        """Get field class name"""
        field_map = {
            'char': 'CharField',
            'text': 'TextField',
            'integer': 'IntegerField',
            'float': 'FloatField',
            'boolean': 'BooleanField',
            'date': 'DateField',
            'datetime': 'DateTimeField',
            'selection': 'SelectionField',
            'many2one': 'Many2OneField',
            'one2many': 'One2ManyField',
            'many2many': 'Many2ManyField',
            'binary': 'BinaryField',
            'image': 'ImageField',
        }
        return field_map.get(self.field_type, 'CharField')
    
    def validate_field(self):
        """Validate field configuration"""
        errors = []
        
        # Check required fields
        if not self.technical_name:
            errors.append("Technical name is required")
        
        if not self.label:
            errors.append("Field label is required")
        
        # Check field type specific requirements
        if self.field_type == 'selection' and not self.selection_options:
            errors.append("Selection options are required for selection fields")
        
        if self.field_type in ['many2one', 'one2many', 'many2many'] and not self.comodel_name:
            errors.append("Related model is required for relationship fields")
        
        if self.field_type == 'one2many' and not self.inverse_name:
            errors.append("Inverse field is required for One2Many fields")
        
        # Check validation rules
        if self.min_value is not None and self.max_value is not None:
            if self.min_value > self.max_value:
                errors.append("Minimum value cannot be greater than maximum value")
        
        if self.min_length is not None and self.max_length is not None:
            if self.min_length > self.max_length:
                errors.append("Minimum length cannot be greater than maximum length")
        
        return errors
    
    def get_field_summary(self):
        """Get field summary"""
        return {
            'id': self.id,
            'name': self.name,
            'technical_name': self.technical_name,
            'label': self.label,
            'field_type': self.field_type,
            'required': self.required,
            'readonly': self.readonly,
            'sequence': self.sequence,
        }


class StudioFieldDependency(BaseModel, KidsClothingMixin):
    """Studio Field Dependency"""
    
    _name = 'studio.field.dependency'
    _description = 'Studio Field Dependency'
    
    field_id = Many2OneField('studio.field', 'Field', required=True)
    depends_on_field = CharField('Depends On Field', required=True, size=100)
    condition = SelectionField([
        ('equals', 'Equals'),
        ('not_equals', 'Not Equals'),
        ('greater_than', 'Greater Than'),
        ('less_than', 'Less Than'),
        ('contains', 'Contains'),
        ('not_contains', 'Not Contains'),
    ], 'Condition', required=True)
    value = TextField('Value')
    
    def get_dependency_code(self):
        """Get dependency code"""
        return f"depends=['{self.depends_on_field}']"