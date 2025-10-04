#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Custom Field Model
=====================================

Custom field management for dynamic field creation.
"""

from core_framework.orm import (
    BaseModel, CharField, TextField, SelectionField, Many2OneField,
    BooleanField, One2ManyField, IntegerField, FloatField, DateTimeField
)
from addons.core_base.models.base_mixins import KidsClothingMixin


class CustomField(BaseModel, KidsClothingMixin):
    """Custom Field Model"""
    
    _name = 'custom.field'
    _description = 'Custom Field'
    _order = 'sequence, name'
    
    # Basic Information
    name = CharField('Field Name', required=True, size=200)
    field_name = CharField('Technical Name', required=True, size=100)
    label = CharField('Field Label', required=True, size=200)
    help_text = TextField('Help Text')
    
    # Field Configuration
    model_name = CharField('Model Name', required=True, size=100)
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
    
    # Field Validation
    validation_rules = TextField('Validation Rules', help='JSON validation rules')
    min_value = FloatField('Minimum Value')
    max_value = FloatField('Maximum Value')
    min_length = IntegerField('Minimum Length')
    max_length = IntegerField('Maximum Length')
    
    # Field Dependencies
    depends_on_ids = One2ManyField('custom.field.dependency', 'field_id', 'Dependencies')
    
    # Field Permissions
    permission_ids = One2ManyField('custom.field.permission', 'field_id', 'Permissions')
    
    # Field History
    version = IntegerField('Version', default=1)
    migration_ids = One2ManyField('custom.field.migration', 'field_id', 'Migrations')
    
    # Access Control
    user_id = Many2OneField('users.user', 'Created By', required=True)
    group_ids = One2ManyField('users.group', 'field_group_ids', 'Access Groups')
    
    def create_field_in_model(self):
        """Create field in the target model"""
        try:
            # Get field type configuration
            field_type = self.field_type_id
            
            # Create field definition
            field_definition = self._get_field_definition()
            
            # Add field to model
            self._add_field_to_model(field_definition)
            
            # Create migration record
            self._create_migration_record('create', field_definition)
            
            return True
            
        except Exception as e:
            raise e
    
    def update_field_in_model(self, old_definition):
        """Update field in the target model"""
        try:
            # Get new field definition
            new_definition = self._get_field_definition()
            
            # Update field in model
            self._update_field_in_model(old_definition, new_definition)
            
            # Create migration record
            self._create_migration_record('update', new_definition, old_definition)
            
            # Increment version
            self.write({'version': self.version + 1})
            
            return True
            
        except Exception as e:
            raise e
    
    def delete_field_from_model(self):
        """Delete field from the target model"""
        try:
            # Get field definition
            field_definition = self._get_field_definition()
            
            # Remove field from model
            self._remove_field_from_model(field_definition)
            
            # Create migration record
            self._create_migration_record('delete', field_definition)
            
            # Mark as inactive
            self.write({'active': False})
            
            return True
            
        except Exception as e:
            raise e
    
    def _get_field_definition(self):
        """Get field definition based on field type"""
        field_type = self.field_type_id
        
        definition = {
            'name': self.field_name,
            'string': self.label,
            'help': self.help_text,
            'required': self.required,
            'readonly': self.readonly,
            'invisible': self.invisible,
            'default': self.default_value,
            'sequence': self.sequence,
        }
        
        # Add type-specific properties
        if field_type.code == 'char':
            definition.update({
                'size': self.max_length or 255,
                'min_length': self.min_length,
                'max_length': self.max_length,
            })
        elif field_type.code == 'text':
            definition.update({
                'min_length': self.min_length,
                'max_length': self.max_length,
            })
        elif field_type.code == 'integer':
            definition.update({
                'min_value': self.min_value,
                'max_value': self.max_value,
            })
        elif field_type.code == 'float':
            definition.update({
                'min_value': self.min_value,
                'max_value': self.max_value,
                'digits': (16, 2),  # Default precision
            })
        elif field_type.code == 'selection':
            definition.update({
                'selection': self._get_selection_values(),
            })
        elif field_type.code == 'many2one':
            definition.update({
                'comodel_name': self._get_related_model(),
            })
        
        return definition
    
    def _get_selection_values(self):
        """Get selection values for selection fields"""
        # Implementation to get selection values
        return [
            ('option1', 'Option 1'),
            ('option2', 'Option 2'),
        ]
    
    def _get_related_model(self):
        """Get related model for relational fields"""
        # Implementation to get related model
        return 'res.partner'
    
    def _add_field_to_model(self, field_definition):
        """Add field to the target model"""
        # Implementation to add field to model
        # This would integrate with the ORM system
        pass
    
    def _update_field_in_model(self, old_definition, new_definition):
        """Update field in the target model"""
        # Implementation to update field in model
        pass
    
    def _remove_field_from_model(self, field_definition):
        """Remove field from the target model"""
        # Implementation to remove field from model
        pass
    
    def _create_migration_record(self, operation, new_definition, old_definition=None):
        """Create migration record"""
        migration_data = {
            'field_id': self.id,
            'operation': operation,
            'new_definition': str(new_definition),
            'old_definition': str(old_definition) if old_definition else None,
            'user_id': self.env.uid,
        }
        
        self.env['custom.field.migration'].create(migration_data)
    
    def validate_field(self):
        """Validate field configuration"""
        errors = []
        
        # Check field name uniqueness
        existing_field = self.env['custom.field'].search([
            ('field_name', '=', self.field_name),
            ('model_name', '=', self.model_name),
            ('id', '!=', self.id),
        ])
        
        if existing_field:
            errors.append(f"Field name '{self.field_name}' already exists in model '{self.model_name}'")
        
        # Check field type compatibility
        if self.field_type_id.code in ['integer', 'float']:
            if self.min_value and self.max_value and self.min_value > self.max_value:
                errors.append("Minimum value cannot be greater than maximum value")
        
        # Check length constraints
        if self.min_length and self.max_length and self.min_length > self.max_length:
            errors.append("Minimum length cannot be greater than maximum length")
        
        return errors
    
    def get_field_summary(self):
        """Get field summary"""
        return {
            'id': self.id,
            'name': self.name,
            'field_name': self.field_name,
            'label': self.label,
            'model_name': self.model_name,
            'field_type': self.field_type_id.name,
            'required': self.required,
            'readonly': self.readonly,
            'sequence': self.sequence,
            'version': self.version,
            'active': self.active,
            'create_date': self.create_date,
        }
    
    def duplicate_field(self, new_name=None):
        """Duplicate field"""
        new_name = new_name or f"{self.name} (Copy)"
        
        new_field = self.create({
            'name': new_name,
            'field_name': f"{self.field_name}_copy",
            'label': f"{self.label} (Copy)",
            'help_text': self.help_text,
            'model_name': self.model_name,
            'field_type_id': self.field_type_id.id,
            'field_group_id': self.field_group_id.id,
            'required': self.required,
            'readonly': self.readonly,
            'invisible': self.invisible,
            'default_value': self.default_value,
            'sequence': self.sequence,
            'validation_rules': self.validation_rules,
            'min_value': self.min_value,
            'max_value': self.max_value,
            'min_length': self.min_length,
            'max_length': self.max_length,
            'user_id': self.user_id.id,
        })
        
        return new_field


class CustomFieldDependency(BaseModel, KidsClothingMixin):
    """Custom Field Dependency Model"""
    
    _name = 'custom.field.dependency'
    _description = 'Custom Field Dependency'
    
    field_id = Many2OneField('custom.field', 'Field', required=True)
    depends_on_field = CharField('Depends On Field', required=True, size=100)
    condition = SelectionField([
        ('equal', 'Equal'),
        ('not_equal', 'Not Equal'),
        ('greater', 'Greater Than'),
        ('less', 'Less Than'),
        ('contains', 'Contains'),
        ('not_contains', 'Not Contains'),
    ], 'Condition', required=True)
    value = CharField('Value', size=200)
    
    def evaluate_dependency(self, record):
        """Evaluate dependency condition"""
        field_value = getattr(record, self.depends_on_field, '')
        
        if self.condition == 'equal':
            return str(field_value) == self.value
        elif self.condition == 'not_equal':
            return str(field_value) != self.value
        elif self.condition == 'greater':
            return float(field_value) > float(self.value)
        elif self.condition == 'less':
            return float(field_value) < float(self.value)
        elif self.condition == 'contains':
            return self.value in str(field_value)
        elif self.condition == 'not_contains':
            return self.value not in str(field_value)
        
        return False