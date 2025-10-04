#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Field Group Model
====================================

Field group management for organizing custom fields.
"""

from core_framework.orm import (
    BaseModel, CharField, TextField, SelectionField, Many2OneField,
    BooleanField, One2ManyField, IntegerField, ImageField
)
from addons.core_base.models.base_mixins import KidsClothingMixin


class FieldGroup(BaseModel, KidsClothingMixin):
    """Field Group Model for Organizing Custom Fields"""
    
    _name = 'custom.field.group'
    _description = 'Custom Field Group'
    _order = 'sequence, name'
    
    # Basic Information
    name = CharField('Group Name', required=True, size=200)
    technical_name = CharField('Technical Name', required=True, size=100)
    description = TextField('Description')
    
    # Group Configuration
    group_type = SelectionField([
        ('model', 'Model Group'),
        ('category', 'Category Group'),
        ('functional', 'Functional Group'),
        ('custom', 'Custom Group'),
    ], 'Group Type', default='category')
    
    # Group Hierarchy
    parent_id = Many2OneField('custom.field.group', 'Parent Group')
    child_ids = One2ManyField('custom.field.group', 'parent_id', 'Sub Groups')
    
    # Group Settings
    sequence = IntegerField('Sequence', default=10)
    active = BooleanField('Active', default=True)
    is_system = BooleanField('System Group', default=False)
    
    # Group Properties
    color = CharField('Color', size=20, default='#000000')
    icon = CharField('Icon', size=100)
    image = ImageField('Group Image')
    
    # Group Content
    field_ids = One2ManyField('custom.field', 'field_group_id', 'Fields')
    field_count = IntegerField('Field Count', default=0)
    
    # Group Access
    user_id = Many2OneField('users.user', 'Created By', required=True)
    group_ids = One2ManyField('users.group', 'field_group_access_ids', 'Access Groups')
    
    def add_field(self, field_id):
        """Add field to group"""
        field = self.env['custom.field'].browse(field_id)
        if field:
            field.write({'field_group_id': self.id})
            self.write({'field_count': self.field_count + 1})
            return True
        return False
    
    def remove_field(self, field_id):
        """Remove field from group"""
        field = self.env['custom.field'].browse(field_id)
        if field and field.field_group_id.id == self.id:
            field.write({'field_group_id': False})
            self.write({'field_count': max(0, self.field_count - 1)})
            return True
        return False
    
    def get_group_hierarchy(self):
        """Get group hierarchy"""
        hierarchy = []
        current_group = self
        
        while current_group:
            hierarchy.insert(0, {
                'id': current_group.id,
                'name': current_group.name,
                'technical_name': current_group.technical_name,
            })
            current_group = current_group.parent_id
        
        return hierarchy
    
    def get_all_fields(self):
        """Get all fields in group and sub-groups"""
        all_fields = []
        
        # Add fields from current group
        all_fields.extend(self.field_ids)
        
        # Add fields from sub-groups
        for child_group in self.child_ids:
            all_fields.extend(child_group.get_all_fields())
        
        return all_fields
    
    def get_group_summary(self):
        """Get group summary"""
        return {
            'id': self.id,
            'name': self.name,
            'technical_name': self.technical_name,
            'group_type': self.group_type,
            'field_count': self.field_count,
            'child_count': len(self.child_ids),
            'parent_name': self.parent_id.name if self.parent_id else None,
            'is_system': self.is_system,
        }


class FieldGroupTemplate(BaseModel, KidsClothingMixin):
    """Field Group Template for Predefined Groups"""
    
    _name = 'custom.field.group.template'
    _description = 'Field Group Template'
    
    name = CharField('Template Name', required=True, size=200)
    description = TextField('Description')
    
    # Template Configuration
    group_config = TextField('Group Configuration', 
                           help='JSON group configuration')
    field_templates = TextField('Field Templates', 
                               help='JSON field templates')
    
    # Template Usage
    usage_count = IntegerField('Usage Count', default=0)
    is_public = BooleanField('Public Template', default=False)
    
    def create_group_from_template(self, group_name, model_name=None):
        """Create group from template"""
        try:
            # Parse group configuration
            group_config = self._parse_group_config()
            
            # Create group
            group_data = {
                'name': group_name,
                'technical_name': group_name.lower().replace(' ', '_'),
                'description': group_config.get('description', ''),
                'group_type': group_config.get('group_type', 'custom'),
                'color': group_config.get('color', '#000000'),
                'icon': group_config.get('icon', ''),
                'user_id': self.env.uid,
            }
            
            group = self.env['custom.field.group'].create(group_data)
            
            # Create fields from templates
            if model_name:
                self._create_fields_from_template(group.id, model_name)
            
            # Update usage count
            self.write({'usage_count': self.usage_count + 1})
            
            return group
            
        except Exception as e:
            raise e
    
    def _parse_group_config(self):
        """Parse group configuration"""
        # Parse JSON group configuration
        import json
        try:
            return json.loads(self.group_config) if self.group_config else {}
        except:
            return {}
    
    def _create_fields_from_template(self, group_id, model_name):
        """Create fields from template"""
        # Parse field templates and create fields
        import json
        try:
            field_templates = json.loads(self.field_templates) if self.field_templates else []
            
            for field_template in field_templates:
                field_data = {
                    'name': field_template.get('name', ''),
                    'field_name': field_template.get('field_name', ''),
                    'label': field_template.get('label', ''),
                    'model_name': model_name,
                    'field_group_id': group_id,
                    'field_type_id': self._get_field_type_id(field_template.get('field_type')),
                    'user_id': self.env.uid,
                }
                
                self.env['custom.field'].create(field_data)
                
        except Exception as e:
            raise e
    
    def _get_field_type_id(self, field_type_name):
        """Get field type ID by name"""
        field_type = self.env['custom.field.type'].search([('technical_name', '=', field_type_name)], limit=1)
        return field_type.id if field_type else False
    
    def get_template_summary(self):
        """Get template summary"""
        return {
            'id': self.id,
            'name': self.name,
            'usage_count': self.usage_count,
            'is_public': self.is_public,
        }