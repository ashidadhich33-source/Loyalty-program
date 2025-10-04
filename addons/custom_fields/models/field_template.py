#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Field Template Model
=======================================

Field template management for reusable field configurations.
"""

from core_framework.orm import (
    BaseModel, CharField, TextField, SelectionField, Many2OneField,
    BooleanField, One2ManyField, IntegerField, FloatField
)
from addons.core_base.models.base_mixins import KidsClothingMixin


class FieldTemplate(BaseModel, KidsClothingMixin):
    """Field Template Model for Reusable Field Configurations"""
    
    _name = 'custom.field.template'
    _description = 'Custom Field Template'
    _order = 'sequence, name'
    
    # Basic Information
    name = CharField('Template Name', required=True, size=200)
    technical_name = CharField('Technical Name', required=True, size=100)
    description = TextField('Description')
    
    # Template Configuration
    template_type = SelectionField([
        ('basic', 'Basic Field'),
        ('relational', 'Relational Field'),
        ('selection', 'Selection Field'),
        ('computed', 'Computed Field'),
        ('custom', 'Custom Field'),
    ], 'Template Type', required=True)
    
    # Field Configuration
    field_type_id = Many2OneField('custom.field.type', 'Field Type', required=True)
    field_group_id = Many2OneField('custom.field.group', 'Field Group')
    
    # Field Properties
    required = BooleanField('Required', default=False)
    readonly = BooleanField('Readonly', default=False)
    invisible = BooleanField('Invisible', default=False)
    default_value = TextField('Default Value')
    
    # Field Settings
    sequence = IntegerField('Sequence', default=10)
    active = BooleanField('Active', default=True)
    is_public = BooleanField('Public Template', default=False)
    is_featured = BooleanField('Featured Template', default=False)
    
    # Field Configuration Data
    field_config = TextField('Field Configuration', 
                            help='JSON field configuration')
    validation_rules = TextField('Validation Rules', 
                                help='JSON validation rules')
    display_options = TextField('Display Options', 
                               help='JSON display options')
    
    # Field Examples
    example_code = TextField('Example Code', 
                           help='Example field definition code')
    example_xml = TextField('Example XML', 
                          help='Example XML field definition')
    
    # Template Usage
    usage_count = IntegerField('Usage Count', default=0)
    download_count = IntegerField('Download Count', default=0)
    rating = FloatField('Rating', digits=(3, 2), default=0.0)
    
    # Template Dependencies
    depends_on_ids = One2ManyField('custom.field.template.dependency', 'template_id', 'Dependencies')
    required_addons = TextField('Required Addons', 
                               help='Comma-separated list of required addons')
    
    # Access Control
    user_id = Many2OneField('users.user', 'Created By', required=True)
    group_ids = One2ManyField('users.group', 'field_template_group_ids', 'Access Groups')
    
    def create_field_from_template(self, model_name, field_name=None, custom_config=None):
        """Create field from template"""
        try:
            # Parse field configuration
            field_config = self._parse_field_config()
            
            # Apply custom configuration
            if custom_config:
                field_config.update(custom_config)
            
            # Generate field name if not provided
            if not field_name:
                field_name = self._generate_field_name(model_name)
            
            # Create field data
            field_data = {
                'name': field_config.get('name', self.name),
                'field_name': field_name,
                'label': field_config.get('label', self.name),
                'model_name': model_name,
                'field_type_id': self.field_type_id.id,
                'field_group_id': self.field_group_id.id if self.field_group_id else False,
                'required': field_config.get('required', self.required),
                'readonly': field_config.get('readonly', self.readonly),
                'invisible': field_config.get('invisible', self.invisible),
                'default_value': field_config.get('default_value', self.default_value),
                'validation_rules': field_config.get('validation_rules', self.validation_rules),
                'user_id': self.env.uid,
            }
            
            # Create field
            field = self.env['custom.field'].create(field_data)
            
            # Update usage count
            self.write({'usage_count': self.usage_count + 1})
            
            return field
            
        except Exception as e:
            raise e
    
    def _parse_field_config(self):
        """Parse field configuration"""
        import json
        try:
            return json.loads(self.field_config) if self.field_config else {}
        except:
            return {}
    
    def _generate_field_name(self, model_name):
        """Generate field name from template"""
        base_name = self.technical_name.lower().replace(' ', '_')
        return f"{model_name}_{base_name}"
    
    def validate_template(self):
        """Validate template configuration"""
        errors = []
        
        # Check required fields
        if not self.name:
            errors.append("Template name is required")
        
        if not self.technical_name:
            errors.append("Technical name is required")
        
        if not self.field_type_id:
            errors.append("Field type is required")
        
        # Validate field configuration
        field_config = self._parse_field_config()
        if field_config:
            validation_errors = self.field_type_id.validate_field_config(field_config)
            errors.extend(validation_errors)
        
        # Validate validation rules
        if self.validation_rules:
            try:
                import json
                json.loads(self.validation_rules)
            except:
                errors.append("Invalid validation rules JSON")
        
        return errors
    
    def get_field_code(self, field_name, model_name):
        """Get field code for this template"""
        field_config = self._parse_field_config()
        field_config['name'] = field_name
        
        return self.field_type_id.generate_field_code(field_config)
    
    def get_field_xml(self, field_name):
        """Get field XML for this template"""
        if self.example_xml:
            return self.example_xml.replace('field_name', field_name)
        
        # Generate default XML
        field_attrs = []
        if self.required:
            field_attrs.append('required="1"')
        if self.readonly:
            field_attrs.append('readonly="1"')
        if self.invisible:
            field_attrs.append('invisible="1"')
        
        attrs_str = " ".join(field_attrs)
        return f'<field name="{field_name}" {attrs_str}/>'
    
    def clone_template(self, new_name):
        """Clone template with new name"""
        try:
            clone_data = {
                'name': new_name,
                'technical_name': f"{self.technical_name}_clone",
                'description': f"Clone of {self.name}",
                'field_type_id': self.field_type_id.id,
                'field_group_id': self.field_group_id.id if self.field_group_id else False,
                'required': self.required,
                'readonly': self.readonly,
                'invisible': self.invisible,
                'default_value': self.default_value,
                'field_config': self.field_config,
                'validation_rules': self.validation_rules,
                'display_options': self.display_options,
                'example_code': self.example_code,
                'example_xml': self.example_xml,
                'user_id': self.env.uid,
            }
            
            return self.env['custom.field.template'].create(clone_data)
            
        except Exception as e:
            raise e
    
    def get_template_summary(self):
        """Get template summary"""
        return {
            'id': self.id,
            'name': self.name,
            'technical_name': self.technical_name,
            'template_type': self.template_type,
            'field_type': self.field_type_id.name,
            'usage_count': self.usage_count,
            'download_count': self.download_count,
            'rating': self.rating,
            'is_public': self.is_public,
            'is_featured': self.is_featured,
        }


class FieldTemplateDependency(BaseModel, KidsClothingMixin):
    """Field Template Dependency"""
    
    _name = 'custom.field.template.dependency'
    _description = 'Field Template Dependency'
    
    template_id = Many2OneField('custom.field.template', 'Template', required=True)
    depends_on_template = CharField('Depends On Template', required=True, size=100)
    dependency_type = SelectionField([
        ('required', 'Required'),
        ('optional', 'Optional'),
        ('conflict', 'Conflict'),
    ], 'Dependency Type', default='required')
    version_requirement = CharField('Version Requirement', size=50)
    description = TextField('Description')