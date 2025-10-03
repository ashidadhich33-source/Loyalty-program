# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Database - Database Information Management
===========================================================

Standalone version of the database information management model.
"""

from core_framework.orm import BaseModel, CharField, TextField, BooleanField, IntegerField, DateTimeField, Many2OneField, SelectionField, FloatField, One2ManyField
from core_framework.orm import Field
from typing import Dict, Any, Optional
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class DatabaseInfo(BaseModel):
    """Database information model for Kids Clothing ERP"""
    
    _name = 'database.info'
    _description = 'Database Information'
    _table = 'database_info'
    
    # Basic fields
    name = CharField(
        string='Database Name',
        size=100,
        required=True,
        help='Name of the database'
    )
    
    description = TextField(
        string='Description',
        help='Description of the database'
    )
    
    # Database connection
    host = CharField(
        string='Host',
        size=100,
        required=True,
        help='Database host'
    )
    
    port = IntegerField(
        string='Port',
        default=5432,
        help='Database port'
    )
    
    user = CharField(
        string='User',
        size=100,
        required=True,
        help='Database user'
    )
    
    password = CharField(
        string='Password',
        size=255,
        help='Database password'
    )
    
    # Database status
    is_active = BooleanField(
        string='Active',
        default=True,
        help='Whether the database is active'
    )
    
    is_default = BooleanField(
        string='Default Database',
        default=False,
        help='Whether this is the default database'
    )
    
    is_primary = BooleanField(
        string='Primary Database',
        default=False,
        help='Whether this is the primary database'
    )
    
    # Database type and version
    database_type = SelectionField(
        string='Database Type',
        selection=[
            ('postgresql', 'PostgreSQL'),
            ('mysql', 'MySQL'),
            ('oracle', 'Oracle'),
            ('sqlserver', 'SQL Server'),
            ('sqlite', 'SQLite'),
        ],
        default='postgresql',
        help='Type of database'
    )
    
    database_version = CharField(
        string='Database Version',
        size=50,
        help='Version of the database'
    )
    
    ocean_version = CharField(
        string='Ocean ERP Version',
        size=50,
        help='Ocean ERP version running on this database'
    )
    
    # Database size and performance
    database_size = FloatField(
        string='Database Size (MB)',
        default=0.0,
        help='Size of the database in MB'
    )
    
    table_count = IntegerField(
        string='Table Count',
        default=0,
        help='Number of tables in the database'
    )
    
    record_count = IntegerField(
        string='Record Count',
        default=0,
        help='Total number of records in the database'
    )
    
    # Database health
    health_status = SelectionField(
        string='Health Status',
        selection=[
            ('healthy', 'Healthy'),
            ('warning', 'Warning'),
            ('critical', 'Critical'),
            ('unknown', 'Unknown'),
        ],
        default='unknown',
        help='Health status of the database'
    )
    
    last_backup = DateTimeField(
        string='Last Backup',
        help='Last backup timestamp'
    )
    
    last_maintenance = DateTimeField(
        string='Last Maintenance',
        help='Last maintenance timestamp'
    )
    
    # Database configuration
    max_connections = IntegerField(
        string='Max Connections',
        default=100,
        help='Maximum number of connections'
    )
    
    current_connections = IntegerField(
        string='Current Connections',
        default=0,
        help='Current number of connections'
    )
    
    # Database features
    enable_backup = BooleanField(
        string='Enable Backup',
        default=True,
        help='Enable automatic backup'
    )
    
    enable_monitoring = BooleanField(
        string='Enable Monitoring',
        default=True,
        help='Enable database monitoring'
    )
    
    enable_replication = BooleanField(
        string='Enable Replication',
        default=False,
        help='Enable database replication'
    )
    
    # Database security
    ssl_enabled = BooleanField(
        string='SSL Enabled',
        default=False,
        help='Whether SSL is enabled'
    )
    
    encryption_enabled = BooleanField(
        string='Encryption Enabled',
        default=False,
        help='Whether encryption is enabled'
    )
    
    # Database analytics
    total_queries = IntegerField(
        string='Total Queries',
        default=0,
        help='Total number of queries executed'
    )
    
    slow_queries = IntegerField(
        string='Slow Queries',
        default=0,
        help='Number of slow queries'
    )
    
    average_response_time = FloatField(
        string='Average Response Time (ms)',
        default=0.0,
        help='Average response time in milliseconds'
    )
    
    # Database maintenance
    maintenance_schedule = SelectionField(
        string='Maintenance Schedule',
        selection=[
            ('daily', 'Daily'),
            ('weekly', 'Weekly'),
            ('monthly', 'Monthly'),
            ('manual', 'Manual'),
        ],
        default='weekly',
        help='Maintenance schedule'
    )
    
    next_maintenance = DateTimeField(
        string='Next Maintenance',
        help='Next maintenance scheduled time'
    )
    
    # Database connections
    connection_ids = One2ManyField(
        string='Connections',
        comodel_name='database.connection',
        inverse_name='database_id',
        help='Database connections'
    )
    
    # Database backups
    backup_ids = One2ManyField(
        string='Backups',
        comodel_name='database.backup',
        inverse_name='database_id',
        help='Database backups'
    )
    
    # Database migrations
    migration_ids = One2ManyField(
        string='Migrations',
        comodel_name='database.migration',
        inverse_name='database_id',
        help='Database migrations'
    )
    
    # Database monitoring
    monitoring_ids = One2ManyField(
        string='Monitoring',
        comodel_name='database.monitoring',
        inverse_name='database_id',
        help='Database monitoring records'
    )
    
    # Database analytics
    analytics_ids = One2ManyField(
        string='Analytics',
        comodel_name='database.analytics',
        inverse_name='database_id',
        help='Database analytics records'
    )
    
    def create(self, vals: Dict[str, Any]):
        """Override create to set default values"""
        # Set default values
        if 'host' not in vals:
            vals['host'] = 'localhost'
        
        if 'port' not in vals:
            vals['port'] = 5432
        
        if 'user' not in vals:
            vals['user'] = 'ocean'
        
        return super().create(vals)
    
    def write(self, vals: Dict[str, Any]):
        """Override write to handle database updates"""
        result = super().write(vals)
        
        # Update health status if connection details changed
        if any(field in vals for field in ['host', 'port', 'user', 'password']):
            for database in self:
                database._update_health_status()
        
        return result
    
    def unlink(self):
        """Override unlink to prevent deletion of active databases"""
        for database in self:
            if database.is_active:
                raise ValueError('Cannot delete active database. Please deactivate first.')
            
            if database.is_primary:
                raise ValueError('Cannot delete primary database.')
        
        return super().unlink()
    
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
        other_databases = self.search([('is_default', '=', True)])
        for database in other_databases:
            database.is_default = False
        
        # Set this database as default
        self.is_default = True
        return True
    
    def action_set_primary(self):
        """Set as primary database"""
        # Remove primary from other databases
        other_databases = self.search([('is_primary', '=', True)])
        for database in other_databases:
            database.is_primary = False
        
        # Set this database as primary
        self.is_primary = True
        return True
    
    def action_test_connection(self):
        """Test database connection"""
        self.ensure_one()
        
        try:
            # In standalone version, we'll do basic validation
            if not self.host or not self.user:
                raise ValueError('Host and user are required')
            
            self.health_status = 'healthy'
            return True
        except Exception as e:
            self.health_status = 'critical'
            raise ValueError(f'Database connection failed: {str(e)}')
    
    def action_backup_database(self):
        """Create database backup"""
        self.ensure_one()
        
        # In standalone version, we'll create a mock backup
        backup_data = {
            'database_id': self.id,
            'backup_type': 'manual',
            'status': 'completed',
        }
        
        # This would need actual implementation to create backup
        self.last_backup = datetime.now()
        return backup_data
    
    def action_restore_database(self, backup_id: int):
        """Restore database from backup"""
        self.ensure_one()
        
        # In standalone version, we'll do basic validation
        if not backup_id:
            raise ValueError('Backup ID is required')
        
        # This would need actual implementation to restore database
        return True
    
    def action_migrate_database(self):
        """Migrate database"""
        self.ensure_one()
        
        # In standalone version, we'll create a mock migration
        migration_data = {
            'database_id': self.id,
            'migration_type': 'upgrade',
            'status': 'completed',
        }
        
        # This would need actual implementation to migrate database
        return migration_data
    
    def action_monitor_database(self):
        """Monitor database"""
        self.ensure_one()
        
        # In standalone version, we'll create a mock monitoring
        monitoring_data = {
            'database_id': self.id,
            'monitoring_type': 'health_check',
            'status': 'completed',
        }
        
        # This would need actual implementation to monitor database
        return monitoring_data
    
    def action_analyze_database(self):
        """Analyze database performance"""
        self.ensure_one()
        
        # In standalone version, we'll create a mock analytics
        analytics_data = {
            'database_id': self.id,
            'analytics_type': 'performance',
            'status': 'completed',
        }
        
        # This would need actual implementation to analyze database
        return analytics_data
    
    def action_maintain_database(self):
        """Maintain database"""
        self.ensure_one()
        
        # This would need actual implementation to maintain database
        self.last_maintenance = datetime.now()
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
            'ocean_version': self.ocean_version,
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
    
    @classmethod
    def get_active_databases(cls):
        """Get active databases"""
        return cls.search([('is_active', '=', True)])
    
    @classmethod
    def get_default_database(cls):
        """Get default database"""
        return cls.search([('is_default', '=', True)], limit=1)
    
    @classmethod
    def get_primary_database(cls):
        """Get primary database"""
        return cls.search([('is_primary', '=', True)], limit=1)
    
    @classmethod
    def get_databases_by_type(cls, database_type: str):
        """Get databases by type"""
        return cls.search([
            ('database_type', '=', database_type),
            ('is_active', '=', True),
        ])
    
    @classmethod
    def get_databases_by_health(cls, health_status: str):
        """Get databases by health status"""
        return cls.search([
            ('health_status', '=', health_status),
            ('is_active', '=', True),
        ])
    
    @classmethod
    def get_database_analytics_summary(cls):
        """Get database analytics summary"""
        # In standalone version, we'll return mock data
        return {
            'total_databases': 0,
            'active_databases': 0,
            'healthy_databases': 0,
            'critical_databases': 0,
            'inactive_databases': 0,
            'warning_databases': 0,
            'active_percentage': 0,
            'healthy_percentage': 0,
        }
    
    def _check_name(self):
        """Validate database name"""
        if self.name:
            # Check for duplicate names
            existing = self.search([
                ('name', '=', self.name),
                ('id', '!=', self.id),
            ])
            if existing:
                raise ValueError('Database name must be unique')
    
    def _check_default_database(self):
        """Validate default database"""
        if self.is_default:
            # Check if there's already a default database
            existing_default = self.search([
                ('is_default', '=', True),
                ('id', '!=', self.id),
            ])
            if existing_default:
                raise ValueError('Only one database can be set as default')
    
    def _check_primary_database(self):
        """Validate primary database"""
        if self.is_primary:
            # Check if there's already a primary database
            existing_primary = self.search([
                ('is_primary', '=', True),
                ('id', '!=', self.id),
            ])
            if existing_primary:
                raise ValueError('Only one database can be set as primary')
    
    def _check_connections(self):
        """Validate connections"""
        if self.current_connections > self.max_connections:
            raise ValueError('Current connections exceed maximum connections')
    
    def action_duplicate(self):
        """Duplicate database"""
        self.ensure_one()
        
        new_database = self.copy({
            'name': f'{self.name}_copy',
            'is_default': False,
            'is_primary': False,
        })
        
        return new_database
    
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
            'ocean_version': self.ocean_version,
            'max_connections': self.max_connections,
            'enable_backup': self.enable_backup,
            'enable_monitoring': self.enable_monitoring,
            'enable_replication': self.enable_replication,
            'ssl_enabled': self.ssl_enabled,
            'encryption_enabled': self.encryption_enabled,
            'maintenance_schedule': self.maintenance_schedule,
        }
    
    def action_import_database(self, database_data: Dict[str, Any]):
        """Import database configuration"""
        self.ensure_one()
        
        self.write(database_data)
        return True