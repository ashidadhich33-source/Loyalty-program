# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)


class UserPermissions(models.Model):
    """User permissions model for Kids Clothing ERP"""
    
    _name = 'user.permissions'
    _description = 'User Permissions'
    _order = 'name'
    
    # Basic fields
    name = fields.Char(
        string='Permission Name',
        required=True,
        help='Name of the permission'
    )
    
    description = fields.Text(
        string='Description',
        help='Description of the permission'
    )
    
    code = fields.Char(
        string='Code',
        required=True,
        help='Unique code for the permission'
    )
    
    # Permission details
    model_name = fields.Char(
        string='Model',
        help='Model this permission applies to'
    )
    
    access_level = fields.Selection([
        ('read', 'Read'),
        ('write', 'Write'),
        ('create', 'Create'),
        ('delete', 'Delete'),
        ('admin', 'Administrator'),
    ], string='Access Level', default='read', help='Level of access granted')
    
    # Permission scope
    scope = fields.Selection([
        ('global', 'Global'),
        ('company', 'Company'),
        ('department', 'Department'),
        ('user', 'User'),
    ], string='Scope', default='global', help='Scope of the permission')
    
    # Permission category
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
    ], string='Category', default='custom', help='Permission category')
    
    # Permission status
    is_active = fields.Boolean(
        string='Active',
        default=True,
        help='Whether the permission is active'
    )
    
    is_system_permission = fields.Boolean(
        string='System Permission',
        default=False,
        help='Whether this is a system permission (cannot be deleted)'
    )
    
    # Permission relationships
    user_id = fields.Many2one(
        'res.users',
        string='User',
        help='User this permission is assigned to'
    )
    
    group_ids = fields.Many2many(
        'res.groups',
        'group_permission_rel',
        'permission_id',
        'group_id',
        string='Groups',
        help='Groups this permission is assigned to'
    )
    
    role_ids = fields.Many2many(
        'user.role',
        'role_permission_rel',
        'permission_id',
        'role_id',
        string='Roles',
        help='Roles this permission is assigned to'
    )
    
    # Permission conditions
    condition = fields.Text(
        string='Condition',
        help='Python condition to evaluate for permission'
    )
    
    # Permission restrictions
    ip_restrictions = fields.Text(
        string='IP Restrictions',
        help='Comma-separated list of allowed IP addresses'
    )
    
    time_restrictions = fields.Text(
        string='Time Restrictions',
        help='Time restrictions for permission (e.g., 9:00-17:00)'
    )
    
    # Permission analytics
    usage_count = fields.Integer(
        string='Usage Count',
        default=0,
        help='Number of times this permission has been used'
    )
    
    last_used = fields.Datetime(
        string='Last Used',
        help='When this permission was last used'
    )
    
    # Permission dependencies
    depends_on = fields.Many2many(
        'user.permissions',
        'permission_dependency_rel',
        'permission_id',
        'dependency_id',
        string='Depends On',
        help='Permissions this permission depends on'
    )
    
    required_by = fields.Many2many(
        'user.permissions',
        'permission_dependency_rel',
        'dependency_id',
        'permission_id',
        string='Required By',
        help='Permissions that depend on this permission'
    )
    
    @api.model
    def create(self, vals):
        """Override create to set default values"""
        # Generate code if not provided
        if 'code' not in vals and 'name' in vals:
            vals['code'] = vals['name'].lower().replace(' ', '_').replace('-', '_')
        
        return super(UserPermissions, self).create(vals)
    
    def write(self, vals):
        """Override write to handle permission updates"""
        result = super(UserPermissions, self).write(vals)
        
        # Update last used timestamp
        if vals:
            self.last_used = fields.Datetime.now()
        
        return result
    
    def unlink(self):
        """Override unlink to prevent deletion of system permissions"""
        for permission in self:
            if permission.is_system_permission:
                raise ValidationError(_('System permissions cannot be deleted'))
        
        return super(UserPermissions, self).unlink()
    
    def check_permission(self, user_id, context=None):
        """Check if user has this permission"""
        user = self.env['res.users'].browse(user_id)
        
        # Check if permission is active
        if not self.is_active:
            return False
        
        # Check if user is assigned to this permission
        if self.user_id and self.user_id.id != user_id:
            return False
        
        # Check if user is in any of the groups
        if self.group_ids:
            user_groups = user.groups_id
            if not any(group in user_groups for group in self.group_ids):
                return False
        
        # Check if user has any of the roles
        if self.role_ids:
            user_roles = user.role_ids
            if not any(role in user_roles for role in self.role_ids):
                return False
        
        # Check conditions
        if self.condition:
            try:
                # Evaluate condition in user context
                eval_context = {
                    'user': user,
                    'self': self,
                    'context': context or {},
                }
                if not eval(self.condition, eval_context):
                    return False
            except Exception as e:
                _logger.error(f"Error evaluating permission condition: {str(e)}")
                return False
        
        # Check IP restrictions
        if self.ip_restrictions:
            client_ip = context.get('ip_address') if context else None
            if client_ip:
                allowed_ips = [ip.strip() for ip in self.ip_restrictions.split(',')]
                if client_ip not in allowed_ips:
                    return False
        
        # Check time restrictions
        if self.time_restrictions:
            current_time = fields.Datetime.now().time()
            # Parse time restrictions (e.g., "9:00-17:00")
            # This would need more complex parsing logic
            pass
        
        # Update usage statistics
        self.usage_count += 1
        self.last_used = fields.Datetime.now()
        
        return True
    
    def grant_permission(self, user_id):
        """Grant permission to user"""
        self.ensure_one()
        
        user = self.env['res.users'].browse(user_id)
        
        # Add to user's custom permissions
        if self not in user.custom_permissions:
            user.custom_permissions = [(4, self.id)]
            
            # Log permission grant
            self.env['user.activity'].create({
                'user_id': user_id,
                'activity_type': 'permission_grant',
                'description': f'Permission granted: {self.name}',
            })
    
    def revoke_permission(self, user_id):
        """Revoke permission from user"""
        self.ensure_one()
        
        user = self.env['res.users'].browse(user_id)
        
        # Remove from user's custom permissions
        if self in user.custom_permissions:
            user.custom_permissions = [(3, self.id)]
            
            # Log permission revocation
            self.env['user.activity'].create({
                'user_id': user_id,
                'activity_type': 'permission_revoke',
                'description': f'Permission revoked: {self.name}',
            })
    
    def get_permission_users(self):
        """Get all users with this permission"""
        users = set()
        
        # Get users from direct assignment
        if self.user_id:
            users.add(self.user_id)
        
        # Get users from groups
        for group in self.group_ids:
            users.update(group.users)
        
        # Get users from roles
        for role in self.role_ids:
            users.update(role.users)
        
        return list(users)
    
    def get_permission_statistics(self):
        """Get permission statistics"""
        return {
            'usage_count': self.usage_count,
            'last_used': self.last_used,
            'is_active': self.is_active,
            'is_system_permission': self.is_system_permission,
            'access_level': self.access_level,
            'scope': self.scope,
            'category': self.category,
            'user_count': len(self.get_permission_users()),
            'group_count': len(self.group_ids),
            'role_count': len(self.role_ids),
        }
    
    @api.model
    def get_permissions_by_category(self, category):
        """Get permissions by category"""
        return self.search([
            ('category', '=', category),
            ('is_active', '=', True),
        ])
    
    @api.model
    def get_permissions_by_model(self, model_name):
        """Get permissions by model"""
        return self.search([
            ('model_name', '=', model_name),
            ('is_active', '=', True),
        ])
    
    @api.model
    def get_system_permissions(self):
        """Get all system permissions"""
        return self.search([
            ('is_system_permission', '=', True),
            ('is_active', '=', True),
        ])
    
    @api.model
    def get_custom_permissions(self):
        """Get all custom permissions"""
        return self.search([
            ('is_system_permission', '=', False),
            ('is_active', '=', True),
        ])
    
    @api.model
    def get_permission_analytics(self):
        """Get permission analytics"""
        total_permissions = self.search_count([])
        active_permissions = self.search_count([('is_active', '=', True)])
        system_permissions = self.search_count([('is_system_permission', '=', True)])
        custom_permissions = self.search_count([('is_system_permission', '=', False)])
        
        return {
            'total_permissions': total_permissions,
            'active_permissions': active_permissions,
            'system_permissions': system_permissions,
            'custom_permissions': custom_permissions,
            'inactive_permissions': total_permissions - active_permissions,
            'active_percentage': (active_permissions / total_permissions * 100) if total_permissions > 0 else 0,
        }
    
    @api.constrains('code')
    def _check_code(self):
        """Validate permission code"""
        for permission in self:
            if permission.code:
                # Check for duplicate codes
                existing = self.search([
                    ('code', '=', permission.code),
                    ('id', '!=', permission.id),
                ])
                if existing:
                    raise ValidationError(_('Permission code must be unique'))
    
    @api.constrains('depends_on')
    def _check_dependencies(self):
        """Validate permission dependencies"""
        for permission in self:
            if permission in permission.depends_on:
                raise ValidationError(_('Permission cannot depend on itself'))
            
            # Check for circular dependencies
            for dep in permission.depends_on:
                if permission in dep.required_by:
                    raise ValidationError(_('Circular dependency detected'))
    
    def action_activate(self):
        """Activate permission"""
        self.is_active = True
        return True
    
    def action_deactivate(self):
        """Deactivate permission"""
        self.is_active = False
        return True
    
    def action_duplicate(self):
        """Duplicate permission"""
        self.ensure_one()
        
        new_permission = self.copy({
            'name': f'{self.name} (Copy)',
            'code': f'{self.code}_copy',
            'is_system_permission': False,
        })
        
        return {
            'type': 'ir.actions.act_window',
            'name': 'Duplicated Permission',
            'res_model': 'user.permissions',
            'res_id': new_permission.id,
            'view_mode': 'form',
            'target': 'current',
        }
    
    def action_export_permission(self):
        """Export permission definition"""
        self.ensure_one()
        
        return {
            'name': self.name,
            'description': self.description,
            'code': self.code,
            'model_name': self.model_name,
            'access_level': self.access_level,
            'scope': self.scope,
            'category': self.category,
            'condition': self.condition,
            'ip_restrictions': self.ip_restrictions,
            'time_restrictions': self.time_restrictions,
        }
    
    def action_import_permission(self, permission_data):
        """Import permission definition"""
        self.ensure_one()
        
        self.write(permission_data)
        return True