# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Users - User Management
==========================================

Standalone version of the user management model.
"""

from core_framework.orm import BaseModel, CharField, TextField, BooleanField, IntegerField, DateTimeField, Many2OneField, SelectionField, FloatField, One2ManyField, Many2ManyField
from core_framework.orm import Field
from typing import Dict, Any, Optional, List
import logging
from datetime import datetime, timedelta
import secrets
import string
import re

logger = logging.getLogger(__name__)

class ResUsers(BaseModel):
    """Extended user model for Kids Clothing ERP"""
    
    _name = 'res.users'
    _description = 'Users'
    _table = 'res_users'
    
    # Basic user information
    name = CharField(
        string='Name',
        size=255,
        required=True,
        help='User full name'
    )
    
    login = CharField(
        string='Login',
        size=64,
        required=True,
        help='User login name'
    )
    
    email = CharField(
        string='Email',
        size=240,
        help='User email address'
    )
    
    password = CharField(
        string='Password',
        size=255,
        help='User password (encrypted)'
    )
    
    active = BooleanField(
        string='Active',
        default=True,
        help='Whether user is active'
    )
    
    # Kids Clothing specific fields
    employee_id = IntegerField(
        string='Employee ID',
        help='Related employee record'
    )
    
    department_id = IntegerField(
        string='Department ID',
        help='User department'
    )
    
    job_title = CharField(
        string='Job Title',
        size=100,
        help='User job title'
    )
    
    # User preferences
    theme_preference = SelectionField(
        string='Theme Preference',
        selection=[
            ('light', 'Light Theme'),
            ('dark', 'Dark Theme'),
            ('kids', 'Kids Theme'),
        ],
        default='kids',
        help='User theme preference'
    )
    
    language_preference = SelectionField(
        string='Language Preference',
        selection=[
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
        ],
        default='en_US',
        help='User language preference'
    )
    
    timezone_preference = SelectionField(
        string='Timezone Preference',
        selection=[
            ('Asia/Kolkata', 'India Standard Time'),
            ('Asia/Dubai', 'Gulf Standard Time'),
            ('America/New_York', 'Eastern Time'),
            ('Europe/London', 'Greenwich Mean Time'),
        ],
        default='Asia/Kolkata',
        help='User timezone preference'
    )
    
    # User settings
    enable_notifications = BooleanField(
        string='Enable Notifications',
        default=True,
        help='Enable push notifications'
    )
    
    enable_sound = BooleanField(
        string='Enable Sound',
        default=True,
        help='Enable sound notifications'
    )
    
    enable_animations = BooleanField(
        string='Enable Animations',
        default=True,
        help='Enable UI animations'
    )
    
    touchscreen_mode = BooleanField(
        string='Touchscreen Mode',
        default=False,
        help='Enable touchscreen mode'
    )
    
    compact_mode = BooleanField(
        string='Compact Mode',
        default=False,
        help='Enable compact interface mode'
    )
    
    # User status
    is_active_user = BooleanField(
        string='Active User',
        default=True,
        help='Whether user is active'
    )
    
    last_login_date = DateTimeField(
        string='Last Login',
        help='Last login date and time'
    )
    
    login_count = IntegerField(
        string='Login Count',
        default=0,
        help='Total number of logins'
    )
    
    failed_login_count = IntegerField(
        string='Failed Login Count',
        default=0,
        help='Number of failed login attempts'
    )
    
    last_failed_login = DateTimeField(
        string='Last Failed Login',
        help='Last failed login attempt'
    )
    
    account_locked = BooleanField(
        string='Account Locked',
        default=False,
        help='Whether account is locked'
    )
    
    lock_reason = TextField(
        string='Lock Reason',
        help='Reason for account lock'
    )
    
    # User permissions
    custom_permissions = One2ManyField(
        string='Custom Permissions',
        comodel_name='user.permissions',
        inverse_name='user_id',
        help='Custom permissions for this user'
    )
    
    # User activity
    activity_logs = One2ManyField(
        string='Activity Logs',
        comodel_name='user.activity',
        inverse_name='user_id',
        help='User activity logs'
    )
    
    # User preferences
    user_preferences = One2ManyField(
        string='User Preferences',
        comodel_name='user.preferences',
        inverse_name='user_id',
        help='User preferences and settings'
    )
    
    # Multi-company access
    company_ids = Many2ManyField(
        string='Companies',
        comodel_name='res.company',
        help='Companies this user can access'
    )
    
    default_company_id = IntegerField(
        string='Default Company ID',
        help='Default company for this user'
    )
    
    # User roles
    role_ids = Many2ManyField(
        string='Roles',
        comodel_name='user.role',
        help='User roles'
    )
    
    # User profile
    profile_image = CharField(
        string='Profile Image',
        size=255,
        help='User profile image path'
    )
    
    bio = TextField(
        string='Bio',
        help='User biography'
    )
    
    phone = CharField(
        string='Phone',
        size=20,
        help='User phone number'
    )
    
    mobile = CharField(
        string='Mobile',
        size=20,
        help='User mobile number'
    )
    
    # Address information
    street = CharField(
        string='Street',
        size=100,
        help='Street address'
    )
    
    street2 = CharField(
        string='Street2',
        size=100,
        help='Street address line 2'
    )
    
    city = CharField(
        string='City',
        size=50,
        help='City'
    )
    
    state_id = IntegerField(
        string='State ID',
        help='State'
    )
    
    zip = CharField(
        string='ZIP',
        size=10,
        help='ZIP code'
    )
    
    country_id = IntegerField(
        string='Country ID',
        help='Country'
    )
    
    # Social media
    website = CharField(
        string='Website',
        size=100,
        help='User website'
    )
    
    linkedin = CharField(
        string='LinkedIn',
        size=100,
        help='LinkedIn profile'
    )
    
    twitter = CharField(
        string='Twitter',
        size=50,
        help='Twitter handle'
    )
    
    facebook = CharField(
        string='Facebook',
        size=100,
        help='Facebook profile'
    )
    
    # Emergency contact
    emergency_contact_name = CharField(
        string='Emergency Contact Name',
        size=100,
        help='Emergency contact name'
    )
    
    emergency_contact_phone = CharField(
        string='Emergency Contact Phone',
        size=20,
        help='Emergency contact phone'
    )
    
    emergency_contact_relation = CharField(
        string='Emergency Contact Relation',
        size=50,
        help='Emergency contact relation'
    )
    
    def create(self, vals: Dict[str, Any]):
        """Override create to set default values"""
        # Set default company if not provided
        if 'company_ids' not in vals and 'default_company_id' not in vals:
            # In standalone version, we'll set a default company ID
            vals['default_company_id'] = 1
        
        # Set default groups
        if 'groups_id' not in vals:
            # In standalone version, we'll set default group
            vals['groups_id'] = [1]  # Default user group
        
        return super().create(vals)
    
    def write(self, vals: Dict[str, Any]):
        """Override write to handle user updates"""
        result = super().write(vals)
        
        # Log user updates
        for user in self:
            if vals:
                logger.info(f"User {user.name} profile updated: {', '.join(vals.keys())}")
        
        return result
    
    def unlink(self):
        """Override unlink to prevent deletion of admin users"""
        for user in self:
            if user.id == 1:  # Admin user
                raise ValueError('System users cannot be deleted')
        
        return super().unlink()
    
    def action_login(self):
        """Handle user login"""
        self.ensure_one()
        
        # Check if account is locked
        if self.account_locked:
            raise ValueError(f'Account is locked: {self.lock_reason}')
        
        # Update login information
        self.last_login_date = datetime.now()
        self.login_count += 1
        self.failed_login_count = 0
        self.last_failed_login = None
        
        # Log login activity
        logger.info(f"User {self.name} logged in")
        
        return True
    
    def action_failed_login(self):
        """Handle failed login attempt"""
        self.ensure_one()
        
        self.failed_login_count += 1
        self.last_failed_login = datetime.now()
        
        # Lock account after 5 failed attempts
        if self.failed_login_count >= 5:
            self.account_locked = True
            self.lock_reason = 'Too many failed login attempts'
            
            # Log account lock
            logger.warning(f"Account {self.name} locked due to failed login attempts")
        
        return True
    
    def action_unlock_account(self):
        """Unlock user account"""
        self.ensure_one()
        
        self.account_locked = False
        self.lock_reason = None
        self.failed_login_count = 0
        self.last_failed_login = None
        
        # Log account unlock
        logger.info(f"Account {self.name} unlocked")
        
        return True
    
    def action_reset_password(self):
        """Reset user password"""
        self.ensure_one()
        
        # Generate temporary password
        alphabet = string.ascii_letters + string.digits
        temp_password = ''.join(secrets.choice(alphabet) for _ in range(12))
        
        # Set temporary password
        self.password = temp_password
        
        # Log password reset
        logger.info(f"Password reset for user {self.name}")
        
        return temp_password
    
    def action_change_password(self, old_password: str, new_password: str):
        """Change user password"""
        self.ensure_one()
        
        # Validate old password (simplified for standalone)
        if old_password != self.password:
            raise ValueError('Current password is incorrect')
        
        # Validate new password
        if len(new_password) < 8:
            raise ValueError('Password must be at least 8 characters long')
        
        # Set new password
        self.password = new_password
        
        # Log password change
        logger.info(f"Password changed for user {self.name}")
        
        return True
    
    def get_user_permissions(self):
        """Get all permissions for this user"""
        permissions = set()
        
        # In standalone version, we'll implement basic permission system
        # This is a simplified version
        permissions.add('base.user')
        
        return list(permissions)
    
    def has_permission(self, permission_name: str):
        """Check if user has specific permission"""
        return permission_name in self.get_user_permissions()
    
    def get_user_activity(self, days: int = 30):
        """Get user activity for specified days"""
        date_from = datetime.now() - timedelta(days=days)
        
        # In standalone version, we'll return basic activity info
        return {
            'login_count': self.login_count,
            'last_login': self.last_login_date,
            'failed_logins': self.failed_login_count,
        }
    
    def get_user_statistics(self):
        """Get user statistics"""
        return {
            'total_logins': self.login_count,
            'last_login': self.last_login_date,
            'failed_logins': self.failed_login_count,
            'account_locked': self.account_locked,
            'is_active': self.active,
            'companies_count': 1,  # Simplified for standalone
            'permissions_count': len(self.get_user_permissions()),
        }
    
    @classmethod
    def get_active_users(cls):
        """Get all active users"""
        return cls.search([('active', '=', True)])
    
    @classmethod
    def get_users_by_company(cls, company_id: int):
        """Get users by company"""
        return cls.search([
            ('default_company_id', '=', company_id),
            ('active', '=', True),
        ])
    
    @classmethod
    def get_user_analytics(cls):
        """Get user analytics"""
        # In standalone version, we'll return mock data
        return {
            'total_users': 0,
            'active_users': 0,
            'locked_users': 0,
            'inactive_users': 0,
            'active_percentage': 0,
        }
    
    def _validate_email(self, email: str) -> bool:
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def _validate_phone(self, phone: str) -> bool:
        """Validate phone number format"""
        # Remove all non-digit characters
        clean_phone = re.sub(r'\D', '', phone)
        # Check if it's a valid Indian phone number
        return len(clean_phone) == 10 and clean_phone[0] in '6789'
    
    def _check_email(self):
        """Validate email format"""
        if self.email and not self._validate_email(self.email):
            raise ValueError('Invalid email format')
    
    def _check_phone(self):
        """Validate phone numbers"""
        if self.phone and not self._validate_phone(self.phone):
            raise ValueError('Invalid phone number format')
        if self.mobile and not self._validate_phone(self.mobile):
            raise ValueError('Invalid mobile number format')