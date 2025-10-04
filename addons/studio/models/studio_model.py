#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Studio Model
===============================

Studio model management for customization projects.
"""

from core_framework.orm import (
    BaseModel, CharField, TextField, SelectionField, Many2OneField,
    BooleanField, One2ManyField, IntegerField, DateTimeField, FloatField
)
from addons.core_base.models.base_mixins import KidsClothingMixin


class StudioModel(BaseModel, KidsClothingMixin):
    """Studio Model for Custom Model Creation"""
    
    _name = 'studio.model'
    _description = 'Studio Model'
    _order = 'sequence, name'
    
    # Basic Information
    name = CharField('Model Name', required=True, size=200)
    technical_name = CharField('Technical Name', required=True, size=100)
    description = TextField('Description')
    project_id = Many2OneField('studio.project', 'Project', required=True)
    
    # Model Configuration
    model_type = SelectionField([
        ('base', 'Base Model'),
        ('extension', 'Model Extension'),
        ('custom', 'Custom Model'),
        ('transient', 'Transient Model'),
    ], 'Model Type', default='custom')
    
    parent_model = CharField('Parent Model', size=100, 
                           help='Parent model to inherit from')
    
    # Model Settings
    sequence = IntegerField('Sequence', default=10)
    active = BooleanField('Active', default=True)
    is_published = BooleanField('Published', default=False)
    
    # Model Statistics
    field_count = IntegerField('Field Count', default=0)
    view_count = IntegerField('View Count', default=0)
    record_count = IntegerField('Record Count', default=0)
    
    # Model Components
    field_ids = One2ManyField('studio.field', 'model_id', 'Fields')
    view_ids = One2ManyField('studio.view', 'model_id', 'Views')
    form_ids = One2ManyField('studio.form', 'model_id', 'Forms')
    workflow_ids = One2ManyField('studio.workflow', 'model_id', 'Workflows')
    
    # Access Control
    user_id = Many2OneField('users.user', 'Created By', required=True)
    group_ids = One2ManyField('users.group', 'model_group_ids', 'Access Groups')
    
    def generate_model_code(self):
        """Generate Python model code"""
        code_lines = []
        
        # Add imports
        code_lines.append("from core_framework.orm import BaseModel, CharField, TextField, BooleanField")
        code_lines.append("from addons.core_base.models.base_mixins import KidsClothingMixin")
        code_lines.append("")
        
        # Add class definition
        code_lines.append(f"class {self._get_class_name()}(BaseModel, KidsClothingMixin):")
        code_lines.append(f'    """{self.description or self.name}"""')
        code_lines.append("")
        code_lines.append(f"    _name = '{self.technical_name}'")
        code_lines.append(f"    _description = '{self.description or self.name}'")
        code_lines.append("")
        
        # Add fields
        for field in self.field_ids:
            field_code = field.generate_field_code()
            code_lines.append(f"    {field_code}")
        
        # Add methods
        code_lines.append("")
        code_lines.append("    def get_model_summary(self):")
        code_lines.append("        \"\"\"Get model summary\"\"\"")
        code_lines.append("        return {")
        code_lines.append(f"            'name': '{self.name}',")
        code_lines.append(f"            'technical_name': '{self.technical_name}',")
        code_lines.append(f"            'field_count': {self.field_count},")
        code_lines.append(f"            'view_count': {self.view_count},")
        code_lines.append("        }")
        
        return "\n".join(code_lines)
    
    def _get_class_name(self):
        """Get Python class name from technical name"""
        parts = self.technical_name.split('.')
        return ''.join(word.capitalize() for word in parts)
    
    def deploy_model(self):
        """Deploy model to system"""
        try:
            # Generate model code
            model_code = self.generate_model_code()
            
            # Create model file
            model_file_path = f"addons/{self.project_id.code}/models/{self.technical_name.replace('.', '_')}.py"
            
            # Write model file
            with open(model_file_path, 'w') as f:
                f.write(model_code)
            
            # Update statistics
            self.write({
                'field_count': len(self.field_ids),
                'view_count': len(self.view_ids),
                'is_published': True,
            })
            
            return True
            
        except Exception as e:
            raise e
    
    def get_model_summary(self):
        """Get model summary"""
        return {
            'id': self.id,
            'name': self.name,
            'technical_name': self.technical_name,
            'model_type': self.model_type,
            'field_count': self.field_count,
            'view_count': self.view_count,
            'record_count': self.record_count,
            'is_published': self.is_published,
        }