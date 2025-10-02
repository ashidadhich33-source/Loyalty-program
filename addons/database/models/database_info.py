# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
import logging
import psycopg2
import os
from datetime import datetime, timedelta

_logger = logging.getLogger(__name__)


class DatabaseInfo(models.Model):
    """Database information model for Kids Clothing ERP"""
    
    _name = 'database.info'
    _description = 'Database Information'
    _order = 'name'
    
    # Basic fields
    name = fields.Char(
        string='Database Name',
        required=True,
        help='Name of the database'
    )
    
    description = fields.Text(
        string='Description',
        help='Description of the database'
    )
    
    # Database connection
    host = fields.Char(
        string='Host',
        required=True,
        help='Database host'
    )
    
    port = fields.Integer(
        string='Port',
        default=5432,
        help='Database port'
    )
    
    user = fields.Char(
        string='User',
        required=True,
        help='Database user'
    )
    
    password = fields.Char(
        string='Password',
        help='Database password'
    )
    
    # Database status
    is_active = fields.Boolean(
        string='Active',
        default=True,
        help='Whether the database is active'
    )
    
    is_default = fields.Boolean(
        string='Default Database',
        default=False,
        help='Whether this is the default database'
    )
    
    is_primary = fields.Boolean(
        string='Primary Database',
        default=False,
        help='Whether this is the primary database'
    )
    
    # Database type and version
    database_type = fields.Selection([
        ('postgresql', 'PostgreSQL'),
        ('mysql', 'MySQL'),
        ('oracle', 'Oracle'),
        ('sqlserver', 'SQL Server'),
        ('sqlite', 'SQLite'),
    ], string='Database Type', default='postgresql', help='Type of database')
    
    database_version = fields.Char(
        string='Database Version',
        help='Version of the database'
    )
    
    odoo_version = fields.Char(
        string='Odoo Version',
        help='Odoo version running on this database'
    )
    
    # Database size and performance
    database_size = fields.Float(
        string='Database Size (MB)',
        compute='_compute_database_size',
        store=True,
        help='Size of the database in MB'
    )
    
    table_count = fields.Integer(
        string='Table Count',
        compute='_compute_table_count',
        store=True,
        help='Number of tables in the database'
    )
    
    record_count = fields.Integer(
        string='Record Count',
        compute='_compute_record_count',
        store=True,
        help='Total number of records in the database'
    )
    
    # Database health
    health_status = fields.Selection([
        ('healthy', 'Healthy'),
        ('warning', 'Warning'),
        ('critical', 'Critical'),
        ('unknown', 'Unknown'),
    ], string='Health Status', default='unknown', help='Health status of the database')
    
    last_backup = fields.Datetime(
        string='Last Backup',
        help='Last backup timestamp'
    )
    
    last_maintenance = fields.Datetime(
        string='Last Maintenance',
        help='Last maintenance timestamp'
    )
    
    # Database configuration
    max_connections = fields.Integer(
        string='Max Connections',
        default=100,
        help='Maximum number of connections'
    )
    
    current_connections = fields.Integer(
        string='Current Connections',
        compute='_compute_current_connections',
        store=True,
        help='Current number of connections'
    )
    
    # Database features
    enable_backup = fields.Boolean(
        string='Enable Backup',
        default=True,
        help='Enable automatic backup'
    )
    
    enable_monitoring = fields.Boolean(
        string='Enable Monitoring',
        default=True,
        help='Enable database monitoring'
    )
    
    enable_replication = fields.Boolean(
        string='Enable Replication',
        default=False,
        help='Enable database replication'
    )
    
    # Database security
    ssl_enabled = fields.Boolean(
        string='SSL Enabled',
        default=False,
        help='Whether SSL is enabled'
    )
    
    encryption_enabled = fields.Boolean(
        string='Encryption Enabled',
        default=False,
        help='Whether encryption is enabled'
    )
    
    # Database analytics
    total_queries = fields.Integer(
        string='Total Queries',
        compute='_compute_total_queries',
        store=True,
        help='Total number of queries executed'
    )
    
    slow_queries = fields.Integer(
        string='Slow Queries',
        compute='_compute_slow_queries',
        store=True,
        help='Number of slow queries'
    )
    
    average_response_time = fields.Float(
        string='Average Response Time (ms)',
        compute='_compute_average_response_time',
        store=True,
        help='Average response time in milliseconds'
    )
    
    # Database maintenance
    maintenance_schedule = fields.Selection([
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('manual', 'Manual'),
    ], string='Maintenance Schedule', default='weekly', help='Maintenance schedule')
    
    next_maintenance = fields.Datetime(
        string='Next Maintenance',
        compute='_compute_next_maintenance',
        store=True,
        help='Next maintenance scheduled time'
    )
    
    # Database connections
    connection_ids = fields.One2many(
        'database.connection',
        'database_id',
        string='Connections',
        help='Database connections'
    )
    
    # Database backups
    backup_ids = fields.One2many(
        'database.backup',
        'database_id',
        string='Backups',
        help='Database backups'
    )
    
    # Database migrations
    migration_ids = fields.One2many(
        'database.migration',
        'database_id',
        string='Migrations',
        help='Database migrations'
    )
    
    # Database monitoring
    monitoring_ids = fields.One2many(
        'database.monitoring',
        'database_id',
        string='Monitoring',
        help='Database monitoring records'
    )
    
    # Database analytics
    analytics_ids = fields.One2many(
        'database.analytics',
        'database_id',
        string='Analytics',
        help='Database analytics records'
    )
    
    @api.depends('name')
    def _compute_database_size(self):
        """Compute database size"""
        for database in self:
            try:
                # This would need actual implementation to get database size
                database.database_size = 0.0
            except Exception as e:
                _logger.error(f"Error computing database size: {str(e)}")
                database.database_size = 0.0
    
    @api.depends('name')
    def _compute_table_count(self):
        """Compute table count"""
        for database in self:
            try:
                # This would need actual implementation to get table count
                database.table_count = 0
            except Exception as e:
                _logger.error(f"Error computing table count: {str(e)}")
                database.table_count = 0
    
    @api.depends('name')
    def _compute_record_count(self):
        """Compute record count"""
        for database in self:
            try:
                # This would need actual implementation to get record count
                database.record_count = 0
            except Exception as e:
                _logger.error(f"Error computing record count: {str(e)}")
                database.record_count = 0
    
    @api.depends('name')
    def _compute_current_connections(self):
        """Compute current connections"""
        for database in self:
            try:
                # This would need actual implementation to get current connections
                database.current_connections = 0
            except Exception as e:
                _logger.error(f"Error computing current connections: {str(e)}")
                database.current_connections = 0
    
    @api.depends('name')
    def _compute_total_queries(self):
        """Compute total queries"""
        for database in self:
            try:
                # This would need actual implementation to get total queries
                database.total_queries = 0
            except Exception as e:
                _logger.error(f"Error computing total queries: {str(e)}")
                database.total_queries = 0
    
    @api.depends('name')
    def _compute_slow_queries(self):
        """Compute slow queries"""
        for database in self:
            try:
                # This would need actual implementation to get slow queries
                database.slow_queries = 0
            except Exception as e:
                _logger.error(f"Error computing slow queries: {str(e)}")
                database.slow_queries = 0
    
    @api.depends('name')
    def _compute_average_response_time(self):
        """Compute average response time"""
        for database in self:
            try:
                # This would need actual implementation to get average response time
                database.average_response_time = 0.0
            except Exception as e:
                _logger.error(f"Error computing average response time: {str(e)}")
                database.average_response_time = 0.0
    
    @api.depends('maintenance_schedule', 'last_maintenance')
    def _compute_next_maintenance(self):
        """Compute next maintenance time"""
        for database in self:
            if database.last_maintenance:
                if database.maintenance_schedule == 'daily':
                    database.next_maintenance = database.last_maintenance + timedelta(days=1)
                elif database.maintenance_schedule == 'weekly':
                    database.next_maintenance = database.last_maintenance + timedelta(weeks=1)
                elif database.maintenance_schedule == 'monthly':
                    database.next_maintenance = database.last_maintenance + timedelta(days=30)
                else:
                    database.next_maintenance = False
            else:
                database.next_maintenance = fields.Datetime.now()
    
    @api.model
    def create(self, vals):
        """Override create to set default values"""
        # Set default values
        if 'host' not in vals:
            vals['host'] = 'localhost'
        
        if 'port' not in vals:
            vals['port'] = 5432
        
        if 'user' not in vals:
            vals['user'] = 'odoo'
        
        return super(DatabaseInfo, self).create(vals)
    
    def write(self, vals):
        """Override write to handle database updates"""
        result = super(DatabaseInfo, self).write(vals)
        
        # Update health status if connection details changed
        if any(field in vals for field in ['host', 'port', 'user', 'password']):
            for database in self:
                database._update_health_status()
        
        return result
    
    def unlink(self):
        """Override unlink to prevent deletion of active databases"""
        for database in self:
            if database.is_active:
                raise ValidationError(_('Cannot delete active database. Please deactivate first.'))
            
            if database.is_primary:
                raise ValidationError(_('Cannot delete primary database.'))
        
        return super(DatabaseInfo, self).unlink()
    
    def action_activate(self):
        """Activate database"""
        self.is_active = True
        return True
    
    def action_deactivate(self):
        """Deactivate database"""
        self.is_active = False
        return True
    
    def action_set_default(self):
        """Set as default database"""
        # Remove default from other databases
        self.search([('is_default', '=', True)]).write({'is_default': False})
        
        # Set this database as default
        self.is_default = True
        return True
    
    def action_set_primary(self):
        """Set as primary database"""
        # Remove primary from other databases
        self.search([('is_primary', '=', True)]).write({'is_primary': False})
        
        # Set this database as primary
        self.is_primary = True
        return True
    
    def action_test_connection(self):
        """Test database connection"""
        self.ensure_one()
        
        try:
            # Test connection
            conn = psycopg2.connect(
                host=self.host,
                port=self.port,
                database=self.name,
                user=self.user,
                password=self.password
            )
            conn.close()
            
            self.health_status = 'healthy'
            return True
        except Exception as e:
            self.health_status = 'critical'
            raise ValidationError(_('Database connection failed: %s') % str(e))
    
    def action_backup_database(self):
        """Create database backup"""
        self.ensure_one()
        
        backup = self.env['database.backup'].create({
            'database_id': self.id,
            'backup_type': 'manual',
            'status': 'in_progress',
        })
        
        # This would need actual implementation to create backup
        backup.status = 'completed'
        backup.backup_file = f'backup_{self.name}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.sql'
        
        self.last_backup = fields.Datetime.now()
        return backup
    
    def action_restore_database(self, backup_id):
        """Restore database from backup"""
        self.ensure_one()
        
        backup = self.env['database.backup'].browse(backup_id)
        
        if not backup.exists():
            raise ValidationError(_('Backup not found'))
        
        if backup.status != 'completed':
            raise ValidationError(_('Backup is not completed'))
        
        # This would need actual implementation to restore database
        return True
    
    def action_migrate_database(self):
        """Migrate database"""
        self.ensure_one()
        
        migration = self.env['database.migration'].create({
            'database_id': self.id,
            'migration_type': 'upgrade',
            'status': 'in_progress',
        })
        
        # This would need actual implementation to migrate database
        migration.status = 'completed'
        return migration
    
    def action_monitor_database(self):
        """Monitor database"""
        self.ensure_one()
        
        monitoring = self.env['database.monitoring'].create({
            'database_id': self.id,
            'monitoring_type': 'health_check',
            'status': 'in_progress',
        })
        
        # This would need actual implementation to monitor database
        monitoring.status = 'completed'
        return monitoring
    
    def action_analyze_database(self):
        """Analyze database performance"""
        self.ensure_one()
        
        analytics = self.env['database.analytics'].create({
            'database_id': self.id,
            'analytics_type': 'performance',
            'status': 'in_progress',
        })
        
        # This would need actual implementation to analyze database
        analytics.status = 'completed'
        return analytics
    
    def action_maintain_database(self):
        """Maintain database"""
        self.ensure_one()
        
        # This would need actual implementation to maintain database
        self.last_maintenance = fields.Datetime.now()
        return True
    
    def _update_health_status(self):
        """Update database health status"""
        try:
            self.action_test_connection()
        except Exception:
            self.health_status = 'critical'
    
    def get_database_info(self):
        """Get database information"""
        return {
            'name': self.name,
            'description': self.description,
            'host': self.host,
            'port': self.port,
            'user': self.user,
            'database_type': self.database_type,
            'database_version': self.database_version,
            'odoo_version': self.odoo_version,
            'database_size': self.database_size,
            'table_count': self.table_count,
            'record_count': self.record_count,
            'health_status': self.health_status,
            'is_active': self.is_active,
            'is_default': self.is_default,
            'is_primary': self.is_primary,
        }
    
    def get_database_analytics(self):
        """Get database analytics"""
        return {
            'total_queries': self.total_queries,
            'slow_queries': self.slow_queries,
            'average_response_time': self.average_response_time,
            'current_connections': self.current_connections,
            'max_connections': self.max_connections,
            'database_size': self.database_size,
            'table_count': self.table_count,
            'record_count': self.record_count,
            'health_status': self.health_status,
            'last_backup': self.last_backup,
            'last_maintenance': self.last_maintenance,
            'next_maintenance': self.next_maintenance,
        }
    
    @api.model
    def get_active_databases(self):
        """Get active databases"""
        return self.search([('is_active', '=', True)])
    
    @api.model
    def get_default_database(self):
        """Get default database"""
        return self.search([('is_default', '=', True)], limit=1)
    
    @api.model
    def get_primary_database(self):
        """Get primary database"""
        return self.search([('is_primary', '=', True)], limit=1)
    
    @api.model
    def get_databases_by_type(self, database_type):
        """Get databases by type"""
        return self.search([
            ('database_type', '=', database_type),
            ('is_active', '=', True),
        ])
    
    @api.model
    def get_databases_by_health(self, health_status):
        """Get databases by health status"""
        return self.search([
            ('health_status', '=', health_status),
            ('is_active', '=', True),
        ])
    
    @api.model
    def get_database_analytics_summary(self):
        """Get database analytics summary"""
        total_databases = self.search_count([])
        active_databases = self.search_count([('is_active', '=', True)])
        healthy_databases = self.search_count([('health_status', '=', 'healthy')])
        critical_databases = self.search_count([('health_status', '=', 'critical')])
        
        return {
            'total_databases': total_databases,
            'active_databases': active_databases,
            'healthy_databases': healthy_databases,
            'critical_databases': critical_databases,
            'inactive_databases': total_databases - active_databases,
            'warning_databases': total_databases - healthy_databases - critical_databases,
            'active_percentage': (active_databases / total_databases * 100) if total_databases > 0 else 0,
            'healthy_percentage': (healthy_databases / total_databases * 100) if total_databases > 0 else 0,
        }
    
    @api.constrains('name')
    def _check_name(self):
        """Validate database name"""
        for database in self:
            if database.name:
                # Check for duplicate names
                existing = self.search([
                    ('name', '=', database.name),
                    ('id', '!=', database.id),
                ])
                if existing:
                    raise ValidationError(_('Database name must be unique'))
    
    @api.constrains('is_default')
    def _check_default_database(self):
        """Validate default database"""
        for database in self:
            if database.is_default:
                # Check if there's already a default database
                existing_default = self.search([
                    ('is_default', '=', True),
                    ('id', '!=', database.id),
                ])
                if existing_default:
                    raise ValidationError(_('Only one database can be set as default'))
    
    @api.constrains('is_primary')
    def _check_primary_database(self):
        """Validate primary database"""
        for database in self:
            if database.is_primary:
                # Check if there's already a primary database
                existing_primary = self.search([
                    ('is_primary', '=', True),
                    ('id', '!=', database.id),
                ])
                if existing_primary:
                    raise ValidationError(_('Only one database can be set as primary'))
    
    @api.constrains('max_connections', 'current_connections')
    def _check_connections(self):
        """Validate connections"""
        for database in self:
            if database.current_connections > database.max_connections:
                raise ValidationError(_('Current connections exceed maximum connections'))
    
    def action_duplicate(self):
        """Duplicate database"""
        self.ensure_one()
        
        new_database = self.copy({
            'name': f'{self.name}_copy',
            'is_default': False,
            'is_primary': False,
        })
        
        return {
            'type': 'ir.actions.act_window',
            'name': 'Duplicated Database',
            'res_model': 'database.info',
            'res_id': new_database.id,
            'view_mode': 'form',
            'target': 'current',
        }
    
    def action_export_database(self):
        """Export database configuration"""
        self.ensure_one()
        
        return {
            'name': self.name,
            'description': self.description,
            'host': self.host,
            'port': self.port,
            'user': self.user,
            'database_type': self.database_type,
            'database_version': self.database_version,
            'odoo_version': self.odoo_version,
            'max_connections': self.max_connections,
            'enable_backup': self.enable_backup,
            'enable_monitoring': self.enable_monitoring,
            'enable_replication': self.enable_replication,
            'ssl_enabled': self.ssl_enabled,
            'encryption_enabled': self.encryption_enabled,
            'maintenance_schedule': self.maintenance_schedule,
        }
    
    def action_import_database(self, database_data):
        """Import database configuration"""
        self.ensure_one()
        
        self.write(database_data)
        return True