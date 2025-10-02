# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging
import os
from datetime import datetime, timedelta

_logger = logging.getLogger(__name__)


class DatabaseBackup(models.Model):
    """Database backup model for Kids Clothing ERP"""
    
    _name = 'database.backup'
    _description = 'Database Backup'
    _order = 'create_date desc'
    
    # Basic fields
    name = fields.Char(
        string='Backup Name',
        required=True,
        help='Name of the backup'
    )
    
    description = fields.Text(
        string='Description',
        help='Description of the backup'
    )
    
    # Database relationship
    database_id = fields.Many2one(
        'database.info',
        string='Database',
        required=True,
        help='Database this backup belongs to'
    )
    
    # Backup details
    backup_type = fields.Selection([
        ('full', 'Full Backup'),
        ('incremental', 'Incremental Backup'),
        ('differential', 'Differential Backup'),
        ('manual', 'Manual Backup'),
        ('scheduled', 'Scheduled Backup'),
        ('emergency', 'Emergency Backup'),
    ], string='Backup Type', default='full', help='Type of backup')
    
    # Backup status
    status = fields.Selection([
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='pending', help='Status of the backup')
    
    # Backup file information
    backup_file = fields.Char(
        string='Backup File',
        help='Name of the backup file'
    )
    
    backup_path = fields.Char(
        string='Backup Path',
        help='Path to the backup file'
    )
    
    backup_size = fields.Float(
        string='Backup Size (MB)',
        compute='_compute_backup_size',
        store=True,
        help='Size of the backup file in MB'
    )
    
    # Backup timing
    start_time = fields.Datetime(
        string='Start Time',
        help='Backup start time'
    )
    
    end_time = fields.Datetime(
        string='End Time',
        help='Backup end time'
    )
    
    duration = fields.Float(
        string='Duration (minutes)',
        compute='_compute_duration',
        store=True,
        help='Backup duration in minutes'
    )
    
    # Backup settings
    compression_enabled = fields.Boolean(
        string='Compression Enabled',
        default=True,
        help='Whether compression is enabled'
    )
    
    encryption_enabled = fields.Boolean(
        string='Encryption Enabled',
        default=False,
        help='Whether encryption is enabled'
    )
    
    include_data = fields.Boolean(
        string='Include Data',
        default=True,
        help='Whether to include data in backup'
    )
    
    include_schema = fields.Boolean(
        string='Include Schema',
        default=True,
        help='Whether to include schema in backup'
    )
    
    include_indexes = fields.Boolean(
        string='Include Indexes',
        default=True,
        help='Whether to include indexes in backup'
    )
    
    # Backup retention
    retention_days = fields.Integer(
        string='Retention Days',
        default=30,
        help='Number of days to retain backup'
    )
    
    expiry_date = fields.Datetime(
        string='Expiry Date',
        compute='_compute_expiry_date',
        store=True,
        help='Date when backup expires'
    )
    
    is_expired = fields.Boolean(
        string='Expired',
        compute='_compute_is_expired',
        store=True,
        help='Whether backup is expired'
    )
    
    # Backup verification
    verification_enabled = fields.Boolean(
        string='Verification Enabled',
        default=True,
        help='Whether backup verification is enabled'
    )
    
    verification_status = fields.Selection([
        ('not_verified', 'Not Verified'),
        ('verified', 'Verified'),
        ('verification_failed', 'Verification Failed'),
    ], string='Verification Status', default='not_verified', help='Backup verification status')
    
    verification_time = fields.Datetime(
        string='Verification Time',
        help='Backup verification time'
    )
    
    # Backup scheduling
    is_scheduled = fields.Boolean(
        string='Scheduled Backup',
        default=False,
        help='Whether this is a scheduled backup'
    )
    
    schedule_frequency = fields.Selection([
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('custom', 'Custom'),
    ], string='Schedule Frequency', help='Backup schedule frequency')
    
    next_backup = fields.Datetime(
        string='Next Backup',
        compute='_compute_next_backup',
        store=True,
        help='Next scheduled backup time'
    )
    
    # Backup analytics
    success_rate = fields.Float(
        string='Success Rate (%)',
        compute='_compute_success_rate',
        store=True,
        help='Backup success rate percentage'
    )
    
    total_backups = fields.Integer(
        string='Total Backups',
        compute='_compute_total_backups',
        store=True,
        help='Total number of backups'
    )
    
    successful_backups = fields.Integer(
        string='Successful Backups',
        compute='_compute_successful_backups',
        store=True,
        help='Number of successful backups'
    )
    
    failed_backups = fields.Integer(
        string='Failed Backups',
        compute='_compute_failed_backups',
        store=True,
        help='Number of failed backups'
    )
    
    # Backup metadata
    metadata = fields.Text(
        string='Metadata',
        help='Backup metadata (JSON format)'
    )
    
    # Backup logs
    log_file = fields.Char(
        string='Log File',
        help='Path to backup log file'
    )
    
    error_message = fields.Text(
        string='Error Message',
        help='Error message if backup failed'
    )
    
    @api.depends('backup_file', 'backup_path')
    def _compute_backup_size(self):
        """Compute backup size"""
        for backup in self:
            if backup.backup_file and backup.backup_path:
                try:
                    file_path = os.path.join(backup.backup_path, backup.backup_file)
                    if os.path.exists(file_path):
                        backup.backup_size = os.path.getsize(file_path) / (1024 * 1024)  # Convert to MB
                    else:
                        backup.backup_size = 0.0
                except Exception as e:
                    _logger.error(f"Error computing backup size: {str(e)}")
                    backup.backup_size = 0.0
            else:
                backup.backup_size = 0.0
    
    @api.depends('start_time', 'end_time')
    def _compute_duration(self):
        """Compute backup duration"""
        for backup in self:
            if backup.start_time and backup.end_time:
                start = fields.Datetime.from_string(backup.start_time)
                end = fields.Datetime.from_string(backup.end_time)
                duration = (end - start).total_seconds() / 60  # Convert to minutes
                backup.duration = duration
            else:
                backup.duration = 0.0
    
    @api.depends('create_date', 'retention_days')
    def _compute_expiry_date(self):
        """Compute expiry date"""
        for backup in self:
            if backup.create_date:
                create_date = fields.Datetime.from_string(backup.create_date)
                backup.expiry_date = create_date + timedelta(days=backup.retention_days)
            else:
                backup.expiry_date = False
    
    @api.depends('expiry_date')
    def _compute_is_expired(self):
        """Compute if backup is expired"""
        for backup in self:
            if backup.expiry_date:
                expiry_date = fields.Datetime.from_string(backup.expiry_date)
                backup.is_expired = expiry_date < fields.Datetime.now()
            else:
                backup.is_expired = False
    
    @api.depends('schedule_frequency', 'create_date')
    def _compute_next_backup(self):
        """Compute next backup time"""
        for backup in self:
            if backup.is_scheduled and backup.schedule_frequency:
                if backup.create_date:
                    create_date = fields.Datetime.from_string(backup.create_date)
                    if backup.schedule_frequency == 'daily':
                        backup.next_backup = create_date + timedelta(days=1)
                    elif backup.schedule_frequency == 'weekly':
                        backup.next_backup = create_date + timedelta(weeks=1)
                    elif backup.schedule_frequency == 'monthly':
                        backup.next_backup = create_date + timedelta(days=30)
                    else:
                        backup.next_backup = False
                else:
                    backup.next_backup = fields.Datetime.now()
            else:
                backup.next_backup = False
    
    @api.depends('database_id')
    def _compute_success_rate(self):
        """Compute success rate"""
        for backup in self:
            database_backups = self.search([('database_id', '=', backup.database_id.id)])
            if database_backups:
                successful = database_backups.filtered(lambda b: b.status == 'completed')
                backup.success_rate = (len(successful) / len(database_backups)) * 100
            else:
                backup.success_rate = 0.0
    
    @api.depends('database_id')
    def _compute_total_backups(self):
        """Compute total backups"""
        for backup in self:
            backup.total_backups = self.search_count([('database_id', '=', backup.database_id.id)])
    
    @api.depends('database_id')
    def _compute_successful_backups(self):
        """Compute successful backups"""
        for backup in self:
            backup.successful_backups = self.search_count([
                ('database_id', '=', backup.database_id.id),
                ('status', '=', 'completed')
            ])
    
    @api.depends('database_id')
    def _compute_failed_backups(self):
        """Compute failed backups"""
        for backup in self:
            backup.failed_backups = self.search_count([
                ('database_id', '=', backup.database_id.id),
                ('status', '=', 'failed')
            ])
    
    @api.model
    def create(self, vals):
        """Override create to set default values"""
        # Generate backup name if not provided
        if 'name' not in vals:
            database = self.env['database.info'].browse(vals.get('database_id'))
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            vals['name'] = f'{database.name}_backup_{timestamp}'
        
        # Set start time
        if 'start_time' not in vals:
            vals['start_time'] = fields.Datetime.now()
        
        return super(DatabaseBackup, self).create(vals)
    
    def write(self, vals):
        """Override write to handle backup updates"""
        result = super(DatabaseBackup, self).write(vals)
        
        # Update end time if status changed to completed or failed
        if 'status' in vals and vals['status'] in ['completed', 'failed']:
            for backup in self:
                backup.end_time = fields.Datetime.now()
        
        return result
    
    def unlink(self):
        """Override unlink to prevent deletion of completed backups"""
        for backup in self:
            if backup.status == 'completed' and not backup.is_expired:
                raise ValidationError(_('Cannot delete completed backup that has not expired'))
        
        return super(DatabaseBackup, self).unlink()
    
    def action_start_backup(self):
        """Start backup process"""
        self.ensure_one()
        
        self.status = 'in_progress'
        self.start_time = fields.Datetime.now()
        
        # This would need actual implementation to start backup
        return True
    
    def action_complete_backup(self):
        """Complete backup process"""
        self.ensure_one()
        
        self.status = 'completed'
        self.end_time = fields.Datetime.now()
        
        # Update database last backup
        self.database_id.last_backup = fields.Datetime.now()
        
        return True
    
    def action_fail_backup(self, error_message):
        """Fail backup process"""
        self.ensure_one()
        
        self.status = 'failed'
        self.end_time = fields.Datetime.now()
        self.error_message = error_message
        
        return True
    
    def action_cancel_backup(self):
        """Cancel backup process"""
        self.ensure_one()
        
        self.status = 'cancelled'
        self.end_time = fields.Datetime.now()
        
        return True
    
    def action_verify_backup(self):
        """Verify backup"""
        self.ensure_one()
        
        if not self.verification_enabled:
            return True
        
        try:
            # This would need actual implementation to verify backup
            self.verification_status = 'verified'
            self.verification_time = fields.Datetime.now()
            return True
        except Exception as e:
            self.verification_status = 'verification_failed'
            self.error_message = str(e)
            return False
    
    def action_restore_backup(self):
        """Restore backup"""
        self.ensure_one()
        
        if self.status != 'completed':
            raise ValidationError(_('Only completed backups can be restored'))
        
        if self.verification_enabled and self.verification_status != 'verified':
            raise ValidationError(_('Backup must be verified before restoration'))
        
        # This would need actual implementation to restore backup
        return True
    
    def action_cleanup_backup(self):
        """Cleanup expired backup"""
        self.ensure_one()
        
        if not self.is_expired:
            raise ValidationError(_('Only expired backups can be cleaned up'))
        
        # This would need actual implementation to cleanup backup
        return True
    
    def action_schedule_backup(self):
        """Schedule backup"""
        self.ensure_one()
        
        self.is_scheduled = True
        return True
    
    def action_unschedule_backup(self):
        """Unschedule backup"""
        self.ensure_one()
        
        self.is_scheduled = False
        return True
    
    def get_backup_info(self):
        """Get backup information"""
        return {
            'name': self.name,
            'description': self.description,
            'database_id': self.database_id.id,
            'backup_type': self.backup_type,
            'status': self.status,
            'backup_file': self.backup_file,
            'backup_path': self.backup_path,
            'backup_size': self.backup_size,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'duration': self.duration,
            'compression_enabled': self.compression_enabled,
            'encryption_enabled': self.encryption_enabled,
            'include_data': self.include_data,
            'include_schema': self.include_schema,
            'include_indexes': self.include_indexes,
            'retention_days': self.retention_days,
            'expiry_date': self.expiry_date,
            'is_expired': self.is_expired,
            'verification_enabled': self.verification_enabled,
            'verification_status': self.verification_status,
            'verification_time': self.verification_time,
            'is_scheduled': self.is_scheduled,
            'schedule_frequency': self.schedule_frequency,
            'next_backup': self.next_backup,
            'success_rate': self.success_rate,
            'total_backups': self.total_backups,
            'successful_backups': self.successful_backups,
            'failed_backups': self.failed_backups,
            'error_message': self.error_message,
        }
    
    def get_backup_analytics(self):
        """Get backup analytics"""
        return {
            'success_rate': self.success_rate,
            'total_backups': self.total_backups,
            'successful_backups': self.successful_backups,
            'failed_backups': self.failed_backups,
            'backup_size': self.backup_size,
            'duration': self.duration,
            'verification_status': self.verification_status,
            'is_expired': self.is_expired,
            'is_scheduled': self.is_scheduled,
            'next_backup': self.next_backup,
        }
    
    @api.model
    def get_backups_by_database(self, database_id):
        """Get backups by database"""
        return self.search([
            ('database_id', '=', database_id),
            ('status', '=', 'completed'),
        ])
    
    @api.model
    def get_backups_by_type(self, backup_type):
        """Get backups by type"""
        return self.search([
            ('backup_type', '=', backup_type),
            ('status', '=', 'completed'),
        ])
    
    @api.model
    def get_scheduled_backups(self):
        """Get scheduled backups"""
        return self.search([
            ('is_scheduled', '=', True),
            ('status', '=', 'completed'),
        ])
    
    @api.model
    def get_expired_backups(self):
        """Get expired backups"""
        return self.search([('is_expired', '=', True)])
    
    @api.model
    def get_backup_analytics_summary(self):
        """Get backup analytics summary"""
        total_backups = self.search_count([])
        completed_backups = self.search_count([('status', '=', 'completed')])
        failed_backups = self.search_count([('status', '=', 'failed')])
        scheduled_backups = self.search_count([('is_scheduled', '=', True)])
        expired_backups = self.search_count([('is_expired', '=', True)])
        
        return {
            'total_backups': total_backups,
            'completed_backups': completed_backups,
            'failed_backups': failed_backups,
            'scheduled_backups': scheduled_backups,
            'expired_backups': expired_backups,
            'pending_backups': total_backups - completed_backups - failed_backups,
            'success_rate': (completed_backups / total_backups * 100) if total_backups > 0 else 0,
        }
    
    @api.constrains('name')
    def _check_name(self):
        """Validate backup name"""
        for backup in self:
            if backup.name:
                # Check for duplicate names
                existing = self.search([
                    ('name', '=', backup.name),
                    ('id', '!=', backup.id),
                ])
                if existing:
                    raise ValidationError(_('Backup name must be unique'))
    
    @api.constrains('retention_days')
    def _check_retention_days(self):
        """Validate retention days"""
        for backup in self:
            if backup.retention_days <= 0:
                raise ValidationError(_('Retention days must be greater than 0'))
    
    @api.constrains('backup_size')
    def _check_backup_size(self):
        """Validate backup size"""
        for backup in self:
            if backup.backup_size < 0:
                raise ValidationError(_('Backup size cannot be negative'))
    
    def action_duplicate(self):
        """Duplicate backup"""
        self.ensure_one()
        
        new_backup = self.copy({
            'name': f'{self.name} (Copy)',
            'status': 'pending',
            'start_time': False,
            'end_time': False,
        })
        
        return {
            'type': 'ir.actions.act_window',
            'name': 'Duplicated Backup',
            'res_model': 'database.backup',
            'res_id': new_backup.id,
            'view_mode': 'form',
            'target': 'current',
        }
    
    def action_export_backup(self):
        """Export backup configuration"""
        self.ensure_one()
        
        return {
            'name': self.name,
            'description': self.description,
            'database_id': self.database_id.id,
            'backup_type': self.backup_type,
            'compression_enabled': self.compression_enabled,
            'encryption_enabled': self.encryption_enabled,
            'include_data': self.include_data,
            'include_schema': self.include_schema,
            'include_indexes': self.include_indexes,
            'retention_days': self.retention_days,
            'verification_enabled': self.verification_enabled,
            'is_scheduled': self.is_scheduled,
            'schedule_frequency': self.schedule_frequency,
        }
    
    def action_import_backup(self, backup_data):
        """Import backup configuration"""
        self.ensure_one()
        
        self.write(backup_data)
        return True