# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging
from datetime import datetime, timedelta

_logger = logging.getLogger(__name__)


class DatabaseMigration(models.Model):
    """Database migration model for Kids Clothing ERP"""
    
    _name = 'database.migration'
    _description = 'Database Migration'
    _order = 'create_date desc'
    
    # Basic fields
    name = fields.Char(
        string='Migration Name',
        required=True,
        help='Name of the migration'
    )
    
    description = fields.Text(
        string='Description',
        help='Description of the migration'
    )
    
    # Database relationship
    database_id = fields.Many2one(
        'database.info',
        string='Database',
        required=True,
        help='Database this migration belongs to'
    )
    
    # Migration details
    migration_type = fields.Selection([
        ('upgrade', 'Upgrade'),
        ('downgrade', 'Downgrade'),
        ('schema_change', 'Schema Change'),
        ('data_migration', 'Data Migration'),
        ('index_optimization', 'Index Optimization'),
        ('cleanup', 'Cleanup'),
        ('custom', 'Custom'),
    ], string='Migration Type', default='upgrade', help='Type of migration')
    
    # Migration status
    status = fields.Selection([
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('rolled_back', 'Rolled Back'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='pending', help='Status of the migration')
    
    # Migration versioning
    from_version = fields.Char(
        string='From Version',
        help='Source version for migration'
    )
    
    to_version = fields.Char(
        string='To Version',
        help='Target version for migration'
    )
    
    migration_script = fields.Text(
        string='Migration Script',
        help='Migration script content'
    )
    
    rollback_script = fields.Text(
        string='Rollback Script',
        help='Rollback script content'
    )
    
    # Migration timing
    start_time = fields.Datetime(
        string='Start Time',
        help='Migration start time'
    )
    
    end_time = fields.Datetime(
        string='End Time',
        help='Migration end time'
    )
    
    duration = fields.Float(
        string='Duration (minutes)',
        compute='_compute_duration',
        store=True,
        help='Migration duration in minutes'
    )
    
    # Migration settings
    backup_before_migration = fields.Boolean(
        string='Backup Before Migration',
        default=True,
        help='Whether to backup before migration'
    )
    
    backup_id = fields.Many2one(
        'database.backup',
        string='Backup',
        help='Backup created before migration'
    )
    
    rollback_enabled = fields.Boolean(
        string='Rollback Enabled',
        default=True,
        help='Whether rollback is enabled'
    )
    
    # Migration validation
    validation_enabled = fields.Boolean(
        string='Validation Enabled',
        default=True,
        help='Whether validation is enabled'
    )
    
    validation_status = fields.Selection([
        ('not_validated', 'Not Validated'),
        ('validated', 'Validated'),
        ('validation_failed', 'Validation Failed'),
    ], string='Validation Status', default='not_validated', help='Migration validation status')
    
    validation_time = fields.Datetime(
        string='Validation Time',
        help='Migration validation time'
    )
    
    # Migration impact
    affected_tables = fields.Text(
        string='Affected Tables',
        help='Tables affected by migration'
    )
    
    affected_records = fields.Integer(
        string='Affected Records',
        help='Number of records affected by migration'
    )
    
    # Migration scheduling
    is_scheduled = fields.Boolean(
        string='Scheduled Migration',
        default=False,
        help='Whether this is a scheduled migration'
    )
    
    scheduled_time = fields.Datetime(
        string='Scheduled Time',
        help='Scheduled migration time'
    )
    
    # Migration dependencies
    depends_on = fields.Many2many(
        'database.migration',
        'database_migration_dependency_rel',
        'migration_id',
        'dependency_id',
        string='Depends On',
        help='Migrations this migration depends on'
    )
    
    required_by = fields.Many2many(
        'database.migration',
        'database_migration_dependency_rel',
        'dependency_id',
        'migration_id',
        string='Required By',
        help='Migrations that depend on this migration'
    )
    
    # Migration analytics
    success_rate = fields.Float(
        string='Success Rate (%)',
        compute='_compute_success_rate',
        store=True,
        help='Migration success rate percentage'
    )
    
    total_migrations = fields.Integer(
        string='Total Migrations',
        compute='_compute_total_migrations',
        store=True,
        help='Total number of migrations'
    )
    
    successful_migrations = fields.Integer(
        string='Successful Migrations',
        compute='_compute_successful_migrations',
        store=True,
        help='Number of successful migrations'
    )
    
    failed_migrations = fields.Integer(
        string='Failed Migrations',
        compute='_compute_failed_migrations',
        store=True,
        help='Number of failed migrations'
    )
    
    # Migration metadata
    metadata = fields.Text(
        string='Metadata',
        help='Migration metadata (JSON format)'
    )
    
    # Migration logs
    log_file = fields.Char(
        string='Log File',
        help='Path to migration log file'
    )
    
    error_message = fields.Text(
        string='Error Message',
        help='Error message if migration failed'
    )
    
    # Migration results
    result_summary = fields.Text(
        string='Result Summary',
        help='Migration result summary'
    )
    
    performance_impact = fields.Selection([
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ], string='Performance Impact', help='Performance impact of migration')
    
    @api.depends('start_time', 'end_time')
    def _compute_duration(self):
        """Compute migration duration"""
        for migration in self:
            if migration.start_time and migration.end_time:
                start = fields.Datetime.from_string(migration.start_time)
                end = fields.Datetime.from_string(migration.end_time)
                duration = (end - start).total_seconds() / 60  # Convert to minutes
                migration.duration = duration
            else:
                migration.duration = 0.0
    
    @api.depends('database_id')
    def _compute_success_rate(self):
        """Compute success rate"""
        for migration in self:
            database_migrations = self.search([('database_id', '=', migration.database_id.id)])
            if database_migrations:
                successful = database_migrations.filtered(lambda m: m.status == 'completed')
                migration.success_rate = (len(successful) / len(database_migrations)) * 100
            else:
                migration.success_rate = 0.0
    
    @api.depends('database_id')
    def _compute_total_migrations(self):
        """Compute total migrations"""
        for migration in self:
            migration.total_migrations = self.search_count([('database_id', '=', migration.database_id.id)])
    
    @api.depends('database_id')
    def _compute_successful_migrations(self):
        """Compute successful migrations"""
        for migration in self:
            migration.successful_migrations = self.search_count([
                ('database_id', '=', migration.database_id.id),
                ('status', '=', 'completed')
            ])
    
    @api.depends('database_id')
    def _compute_failed_migrations(self):
        """Compute failed migrations"""
        for migration in self:
            migration.failed_migrations = self.search_count([
                ('database_id', '=', migration.database_id.id),
                ('status', '=', 'failed')
            ])
    
    @api.model
    def create(self, vals):
        """Override create to set default values"""
        # Generate migration name if not provided
        if 'name' not in vals:
            database = self.env['database.info'].browse(vals.get('database_id'))
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            vals['name'] = f'{database.name}_migration_{timestamp}'
        
        return super(DatabaseMigration, self).create(vals)
    
    def write(self, vals):
        """Override write to handle migration updates"""
        result = super(DatabaseMigration, self).write(vals)
        
        # Update end time if status changed to completed, failed, or rolled back
        if 'status' in vals and vals['status'] in ['completed', 'failed', 'rolled_back']:
            for migration in self:
                migration.end_time = fields.Datetime.now()
        
        return result
    
    def unlink(self):
        """Override unlink to prevent deletion of completed migrations"""
        for migration in self:
            if migration.status == 'completed':
                raise ValidationError(_('Cannot delete completed migration'))
        
        return super(DatabaseMigration, self).unlink()
    
    def action_start_migration(self):
        """Start migration process"""
        self.ensure_one()
        
        # Check dependencies
        for dep in self.depends_on:
            if dep.status != 'completed':
                raise ValidationError(_('Migration dependencies not completed'))
        
        self.status = 'in_progress'
        self.start_time = fields.Datetime.now()
        
        # Create backup if enabled
        if self.backup_before_migration:
            backup = self.env['database.backup'].create({
                'database_id': self.database_id.id,
                'backup_type': 'manual',
                'name': f'Pre-migration backup for {self.name}',
                'status': 'in_progress',
            })
            self.backup_id = backup.id
        
        # This would need actual implementation to start migration
        return True
    
    def action_complete_migration(self):
        """Complete migration process"""
        self.ensure_one()
        
        self.status = 'completed'
        self.end_time = fields.Datetime.now()
        
        # Complete backup if created
        if self.backup_id:
            self.backup_id.action_complete_backup()
        
        return True
    
    def action_fail_migration(self, error_message):
        """Fail migration process"""
        self.ensure_one()
        
        self.status = 'failed'
        self.end_time = fields.Datetime.now()
        self.error_message = error_message
        
        return True
    
    def action_rollback_migration(self):
        """Rollback migration"""
        self.ensure_one()
        
        if not self.rollback_enabled:
            raise ValidationError(_('Rollback is not enabled for this migration'))
        
        if self.status not in ['completed', 'failed']:
            raise ValidationError(_('Only completed or failed migrations can be rolled back'))
        
        self.status = 'rolled_back'
        self.end_time = fields.Datetime.now()
        
        # This would need actual implementation to rollback migration
        return True
    
    def action_cancel_migration(self):
        """Cancel migration"""
        self.ensure_one()
        
        if self.status not in ['pending', 'in_progress']:
            raise ValidationError(_('Only pending or in-progress migrations can be cancelled'))
        
        self.status = 'cancelled'
        self.end_time = fields.Datetime.now()
        
        return True
    
    def action_validate_migration(self):
        """Validate migration"""
        self.ensure_one()
        
        if not self.validation_enabled:
            return True
        
        try:
            # This would need actual implementation to validate migration
            self.validation_status = 'validated'
            self.validation_time = fields.Datetime.now()
            return True
        except Exception as e:
            self.validation_status = 'validation_failed'
            self.error_message = str(e)
            return False
    
    def action_schedule_migration(self, scheduled_time):
        """Schedule migration"""
        self.ensure_one()
        
        self.is_scheduled = True
        self.scheduled_time = scheduled_time
        return True
    
    def action_unschedule_migration(self):
        """Unschedule migration"""
        self.ensure_one()
        
        self.is_scheduled = False
        self.scheduled_time = False
        return True
    
    def action_execute_migration(self):
        """Execute migration"""
        self.ensure_one()
        
        if self.status != 'pending':
            raise ValidationError(_('Only pending migrations can be executed'))
        
        # Check if scheduled time has passed
        if self.is_scheduled and self.scheduled_time:
            if fields.Datetime.now() < self.scheduled_time:
                raise ValidationError(_('Scheduled time has not been reached'))
        
        return self.action_start_migration()
    
    def get_migration_info(self):
        """Get migration information"""
        return {
            'name': self.name,
            'description': self.description,
            'database_id': self.database_id.id,
            'migration_type': self.migration_type,
            'status': self.status,
            'from_version': self.from_version,
            'to_version': self.to_version,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'duration': self.duration,
            'backup_before_migration': self.backup_before_migration,
            'backup_id': self.backup_id.id if self.backup_id else None,
            'rollback_enabled': self.rollback_enabled,
            'validation_enabled': self.validation_enabled,
            'validation_status': self.validation_status,
            'validation_time': self.validation_time,
            'affected_tables': self.affected_tables,
            'affected_records': self.affected_records,
            'is_scheduled': self.is_scheduled,
            'scheduled_time': self.scheduled_time,
            'success_rate': self.success_rate,
            'total_migrations': self.total_migrations,
            'successful_migrations': self.successful_migrations,
            'failed_migrations': self.failed_migrations,
            'error_message': self.error_message,
            'result_summary': self.result_summary,
            'performance_impact': self.performance_impact,
        }
    
    def get_migration_analytics(self):
        """Get migration analytics"""
        return {
            'success_rate': self.success_rate,
            'total_migrations': self.total_migrations,
            'successful_migrations': self.successful_migrations,
            'failed_migrations': self.failed_migrations,
            'duration': self.duration,
            'validation_status': self.validation_status,
            'is_scheduled': self.is_scheduled,
            'scheduled_time': self.scheduled_time,
            'affected_records': self.affected_records,
            'performance_impact': self.performance_impact,
        }
    
    @api.model
    def get_migrations_by_database(self, database_id):
        """Get migrations by database"""
        return self.search([
            ('database_id', '=', database_id),
            ('status', '=', 'completed'),
        ])
    
    @api.model
    def get_migrations_by_type(self, migration_type):
        """Get migrations by type"""
        return self.search([
            ('migration_type', '=', migration_type),
            ('status', '=', 'completed'),
        ])
    
    @api.model
    def get_scheduled_migrations(self):
        """Get scheduled migrations"""
        return self.search([
            ('is_scheduled', '=', True),
            ('status', '=', 'pending'),
        ])
    
    @api.model
    def get_pending_migrations(self):
        """Get pending migrations"""
        return self.search([('status', '=', 'pending')])
    
    @api.model
    def get_migration_analytics_summary(self):
        """Get migration analytics summary"""
        total_migrations = self.search_count([])
        completed_migrations = self.search_count([('status', '=', 'completed')])
        failed_migrations = self.search_count([('status', '=', 'failed')])
        scheduled_migrations = self.search_count([('is_scheduled', '=', True)])
        pending_migrations = self.search_count([('status', '=', 'pending')])
        
        return {
            'total_migrations': total_migrations,
            'completed_migrations': completed_migrations,
            'failed_migrations': failed_migrations,
            'scheduled_migrations': scheduled_migrations,
            'pending_migrations': pending_migrations,
            'in_progress_migrations': total_migrations - completed_migrations - failed_migrations - pending_migrations,
            'success_rate': (completed_migrations / total_migrations * 100) if total_migrations > 0 else 0,
        }
    
    @api.constrains('name')
    def _check_name(self):
        """Validate migration name"""
        for migration in self:
            if migration.name:
                # Check for duplicate names
                existing = self.search([
                    ('name', '=', migration.name),
                    ('id', '!=', migration.id),
                ])
                if existing:
                    raise ValidationError(_('Migration name must be unique'))
    
    @api.constrains('depends_on')
    def _check_dependencies(self):
        """Validate migration dependencies"""
        for migration in self:
            if migration in migration.depends_on:
                raise ValidationError(_('Migration cannot depend on itself'))
            
            # Check for circular dependencies
            for dep in migration.depends_on:
                if migration in dep.required_by:
                    raise ValidationError(_('Circular dependency detected'))
    
    @api.constrains('from_version', 'to_version')
    def _check_versions(self):
        """Validate migration versions"""
        for migration in self:
            if migration.from_version and migration.to_version:
                if migration.from_version == migration.to_version:
                    raise ValidationError(_('From version and to version cannot be the same'))
    
    def action_duplicate(self):
        """Duplicate migration"""
        self.ensure_one()
        
        new_migration = self.copy({
            'name': f'{self.name} (Copy)',
            'status': 'pending',
            'start_time': False,
            'end_time': False,
        })
        
        return {
            'type': 'ir.actions.act_window',
            'name': 'Duplicated Migration',
            'res_model': 'database.migration',
            'res_id': new_migration.id,
            'view_mode': 'form',
            'target': 'current',
        }
    
    def action_export_migration(self):
        """Export migration configuration"""
        self.ensure_one()
        
        return {
            'name': self.name,
            'description': self.description,
            'database_id': self.database_id.id,
            'migration_type': self.migration_type,
            'from_version': self.from_version,
            'to_version': self.to_version,
            'migration_script': self.migration_script,
            'rollback_script': self.rollback_script,
            'backup_before_migration': self.backup_before_migration,
            'rollback_enabled': self.rollback_enabled,
            'validation_enabled': self.validation_enabled,
            'affected_tables': self.affected_tables,
            'affected_records': self.affected_records,
            'is_scheduled': self.is_scheduled,
            'scheduled_time': self.scheduled_time,
            'performance_impact': self.performance_impact,
        }
    
    def action_import_migration(self, migration_data):
        """Import migration configuration"""
        self.ensure_one()
        
        self.write(migration_data)
        return True