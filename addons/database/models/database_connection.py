# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Database - Database Connection Management
==========================================================

Standalone version of the database connection management model.
"""

from core_framework.orm import BaseModel, CharField, TextField, BooleanField, IntegerField, DateTimeField, Many2OneField, SelectionField, FloatField
from core_framework.orm import Field
from typing import Dict, Any, Optional
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class DatabaseConnection(BaseModel):
    """Database connection model for Kids Clothing ERP"""
    
    _name = 'database.connection'
    _description = 'Database Connection'
    _table = 'database_connection'
    
    # Basic fields
    name = CharField(
        string='Connection Name',
        size=255,
        required=True,
        help='Name of the connection'
    )
    
    description = TextField(
        string='Description',
        help='Description of the connection'
    )
    
    # Database relationship
    database_id = IntegerField(
        string='Database ID',
        required=True,
        help='Database this connection belongs to'
    )
    
    # Connection details
    connection_type = SelectionField(
        string='Connection Type',
        selection=[
            ('direct', 'Direct Connection'),
            ('pooled', 'Pooled Connection'),
            ('replica', 'Replica Connection'),
            ('read_only', 'Read-Only Connection'),
            ('write_only', 'Write-Only Connection'),
        ],
        default='direct',
        help='Type of connection'
    )
    
    # Connection status
    status = SelectionField(
        string='Status',
        selection=[
            ('active', 'Active'),
            ('inactive', 'Inactive'),
            ('error', 'Error'),
            ('timeout', 'Timeout'),
        ],
        default='active',
        help='Status of the connection'
    )
    
    # Connection timing
    created_time = DateTimeField(
        string='Created Time',
        default=datetime.now,
        help='Connection creation time'
    )
    
    last_used = DateTimeField(
        string='Last Used',
        help='Last time connection was used'
    )
    
    last_error = DateTimeField(
        string='Last Error',
        help='Last time connection had an error'
    )
    
    # Connection performance
    response_time = FloatField(
        string='Response Time (ms)',
        default=0.0,
        help='Connection response time in milliseconds'
    )
    
    query_count = IntegerField(
        string='Query Count',
        default=0,
        help='Number of queries executed on this connection'
    )
    
    error_count = IntegerField(
        string='Error Count',
        default=0,
        help='Number of errors on this connection'
    )
    
    # Connection settings
    timeout = IntegerField(
        string='Timeout (seconds)',
        default=30,
        help='Connection timeout in seconds'
    )
    
    max_queries = IntegerField(
        string='Max Queries',
        default=1000,
        help='Maximum number of queries per connection'
    )
    
    # Connection security
    ssl_enabled = BooleanField(
        string='SSL Enabled',
        default=False,
        help='Whether SSL is enabled for this connection'
    )
    
    encryption_enabled = BooleanField(
        string='Encryption Enabled',
        default=False,
        help='Whether encryption is enabled for this connection'
    )
    
    # Connection monitoring
    monitoring_enabled = BooleanField(
        string='Monitoring Enabled',
        default=True,
        help='Whether monitoring is enabled for this connection'
    )
    
    alert_threshold = FloatField(
        string='Alert Threshold (ms)',
        default=1000.0,
        help='Response time threshold for alerts'
    )
    
    # Connection analytics
    average_response_time = FloatField(
        string='Average Response Time (ms)',
        default=0.0,
        help='Average response time in milliseconds'
    )
    
    success_rate = FloatField(
        string='Success Rate (%)',
        default=100.0,
        help='Connection success rate percentage'
    )
    
    # Connection metadata
    metadata = TextField(
        string='Metadata',
        help='Connection metadata (JSON format)'
    )
    
    # Connection logs
    log_file = CharField(
        string='Log File',
        size=255,
        help='Path to connection log file'
    )
    
    error_message = TextField(
        string='Error Message',
        help='Last error message'
    )
    
    def create(self, vals: Dict[str, Any]):
        """Override create to set default values"""
        return super().create(vals)
    
    def write(self, vals: Dict[str, Any]):
        """Override write to handle connection updates"""
        result = super().write(vals)
        
        # Update last used time if connection is used
        if 'query_count' in vals:
            for connection in self:
                connection.last_used = datetime.now()
        
        return result
    
    def action_activate(self):
        """Activate connection"""
        self.status = 'active'
        return True
    
    def action_deactivate(self):
        """Deactivate connection"""
        self.status = 'inactive'
        return True
    
    def action_test_connection(self):
        """Test connection"""
        self.ensure_one()
        
        try:
            # In standalone version, we'll do basic validation
            if not self.database_id:
                raise ValueError('Database ID is required')
            
            self.status = 'active'
            self.last_used = datetime.now()
            return True
        except Exception as e:
            self.status = 'error'
            self.last_error = datetime.now()
            self.error_message = str(e)
            raise ValueError(f'Connection test failed: {str(e)}')
    
    def action_reset_connection(self):
        """Reset connection"""
        self.ensure_one()
        
        self.status = 'active'
        self.error_count = 0
        self.error_message = None
        self.last_error = None
        
        return True
    
    def action_monitor_connection(self):
        """Monitor connection"""
        self.ensure_one()
        
        if not self.monitoring_enabled:
            return True
        
        # Check response time
        if self.response_time > self.alert_threshold:
            logger.warning(f'Connection {self.name} response time {self.response_time}ms exceeds threshold {self.alert_threshold}ms')
        
        # Check error count
        if self.error_count > 10:
            logger.warning(f'Connection {self.name} has {self.error_count} errors')
        
        return True
    
    def action_analyze_connection(self):
        """Analyze connection performance"""
        self.ensure_one()
        
        # Calculate success rate
        if self.query_count > 0:
            self.success_rate = ((self.query_count - self.error_count) / self.query_count) * 100
        
        # Update average response time
        if self.query_count > 0:
            self.average_response_time = self.response_time / self.query_count
        
        return True
    
    def get_connection_info(self):
        """Get connection information"""
        return {
            'name': self.name,
            'description': self.description,
            'database_id': self.database_id,
            'connection_type': self.connection_type,
            'status': self.status,
            'created_time': self.created_time,
            'last_used': self.last_used,
            'last_error': self.last_error,
            'response_time': self.response_time,
            'query_count': self.query_count,
            'error_count': self.error_count,
            'timeout': self.timeout,
            'max_queries': self.max_queries,
            'ssl_enabled': self.ssl_enabled,
            'encryption_enabled': self.encryption_enabled,
            'monitoring_enabled': self.monitoring_enabled,
            'alert_threshold': self.alert_threshold,
            'average_response_time': self.average_response_time,
            'success_rate': self.success_rate,
            'error_message': self.error_message,
        }
    
    def get_connection_analytics(self):
        """Get connection analytics"""
        return {
            'response_time': self.response_time,
            'query_count': self.query_count,
            'error_count': self.error_count,
            'average_response_time': self.average_response_time,
            'success_rate': self.success_rate,
            'status': self.status,
            'last_used': self.last_used,
            'last_error': self.last_error,
        }
    
    @classmethod
    def get_connections_by_database(cls, database_id: int):
        """Get connections by database"""
        return cls.search([
            ('database_id', '=', database_id),
            ('status', '=', 'active'),
        ])
    
    @classmethod
    def get_connections_by_type(cls, connection_type: str):
        """Get connections by type"""
        return cls.search([
            ('connection_type', '=', connection_type),
            ('status', '=', 'active'),
        ])
    
    @classmethod
    def get_connections_by_status(cls, status: str):
        """Get connections by status"""
        return cls.search([
            ('status', '=', status),
        ])
    
    @classmethod
    def get_active_connections(cls):
        """Get active connections"""
        return cls.search([
            ('status', '=', 'active'),
        ])
    
    @classmethod
    def get_error_connections(cls):
        """Get connections with errors"""
        return cls.search([
            ('status', '=', 'error'),
        ])
    
    @classmethod
    def get_connection_analytics_summary(cls):
        """Get connection analytics summary"""
        # In standalone version, we'll return mock data
        return {
            'total_connections': 0,
            'active_connections': 0,
            'error_connections': 0,
            'timeout_connections': 0,
            'average_response_time': 0.0,
            'average_success_rate': 0.0,
        }
    
    def _check_name(self):
        """Validate connection name"""
        if self.name:
            # Check for duplicate names
            existing = self.search([
                ('name', '=', self.name),
                ('id', '!=', self.id),
            ])
            if existing:
                raise ValueError('Connection name must be unique')
    
    def _check_timeout(self):
        """Validate timeout"""
        if self.timeout <= 0:
            raise ValueError('Timeout must be greater than 0')
    
    def _check_max_queries(self):
        """Validate max queries"""
        if self.max_queries <= 0:
            raise ValueError('Max queries must be greater than 0')
    
    def _check_alert_threshold(self):
        """Validate alert threshold"""
        if self.alert_threshold <= 0:
            raise ValueError('Alert threshold must be greater than 0')
    
    def action_duplicate(self):
        """Duplicate connection"""
        self.ensure_one()
        
        new_connection = self.copy({
            'name': f'{self.name} (Copy)',
            'status': 'inactive',
            'query_count': 0,
            'error_count': 0,
        })
        
        return new_connection
    
    def action_export_connection(self):
        """Export connection configuration"""
        self.ensure_one()
        
        return {
            'name': self.name,
            'description': self.description,
            'database_id': self.database_id,
            'connection_type': self.connection_type,
            'timeout': self.timeout,
            'max_queries': self.max_queries,
            'ssl_enabled': self.ssl_enabled,
            'encryption_enabled': self.encryption_enabled,
            'monitoring_enabled': self.monitoring_enabled,
            'alert_threshold': self.alert_threshold,
        }
    
    def action_import_connection(self, connection_data: Dict[str, Any]):
        """Import connection configuration"""
        self.ensure_one()
        
        self.write(connection_data)
        return True