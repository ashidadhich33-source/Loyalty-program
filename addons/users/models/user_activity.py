# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Users - User Activity
========================================

Standalone version of the user activity model.
"""

from core_framework.orm import BaseModel, CharField, TextField, BooleanField, IntegerField, DateTimeField, Many2OneField, SelectionField
from core_framework.orm import Field
from typing import Dict, Any, Optional
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class UserActivity(BaseModel):
    """User activity model for Kids Clothing ERP"""
    
    _name = 'user.activity'
    _description = 'User Activity'
    _table = 'user_activity'
    
    # Basic activity information
    user_id = IntegerField(
        string='User ID',
        required=True,
        help='User who performed the activity'
    )
    
    activity_type = SelectionField(
        string='Activity Type',
        selection=[
            ('login', 'Login'),
            ('logout', 'Logout'),
            ('create', 'Create'),
            ('update', 'Update'),
            ('delete', 'Delete'),
            ('view', 'View'),
            ('search', 'Search'),
            ('export', 'Export'),
            ('import', 'Import'),
            ('security', 'Security'),
            ('group_assignment', 'Group Assignment'),
            ('group_removal', 'Group Removal'),
            ('permission_change', 'Permission Change'),
            ('password_change', 'Password Change'),
            ('profile_update', 'Profile Update'),
            ('system_access', 'System Access'),
        ],
        required=True,
        help='Type of activity'
    )
    
    description = TextField(
        string='Description',
        help='Activity description'
    )
    
    # Activity details
    model_name = CharField(
        string='Model Name',
        size=100,
        help='Model involved in the activity'
    )
    
    record_id = IntegerField(
        string='Record ID',
        help='Record involved in the activity'
    )
    
    # Activity metadata
    ip_address = CharField(
        string='IP Address',
        size=45,
        help='IP address of the user'
    )
    
    user_agent = TextField(
        string='User Agent',
        help='User agent string'
    )
    
    session_id = CharField(
        string='Session ID',
        size=100,
        help='Session ID'
    )
    
    # Activity timing
    activity_date = DateTimeField(
        string='Activity Date',
        default=datetime.now,
        help='Date and time of the activity'
    )
    
    duration = IntegerField(
        string='Duration (seconds)',
        help='Duration of the activity in seconds'
    )
    
    # Activity status
    is_successful = BooleanField(
        string='Successful',
        default=True,
        help='Whether the activity was successful'
    )
    
    error_message = TextField(
        string='Error Message',
        help='Error message if activity failed'
    )
    
    # Activity category
    category = SelectionField(
        string='Category',
        selection=[
            ('authentication', 'Authentication'),
            ('data_access', 'Data Access'),
            ('data_modification', 'Data Modification'),
            ('system_administration', 'System Administration'),
            ('security', 'Security'),
            ('reporting', 'Reporting'),
            ('communication', 'Communication'),
            ('other', 'Other'),
        ],
        default='other',
        help='Activity category'
    )
    
    # Activity priority
    priority = SelectionField(
        string='Priority',
        selection=[
            ('low', 'Low'),
            ('medium', 'Medium'),
            ('high', 'High'),
            ('critical', 'Critical'),
        ],
        default='medium',
        help='Activity priority'
    )
    
    def create(self, vals: Dict[str, Any]):
        """Override create to set default values"""
        # Set activity date if not provided
        if 'activity_date' not in vals:
            vals['activity_date'] = datetime.now()
        
        # Set category based on activity type
        if 'category' not in vals:
            category_mapping = {
                'login': 'authentication',
                'logout': 'authentication',
                'create': 'data_modification',
                'update': 'data_modification',
                'delete': 'data_modification',
                'view': 'data_access',
                'search': 'data_access',
                'export': 'data_access',
                'import': 'data_modification',
                'security': 'security',
                'group_assignment': 'system_administration',
                'group_removal': 'system_administration',
                'permission_change': 'system_administration',
                'password_change': 'security',
                'profile_update': 'data_modification',
                'system_access': 'system_administration',
            }
            vals['category'] = category_mapping.get(vals.get('activity_type', ''), 'other')
        
        return super().create(vals)
    
    def get_activity_info(self):
        """Get activity information"""
        return {
            'user_id': self.user_id,
            'activity_type': self.activity_type,
            'description': self.description,
            'model_name': self.model_name,
            'record_id': self.record_id,
            'ip_address': self.ip_address,
            'activity_date': self.activity_date,
            'duration': self.duration,
            'is_successful': self.is_successful,
            'category': self.category,
            'priority': self.priority,
        }
    
    @classmethod
    def get_activities_by_user(cls, user_id: int, limit: int = 100):
        """Get activities by user"""
        return cls.search([
            ('user_id', '=', user_id),
        ], order='activity_date desc', limit=limit)
    
    @classmethod
    def get_activities_by_type(cls, activity_type: str, limit: int = 100):
        """Get activities by type"""
        return cls.search([
            ('activity_type', '=', activity_type),
        ], order='activity_date desc', limit=limit)
    
    @classmethod
    def get_activities_by_category(cls, category: str, limit: int = 100):
        """Get activities by category"""
        return cls.search([
            ('category', '=', category),
        ], order='activity_date desc', limit=limit)
    
    @classmethod
    def get_recent_activities(cls, hours: int = 24, limit: int = 100):
        """Get recent activities"""
        from datetime import timedelta
        date_from = datetime.now() - timedelta(hours=hours)
        
        return cls.search([
            ('activity_date', '>=', date_from),
        ], order='activity_date desc', limit=limit)
    
    @classmethod
    def get_failed_activities(cls, limit: int = 100):
        """Get failed activities"""
        return cls.search([
            ('is_successful', '=', False),
        ], order='activity_date desc', limit=limit)
    
    @classmethod
    def get_activity_analytics(cls, days: int = 30):
        """Get activity analytics"""
        from datetime import timedelta
        date_from = datetime.now() - timedelta(days=days)
        
        total_activities = cls.search_count([
            ('activity_date', '>=', date_from),
        ])
        
        successful_activities = cls.search_count([
            ('activity_date', '>=', date_from),
            ('is_successful', '=', True),
        ])
        
        failed_activities = cls.search_count([
            ('activity_date', '>=', date_from),
            ('is_successful', '=', False),
        ])
        
        # Get activities by type
        activities_by_type = {}
        for activity_type in ['login', 'logout', 'create', 'update', 'delete', 'view']:
            count = cls.search_count([
                ('activity_date', '>=', date_from),
                ('activity_type', '=', activity_type),
            ])
            activities_by_type[activity_type] = count
        
        return {
            'total_activities': total_activities,
            'successful_activities': successful_activities,
            'failed_activities': failed_activities,
            'success_rate': (successful_activities / total_activities * 100) if total_activities > 0 else 0,
            'activities_by_type': activities_by_type,
        }
    
    @classmethod
    def cleanup_old_activities(cls, days: int = 90):
        """Cleanup old activities"""
        from datetime import timedelta
        date_from = datetime.now() - timedelta(days=days)
        
        old_activities = cls.search([
            ('activity_date', '<', date_from),
        ])
        
        deleted_count = len(old_activities)
        old_activities.unlink()
        
        logger.info(f"Cleaned up {deleted_count} old activities")
        return deleted_count
    
    def _check_activity_type(self):
        """Validate activity type"""
        valid_types = [
            'login', 'logout', 'create', 'update', 'delete', 'view',
            'search', 'export', 'import', 'security', 'group_assignment',
            'group_removal', 'permission_change', 'password_change',
            'profile_update', 'system_access'
        ]
        
        if self.activity_type not in valid_types:
            raise ValueError(f'Invalid activity type: {self.activity_type}')
    
    def _check_priority(self):
        """Validate priority"""
        valid_priorities = ['low', 'medium', 'high', 'critical']
        if self.priority not in valid_priorities:
            raise ValueError(f'Invalid priority: {self.priority}')
    
    def _check_category(self):
        """Validate category"""
        valid_categories = [
            'authentication', 'data_access', 'data_modification',
            'system_administration', 'security', 'reporting',
            'communication', 'other'
        ]
        
        if self.category not in valid_categories:
            raise ValueError(f'Invalid category: {self.category}')