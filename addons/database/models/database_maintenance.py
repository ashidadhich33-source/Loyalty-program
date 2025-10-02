# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging
from datetime import datetime, timedelta

_logger = logging.getLogger(__name__)


class DatabaseMaintenance(models.Model):
    """Database maintenance model for Kids Clothing ERP"""
    
    _name = 'database.maintenance'
    _description = 'Database Maintenance'
    _order = 'create_date desc'
    
    # Basic fields
    name = fields.Char(
        string='Maintenance Name',
        required=True,
        help='Name of the maintenance record'
    )
    
    description = fields.Text(
        string='Description',
        help='Description of the maintenance record'
    )
    
    # Database relationship
    database_id = fields.Many2one(
        'database.info',
        string='Database',
        required=True,
        help='Database this maintenance belongs to'
    )
    
    # Maintenance details
    maintenance_type = fields.Selection([
        ('routine', 'Routine Maintenance'),
        ('preventive', 'Preventive Maintenance'),
        ('corrective', 'Corrective Maintenance'),
        ('emergency', 'Emergency Maintenance'),
        ('upgrade', 'Upgrade Maintenance'),
        ('optimization', 'Optimization Maintenance'),
        ('cleanup', 'Cleanup Maintenance'),
        ('custom', 'Custom Maintenance'),
    ], string='Maintenance Type', default='routine', help='Type of maintenance')
    
    # Maintenance status
    status = fields.Selection([
        ('scheduled', 'Scheduled'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='scheduled', help='Status of the maintenance')
    
    # Maintenance scheduling
    scheduled_time = fields.Datetime(
        string='Scheduled Time',
        help='Scheduled maintenance time'
    )
    
    start_time = fields.Datetime(
        string='Start Time',
        help='Maintenance start time'
    )
    
    end_time = fields.Datetime(
        string='End Time',
        help='Maintenance end time'
    )
    
    duration = fields.Float(
        string='Duration (minutes)',
        compute='_compute_duration',
        store=True,
        help='Maintenance duration in minutes'
    )
    
    # Maintenance tasks
    tasks = fields.Text(
        string='Tasks',
        help='Maintenance tasks to perform'
    )
    
    completed_tasks = fields.Text(
        string='Completed Tasks',
        help='Completed maintenance tasks'
    )
    
    # Maintenance impact
    impact_level = fields.Selection([
        ('low', 'Low Impact'),
        ('medium', 'Medium Impact'),
        ('high', 'High Impact'),
        ('critical', 'Critical Impact'),
    ], string='Impact Level', default='low', help='Impact level of maintenance')
    
    downtime_expected = fields.Boolean(
        string='Downtime Expected',
        default=False,
        help='Whether downtime is expected'
    )
    
    downtime_duration = fields.Float(
        string='Downtime Duration (minutes)',
        help='Expected downtime duration in minutes'
    )
    
    # Maintenance requirements
    backup_required = fields.Boolean(
        string='Backup Required',
        default=True,
        help='Whether backup is required before maintenance'
    )
    
    backup_id = fields.Many2one(
        'database.backup',
        string='Backup',
        help='Backup created before maintenance'
    )
    
    maintenance_window = fields.Char(
        string='Maintenance Window',
        help='Maintenance window description'
    )
    
    # Maintenance team
    assigned_to = fields.Many2one(
        'res.users',
        string='Assigned To',
        help='User assigned to maintenance'
    )
    
    team_members = fields.Many2many(
        'res.users',
        'database_maintenance_team_rel',
        'maintenance_id',
        'user_id',
        string='Team Members',
        help='Team members for maintenance'
    )
    
    # Maintenance results
    result_summary = fields.Text(
        string='Result Summary',
        help='Maintenance result summary'
    )
    
    issues_found = fields.Text(
        string='Issues Found',
        help='Issues found during maintenance'
    )
    
    recommendations = fields.Text(
        string='Recommendations',
        help='Recommendations based on maintenance'
    )
    
    # Maintenance metrics
    performance_before = fields.Float(
        string='Performance Before',
        help='Performance metrics before maintenance'
    )
    
    performance_after = fields.Float(
        string='Performance After',
        help='Performance metrics after maintenance'
    )
    
    performance_improvement = fields.Float(
        string='Performance Improvement (%)',
        compute='_compute_performance_improvement',
        store=True,
        help='Performance improvement percentage'
    )
    
    # Maintenance scheduling
    is_recurring = fields.Boolean(
        string='Recurring Maintenance',
        default=False,
        help='Whether this is recurring maintenance'
    )
    
    recurrence_frequency = fields.Selection([
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('yearly', 'Yearly'),
        ('custom', 'Custom'),
    ], string='Recurrence Frequency', help='Recurrence frequency')
    
    next_maintenance = fields.Datetime(
        string='Next Maintenance',
        compute='_compute_next_maintenance',
        store=True,
        help='Next scheduled maintenance time'
    )
    
    # Maintenance notifications
    notification_enabled = fields.Boolean(
        string='Notification Enabled',
        default=True,
        help='Whether notifications are enabled'
    )
    
    notification_email = fields.Char(
        string='Notification Email',
        help='Email address for notifications'
    )
    
    notification_sms = fields.Char(
        string='Notification SMS',
        help='SMS number for notifications'
    )
    
    # Maintenance metadata
    metadata = fields.Text(
        string='Metadata',
        help='Maintenance metadata (JSON format)'
    )
    
    # Maintenance logs
    log_file = fields.Char(
        string='Log File',
        help='Path to maintenance log file'
    )
    
    error_message = fields.Text(
        string='Error Message',
        help='Error message if maintenance failed'
    )
    
    @api.depends('start_time', 'end_time')
    def _compute_duration(self):
        """Compute maintenance duration"""
        for maintenance in self:
            if maintenance.start_time and maintenance.end_time:
                start = fields.Datetime.from_string(maintenance.start_time)
                end = fields.Datetime.from_string(maintenance.end_time)
                duration = (end - start).total_seconds() / 60  # Convert to minutes
                maintenance.duration = duration
            else:
                maintenance.duration = 0.0
    
    @api.depends('performance_before', 'performance_after')
    def _compute_performance_improvement(self):
        """Compute performance improvement"""
        for maintenance in self:
            if maintenance.performance_before and maintenance.performance_after:
                if maintenance.performance_before > 0:
                    improvement = ((maintenance.performance_after - maintenance.performance_before) / maintenance.performance_before) * 100
                    maintenance.performance_improvement = improvement
                else:
                    maintenance.performance_improvement = 0.0
            else:
                maintenance.performance_improvement = 0.0
    
    @api.depends('recurrence_frequency', 'end_time')
    def _compute_next_maintenance(self):
        """Compute next maintenance time"""
        for maintenance in self:
            if maintenance.is_recurring and maintenance.recurrence_frequency and maintenance.end_time:
                end_time = fields.Datetime.from_string(maintenance.end_time)
                if maintenance.recurrence_frequency == 'daily':
                    maintenance.next_maintenance = end_time + timedelta(days=1)
                elif maintenance.recurrence_frequency == 'weekly':
                    maintenance.next_maintenance = end_time + timedelta(weeks=1)
                elif maintenance.recurrence_frequency == 'monthly':
                    maintenance.next_maintenance = end_time + timedelta(days=30)
                elif maintenance.recurrence_frequency == 'quarterly':
                    maintenance.next_maintenance = end_time + timedelta(days=90)
                elif maintenance.recurrence_frequency == 'yearly':
                    maintenance.next_maintenance = end_time + timedelta(days=365)
                else:
                    maintenance.next_maintenance = False
            else:
                maintenance.next_maintenance = False
    
    @api.model
    def create(self, vals):
        """Override create to set default values"""
        # Set default values
        if 'scheduled_time' not in vals:
            vals['scheduled_time'] = fields.Datetime.now()
        
        return super(DatabaseMaintenance, self).create(vals)
    
    def write(self, vals):
        """Override write to handle maintenance updates"""
        result = super(DatabaseMaintenance, self).write(vals)
        
        # Update end time if status changed to completed or failed
        if 'status' in vals and vals['status'] in ['completed', 'failed']:
            for maintenance in self:
                maintenance.end_time = fields.Datetime.now()
        
        return result
    
    def unlink(self):
        """Override unlink to prevent deletion of completed maintenance"""
        for maintenance in self:
            if maintenance.status == 'completed':
                raise ValidationError(_('Cannot delete completed maintenance'))
        
        return super(DatabaseMaintenance, self).unlink()
    
    def action_start_maintenance(self):
        """Start maintenance process"""
        self.ensure_one()
        
        # Check if scheduled time has passed
        if self.scheduled_time and fields.Datetime.now() < self.scheduled_time:
            raise ValidationError(_('Scheduled time has not been reached'))
        
        self.status = 'in_progress'
        self.start_time = fields.Datetime.now()
        
        # Create backup if required
        if self.backup_required:
            backup = self.env['database.backup'].create({
                'database_id': self.database_id.id,
                'backup_type': 'manual',
                'name': f'Pre-maintenance backup for {self.name}',
                'status': 'in_progress',
            })
            self.backup_id = backup.id
        
        # This would need actual implementation to start maintenance
        return True
    
    def action_complete_maintenance(self):
        """Complete maintenance process"""
        self.ensure_one()
        
        self.status = 'completed'
        self.end_time = fields.Datetime.now()
        
        # Complete backup if created
        if self.backup_id:
            self.backup_id.action_complete_backup()
        
        # Update database last maintenance
        self.database_id.last_maintenance = fields.Datetime.now()
        
        return True
    
    def action_fail_maintenance(self, error_message):
        """Fail maintenance process"""
        self.ensure_one()
        
        self.status = 'failed'
        self.end_time = fields.Datetime.now()
        self.error_message = error_message
        
        return True
    
    def action_cancel_maintenance(self):
        """Cancel maintenance"""
        self.ensure_one()
        
        if self.status not in ['scheduled', 'in_progress']:
            raise ValidationError(_('Only scheduled or in-progress maintenance can be cancelled'))
        
        self.status = 'cancelled'
        self.end_time = fields.Datetime.now()
        
        return True
    
    def action_reschedule_maintenance(self, new_time):
        """Reschedule maintenance"""
        self.ensure_one()
        
        if self.status != 'scheduled':
            raise ValidationError(_('Only scheduled maintenance can be rescheduled'))
        
        self.scheduled_time = new_time
        return True
    
    def action_send_notification(self, notification_type, message):
        """Send maintenance notification"""
        self.ensure_one()
        
        if not self.notification_enabled:
            return True
        
        # This would need actual implementation to send notifications
        if self.notification_email:
            # Send email notification
            pass
        
        if self.notification_sms:
            # Send SMS notification
            pass
        
        return True
    
    def action_generate_maintenance_report(self):
        """Generate maintenance report"""
        self.ensure_one()
        
        if self.status != 'completed':
            raise ValidationError(_('Only completed maintenance can generate reports'))
        
        # This would need actual implementation to generate report
        return True
    
    def action_schedule_recurring_maintenance(self):
        """Schedule recurring maintenance"""
        self.ensure_one()
        
        if not self.is_recurring:
            raise ValidationError(_('Maintenance must be marked as recurring'))
        
        # This would need actual implementation to schedule recurring maintenance
        return True
    
    def get_maintenance_info(self):
        """Get maintenance information"""
        return {
            'name': self.name,
            'description': self.description,
            'database_id': self.database_id.id,
            'maintenance_type': self.maintenance_type,
            'status': self.status,
            'scheduled_time': self.scheduled_time,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'duration': self.duration,
            'tasks': self.tasks,
            'completed_tasks': self.completed_tasks,
            'impact_level': self.impact_level,
            'downtime_expected': self.downtime_expected,
            'downtime_duration': self.downtime_duration,
            'backup_required': self.backup_required,
            'backup_id': self.backup_id.id if self.backup_id else None,
            'maintenance_window': self.maintenance_window,
            'assigned_to': self.assigned_to.id if self.assigned_to else None,
            'team_members': [member.id for member in self.team_members],
            'result_summary': self.result_summary,
            'issues_found': self.issues_found,
            'recommendations': self.recommendations,
            'performance_before': self.performance_before,
            'performance_after': self.performance_after,
            'performance_improvement': self.performance_improvement,
            'is_recurring': self.is_recurring,
            'recurrence_frequency': self.recurrence_frequency,
            'next_maintenance': self.next_maintenance,
            'notification_enabled': self.notification_enabled,
            'notification_email': self.notification_email,
            'notification_sms': self.notification_sms,
            'error_message': self.error_message,
        }
    
    def get_maintenance_analytics(self):
        """Get maintenance analytics"""
        return {
            'maintenance_type': self.maintenance_type,
            'status': self.status,
            'duration': self.duration,
            'impact_level': self.impact_level,
            'downtime_expected': self.downtime_expected,
            'downtime_duration': self.downtime_duration,
            'performance_before': self.performance_before,
            'performance_after': self.performance_after,
            'performance_improvement': self.performance_improvement,
            'is_recurring': self.is_recurring,
            'recurrence_frequency': self.recurrence_frequency,
            'next_maintenance': self.next_maintenance,
            'assigned_to': self.assigned_to.id if self.assigned_to else None,
            'team_members': [member.id for member in self.team_members],
        }
    
    @api.model
    def get_maintenance_by_database(self, database_id):
        """Get maintenance by database"""
        return self.search([
            ('database_id', '=', database_id),
            ('status', '=', 'completed'),
        ])
    
    @api.model
    def get_maintenance_by_type(self, maintenance_type):
        """Get maintenance by type"""
        return self.search([
            ('maintenance_type', '=', maintenance_type),
            ('status', '=', 'completed'),
        ])
    
    @api.model
    def get_scheduled_maintenance(self):
        """Get scheduled maintenance"""
        return self.search([
            ('status', '=', 'scheduled'),
            ('scheduled_time', '<=', fields.Datetime.now()),
        ])
    
    @api.model
    def get_recurring_maintenance(self):
        """Get recurring maintenance"""
        return self.search([
            ('is_recurring', '=', True),
            ('status', '=', 'completed'),
        ])
    
    @api.model
    def get_maintenance_analytics_summary(self):
        """Get maintenance analytics summary"""
        total_maintenance = self.search_count([])
        completed_maintenance = self.search_count([('status', '=', 'completed')])
        failed_maintenance = self.search_count([('status', '=', 'failed')])
        scheduled_maintenance = self.search_count([('status', '=', 'scheduled')])
        recurring_maintenance = self.search_count([('is_recurring', '=', True)])
        
        return {
            'total_maintenance': total_maintenance,
            'completed_maintenance': completed_maintenance,
            'failed_maintenance': failed_maintenance,
            'scheduled_maintenance': scheduled_maintenance,
            'recurring_maintenance': recurring_maintenance,
            'in_progress_maintenance': total_maintenance - completed_maintenance - failed_maintenance - scheduled_maintenance,
            'success_rate': (completed_maintenance / total_maintenance * 100) if total_maintenance > 0 else 0,
        }
    
    @api.constrains('name')
    def _check_name(self):
        """Validate maintenance name"""
        for maintenance in self:
            if maintenance.name:
                # Check for duplicate names
                existing = self.search([
                    ('name', '=', maintenance.name),
                    ('id', '!=', maintenance.id),
                ])
                if existing:
                    raise ValidationError(_('Maintenance name must be unique'))
    
    @api.constrains('scheduled_time')
    def _check_scheduled_time(self):
        """Validate scheduled time"""
        for maintenance in self:
            if maintenance.scheduled_time:
                if maintenance.scheduled_time < fields.Datetime.now():
                    raise ValidationError(_('Scheduled time cannot be in the past'))
    
    @api.constrains('downtime_duration')
    def _check_downtime_duration(self):
        """Validate downtime duration"""
        for maintenance in self:
            if maintenance.downtime_expected and maintenance.downtime_duration:
                if maintenance.downtime_duration < 0:
                    raise ValidationError(_('Downtime duration cannot be negative'))
    
    def action_duplicate(self):
        """Duplicate maintenance"""
        self.ensure_one()
        
        new_maintenance = self.copy({
            'name': f'{self.name} (Copy)',
            'status': 'scheduled',
            'start_time': False,
            'end_time': False,
        })
        
        return {
            'type': 'ir.actions.act_window',
            'name': 'Duplicated Maintenance',
            'res_model': 'database.maintenance',
            'res_id': new_maintenance.id,
            'view_mode': 'form',
            'target': 'current',
        }
    
    def action_export_maintenance(self):
        """Export maintenance configuration"""
        self.ensure_one()
        
        return {
            'name': self.name,
            'description': self.description,
            'database_id': self.database_id.id,
            'maintenance_type': self.maintenance_type,
            'scheduled_time': self.scheduled_time,
            'tasks': self.tasks,
            'impact_level': self.impact_level,
            'downtime_expected': self.downtime_expected,
            'downtime_duration': self.downtime_duration,
            'backup_required': self.backup_required,
            'maintenance_window': self.maintenance_window,
            'assigned_to': self.assigned_to.id if self.assigned_to else None,
            'team_members': [member.id for member in self.team_members],
            'is_recurring': self.is_recurring,
            'recurrence_frequency': self.recurrence_frequency,
            'notification_enabled': self.notification_enabled,
            'notification_email': self.notification_email,
            'notification_sms': self.notification_sms,
        }
    
    def action_import_maintenance(self, maintenance_data):
        """Import maintenance configuration"""
        self.ensure_one()
        
        self.write(maintenance_data)
        return True