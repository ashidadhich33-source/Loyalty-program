# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Database - Database Backup Management
======================================================

Standalone version of the database backup management model.
"""

from core_framework.orm import BaseModel, CharField, TextField, BooleanField, IntegerField, DateTimeField, Many2OneField, SelectionField, FloatField
from core_framework.orm import Field
from typing import Dict, Any, Optional
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class DatabaseBackup(BaseModel):
    """Database backup model for Kids Clothing ERP"""
    
    _name = 'database.backup'
    _description = 'Database Backup'
    _table = 'database_backup'
    
    # Basic fields
    name = CharField(
        string='Backup Name',
        size=255,
        required=True,
        help='Name of the backup'
    )
    
    description = TextField(
        string='Description',
        help='Description of the backup'
    )
    
    # Database relationship
    database_id = IntegerField(
        string='Database ID',
        required=True,
        help='Database this backup belongs to'
    )
    
    # Backup details
    backup_type = SelectionField(
        string='Backup Type',
        selection=[
            ('full', 'Full Backup'),
            ('incremental', 'Incremental Backup'),
            ('differential', 'Differential Backup'),
            ('manual', 'Manual Backup'),
            ('scheduled', 'Scheduled Backup'),
            ('emergency', 'Emergency Backup'),
        ],
        default='full',
        help='Type of backup'
    )
    
    # Backup status
    status = SelectionField(
        string='Status',
        selection=[
            ('pending', 'Pending'),
            ('in_progress', 'In Progress'),
            ('completed', 'Completed'),
            ('failed', 'Failed'),
            ('cancelled', 'Cancelled'),
        ],
        default='pending',
        help='Status of the backup'
    )
    
    # Backup file information
    backup_file = CharField(
        string='Backup File',
        size=255,
        help='Name of the backup file'
    )
    
    backup_path = CharField(
        string='Backup Path',
        size=255,
        help='Path to the backup file'
    )
    
    backup_size = FloatField(
        string='Backup Size (MB)',
        default=0.0,
        help='Size of the backup file in MB'
    )
    
    # Backup timing
    start_time = DateTimeField(
        string='Start Time',
        help='Backup start time'
    )
    
    end_time = DateTimeField(
        string='End Time',
        help='Backup end time'
    )
    
    duration = FloatField(
        string='Duration (minutes)',
        default=0.0,
        help='Backup duration in minutes'
    )
    
    # Backup settings
    compression_enabled = BooleanField(
        string='Compression Enabled',
        default=True,
        help='Whether compression is enabled'
    )
    
    encryption_enabled = BooleanField(
        string='Encryption Enabled',
        default=False,
        help='Whether encryption is enabled'
    )
    
    include_data = BooleanField(
        string='Include Data',
        default=True,
        help='Whether to include data in backup'
    )
    
    include_schema = BooleanField(
        string='Include Schema',
        default=True,
        help='Whether to include schema in backup'
    )
    
    include_indexes = BooleanField(
        string='Include Indexes',
        default=True,
        help='Whether to include indexes in backup'
    )
    
    # Backup retention
    retention_days = IntegerField(
        string='Retention Days',
        default=30,
        help='Number of days to retain backup'
    )
    
    expiry_date = DateTimeField(
        string='Expiry Date',
        help='Date when backup expires'
    )
    
    is_expired = BooleanField(
        string='Expired',
        default=False,
        help='Whether backup is expired'
    )
    
    # Backup verification
    verification_enabled = BooleanField(
        string='Verification Enabled',
        default=True,
        help='Whether backup verification is enabled'
    )
    
    verification_status = SelectionField(
        string='Verification Status',
        selection=[
            ('not_verified', 'Not Verified'),
            ('verified', 'Verified'),
            ('verification_failed', 'Verification Failed'),
        ],
        default='not_verified',
        help='Backup verification status'
    )
    
    verification_time = DateTimeField(
        string='Verification Time',
        help='Backup verification time'
    )
    
    # Backup scheduling
    is_scheduled = BooleanField(
        string='Scheduled Backup',
        default=False,
        help='Whether this is a scheduled backup'
    )
    
    schedule_frequency = SelectionField(
        string='Schedule Frequency',
        selection=[
            ('daily', 'Daily'),
            ('weekly', 'Weekly'),
            ('monthly', 'Monthly'),
            ('custom', 'Custom'),
        ],
        help='Backup schedule frequency'
    )
    
    next_backup = DateTimeField(
        string='Next Backup',
        help='Next scheduled backup time'
    )
    
    # Backup analytics
    success_rate = FloatField(
        string='Success Rate (%)',
        default=0.0,
        help='Backup success rate percentage'
    )
    
    total_backups = IntegerField(
        string='Total Backups',
        default=0,
        help='Total number of backups'
    )
    
    successful_backups = IntegerField(
        string='Successful Backups',
        default=0,
        help='Number of successful backups'
    )
    
    failed_backups = IntegerField(
        string='Failed Backups',
        default=0,
        help='Number of failed backups'
    )
    
    # Backup metadata
    metadata = TextField(
        string='Metadata',
        help='Backup metadata (JSON format)'
    )
    
    # Backup logs
    log_file = CharField(
        string='Log File',
        size=255,
        help='Path to backup log file'
    )
    
    error_message = TextField(
        string='Error Message',
        help='Error message if backup failed'
    )
    
    def create(self, vals: Dict[str, Any]):
        """Override create to set default values"""
        # Generate backup name if not provided
        if 'name' not in vals:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            vals['name'] = f'backup_{timestamp}'
        
        # Set start time
        if 'start_time' not in vals:
            vals['start_time'] = datetime.now()
        
        return super().create(vals)
    
    def write(self, vals: Dict[str, Any]):
        """Override write to handle backup updates"""
        result = super().write(vals)
        
        # Update end time if status changed to completed or failed
        if 'status' in vals and vals['status'] in ['completed', 'failed']:
            for backup in self:
                backup.end_time = datetime.now()
        
        return result
    
    def unlink(self):
        """Override unlink to prevent deletion of completed backups"""
        for backup in self:
            if backup.status == 'completed' and not backup.is_expired:
                raise ValueError('Cannot delete completed backup that has not expired')
        
        return super().unlink()
    
    def action_start_backup(self):
        """Start backup process"""
        self.ensure_one()
        
        self.status = 'in_progress'
        self.start_time = datetime.now()
        
        try:
            # Import backup manager
            from core_framework.backup_manager import BackupManager
            from core_framework.config import Config
            
            # Get configuration
            config = Config()
            backup_manager = BackupManager(config)
            
            # Prepare backup configuration
            backup_config = {
                'name': self.name,
                'description': self.description,
                'database_name': config.get('database', {}).get('name', 'ocean_erp'),
                'backup_type': self.backup_type,
                'compression_enabled': self.compression_enabled,
                'encryption_enabled': self.encryption_enabled,
                'include_data': self.include_data,
                'include_schema': self.include_schema,
                'include_indexes': self.include_indexes,
            }
            
            # Create backup
            result = backup_manager.create_backup(backup_config)
            
            if result['success']:
                # Update backup record with results
                updated_config = result['backup_config']
                self.write({
                    'backup_file': updated_config.get('backup_file'),
                    'backup_path': updated_config.get('backup_path'),
                    'backup_size': updated_config.get('backup_size', 0),
                    'end_time': updated_config.get('end_time'),
                    'duration': updated_config.get('duration', 0),
                    'status': 'completed'
                })
                return True
            else:
                # Mark as failed
                self.write({
                    'status': 'failed',
                    'error_message': result.get('error', 'Unknown error'),
                    'end_time': datetime.now()
                })
                return False
                
        except Exception as e:
            # Mark as failed
            self.write({
                'status': 'failed',
                'error_message': str(e),
                'end_time': datetime.now()
            })
            return False
    
    def action_complete_backup(self):
        """Complete backup process"""
        self.ensure_one()
        
        self.status = 'completed'
        self.end_time = datetime.now()
        
        # Update database last backup
        database = self.search([('id', '=', self.database_id)])
        if database:
            database.last_backup = datetime.now()
        
        return True
    
    def action_fail_backup(self, error_message: str):
        """Fail backup process"""
        self.ensure_one()
        
        self.status = 'failed'
        self.end_time = datetime.now()
        self.error_message = error_message
        
        return True
    
    def action_cancel_backup(self):
        """Cancel backup process"""
        self.ensure_one()
        
        self.status = 'cancelled'
        self.end_time = datetime.now()
        
        return True
    
    def action_verify_backup(self):
        """Verify backup"""
        self.ensure_one()
        
        if not self.verification_enabled:
            return True
        
        try:
            # Import backup manager
            from core_framework.backup_manager import BackupManager
            from core_framework.config import Config
            
            # Get configuration
            config = Config()
            backup_manager = BackupManager(config)
            
            # Verify backup
            result = backup_manager.verify_backup(self.backup_path)
            
            if result['success']:
                self.verification_status = 'verified'
                self.verification_time = datetime.now()
                return True
            else:
                self.verification_status = 'verification_failed'
                self.error_message = result.get('error', 'Verification failed')
                return False
                
        except Exception as e:
            self.verification_status = 'verification_failed'
            self.error_message = str(e)
            return False
    
    def action_restore_backup(self):
        """Restore backup"""
        self.ensure_one()
        
        if self.status != 'completed':
            raise ValueError('Only completed backups can be restored')
        
        if self.verification_enabled and self.verification_status != 'verified':
            raise ValueError('Backup must be verified before restoration')
        
        try:
            # Import backup manager
            from core_framework.backup_manager import BackupManager
            from core_framework.config import Config
            
            # Get configuration
            config = Config()
            backup_manager = BackupManager(config)
            
            # Prepare restore configuration
            restore_config = {
                'backup_path': self.backup_path,
                'target_database': config.get('database', {}).get('name', 'ocean_erp'),
                'restore_options': {
                    'clean': True,  # Drop existing objects
                    'create': True,  # Create database if not exists
                }
            }
            
            # Execute restore
            result = backup_manager.restore_backup(restore_config)
            
            if result['success']:
                self.logger.info(f"Backup restored successfully: {self.name}")
                return True
            else:
                error_msg = result.get('error', 'Unknown restore error')
                self.logger.error(f"Restore failed: {error_msg}")
                raise ValueError(f"Restore failed: {error_msg}")
                
        except Exception as e:
            self.logger.error(f"Restore error: {e}")
            raise ValueError(f"Restore error: {str(e)}")
    
    def action_cleanup_backup(self):
        """Cleanup expired backup"""
        self.ensure_one()
        
        if not self.is_expired:
            raise ValueError('Only expired backups can be cleaned up')
        
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
            'database_id': self.database_id,
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
    
    @classmethod
    def get_backups_by_database(cls, database_id: int):
        """Get backups by database"""
        return cls.search([
            ('database_id', '=', database_id),
            ('status', '=', 'completed'),
        ])
    
    @classmethod
    def get_backups_by_type(cls, backup_type: str):
        """Get backups by type"""
        return cls.search([
            ('backup_type', '=', backup_type),
            ('status', '=', 'completed'),
        ])
    
    @classmethod
    def get_scheduled_backups(cls):
        """Get scheduled backups"""
        return cls.search([
            ('is_scheduled', '=', True),
            ('status', '=', 'completed'),
        ])
    
    @classmethod
    def get_expired_backups(cls):
        """Get expired backups"""
        return cls.search([('is_expired', '=', True)])
    
    @classmethod
    def get_backup_analytics_summary(cls):
        """Get backup analytics summary"""
        # In standalone version, we'll return mock data
        return {
            'total_backups': 0,
            'completed_backups': 0,
            'failed_backups': 0,
            'scheduled_backups': 0,
            'expired_backups': 0,
            'pending_backups': 0,
            'success_rate': 0,
        }
    
    def _check_name(self):
        """Validate backup name"""
        if self.name:
            # Check for duplicate names
            existing = self.search([
                ('name', '=', self.name),
                ('id', '!=', self.id),
            ])
            if existing:
                raise ValueError('Backup name must be unique')
    
    def _check_retention_days(self):
        """Validate retention days"""
        if self.retention_days <= 0:
            raise ValueError('Retention days must be greater than 0')
    
    def _check_backup_size(self):
        """Validate backup size"""
        if self.backup_size < 0:
            raise ValueError('Backup size cannot be negative')
    
    def action_duplicate(self):
        """Duplicate backup"""
        self.ensure_one()
        
        new_backup = self.copy({
            'name': f'{self.name} (Copy)',
            'status': 'pending',
            'start_time': None,
            'end_time': None,
        })
        
        return new_backup
    
    def action_export_backup(self):
        """Export backup configuration"""
        self.ensure_one()
        
        return {
            'name': self.name,
            'description': self.description,
            'database_id': self.database_id,
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
    
    def action_import_backup(self, backup_data: Dict[str, Any]):
        """Import backup configuration"""
        self.ensure_one()
        
        self.write(backup_data)
        return True