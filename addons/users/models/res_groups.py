# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)


class ResGroups(models.Model):
    """Extended groups model for Kids Clothing ERP"""
    
    _inherit = 'res.groups'
    
    # Group information
    description = fields.Text(
        string='Description',
        help='Detailed description of the group'
    )
    
    category = fields.Selection([
        ('core', 'Core'),
        ('sales', 'Sales'),
        ('inventory', 'Inventory'),
        ('accounting', 'Accounting'),
        ('hr', 'Human Resources'),
        ('pos', 'Point of Sale'),
        ('reports', 'Reports'),
        ('settings', 'Settings'),
        ('custom', 'Custom'),
    ], string='Category', default='custom', help='Group category')
    
    # Group hierarchy
    parent_id = fields.Many2one(
        'res.groups',
        string='Parent Group',
        help='Parent group in hierarchy'
    )
    
    child_ids = fields.One2many(
        'res.groups',
        'parent_id',
        string='Child Groups',
        help='Child groups in hierarchy'
    )
    
    # Group permissions
    permission_ids = fields.Many2many(
        'user.permissions',
        'group_permission_rel',
        'group_id',
        'permission_id',
        string='Permissions',
        help='Permissions assigned to this group'
    )
    
    # Group settings
    is_system_group = fields.Boolean(
        string='System Group',
        default=False,
        help='Whether this is a system group (cannot be deleted)'
    )
    
    is_active = fields.Boolean(
        string='Active',
        default=True,
        help='Whether the group is active'
    )
    
    # Group analytics
    user_count = fields.Integer(
        string='User Count',
        compute='_compute_user_count',
        store=True,
        help='Number of users in this group'
    )
    
    last_used = fields.Datetime(
        string='Last Used',
        help='When this group was last used'
    )
    
    # Group access control
    access_level = fields.Selection([
        ('read', 'Read Only'),
        ('write', 'Read/Write'),
        ('admin', 'Administrator'),
        ('super', 'Super User'),
    ], string='Access Level', default='read', help='Access level for this group')
    
    # Group restrictions
    ip_restrictions = fields.Text(
        string='IP Restrictions',
        help='Comma-separated list of allowed IP addresses'
    )
    
    time_restrictions = fields.Text(
        string='Time Restrictions',
        help='Time restrictions for group access (e.g., 9:00-17:00)'
    )
    
    # Group notifications
    notification_enabled = fields.Boolean(
        string='Notifications Enabled',
        default=True,
        help='Enable notifications for this group'
    )
    
    notification_types = fields.Selection([
        ('email', 'Email'),
        ('sms', 'SMS'),
        ('push', 'Push Notification'),
        ('in_app', 'In-App'),
    ], string='Notification Types', default='email', help='Types of notifications for this group')
    
    @api.depends('users')
    def _compute_user_count(self):
        """Compute user count for this group"""
        for group in self:
            group.user_count = len(group.users)
    
    @api.model
    def create(self, vals):
        """Override create to set default values"""
        # Set default category if not provided
        if 'category' not in vals:
            vals['category'] = 'custom'
        
        return super(ResGroups, self).create(vals)
    
    def write(self, vals):
        """Override write to handle group updates"""
        result = super(ResGroups, self).write(vals)
        
        # Update last used timestamp
        if vals:
            self.last_used = fields.Datetime.now()
        
        return result
    
    def unlink(self):
        """Override unlink to prevent deletion of system groups"""
        for group in self:
            if group.is_system_group:
                raise ValidationError(_('System groups cannot be deleted'))
        
        return super(ResGroups, self).unlink()
    
    def add_user(self, user_id):
        """Add user to this group"""
        self.ensure_one()
        
        user = self.env['res.users'].browse(user_id)
        if user not in self.users:
            self.users = [(4, user_id)]
            
            # Log group assignment
            self.env['user.activity'].create({
                'user_id': user_id,
                'activity_type': 'group_assignment',
                'description': f'Added to group: {self.name}',
            })
    
    def remove_user(self, user_id):
        """Remove user from this group"""
        self.ensure_one()
        
        user = self.env['res.users'].browse(user_id)
        if user in self.users:
            self.users = [(3, user_id)]
            
            # Log group removal
            self.env['user.activity'].create({
                'user_id': user_id,
                'activity_type': 'group_removal',
                'description': f'Removed from group: {self.name}',
            })
    
    def get_group_permissions(self):
        """Get all permissions for this group"""
        permissions = set()
        
        # Get permissions from group
        for permission in self.permission_ids:
            permissions.add(permission.name)
        
        # Get permissions from parent groups
        if self.parent_id:
            parent_permissions = self.parent_id.get_group_permissions()
            permissions.update(parent_permissions)
        
        return list(permissions)
    
    def has_permission(self, permission_name):
        """Check if group has specific permission"""
        return permission_name in self.get_group_permissions()
    
    def get_group_users(self):
        """Get all users in this group"""
        return self.users
    
    def get_group_hierarchy(self):
        """Get group hierarchy"""
        hierarchy = []
        current_group = self
        
        while current_group:
            hierarchy.insert(0, current_group)
            current_group = current_group.parent_id
        
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
    
    @api.model
    def get_groups_by_category(self, category):
        """Get groups by category"""
        return self.search([
            ('category', '=', category),
            ('is_active', '=', True),
        ])
    
    @api.model
    def get_system_groups(self):
        """Get all system groups"""
        return self.search([
            ('is_system_group', '=', True),
            ('is_active', '=', True),
        ])
    
    @api.model
    def get_custom_groups(self):
        """Get all custom groups"""
        return self.search([
            ('is_system_group', '=', False),
            ('is_active', '=', True),
        ])
    
    @api.model
    def get_group_analytics(self):
        """Get group analytics"""
        total_groups = self.search_count([])
        active_groups = self.search_count([('is_active', '=', True)])
        system_groups = self.search_count([('is_system_group', '=', True)])
        custom_groups = self.search_count([('is_system_group', '=', False)])
        
        return {
            'total_groups': total_groups,
            'active_groups': active_groups,
            'system_groups': system_groups,
            'custom_groups': custom_groups,
            'inactive_groups': total_groups - active_groups,
            'active_percentage': (active_groups / total_groups * 100) if total_groups > 0 else 0,
        }
    
    @api.constrains('parent_id')
    def _check_parent_group(self):
        """Validate parent group"""
        for group in self:
            if group.parent_id and group.parent_id == group:
                raise ValidationError(_('Group cannot be its own parent'))
            
            if group.parent_id:
                # Check for circular reference
                current = group.parent_id
                while current:
                    if current == group:
                        raise ValidationError(_('Circular reference in group hierarchy'))
                    current = current.parent_id
    
    @api.constrains('access_level')
    def _check_access_level(self):
        """Validate access level"""
        for group in self:
            if group.access_level == 'super' and not group.is_system_group:
                raise ValidationError(_('Only system groups can have super access level'))
    
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
        
        return {
            'type': 'ir.actions.act_window',
            'name': 'Duplicated Group',
            'res_model': 'res.groups',
            'res_id': new_group.id,
            'view_mode': 'form',
            'target': 'current',
        }
    
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
    
    def action_import_permissions(self, permissions_data):
        """Import group permissions"""
        self.ensure_one()
        
        imported_count = 0
        for perm_data in permissions_data:
            permission = self.env['user.permissions'].search([
                ('name', '=', perm_data['name']),
                ('model_name', '=', perm_data['model']),
            ], limit=1)
            
            if permission:
                self.permission_ids = [(4, permission.id)]
                imported_count += 1
        
        return imported_count