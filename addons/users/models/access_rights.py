# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Users - Access Rights
========================================

Standalone version of the access rights model.
"""

from core_framework.orm import BaseModel, CharField, TextField, BooleanField, IntegerField, DateTimeField, Many2OneField, SelectionField
from core_framework.orm import Field
from typing import Dict, Any, Optional, List
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class AccessRights(BaseModel):
    """Access rights model for Kids Clothing ERP"""
    
    _name = 'access.rights'
    _description = 'Access Rights'
    _table = 'access_rights'
    
    # Basic access rights information
    name = CharField(
        string='Name',
        size=100,
        required=True,
        help='Access rights name'
    )
    
    description = TextField(
        string='Description',
        help='Access rights description'
    )
    
    model_name = CharField(
        string='Model Name',
        size=100,
        required=True,
        help='Model this access right applies to'
    )
    
    # Access control
    group_id = IntegerField(
        string='Group ID',
        help='Group this access right applies to'
    )
    
    user_id = IntegerField(
        string='User ID',
        help='User this access right applies to'
    )
    
    # Access permissions
    perm_read = BooleanField(
        string='Read Access',
        default=False,
        help='Read permission'
    )
    
    perm_write = BooleanField(
        string='Write Access',
        default=False,
        help='Write permission'
    )
    
    perm_create = BooleanField(
        string='Create Access',
        default=False,
        help='Create permission'
    )
    
    perm_unlink = BooleanField(
        string='Delete Access',
        default=False,
        help='Delete permission'
    )
    
    # Access restrictions
    domain_force = TextField(
        string='Domain Force',
        help='Domain restriction for access'
    )
    
    active = BooleanField(
        string='Active',
        default=True,
        help='Whether the access right is active'
    )
    
    # Access rights category
    category = SelectionField(
        string='Category',
        selection=[
            ('core', 'Core'),
            ('sales', 'Sales'),
            ('inventory', 'Inventory'),
            ('accounting', 'Accounting'),
            ('hr', 'Human Resources'),
            ('pos', 'Point of Sale'),
            ('reports', 'Reports'),
            ('settings', 'Settings'),
            ('custom', 'Custom'),
        ],
        default='custom',
        help='Access rights category'
    )
    
    # Access rights priority
    priority = SelectionField(
        string='Priority',
        selection=[
            ('low', 'Low'),
            ('medium', 'Medium'),
            ('high', 'High'),
            ('critical', 'Critical'),
        ],
        default='medium',
        help='Access rights priority'
    )
    
    # Access rights metadata
    created_by = IntegerField(
        string='Created By',
        help='User who created this access right'
    )
    
    created_date = DateTimeField(
        string='Created Date',
        default=datetime.now,
        help='Date when access right was created'
    )
    
    updated_by = IntegerField(
        string='Updated By',
        help='User who last updated this access right'
    )
    
    updated_date = DateTimeField(
        string='Updated Date',
        help='Date when access right was last updated'
    )
    
    def create(self, vals: Dict[str, Any]):
        """Override create to set default values"""
        # Set created date
        if 'created_date' not in vals:
            vals['created_date'] = datetime.now()
        
        # Set updated date
        vals['updated_date'] = datetime.now()
        
        return super().create(vals)
    
    def write(self, vals: Dict[str, Any]):
        """Override write to handle access rights updates"""
        # Set updated date
        vals['updated_date'] = datetime.now()
        
        result = super().write(vals)
        
        # Log access rights updates
        for access_right in self:
            if vals:
                logger.info(f"Access rights {access_right.name} updated: {', '.join(vals.keys())}")
        
        return result
    
    def get_access_rights_info(self):
        """Get access rights information"""
        return {
            'name': self.name,
            'description': self.description,
            'model_name': self.model_name,
            'group_id': self.group_id,
            'user_id': self.user_id,
            'perm_read': self.perm_read,
            'perm_write': self.perm_write,
            'perm_create': self.perm_create,
            'perm_unlink': self.perm_unlink,
            'domain_force': self.domain_force,
            'active': self.active,
            'category': self.category,
            'priority': self.priority,
        }
    
    def check_access(self, operation: str, user_id: int = None, group_id: int = None):
        """Check if access is allowed for specific operation"""
        # Check if access right is active
        if not self.active:
            return False
        
        # Check if it applies to the user or group
        if user_id and self.user_id and self.user_id != user_id:
            return False
        
        if group_id and self.group_id and self.group_id != group_id:
            return False
        
        # Check specific permission
        if operation == 'read':
            return self.perm_read
        elif operation == 'write':
            return self.perm_write
        elif operation == 'create':
            return self.perm_create
        elif operation == 'unlink':
            return self.perm_unlink
        else:
            return False
    
    def get_permissions(self):
        """Get all permissions for this access right"""
        permissions = []
        
        if self.perm_read:
            permissions.append('read')
        if self.perm_write:
            permissions.append('write')
        if self.perm_create:
            permissions.append('create')
        if self.perm_unlink:
            permissions.append('unlink')
        
        return permissions
    
    @classmethod
    def get_access_rights_by_model(cls, model_name: str):
        """Get access rights by model"""
        return cls.search([
            ('model_name', '=', model_name),
            ('active', '=', True),
        ])
    
    @classmethod
    def get_access_rights_by_user(cls, user_id: int):
        """Get access rights by user"""
        return cls.search([
            ('user_id', '=', user_id),
            ('active', '=', True),
        ])
    
    @classmethod
    def get_access_rights_by_group(cls, group_id: int):
        """Get access rights by group"""
        return cls.search([
            ('group_id', '=', group_id),
            ('active', '=', True),
        ])
    
    @classmethod
    def check_user_access(cls, user_id: int, model_name: str, operation: str):
        """Check if user has access to specific model and operation"""
        # Check user-specific access rights
        user_access = cls.search([
            ('user_id', '=', user_id),
            ('model_name', '=', model_name),
            ('active', '=', True),
        ])
        
        for access_right in user_access:
            if access_right.check_access(operation, user_id=user_id):
                return True
        
        # Check group-specific access rights
        # In standalone version, we'll implement basic group checking
        group_access = cls.search([
            ('group_id', '!=', None),
            ('model_name', '=', model_name),
            ('active', '=', True),
        ])
        
        for access_right in group_access:
            if access_right.check_access(operation, group_id=access_right.group_id):
                return True
        
        return False
    
    @classmethod
    def get_access_rights_by_category(cls, category: str):
        """Get access rights by category"""
        return cls.search([
            ('category', '=', category),
            ('active', '=', True),
        ])
    
    @classmethod
    def get_access_rights_analytics(cls):
        """Get access rights analytics"""
        total_access_rights = cls.search_count([])
        active_access_rights = cls.search_count([('active', '=', True)])
        
        # Get access rights by category
        access_rights_by_category = {}
        for category in ['core', 'sales', 'inventory', 'accounting', 'hr', 'pos', 'reports', 'settings', 'custom']:
            count = cls.search_count([
                ('category', '=', category),
                ('active', '=', True),
            ])
            access_rights_by_category[category] = count
        
        # Get access rights by permission type
        read_access = cls.search_count([('perm_read', '=', True), ('active', '=', True)])
        write_access = cls.search_count([('perm_write', '=', True), ('active', '=', True)])
        create_access = cls.search_count([('perm_create', '=', True), ('active', '=', True)])
        delete_access = cls.search_count([('perm_unlink', '=', True), ('active', '=', True)])
        
        return {
            'total_access_rights': total_access_rights,
            'active_access_rights': active_access_rights,
            'inactive_access_rights': total_access_rights - active_access_rights,
            'access_rights_by_category': access_rights_by_category,
            'read_access': read_access,
            'write_access': write_access,
            'create_access': create_access,
            'delete_access': delete_access,
        }
    
    def _check_access_rights_name(self):
        """Validate access rights name"""
        if not self.name:
            raise ValueError('Access rights name is required')
        
        # Check for duplicate names
        existing = self.search([
            ('name', '=', self.name),
            ('id', '!=', self.id),
        ])
        if existing:
            raise ValueError('Access rights name must be unique')
    
    def _check_model_name(self):
        """Validate model name"""
        if not self.model_name:
            raise ValueError('Model name is required')
        
        # In standalone version, we'll do basic validation
        if not self.model_name.replace('.', '').replace('_', '').isalnum():
            raise ValueError('Invalid model name format')
    
    def _check_user_or_group(self):
        """Validate that either user_id or group_id is set"""
        if not self.user_id and not self.group_id:
            raise ValueError('Either user_id or group_id must be set')
        
        if self.user_id and self.group_id:
            raise ValueError('Cannot set both user_id and group_id')
    
    def _check_permissions(self):
        """Validate permissions"""
        if not any([self.perm_read, self.perm_write, self.perm_create, self.perm_unlink]):
            raise ValueError('At least one permission must be granted')
    
    def _check_priority(self):
        """Validate priority"""
        valid_priorities = ['low', 'medium', 'high', 'critical']
        if self.priority not in valid_priorities:
            raise ValueError(f'Invalid priority: {self.priority}')
    
    def _check_category(self):
        """Validate category"""
        valid_categories = ['core', 'sales', 'inventory', 'accounting', 'hr', 'pos', 'reports', 'settings', 'custom']
        if self.category not in valid_categories:
            raise ValueError(f'Invalid category: {self.category}')