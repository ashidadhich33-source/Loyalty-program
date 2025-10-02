# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Users - User Permissions
===========================================

Standalone version of the user permissions model.
"""

from core_framework.orm import BaseModel, CharField, TextField, BooleanField, IntegerField, DateTimeField, Many2OneField, SelectionField
from core_framework.orm import Field
from typing import Dict, Any, Optional
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class UserPermissions(BaseModel):
    """User permissions model for Kids Clothing ERP"""
    
    _name = 'user.permissions'
    _description = 'User Permissions'
    _table = 'user_permissions'
    
    # Basic permission information
    name = CharField(
        string='Name',
        size=100,
        required=True,
        help='Permission name'
    )
    
    description = TextField(
        string='Description',
        help='Permission description'
    )
    
    model_name = CharField(
        string='Model Name',
        size=100,
        help='Model this permission applies to'
    )
    
    access_level = SelectionField(
        string='Access Level',
        selection=[
            ('read', 'Read Only'),
            ('write', 'Read/Write'),
            ('create', 'Create'),
            ('delete', 'Delete'),
            ('admin', 'Administrator'),
        ],
        default='read',
        help='Access level for this permission'
    )
    
    # Permission settings
    is_active = BooleanField(
        string='Active',
        default=True,
        help='Whether the permission is active'
    )
    
    is_system_permission = BooleanField(
        string='System Permission',
        default=False,
        help='Whether this is a system permission'
    )
    
    # Permission category
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
        help='Permission category'
    )
    
    # Permission restrictions
    ip_restrictions = TextField(
        string='IP Restrictions',
        help='Comma-separated list of allowed IP addresses'
    )
    
    time_restrictions = TextField(
        string='Time Restrictions',
        help='Time restrictions for permission access'
    )
    
    # Permission metadata
    created_by = IntegerField(
        string='Created By',
        help='User who created this permission'
    )
    
    created_date = DateTimeField(
        string='Created Date',
        default=datetime.now,
        help='Date when permission was created'
    )
    
    updated_by = IntegerField(
        string='Updated By',
        help='User who last updated this permission'
    )
    
    updated_date = DateTimeField(
        string='Updated Date',
        help='Date when permission was last updated'
    )
    
    def create(self, vals: Dict[str, Any]):
        """Override create to set default values"""
        # Set default category if not provided
        if 'category' not in vals:
            vals['category'] = 'custom'
        
        # Set created date
        if 'created_date' not in vals:
            vals['created_date'] = datetime.now()
        
        return super().create(vals)
    
    def write(self, vals: Dict[str, Any]):
        """Override write to handle permission updates"""
        # Set updated date
        vals['updated_date'] = datetime.now()
        
        result = super().write(vals)
        
        # Log permission updates
        for permission in self:
            if vals:
                logger.info(f"Permission {permission.name} updated: {', '.join(vals.keys())}")
        
        return result
    
    def unlink(self):
        """Override unlink to prevent deletion of system permissions"""
        for permission in self:
            if permission.is_system_permission:
                raise ValueError('System permissions cannot be deleted')
        
        return super().unlink()
    
    def action_activate(self):
        """Activate permission"""
        self.is_active = True
        return True
    
    def action_deactivate(self):
        """Deactivate permission"""
        self.is_active = False
        return True
    
    def get_permission_info(self):
        """Get permission information"""
        return {
            'name': self.name,
            'description': self.description,
            'model_name': self.model_name,
            'access_level': self.access_level,
            'category': self.category,
            'is_active': self.is_active,
            'is_system_permission': self.is_system_permission,
        }
    
    @classmethod
    def get_permissions_by_category(cls, category: str):
        """Get permissions by category"""
        return cls.search([
            ('category', '=', category),
            ('is_active', '=', True),
        ])
    
    @classmethod
    def get_system_permissions(cls):
        """Get all system permissions"""
        return cls.search([
            ('is_system_permission', '=', True),
            ('is_active', '=', True),
        ])
    
    @classmethod
    def get_custom_permissions(cls):
        """Get all custom permissions"""
        return cls.search([
            ('is_system_permission', '=', False),
            ('is_active', '=', True),
        ])
    
    @classmethod
    def get_permissions_by_model(cls, model_name: str):
        """Get permissions by model"""
        return cls.search([
            ('model_name', '=', model_name),
            ('is_active', '=', True),
        ])
    
    @classmethod
    def get_permission_analytics(cls):
        """Get permission analytics"""
        total_permissions = cls.search_count([])
        active_permissions = cls.search_count([('is_active', '=', True)])
        system_permissions = cls.search_count([('is_system_permission', '=', True)])
        custom_permissions = cls.search_count([('is_system_permission', '=', False)])
        
        return {
            'total_permissions': total_permissions,
            'active_permissions': active_permissions,
            'system_permissions': system_permissions,
            'custom_permissions': custom_permissions,
            'inactive_permissions': total_permissions - active_permissions,
            'active_percentage': (active_permissions / total_permissions * 100) if total_permissions > 0 else 0,
        }
    
    def _check_permission_name(self):
        """Validate permission name"""
        if not self.name:
            raise ValueError('Permission name is required')
        
        # Check for duplicate names
        existing = self.search([
            ('name', '=', self.name),
            ('id', '!=', self.id),
        ])
        if existing:
            raise ValueError('Permission name must be unique')
    
    def _check_access_level(self):
        """Validate access level"""
        valid_levels = ['read', 'write', 'create', 'delete', 'admin']
        if self.access_level not in valid_levels:
            raise ValueError(f'Invalid access level: {self.access_level}')
    
    def _check_model_name(self):
        """Validate model name"""
        if self.model_name:
            # In standalone version, we'll do basic validation
            if not self.model_name.replace('.', '').replace('_', '').isalnum():
                raise ValueError('Invalid model name format')