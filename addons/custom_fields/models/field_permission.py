#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Field Permission Model
=========================================

Field permission management for custom field access control.
"""

from core_framework.orm import (
    BaseModel, CharField, TextField, SelectionField, Many2OneField,
    BooleanField, One2ManyField, IntegerField
)
from addons.core_base.models.base_mixins import KidsClothingMixin


class FieldPermission(BaseModel, KidsClothingMixin):
    """Field Permission Model for Custom Field Access Control"""
    
    _name = 'custom.field.permission'
    _description = 'Custom Field Permission'
    _order = 'sequence, name'
    
    # Basic Information
    name = CharField('Permission Name', required=True, size=200)
    technical_name = CharField('Technical Name', required=True, size=100)
    description = TextField('Description')
    
    # Permission Configuration
    field_id = Many2OneField('custom.field', 'Field', required=True)
    model_name = CharField('Model Name', required=True, size=100)
    field_name = CharField('Field Name', required=True, size=100)
    
    # Permission Settings
    permission_type = SelectionField([
        ('read', 'Read Permission'),
        ('write', 'Write Permission'),
        ('create', 'Create Permission'),
        ('delete', 'Delete Permission'),
        ('all', 'All Permissions'),
    ], 'Permission Type', required=True)
    
    # Permission Rules
    rule_type = SelectionField([
        ('user', 'User Rule'),
        ('group', 'Group Rule'),
        ('role', 'Role Rule'),
        ('condition', 'Conditional Rule'),
        ('domain', 'Domain Rule'),
    ], 'Rule Type', required=True)
    
    # Permission Targets
    user_ids = One2ManyField('users.user', 'field_permission_user_ids', 'Users')
    group_ids = One2ManyField('users.group', 'field_permission_group_ids', 'Groups')
    role_ids = One2ManyField('users.role', 'field_permission_role_ids', 'Roles')
    
    # Permission Conditions
    condition_domain = TextField('Condition Domain', 
                                help='Domain condition for permission')
    condition_script = TextField('Condition Script', 
                                 help='Python script for permission condition')
    
    # Permission Settings
    sequence = IntegerField('Sequence', default=10)
    active = BooleanField('Active', default=True)
    is_system = BooleanField('System Permission', default=False)
    
    # Permission Inheritance
    parent_id = Many2OneField('custom.field.permission', 'Parent Permission')
    child_ids = One2ManyField('custom.field.permission', 'parent_id', 'Child Permissions')
    
    # Permission Override
    override_permission = BooleanField('Override Permission', default=False)
    override_type = SelectionField([
        ('allow', 'Allow Override'),
        ('deny', 'Deny Override'),
        ('inherit', 'Inherit Override'),
    ], 'Override Type', default='inherit')
    
    # Access Control
    user_id = Many2OneField('users.user', 'Created By', required=True)
    group_ids = One2ManyField('users.group', 'permission_group_ids', 'Access Groups')
    
    def check_permission(self, user_id, operation='read'):
        """Check if user has permission for field operation"""
        try:
            # Check user-specific permissions
            if self.rule_type == 'user' and user_id in [u.id for u in self.user_ids]:
                return self._check_operation_permission(operation)
            
            # Check group permissions
            if self.rule_type == 'group':
                user_groups = self._get_user_groups(user_id)
                if any(group.id in [g.id for g in self.group_ids] for group in user_groups):
                    return self._check_operation_permission(operation)
            
            # Check role permissions
            if self.rule_type == 'role':
                user_roles = self._get_user_roles(user_id)
                if any(role.id in [r.id for r in self.role_ids] for role in user_roles):
                    return self._check_operation_permission(operation)
            
            # Check conditional permissions
            if self.rule_type == 'condition':
                if self._evaluate_condition(user_id):
                    return self._check_operation_permission(operation)
            
            # Check domain permissions
            if self.rule_type == 'domain':
                if self._evaluate_domain(user_id):
                    return self._check_operation_permission(operation)
            
            # Check parent permissions
            if self.parent_id:
                return self.parent_id.check_permission(user_id, operation)
            
            return False
            
        except Exception as e:
            return False
    
    def _check_operation_permission(self, operation):
        """Check if permission allows operation"""
        if self.permission_type == 'all':
            return True
        elif self.permission_type == operation:
            return True
        else:
            return False
    
    def _get_user_groups(self, user_id):
        """Get user groups"""
        user = self.env['users.user'].browse(user_id)
        return user.group_ids if user else []
    
    def _get_user_roles(self, user_id):
        """Get user roles"""
        user = self.env['users.user'].browse(user_id)
        return user.role_ids if user else []
    
    def _evaluate_condition(self, user_id):
        """Evaluate permission condition"""
        if not self.condition_script:
            return True
        
        try:
            # Execute condition script
            # This would be implemented with proper security measures
            return True
        except:
            return False
    
    def _evaluate_domain(self, user_id):
        """Evaluate permission domain"""
        if not self.condition_domain:
            return True
        
        try:
            # Parse and evaluate domain
            # This would be implemented with proper domain evaluation
            return True
        except:
            return False
    
    def grant_permission(self, user_id, operation='read'):
        """Grant permission to user"""
        try:
            if self.rule_type == 'user':
                if user_id not in [u.id for u in self.user_ids]:
                    self.write({'user_ids': [(4, user_id)]})
                return True
            else:
                return False
        except Exception as e:
            return False
    
    def revoke_permission(self, user_id):
        """Revoke permission from user"""
        try:
            if self.rule_type == 'user':
                if user_id in [u.id for u in self.user_ids]:
                    self.write({'user_ids': [(3, user_id)]})
                return True
            else:
                return False
        except Exception as e:
            return False
    
    def get_permission_summary(self):
        """Get permission summary"""
        return {
            'id': self.id,
            'name': self.name,
            'technical_name': self.technical_name,
            'permission_type': self.permission_type,
            'rule_type': self.rule_type,
            'model_name': self.model_name,
            'field_name': self.field_name,
            'user_count': len(self.user_ids),
            'group_count': len(self.group_ids),
            'role_count': len(self.role_ids),
            'is_system': self.is_system,
        }


class FieldPermissionRule(BaseModel, KidsClothingMixin):
    """Field Permission Rule for Complex Permission Logic"""
    
    _name = 'custom.field.permission.rule'
    _description = 'Custom Field Permission Rule'
    
    permission_id = Many2OneField('custom.field.permission', 'Permission', required=True)
    name = CharField('Rule Name', required=True, size=200)
    description = TextField('Description')
    
    # Rule Configuration
    rule_type = SelectionField([
        ('time_based', 'Time Based'),
        ('location_based', 'Location Based'),
        ('device_based', 'Device Based'),
        ('ip_based', 'IP Based'),
        ('custom', 'Custom Rule'),
    ], 'Rule Type', required=True)
    
    # Rule Conditions
    condition_expression = TextField('Condition Expression', 
                                    help='Expression for rule condition')
    condition_script = TextField('Condition Script', 
                                 help='Python script for rule condition')
    
    # Rule Actions
    action_type = SelectionField([
        ('allow', 'Allow'),
        ('deny', 'Deny'),
        ('log', 'Log Only'),
        ('notify', 'Notify'),
    ], 'Action Type', required=True)
    
    # Rule Settings
    active = BooleanField('Active', default=True)
    priority = IntegerField('Priority', default=10)
    
    def evaluate_rule(self, context):
        """Evaluate permission rule"""
        try:
            if self.rule_type == 'time_based':
                return self._evaluate_time_rule(context)
            elif self.rule_type == 'location_based':
                return self._evaluate_location_rule(context)
            elif self.rule_type == 'device_based':
                return self._evaluate_device_rule(context)
            elif self.rule_type == 'ip_based':
                return self._evaluate_ip_rule(context)
            elif self.rule_type == 'custom':
                return self._evaluate_custom_rule(context)
            else:
                return False
        except Exception as e:
            return False
    
    def _evaluate_time_rule(self, context):
        """Evaluate time-based rule"""
        # Implementation would check time conditions
        return True
    
    def _evaluate_location_rule(self, context):
        """Evaluate location-based rule"""
        # Implementation would check location conditions
        return True
    
    def _evaluate_device_rule(self, context):
        """Evaluate device-based rule"""
        # Implementation would check device conditions
        return True
    
    def _evaluate_ip_rule(self, context):
        """Evaluate IP-based rule"""
        # Implementation would check IP conditions
        return True
    
    def _evaluate_custom_rule(self, context):
        """Evaluate custom rule"""
        # Implementation would execute custom rule script
        return True