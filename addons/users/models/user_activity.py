# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)


class UserActivity(models.Model):
    """User activity tracking model for Kids Clothing ERP"""
    
    _name = 'user.activity'
    _description = 'User Activity'
    _order = 'create_date desc'
    
    # Basic fields
    user_id = fields.Many2one(
        'res.users',
        string='User',
        required=True,
        help='User who performed the activity'
    )
    
    activity_type = fields.Selection([
        ('login', 'Login'),
        ('logout', 'Logout'),
        ('create', 'Create'),
        ('update', 'Update'),
        ('delete', 'Delete'),
        ('read', 'Read'),
        ('search', 'Search'),
        ('export', 'Export'),
        ('import', 'Import'),
        ('print', 'Print'),
        ('email', 'Email'),
        ('sms', 'SMS'),
        ('notification', 'Notification'),
        ('security', 'Security'),
        ('group_assignment', 'Group Assignment'),
        ('group_removal', 'Group Removal'),
        ('permission_grant', 'Permission Grant'),
        ('permission_revoke', 'Permission Revoke'),
        ('access_grant', 'Access Grant'),
        ('access_revoke', 'Access Revoke'),
        ('password_change', 'Password Change'),
        ('password_reset', 'Password Reset'),
        ('account_lock', 'Account Lock'),
        ('account_unlock', 'Account Unlock'),
        ('profile_update', 'Profile Update'),
        ('preference_change', 'Preference Change'),
        ('system_access', 'System Access'),
        ('data_access', 'Data Access'),
        ('report_generation', 'Report Generation'),
        ('backup', 'Backup'),
        ('restore', 'Restore'),
        ('other', 'Other'),
    ], string='Activity Type', required=True, help='Type of activity')
    
    description = fields.Text(
        string='Description',
        required=True,
        help='Description of the activity'
    )
    
    # Activity details
    model_name = fields.Char(
        string='Model',
        help='Model involved in the activity'
    )
    
    record_id = fields.Integer(
        string='Record ID',
        help='ID of the record involved in the activity'
    )
    
    record_name = fields.Char(
        string='Record Name',
        help='Name of the record involved in the activity'
    )
    
    # Activity context
    ip_address = fields.Char(
        string='IP Address',
        help='IP address of the user'
    )
    
    user_agent = fields.Text(
        string='User Agent',
        help='User agent string'
    )
    
    session_id = fields.Char(
        string='Session ID',
        help='Session ID'
    )
    
    # Activity data
    old_values = fields.Text(
        string='Old Values',
        help='Old values (JSON format)'
    )
    
    new_values = fields.Text(
        string='New Values',
        help='New values (JSON format)'
    )
    
    # Activity status
    status = fields.Selection([
        ('success', 'Success'),
        ('failed', 'Failed'),
        ('warning', 'Warning'),
        ('info', 'Info'),
    ], string='Status', default='success', help='Status of the activity')
    
    error_message = fields.Text(
        string='Error Message',
        help='Error message if activity failed'
    )
    
    # Activity timing
    duration = fields.Float(
        string='Duration (seconds)',
        help='Duration of the activity in seconds'
    )
    
    start_time = fields.Datetime(
        string='Start Time',
        help='Start time of the activity'
    )
    
    end_time = fields.Datetime(
        string='End Time',
        help='End time of the activity'
    )
    
    # Activity location
    location = fields.Char(
        string='Location',
        help='Location of the activity'
    )
    
    country = fields.Char(
        string='Country',
        help='Country of the activity'
    )
    
    city = fields.Char(
        string='City',
        help='City of the activity'
    )
    
    # Activity device
    device_type = fields.Selection([
        ('desktop', 'Desktop'),
        ('tablet', 'Tablet'),
        ('mobile', 'Mobile'),
        ('other', 'Other'),
    ], string='Device Type', help='Type of device used')
    
    browser = fields.Char(
        string='Browser',
        help='Browser used'
    )
    
    operating_system = fields.Char(
        string='Operating System',
        help='Operating system used'
    )
    
    # Activity severity
    severity = fields.Selection([
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ], string='Severity', default='low', help='Severity of the activity')
    
    # Activity category
    category = fields.Selection([
        ('authentication', 'Authentication'),
        ('authorization', 'Authorization'),
        ('data_access', 'Data Access'),
        ('data_modification', 'Data Modification'),
        ('system_administration', 'System Administration'),
        ('user_management', 'User Management'),
        ('security', 'Security'),
        ('reporting', 'Reporting'),
        ('communication', 'Communication'),
        ('other', 'Other'),
    ], string='Category', default='other', help='Category of the activity')
    
    # Activity tags
    tags = fields.Char(
        string='Tags',
        help='Comma-separated tags for the activity'
    )
    
    # Activity metadata
    metadata = fields.Text(
        string='Metadata',
        help='Additional metadata (JSON format)'
    )
    
    @api.model
    def create(self, vals):
        """Override create to set default values"""
        # Set start time if not provided
        if 'start_time' not in vals:
            vals['start_time'] = fields.Datetime.now()
        
        # Set end time if not provided
        if 'end_time' not in vals:
            vals['end_time'] = fields.Datetime.now()
        
        # Calculate duration if not provided
        if 'duration' not in vals and 'start_time' in vals and 'end_time' in vals:
            start = fields.Datetime.from_string(vals['start_time'])
            end = fields.Datetime.from_string(vals['end_time'])
            vals['duration'] = (end - start).total_seconds()
        
        return super(UserActivity, self).create(vals)
    
    def write(self, vals):
        """Override write to handle activity updates"""
        result = super(UserActivity, self).write(vals)
        
        # Update duration if start_time or end_time changed
        if 'start_time' in vals or 'end_time' in vals:
            for activity in self:
                if activity.start_time and activity.end_time:
                    start = fields.Datetime.from_string(activity.start_time)
                    end = fields.Datetime.from_string(activity.end_time)
                    activity.duration = (end - start).total_seconds()
        
        return result
    
    def get_activity_summary(self):
        """Get activity summary"""
        return {
            'user': self.user_id.name,
            'type': self.activity_type,
            'description': self.description,
            'status': self.status,
            'duration': self.duration,
            'severity': self.severity,
            'category': self.category,
            'ip_address': self.ip_address,
            'device_type': self.device_type,
            'browser': self.browser,
            'operating_system': self.operating_system,
            'location': self.location,
            'country': self.country,
            'city': self.city,
        }
    
    def get_activity_details(self):
        """Get detailed activity information"""
        return {
            'id': self.id,
            'user_id': self.user_id.id,
            'user_name': self.user_id.name,
            'activity_type': self.activity_type,
            'description': self.description,
            'model_name': self.model_name,
            'record_id': self.record_id,
            'record_name': self.record_name,
            'status': self.status,
            'error_message': self.error_message,
            'duration': self.duration,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'ip_address': self.ip_address,
            'user_agent': self.user_agent,
            'session_id': self.session_id,
            'old_values': self.old_values,
            'new_values': self.new_values,
            'location': self.location,
            'country': self.country,
            'city': self.city,
            'device_type': self.device_type,
            'browser': self.browser,
            'operating_system': self.operating_system,
            'severity': self.severity,
            'category': self.category,
            'tags': self.tags,
            'metadata': self.metadata,
        }
    
    @api.model
    def get_user_activities(self, user_id, days=30):
        """Get activities for a specific user"""
        date_from = fields.Datetime.now() - timedelta(days=days)
        
        return self.search([
            ('user_id', '=', user_id),
            ('create_date', '>=', date_from),
        ], order='create_date desc')
    
    @api.model
    def get_activities_by_type(self, activity_type, days=30):
        """Get activities by type"""
        date_from = fields.Datetime.now() - timedelta(days=days)
        
        return self.search([
            ('activity_type', '=', activity_type),
            ('create_date', '>=', date_from),
        ], order='create_date desc')
    
    @api.model
    def get_activities_by_status(self, status, days=30):
        """Get activities by status"""
        date_from = fields.Datetime.now() - timedelta(days=days)
        
        return self.search([
            ('status', '=', status),
            ('create_date', '>=', date_from),
        ], order='create_date desc')
    
    @api.model
    def get_activities_by_severity(self, severity, days=30):
        """Get activities by severity"""
        date_from = fields.Datetime.now() - timedelta(days=days)
        
        return self.search([
            ('severity', '=', severity),
            ('create_date', '>=', date_from),
        ], order='create_date desc')
    
    @api.model
    def get_activities_by_category(self, category, days=30):
        """Get activities by category"""
        date_from = fields.Datetime.now() - timedelta(days=days)
        
        return self.search([
            ('category', '=', category),
            ('create_date', '>=', date_from),
        ], order='create_date desc')
    
    @api.model
    def get_activity_analytics(self, days=30):
        """Get activity analytics"""
        date_from = fields.Datetime.now() - timedelta(days=days)
        
        activities = self.search([
            ('create_date', '>=', date_from),
        ])
        
        # Count by type
        type_counts = {}
        for activity in activities:
            type_counts[activity.activity_type] = type_counts.get(activity.activity_type, 0) + 1
        
        # Count by status
        status_counts = {}
        for activity in activities:
            status_counts[activity.status] = status_counts.get(activity.status, 0) + 1
        
        # Count by severity
        severity_counts = {}
        for activity in activities:
            severity_counts[activity.severity] = severity_counts.get(activity.severity, 0) + 1
        
        # Count by category
        category_counts = {}
        for activity in activities:
            category_counts[activity.category] = category_counts.get(activity.category, 0) + 1
        
        # Count by user
        user_counts = {}
        for activity in activities:
            user_counts[activity.user_id.name] = user_counts.get(activity.user_id.name, 0) + 1
        
        return {
            'total_activities': len(activities),
            'type_counts': type_counts,
            'status_counts': status_counts,
            'severity_counts': severity_counts,
            'category_counts': category_counts,
            'user_counts': user_counts,
            'average_duration': sum(activities.mapped('duration')) / len(activities) if activities else 0,
            'most_active_user': max(user_counts.items(), key=lambda x: x[1])[0] if user_counts else None,
            'most_common_type': max(type_counts.items(), key=lambda x: x[1])[0] if type_counts else None,
        }
    
    @api.model
    def get_security_activities(self, days=30):
        """Get security-related activities"""
        date_from = fields.Datetime.now() - timedelta(days=days)
        
        return self.search([
            ('category', '=', 'security'),
            ('create_date', '>=', date_from),
        ], order='create_date desc')
    
    @api.model
    def get_failed_activities(self, days=30):
        """Get failed activities"""
        date_from = fields.Datetime.now() - timedelta(days=days)
        
        return self.search([
            ('status', '=', 'failed'),
            ('create_date', '>=', date_from),
        ], order='create_date desc')
    
    @api.model
    def get_critical_activities(self, days=30):
        """Get critical activities"""
        date_from = fields.Datetime.now() - timedelta(days=days)
        
        return self.search([
            ('severity', '=', 'critical'),
            ('create_date', '>=', date_from),
        ], order='create_date desc')
    
    @api.model
    def cleanup_old_activities(self, days=365):
        """Clean up old activities"""
        date_from = fields.Datetime.now() - timedelta(days=days)
        
        old_activities = self.search([
            ('create_date', '<', date_from),
        ])
        
        count = len(old_activities)
        old_activities.unlink()
        
        _logger.info(f"Cleaned up {count} old activities")
        return count
    
    @api.model
    def export_activities(self, domain=None, limit=None):
        """Export activities to CSV"""
        if domain is None:
            domain = []
        
        activities = self.search(domain, limit=limit)
        
        export_data = []
        for activity in activities:
            export_data.append({
                'id': activity.id,
                'user': activity.user_id.name,
                'activity_type': activity.activity_type,
                'description': activity.description,
                'status': activity.status,
                'duration': activity.duration,
                'create_date': activity.create_date,
                'ip_address': activity.ip_address,
                'device_type': activity.device_type,
                'browser': activity.browser,
                'operating_system': activity.operating_system,
                'location': activity.location,
                'country': activity.country,
                'city': activity.city,
                'severity': activity.severity,
                'category': activity.category,
            })
        
        return export_data
    
    def action_mark_as_resolved(self):
        """Mark activity as resolved"""
        self.status = 'success'
        return True
    
    def action_mark_as_failed(self):
        """Mark activity as failed"""
        self.status = 'failed'
        return True
    
    def action_set_severity(self, severity):
        """Set activity severity"""
        self.severity = severity
        return True
    
    def action_add_tag(self, tag):
        """Add tag to activity"""
        if self.tags:
            tags = self.tags.split(',')
            if tag not in tags:
                tags.append(tag)
                self.tags = ','.join(tags)
        else:
            self.tags = tag
        return True
    
    def action_remove_tag(self, tag):
        """Remove tag from activity"""
        if self.tags:
            tags = self.tags.split(',')
            if tag in tags:
                tags.remove(tag)
                self.tags = ','.join(tags)
        return True