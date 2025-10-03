# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Users - Groups Management
===========================================

Standalone version of the groups management model.
"""

from core_framework.orm import BaseModel, CharField, TextField, BooleanField, IntegerField, DateTimeField, Many2OneField, SelectionField, One2ManyField, Many2ManyField
from core_framework.orm import Field
from typing import Dict, Any, Optional, List
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class ResGroups(BaseModel):
    """Extended groups model for Kids Clothing ERP"""
    
    _name = 'ocean.groups'
    _description = 'Groups'
    _table = 'res_groups'
    
    # Basic group information
    name = CharField(
        string='Name',
        size=100,
        required=True,
        help='Group name'
    )
    
    description = TextField(
        string='Description',
        help='Detailed description of the group'
    )
    
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
        help='Group category'
    )
    
    # Group hierarchy
    parent_id = IntegerField(
        string='Parent Group ID',
        help='Parent group in hierarchy'
    )
    
    child_ids = One2ManyField(
        string='Child Groups',
        comodel_name='ocean.groups',
        inverse_name='parent_id',
        help='Child groups in hierarchy'
    )
    
    # Group permissions
    permission_ids = Many2ManyField(
        string='Permissions',
        comodel_name='user.permissions',
        help='Permissions assigned to this group'
    )
    
    # Group settings
    is_system_group = BooleanField(
        string='System Group',
        default=False,
        help='Whether this is a system group (cannot be deleted)'
    )
    
    is_active = BooleanField(
        string='Active',
        default=True,
        help='Whether the group is active'
    )
    
    # Group analytics
    user_count = IntegerField(
        string='User Count',
        default=0,
        help='Number of users in this group'
    )
    
    last_used = DateTimeField(
        string='Last Used',
        help='When this group was last used'
    )
    
    # Group access control
    access_level = SelectionField(
        string='Access Level',
        selection=[
            ('read', 'Read Only'),
            ('write', 'Read/Write'),
            ('admin', 'Administrator'),
            ('super', 'Super User'),
        ],
        default='read',
        help='Access level for this group'
    )
    
    # Group restrictions
    ip_restrictions = TextField(
        string='IP Restrictions',
        help='Comma-separated list of allowed IP addresses'
    )
    
    time_restrictions = TextField(
        string='Time Restrictions',
        help='Time restrictions for group access (e.g., 9:00-17:00)'
    )
    
    # Group notifications
    notification_enabled = BooleanField(
        string='Notifications Enabled',
        default=True,
        help='Enable notifications for this group'
    )
    
    notification_types = SelectionField(
        string='Notification Types',
        selection=[
            ('email', 'Email'),
            ('sms', 'SMS'),
            ('push', 'Push Notification'),
            ('in_app', 'In-App'),
        ],
        default='email',
        help='Types of notifications for this group'
    )
    
    def create(self, vals: Dict[str, Any]):
        """Override create to set default values"""
        # Set default category if not provided
        if 'category' not in vals:
            vals['category'] = 'custom'
        
        return super().create(vals)
    
    def write(self, vals: Dict[str, Any]):
        """Override write to handle group updates"""
        result = super().write(vals)
        
        # Update last used timestamp
        if vals:
            self.last_used = datetime.now()
        
        return result
    
    def unlink(self):
        """Override unlink to prevent deletion of system groups"""
        for group in self:
            if group.is_system_group:
                raise ValueError('System groups cannot be deleted')
        
        return super().unlink()
    
    def add_user(self, user_id: int):
        """Add user to this group"""
        self.ensure_one()
        
        # In standalone version, we'll implement basic group assignment
        logger.info(f"Adding user {user_id} to group {self.name}")
        
        # Log group assignment
        logger.info(f"User {user_id} added to group: {self.name}")
    
    def remove_user(self, user_id: int):
        """Remove user from this group"""
        self.ensure_one()
        
        # In standalone version, we'll implement basic group removal
        logger.info(f"Removing user {user_id} from group {self.name}")
        
        # Log group removal
        logger.info(f"User {user_id} removed from group: {self.name}")
    
    def get_group_permissions(self):
        """Get all permissions for this group"""
        permissions = set()
        
        # Get permissions from group
        for permission in self.permission_ids:
            permissions.add(permission.name)
        
        # Get permissions from parent groups
        if self.parent_id:
            parent_group = self.search([('id', '=', self.parent_id)])
            if parent_group:
                parent_permissions = parent_group.get_group_permissions()
                permissions.update(parent_permissions)
        
        return list(permissions)
    
    def has_permission(self, permission_name: str):
        """Check if group has specific permission"""
        return permission_name in self.get_group_permissions()
    
    def get_group_users(self):
        """Get all users in this group"""
        # In standalone version, we'll return basic user info
        return []
    
    def get_group_hierarchy(self):
        """Get group hierarchy"""
        hierarchy = []
        current_group = self
        
        while current_group:
            hierarchy.insert(0, current_group)
            if current_group.parent_id:
                current_group = self.search([('id', '=', current_group.parent_id)])
            else:
                current_group = None
        
        return hierarchy
    
    def get_child_groups(self):
        """Get all child groups"""
        child_groups = []
        
        for child in self.child_ids:
            child_groups.append(child)
            child_groups.extend(child.get_child_groups())
        
        return child_groups
    
    def get_group_statistics(self):
        """Get group statistics"""
        return {
            'user_count': self.user_count,
            'permission_count': len(self.permission_ids),
            'child_group_count': len(self.child_ids),
            'is_system_group': self.is_system_group,
            'is_active': self.is_active,
            'access_level': self.access_level,
            'last_used': self.last_used,
        }
    
    @classmethod
    def get_groups_by_category(cls, category: str):
        """Get groups by category"""
        return cls.search([
            ('category', '=', category),
            ('is_active', '=', True),
        ])
    
    @classmethod
    def get_system_groups(cls):
        """Get all system groups"""
        return cls.search([
            ('is_system_group', '=', True),
            ('is_active', '=', True),
        ])
    
    @classmethod
    def get_custom_groups(cls):
        """Get all custom groups"""
        return cls.search([
            ('is_system_group', '=', False),
            ('is_active', '=', True),
        ])
    
    @classmethod
    def get_group_analytics(cls):
        """Get group analytics"""
        # In standalone version, we'll return mock data
        return {
            'total_groups': 0,
            'active_groups': 0,
            'system_groups': 0,
            'custom_groups': 0,
            'inactive_groups': 0,
            'active_percentage': 0,
        }
    
    def _check_parent_group(self):
        """Validate parent group"""
        if self.parent_id and self.parent_id == self.id:
            raise ValueError('Group cannot be its own parent')
        
        if self.parent_id:
            # Check for circular reference
            current = self.search([('id', '=', self.parent_id)])
            while current:
                if current.id == self.id:
                    raise ValueError('Circular reference in group hierarchy')
                if current.parent_id:
                    current = self.search([('id', '=', current.parent_id)])
                else:
                    current = None
    
    def _check_access_level(self):
        """Validate access level"""
        if self.access_level == 'super' and not self.is_system_group:
            raise ValueError('Only system groups can have super access level')
    
    def action_activate(self):
        """Activate group"""
        self.is_active = True
        return True
    
    def action_deactivate(self):
        """Deactivate group"""
        self.is_active = False
        return True
    
    def action_duplicate(self):
        """Duplicate group"""
        self.ensure_one()
        
        new_group = self.copy({
            'name': f'{self.name} (Copy)',
            'is_system_group': False,
        })
        
        return new_group
    
    def action_export_permissions(self):
        """Export group permissions"""
        self.ensure_one()
        
        permissions = []
        for permission in self.permission_ids:
            permissions.append({
                'name': permission.name,
                'description': permission.description,
                'model': permission.model_name,
                'access_level': permission.access_level,
            })
        
        return permissions
    
    def action_import_permissions(self, permissions_data: List[Dict]):
        """Import group permissions"""
        self.ensure_one()
        
        imported_count = 0
        for perm_data in permissions_data:
            permission = self.search([
                ('name', '=', perm_data['name']),
                ('model_name', '=', perm_data['model']),
            ], limit=1)
            
            if permission:
                self.permission_ids = [(4, permission.id)]
                imported_count += 1
        
        return imported_count