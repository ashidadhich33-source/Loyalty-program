# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
import logging
from datetime import datetime, timedelta

_logger = logging.getLogger(__name__)


class ResUsers(models.Model):
    """Extended user model for Kids Clothing ERP"""
    
    _inherit = 'res.users'
    
    # Kids Clothing specific fields
    employee_id = fields.Many2one(
        'hr.employee',
        string='Employee',
        help='Related employee record'
    )
    
    department_id = fields.Many2one(
        'hr.department',
        string='Department',
        help='User department'
    )
    
    job_title = fields.Char(
        string='Job Title',
        help='User job title'
    )
    
    # User preferences
    theme_preference = fields.Selection([
        ('light', 'Light Theme'),
        ('dark', 'Dark Theme'),
        ('kids', 'Kids Theme'),
    ], string='Theme Preference', default='kids', help='User theme preference')
    
    language_preference = fields.Selection([
        ('en_US', 'English'),
        ('hi_IN', 'Hindi'),
        ('ta_IN', 'Tamil'),
        ('te_IN', 'Telugu'),
        ('bn_IN', 'Bengali'),
        ('gu_IN', 'Gujarati'),
        ('kn_IN', 'Kannada'),
        ('ml_IN', 'Malayalam'),
        ('mr_IN', 'Marathi'),
        ('pa_IN', 'Punjabi'),
    ], string='Language Preference', default='en_US', help='User language preference')
    
    timezone_preference = fields.Selection([
        ('Asia/Kolkata', 'India Standard Time'),
        ('Asia/Dubai', 'Gulf Standard Time'),
        ('America/New_York', 'Eastern Time'),
        ('Europe/London', 'Greenwich Mean Time'),
    ], string='Timezone Preference', default='Asia/Kolkata', help='User timezone preference')
    
    # User settings
    enable_notifications = fields.Boolean(
        string='Enable Notifications',
        default=True,
        help='Enable push notifications'
    )
    
    enable_sound = fields.Boolean(
        string='Enable Sound',
        default=True,
        help='Enable sound notifications'
    )
    
    enable_animations = fields.Boolean(
        string='Enable Animations',
        default=True,
        help='Enable UI animations'
    )
    
    touchscreen_mode = fields.Boolean(
        string='Touchscreen Mode',
        default=False,
        help='Enable touchscreen mode'
    )
    
    compact_mode = fields.Boolean(
        string='Compact Mode',
        default=False,
        help='Enable compact interface mode'
    )
    
    # User status
    is_active_user = fields.Boolean(
        string='Active User',
        default=True,
        help='Whether user is active'
    )
    
    last_login_date = fields.Datetime(
        string='Last Login',
        help='Last login date and time'
    )
    
    login_count = fields.Integer(
        string='Login Count',
        default=0,
        help='Total number of logins'
    )
    
    failed_login_count = fields.Integer(
        string='Failed Login Count',
        default=0,
        help='Number of failed login attempts'
    )
    
    last_failed_login = fields.Datetime(
        string='Last Failed Login',
        help='Last failed login attempt'
    )
    
    account_locked = fields.Boolean(
        string='Account Locked',
        default=False,
        help='Whether account is locked'
    )
    
    lock_reason = fields.Text(
        string='Lock Reason',
        help='Reason for account lock'
    )
    
    # User permissions
    custom_permissions = fields.One2many(
        'user.permissions',
        'user_id',
        string='Custom Permissions',
        help='Custom permissions for this user'
    )
    
    # User activity
    activity_logs = fields.One2many(
        'user.activity',
        'user_id',
        string='Activity Logs',
        help='User activity logs'
    )
    
    # User preferences
    user_preferences = fields.One2many(
        'user.preferences',
        'user_id',
        string='User Preferences',
        help='User preferences and settings'
    )
    
    # Multi-company access
    company_ids = fields.Many2many(
        'res.company',
        'user_company_rel',
        'user_id',
        'company_id',
        string='Companies',
        help='Companies this user can access'
    )
    
    default_company_id = fields.Many2one(
        'res.company',
        string='Default Company',
        help='Default company for this user'
    )
    
    # User roles
    role_ids = fields.Many2many(
        'user.role',
        'user_role_rel',
        'user_id',
        'role_id',
        string='Roles',
        help='User roles'
    )
    
    # User profile
    profile_image = fields.Binary(
        string='Profile Image',
        help='User profile image'
    )
    
    bio = fields.Text(
        string='Bio',
        help='User biography'
    )
    
    phone = fields.Char(
        string='Phone',
        help='User phone number'
    )
    
    mobile = fields.Char(
        string='Mobile',
        help='User mobile number'
    )
    
    # Address information
    street = fields.Char(
        string='Street',
        help='Street address'
    )
    
    street2 = fields.Char(
        string='Street2',
        help='Street address line 2'
    )
    
    city = fields.Char(
        string='City',
        help='City'
    )
    
    state_id = fields.Many2one(
        'res.country.state',
        string='State',
        help='State'
    )
    
    zip = fields.Char(
        string='ZIP',
        help='ZIP code'
    )
    
    country_id = fields.Many2one(
        'res.country',
        string='Country',
        help='Country'
    )
    
    # Social media
    website = fields.Char(
        string='Website',
        help='User website'
    )
    
    linkedin = fields.Char(
        string='LinkedIn',
        help='LinkedIn profile'
    )
    
    twitter = fields.Char(
        string='Twitter',
        help='Twitter handle'
    )
    
    facebook = fields.Char(
        string='Facebook',
        help='Facebook profile'
    )
    
    # Emergency contact
    emergency_contact_name = fields.Char(
        string='Emergency Contact Name',
        help='Emergency contact name'
    )
    
    emergency_contact_phone = fields.Char(
        string='Emergency Contact Phone',
        help='Emergency contact phone'
    )
    
    emergency_contact_relation = fields.Char(
        string='Emergency Contact Relation',
        help='Emergency contact relation'
    )
    
    @api.model
    def create(self, vals):
        """Override create to set default values"""
        # Set default company if not provided
        if 'company_ids' not in vals and 'default_company_id' not in vals:
            default_company = self.env['res.company'].search([], limit=1)
            if default_company:
                vals['company_ids'] = [(6, 0, [default_company.id])]
                vals['default_company_id'] = default_company.id
        
        # Set default groups
        if 'groups_id' not in vals:
            default_group = self.env.ref('base.group_user', raise_if_not_found=False)
            if default_group:
                vals['groups_id'] = [(6, 0, [default_group.id])]
        
        return super(ResUsers, self).create(vals)
    
    def write(self, vals):
        """Override write to handle user updates"""
        result = super(ResUsers, self).write(vals)
        
        # Log user updates
        for user in self:
            if vals:
                self.env['user.activity'].create({
                    'user_id': user.id,
                    'activity_type': 'update',
                    'description': f'User profile updated: {", ".join(vals.keys())}',
                    'ip_address': self.env.context.get('ip_address'),
                    'user_agent': self.env.context.get('user_agent'),
                })
        
        return result
    
    def unlink(self):
        """Override unlink to prevent deletion of admin users"""
        for user in self:
            if user.has_group('base.group_system'):
                raise UserError(_('System users cannot be deleted'))
        
        return super(ResUsers, self).unlink()
    
    def action_login(self):
        """Handle user login"""
        self.ensure_one()
        
        # Check if account is locked
        if self.account_locked:
            raise UserError(_('Account is locked: %s') % self.lock_reason)
        
        # Update login information
        self.last_login_date = fields.Datetime.now()
        self.login_count += 1
        self.failed_login_count = 0
        self.last_failed_login = False
        
        # Log login activity
        self.env['user.activity'].create({
            'user_id': self.id,
            'activity_type': 'login',
            'description': 'User logged in',
            'ip_address': self.env.context.get('ip_address'),
            'user_agent': self.env.context.get('user_agent'),
        })
        
        return True
    
    def action_failed_login(self):
        """Handle failed login attempt"""
        self.ensure_one()
        
        self.failed_login_count += 1
        self.last_failed_login = fields.Datetime.now()
        
        # Lock account after 5 failed attempts
        if self.failed_login_count >= 5:
            self.account_locked = True
            self.lock_reason = 'Too many failed login attempts'
            
            # Log account lock
            self.env['user.activity'].create({
                'user_id': self.id,
                'activity_type': 'security',
                'description': 'Account locked due to failed login attempts',
                'ip_address': self.env.context.get('ip_address'),
                'user_agent': self.env.context.get('user_agent'),
            })
        
        return True
    
    def action_unlock_account(self):
        """Unlock user account"""
        self.ensure_one()
        
        self.account_locked = False
        self.lock_reason = False
        self.failed_login_count = 0
        self.last_failed_login = False
        
        # Log account unlock
        self.env['user.activity'].create({
            'user_id': self.id,
            'activity_type': 'security',
            'description': 'Account unlocked',
            'ip_address': self.env.context.get('ip_address'),
            'user_agent': self.env.context.get('user_agent'),
        })
        
        return True
    
    def action_reset_password(self):
        """Reset user password"""
        self.ensure_one()
        
        # Generate temporary password
        import secrets
        import string
        
        alphabet = string.ascii_letters + string.digits
        temp_password = ''.join(secrets.choice(alphabet) for _ in range(12))
        
        # Set temporary password
        self.password = temp_password
        
        # Log password reset
        self.env['user.activity'].create({
            'user_id': self.id,
            'activity_type': 'security',
            'description': 'Password reset',
            'ip_address': self.env.context.get('ip_address'),
            'user_agent': self.env.context.get('user_agent'),
        })
        
        return temp_password
    
    def action_change_password(self, old_password, new_password):
        """Change user password"""
        self.ensure_one()
        
        # Validate old password
        if not self._crypt_context().verify(old_password, self.password):
            raise UserError(_('Current password is incorrect'))
        
        # Validate new password
        if len(new_password) < 8:
            raise UserError(_('Password must be at least 8 characters long'))
        
        # Set new password
        self.password = new_password
        
        # Log password change
        self.env['user.activity'].create({
            'user_id': self.id,
            'activity_type': 'security',
            'description': 'Password changed',
            'ip_address': self.env.context.get('ip_address'),
            'user_agent': self.env.context.get('user_agent'),
        })
        
        return True
    
    def get_user_permissions(self):
        """Get all permissions for this user"""
        permissions = set()
        
        # Get permissions from groups
        for group in self.groups_id:
            for rule in group.rule_ids:
                permissions.add(rule.name)
        
        # Get custom permissions
        for custom_perm in self.custom_permissions:
            permissions.add(custom_perm.name)
        
        return list(permissions)
    
    def has_permission(self, permission_name):
        """Check if user has specific permission"""
        return permission_name in self.get_user_permissions()
    
    def get_user_activity(self, days=30):
        """Get user activity for specified days"""
        date_from = fields.Datetime.now() - timedelta(days=days)
        
        return self.env['user.activity'].search([
            ('user_id', '=', self.id),
            ('create_date', '>=', date_from),
        ], order='create_date desc')
    
    def get_user_statistics(self):
        """Get user statistics"""
        return {
            'total_logins': self.login_count,
            'last_login': self.last_login_date,
            'failed_logins': self.failed_login_count,
            'account_locked': self.account_locked,
            'is_active': self.active,
            'groups_count': len(self.groups_id),
            'permissions_count': len(self.get_user_permissions()),
            'companies_count': len(self.company_ids),
        }
    
    @api.model
    def get_active_users(self):
        """Get all active users"""
        return self.search([('active', '=', True)])
    
    @api.model
    def get_users_by_company(self, company_id):
        """Get users by company"""
        return self.search([
            ('company_ids', 'in', [company_id]),
            ('active', '=', True),
        ])
    
    @api.model
    def get_users_by_group(self, group_id):
        """Get users by group"""
        return self.search([
            ('groups_id', 'in', [group_id]),
            ('active', '=', True),
        ])
    
    @api.model
    def get_users_by_role(self, role_id):
        """Get users by role"""
        return self.search([
            ('role_ids', 'in', [role_id]),
            ('active', '=', True),
        ])
    
    @api.model
    def get_user_analytics(self):
        """Get user analytics"""
        total_users = self.search_count([])
        active_users = self.search_count([('active', '=', True)])
        locked_users = self.search_count([('account_locked', '=', True)])
        
        return {
            'total_users': total_users,
            'active_users': active_users,
            'locked_users': locked_users,
            'inactive_users': total_users - active_users,
            'active_percentage': (active_users / total_users * 100) if total_users > 0 else 0,
        }
    
    @api.constrains('email')
    def _check_email(self):
        """Validate email format"""
        for user in self:
            if user.email and not self._validate_email(user.email):
                raise ValidationError(_('Invalid email format'))
    
    @api.constrains('phone', 'mobile')
    def _check_phone(self):
        """Validate phone numbers"""
        for user in self:
            if user.phone and not self._validate_phone(user.phone):
                raise ValidationError(_('Invalid phone number format'))
            if user.mobile and not self._validate_phone(user.mobile):
                raise ValidationError(_('Invalid mobile number format'))
    
    def _validate_email(self, email):
        """Validate email format"""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def _validate_phone(self, phone):
        """Validate phone number format"""
        import re
        # Remove all non-digit characters
        clean_phone = re.sub(r'\D', '', phone)
        # Check if it's a valid Indian phone number
        return len(clean_phone) == 10 and clean_phone[0] in '6789'
    
    def _crypt_context(self):
        """Get password crypt context"""
        import passlib.context
        return passlib.context.CryptContext(
            schemes=['pbkdf2_sha512', 'plaintext'],
            deprecated=['plaintext']
        )