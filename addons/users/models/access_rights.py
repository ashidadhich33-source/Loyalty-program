# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)


class AccessRights(models.Model):
    """Access rights model for Kids Clothing ERP"""
    
    _name = 'access.rights'
    _description = 'Access Rights'
    _order = 'name'
    
    # Basic fields
    name = fields.Char(
        string='Access Right Name',
        required=True,
        help='Name of the access right'
    )
    
    description = fields.Text(
        string='Description',
        help='Description of the access right'
    )
    
    code = fields.Char(
        string='Code',
        required=True,
        help='Unique code for the access right'
    )
    
    # Access right details
    model_name = fields.Char(
        string='Model',
        required=True,
        help='Model this access right applies to'
    )
    
    access_type = fields.Selection([
        ('read', 'Read'),
        ('write', 'Write'),
        ('create', 'Create'),
        ('delete', 'Delete'),
        ('admin', 'Administrator'),
    ], string='Access Type', required=True, help='Type of access granted')
    
    # Access right scope
    scope = fields.Selection([
        ('global', 'Global'),
        ('company', 'Company'),
        ('department', 'Department'),
        ('user', 'User'),
        ('record', 'Record'),
    ], string='Scope', default='global', help='Scope of the access right')
    
    # Access right category
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
    ], string='Category', default='custom', help='Access right category')
    
    # Access right status
    is_active = fields.Boolean(
        string='Active',
        default=True,
        help='Whether the access right is active'
    )
    
    is_system_right = fields.Boolean(
        string='System Right',
        default=False,
        help='Whether this is a system access right (cannot be deleted)'
    )
    
    # Access right relationships
    user_id = fields.Many2one(
        'res.users',
        string='User',
        help='User this access right is assigned to'
    )
    
    group_id = fields.Many2one(
        'res.groups',
        string='Group',
        help='Group this access right is assigned to'
    )
    
    role_id = fields.Many2one(
        'user.role',
        string='Role',
        help='Role this access right is assigned to'
    )
    
    # Access right conditions
    domain = fields.Text(
        string='Domain',
        help='Domain condition for record-level access'
    )
    
    condition = fields.Text(
        string='Condition',
        help='Python condition to evaluate for access'
    )
    
    # Access right restrictions
    ip_restrictions = fields.Text(
        string='IP Restrictions',
        help='Comma-separated list of allowed IP addresses'
    )
    
    time_restrictions = fields.Text(
        string='Time Restrictions',
        help='Time restrictions for access (e.g., 9:00-17:00)'
    )
    
    # Access right analytics
    usage_count = fields.Integer(
        string='Usage Count',
        default=0,
        help='Number of times this access right has been used'
    )
    
    last_used = fields.Datetime(
        string='Last Used',
        help='When this access right was last used'
    )
    
    # Access right dependencies
    depends_on = fields.Many2many(
        'access.rights',
        'access_right_dependency_rel',
        'access_right_id',
        'dependency_id',
        string='Depends On',
        help='Access rights this access right depends on'
    )
    
    required_by = fields.Many2many(
        'access.rights',
        'access_right_dependency_rel',
        'dependency_id',
        'access_right_id',
        string='Required By',
        help='Access rights that depend on this access right'
    )
    
    @api.model
    def create(self, vals):
        """Override create to set default values"""
        # Generate code if not provided
        if 'code' not in vals and 'name' in vals:
            vals['code'] = vals['name'].lower().replace(' ', '_').replace('-', '_')
        
        return super(AccessRights, self).create(vals)
    
    def write(self, vals):
        """Override write to handle access right updates"""
        result = super(AccessRights, self).write(vals)
        
        # Update last used timestamp
        if vals:
            self.last_used = fields.Datetime.now()
        
        return result
    
    def unlink(self):
        """Override unlink to prevent deletion of system access rights"""
        for access_right in self:
            if access_right.is_system_right:
                raise ValidationError(_('System access rights cannot be deleted'))
        
        return super(AccessRights, self).unlink()
    
    def check_access(self, user_id, record_id=None, context=None):
        """Check if user has this access right"""
        user = self.env['res.users'].browse(user_id)
        
        # Check if access right is active
        if not self.is_active:
            return False
        
        # Check if user is assigned to this access right
        if self.user_id and self.user_id.id != user_id:
            return False
        
        # Check if user is in the group
        if self.group_id and self.group_id not in user.groups_id:
            return False
        
        # Check if user has the role
        if self.role_id and self.role_id not in user.role_ids:
            return False
        
        # Check domain for record-level access
        if self.domain and record_id:
            try:
                domain = eval(self.domain)
                record = self.env[self.model_name].browse(record_id)
                if not record.exists():
                    return False
                
                # Check if record matches domain
                if not self.env[self.model_name].search(domain + [('id', '=', record_id)]):
                    return False
            except Exception as e:
                _logger.error(f"Error evaluating access right domain: {str(e)}")
                return False
        
        # Check conditions
        if self.condition:
            try:
                # Evaluate condition in user context
                eval_context = {
                    'user': user,
                    'self': self,
                    'record_id': record_id,
                    'context': context or {},
                }
                if not eval(self.condition, eval_context):
                    return False
            except Exception as e:
                _logger.error(f"Error evaluating access right condition: {str(e)}")
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
    
    def grant_access(self, user_id):
        """Grant access right to user"""
        self.ensure_one()
        
        user = self.env['res.users'].browse(user_id)
        
        # Add to user's access rights
        if self not in user.access_rights:
            user.access_rights = [(4, self.id)]
            
            # Log access grant
            self.env['user.activity'].create({
                'user_id': user_id,
                'activity_type': 'access_grant',
                'description': f'Access right granted: {self.name}',
            })
    
    def revoke_access(self, user_id):
        """Revoke access right from user"""
        self.ensure_one()
        
        user = self.env['res.users'].browse(user_id)
        
        # Remove from user's access rights
        if self in user.access_rights:
            user.access_rights = [(3, self.id)]
            
            # Log access revocation
            self.env['user.activity'].create({
                'user_id': user_id,
                'activity_type': 'access_revoke',
                'description': f'Access right revoked: {self.name}',
            })
    
    def get_access_users(self):
        """Get all users with this access right"""
        users = set()
        
        # Get users from direct assignment
        if self.user_id:
            users.add(self.user_id)
        
        # Get users from group
        if self.group_id:
            users.update(self.group_id.users)
        
        # Get users from role
        if self.role_id:
            users.update(self.role_id.users)
        
        return list(users)
    
    def get_access_statistics(self):
        """Get access right statistics"""
        return {
            'usage_count': self.usage_count,
            'last_used': self.last_used,
            'is_active': self.is_active,
            'is_system_right': self.is_system_right,
            'access_type': self.access_type,
            'scope': self.scope,
            'category': self.category,
            'user_count': len(self.get_access_users()),
        }
    
    @api.model
    def get_access_rights_by_category(self, category):
        """Get access rights by category"""
        return self.search([
            ('category', '=', category),
            ('is_active', '=', True),
        ])
    
    @api.model
    def get_access_rights_by_model(self, model_name):
        """Get access rights by model"""
        return self.search([
            ('model_name', '=', model_name),
            ('is_active', '=', True),
        ])
    
    @api.model
    def get_system_access_rights(self):
        """Get all system access rights"""
        return self.search([
            ('is_system_right', '=', True),
            ('is_active', '=', True),
        ])
    
    @api.model
    def get_custom_access_rights(self):
        """Get all custom access rights"""
        return self.search([
            ('is_system_right', '=', False),
            ('is_active', '=', True),
        ])
    
    @api.model
    def get_access_right_analytics(self):
        """Get access right analytics"""
        total_access_rights = self.search_count([])
        active_access_rights = self.search_count([('is_active', '=', True)])
        system_access_rights = self.search_count([('is_system_right', '=', True)])
        custom_access_rights = self.search_count([('is_system_right', '=', False)])
        
        return {
            'total_access_rights': total_access_rights,
            'active_access_rights': active_access_rights,
            'system_access_rights': system_access_rights,
            'custom_access_rights': custom_access_rights,
            'inactive_access_rights': total_access_rights - active_access_rights,
            'active_percentage': (active_access_rights / total_access_rights * 100) if total_access_rights > 0 else 0,
        }
    
    @api.constrains('code')
    def _check_code(self):
        """Validate access right code"""
        for access_right in self:
            if access_right.code:
                # Check for duplicate codes
                existing = self.search([
                    ('code', '=', access_right.code),
                    ('id', '!=', access_right.id),
                ])
                if existing:
                    raise ValidationError(_('Access right code must be unique'))
    
    @api.constrains('depends_on')
    def _check_dependencies(self):
        """Validate access right dependencies"""
        for access_right in self:
            if access_right in access_right.depends_on:
                raise ValidationError(_('Access right cannot depend on itself'))
            
            # Check for circular dependencies
            for dep in access_right.depends_on:
                if access_right in dep.required_by:
                    raise ValidationError(_('Circular dependency detected'))
    
    def action_activate(self):
        """Activate access right"""
        self.is_active = True
        return True
    
    def action_deactivate(self):
        """Deactivate access right"""
        self.is_active = False
        return True
    
    def action_duplicate(self):
        """Duplicate access right"""
        self.ensure_one()
        
        new_access_right = self.copy({
            'name': f'{self.name} (Copy)',
            'code': f'{self.code}_copy',
            'is_system_right': False,
        })
        
        return {
            'type': 'ir.actions.act_window',
            'name': 'Duplicated Access Right',
            'res_model': 'access.rights',
            'res_id': new_access_right.id,
            'view_mode': 'form',
            'target': 'current',
        }
    
    def action_export_access_right(self):
        """Export access right definition"""
        self.ensure_one()
        
        return {
            'name': self.name,
            'description': self.description,
            'code': self.code,
            'model_name': self.model_name,
            'access_type': self.access_type,
            'scope': self.scope,
            'category': self.category,
            'domain': self.domain,
            'condition': self.condition,
            'ip_restrictions': self.ip_restrictions,
            'time_restrictions': self.time_restrictions,
        }
    
    def action_import_access_right(self, access_right_data):
        """Import access right definition"""
        self.ensure_one()
        
        self.write(access_right_data)
        return True