# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging
import psycopg2
from datetime import datetime, timedelta

_logger = logging.getLogger(__name__)


class DatabaseConnection(models.Model):
    """Database connection model for Kids Clothing ERP"""
    
    _name = 'database.connection'
    _description = 'Database Connection'
    _order = 'create_date desc'
    
    # Basic fields
    name = fields.Char(
        string='Connection Name',
        required=True,
        help='Name of the connection'
    )
    
    description = fields.Text(
        string='Description',
        help='Description of the connection'
    )
    
    # Database relationship
    database_id = fields.Many2one(
        'database.info',
        string='Database',
        required=True,
        help='Database this connection belongs to'
    )
    
    # Connection details
    connection_type = fields.Selection([
        ('read', 'Read Only'),
        ('write', 'Read/Write'),
        ('admin', 'Administrative'),
        ('backup', 'Backup'),
        ('monitoring', 'Monitoring'),
        ('analytics', 'Analytics'),
    ], string='Connection Type', default='read', help='Type of connection')
    
    # Connection status
    status = fields.Selection([
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('error', 'Error'),
        ('timeout', 'Timeout'),
    ], string='Status', default='active', help='Status of the connection')
    
    # Connection details
    host = fields.Char(
        string='Host',
        help='Connection host (overrides database host)'
    )
    
    port = fields.Integer(
        string='Port',
        help='Connection port (overrides database port)'
    )
    
    user = fields.Char(
        string='User',
        help='Connection user (overrides database user)'
    )
    
    password = fields.Char(
        string='Password',
        help='Connection password (overrides database password)'
    )
    
    database_name = fields.Char(
        string='Database Name',
        help='Connection database name (overrides database name)'
    )
    
    # Connection settings
    connection_timeout = fields.Integer(
        string='Connection Timeout (seconds)',
        default=30,
        help='Connection timeout in seconds'
    )
    
    max_connections = fields.Integer(
        string='Max Connections',
        default=10,
        help='Maximum number of connections for this connection type'
    )
    
    current_connections = fields.Integer(
        string='Current Connections',
        compute='_compute_current_connections',
        store=True,
        help='Current number of connections'
    )
    
    # Connection performance
    response_time = fields.Float(
        string='Response Time (ms)',
        compute='_compute_response_time',
        store=True,
        help='Average response time in milliseconds'
    )
    
    total_queries = fields.Integer(
        string='Total Queries',
        compute='_compute_total_queries',
        store=True,
        help='Total number of queries executed'
    )
    
    successful_queries = fields.Integer(
        string='Successful Queries',
        compute='_compute_successful_queries',
        store=True,
        help='Number of successful queries'
    )
    
    failed_queries = fields.Integer(
        string='Failed Queries',
        compute='_compute_failed_queries',
        store=True,
        help='Number of failed queries'
    )
    
    # Connection security
    ssl_enabled = fields.Boolean(
        string='SSL Enabled',
        default=False,
        help='Whether SSL is enabled for this connection'
    )
    
    encryption_enabled = fields.Boolean(
        string='Encryption Enabled',
        default=False,
        help='Whether encryption is enabled for this connection'
    )
    
    # Connection monitoring
    last_activity = fields.Datetime(
        string='Last Activity',
        help='Last activity timestamp'
    )
    
    last_error = fields.Datetime(
        string='Last Error',
        help='Last error timestamp'
    )
    
    error_count = fields.Integer(
        string='Error Count',
        default=0,
        help='Number of errors'
    )
    
    # Connection analytics
    total_connections = fields.Integer(
        string='Total Connections',
        compute='_compute_total_connections',
        store=True,
        help='Total number of connections made'
    )
    
    average_connection_time = fields.Float(
        string='Average Connection Time (ms)',
        compute='_compute_average_connection_time',
        store=True,
        help='Average connection time in milliseconds'
    )
    
    # Connection features
    enable_pooling = fields.Boolean(
        string='Enable Connection Pooling',
        default=True,
        help='Enable connection pooling'
    )
    
    pool_size = fields.Integer(
        string='Pool Size',
        default=5,
        help='Connection pool size'
    )
    
    pool_timeout = fields.Integer(
        string='Pool Timeout (seconds)',
        default=300,
        help='Connection pool timeout in seconds'
    )
    
    # Connection maintenance
    maintenance_required = fields.Boolean(
        string='Maintenance Required',
        default=False,
        help='Whether maintenance is required'
    )
    
    last_maintenance = fields.Datetime(
        string='Last Maintenance',
        help='Last maintenance timestamp'
    )
    
    next_maintenance = fields.Datetime(
        string='Next Maintenance',
        compute='_compute_next_maintenance',
        store=True,
        help='Next maintenance scheduled time'
    )
    
    @api.depends('database_id')
    def _compute_current_connections(self):
        """Compute current connections"""
        for connection in self:
            # This would need actual implementation to get current connections
            connection.current_connections = 0
    
    @api.depends('database_id')
    def _compute_response_time(self):
        """Compute response time"""
        for connection in self:
            # This would need actual implementation to get response time
            connection.response_time = 0.0
    
    @api.depends('database_id')
    def _compute_total_queries(self):
        """Compute total queries"""
        for connection in self:
            # This would need actual implementation to get total queries
            connection.total_queries = 0
    
    @api.depends('database_id')
    def _compute_successful_queries(self):
        """Compute successful queries"""
        for connection in self:
            # This would need actual implementation to get successful queries
            connection.successful_queries = 0
    
    @api.depends('database_id')
    def _compute_failed_queries(self):
        """Compute failed queries"""
        for connection in self:
            # This would need actual implementation to get failed queries
            connection.failed_queries = 0
    
    @api.depends('database_id')
    def _compute_total_connections(self):
        """Compute total connections"""
        for connection in self:
            # This would need actual implementation to get total connections
            connection.total_connections = 0
    
    @api.depends('database_id')
    def _compute_average_connection_time(self):
        """Compute average connection time"""
        for connection in self:
            # This would need actual implementation to get average connection time
            connection.average_connection_time = 0.0
    
    @api.depends('last_maintenance')
    def _compute_next_maintenance(self):
        """Compute next maintenance time"""
        for connection in self:
            if connection.last_maintenance:
                connection.next_maintenance = connection.last_maintenance + timedelta(days=7)
            else:
                connection.next_maintenance = fields.Datetime.now()
    
    @api.model
    def create(self, vals):
        """Override create to set default values"""
        # Set default values from database if not provided
        if 'database_id' in vals:
            database = self.env['database.info'].browse(vals['database_id'])
            if not vals.get('host'):
                vals['host'] = database.host
            if not vals.get('port'):
                vals['port'] = database.port
            if not vals.get('user'):
                vals['user'] = database.user
            if not vals.get('password'):
                vals['password'] = database.password
            if not vals.get('database_name'):
                vals['database_name'] = database.name
        
        return super(DatabaseConnection, self).create(vals)
    
    def write(self, vals):
        """Override write to handle connection updates"""
        result = super(DatabaseConnection, self).write(vals)
        
        # Update last activity if connection details changed
        if any(field in vals for field in ['host', 'port', 'user', 'password', 'database_name']):
            for connection in self:
                connection.last_activity = fields.Datetime.now()
        
        return result
    
    def unlink(self):
        """Override unlink to prevent deletion of active connections"""
        for connection in self:
            if connection.status == 'active':
                raise ValidationError(_('Cannot delete active connection. Please deactivate first.'))
        
        return super(DatabaseConnection, self).unlink()
    
    def action_activate(self):
        """Activate connection"""
        self.status = 'active'
        return True
    
    def action_deactivate(self):
        """Deactivate connection"""
        self.status = 'inactive'
        return True
    
    def action_test_connection(self):
        """Test database connection"""
        self.ensure_one()
        
        try:
            # Get connection parameters
            host = self.host or self.database_id.host
            port = self.port or self.database_id.port
            user = self.user or self.database_id.user
            password = self.password or self.database_id.password
            database_name = self.database_name or self.database_id.name
            
            # Test connection
            conn = psycopg2.connect(
                host=host,
                port=port,
                database=database_name,
                user=user,
                password=password,
                connect_timeout=self.connection_timeout
            )
            conn.close()
            
            self.status = 'active'
            self.last_activity = fields.Datetime.now()
            return True
        except Exception as e:
            self.status = 'error'
            self.last_error = fields.Datetime.now()
            self.error_count += 1
            raise ValidationError(_('Connection test failed: %s') % str(e))
    
    def action_reset_connection(self):
        """Reset connection"""
        self.ensure_one()
        
        self.status = 'inactive'
        self.last_activity = fields.Datetime.now()
        return True
    
    def action_monitor_connection(self):
        """Monitor connection"""
        self.ensure_one()
        
        # This would need actual implementation to monitor connection
        self.last_activity = fields.Datetime.now()
        return True
    
    def action_analyze_connection(self):
        """Analyze connection performance"""
        self.ensure_one()
        
        # This would need actual implementation to analyze connection
        return True
    
    def action_maintain_connection(self):
        """Maintain connection"""
        self.ensure_one()
        
        # This would need actual implementation to maintain connection
        self.last_maintenance = fields.Datetime.now()
        self.maintenance_required = False
        return True
    
    def get_connection_info(self):
        """Get connection information"""
        return {
            'name': self.name,
            'description': self.description,
            'database_id': self.database_id.id,
            'connection_type': self.connection_type,
            'status': self.status,
            'host': self.host or self.database_id.host,
            'port': self.port or self.database_id.port,
            'user': self.user or self.database_id.user,
            'database_name': self.database_name or self.database_id.name,
            'connection_timeout': self.connection_timeout,
            'max_connections': self.max_connections,
            'current_connections': self.current_connections,
            'response_time': self.response_time,
            'total_queries': self.total_queries,
            'successful_queries': self.successful_queries,
            'failed_queries': self.failed_queries,
            'ssl_enabled': self.ssl_enabled,
            'encryption_enabled': self.encryption_enabled,
            'last_activity': self.last_activity,
            'last_error': self.last_error,
            'error_count': self.error_count,
            'total_connections': self.total_connections,
            'average_connection_time': self.average_connection_time,
            'enable_pooling': self.enable_pooling,
            'pool_size': self.pool_size,
            'pool_timeout': self.pool_timeout,
            'maintenance_required': self.maintenance_required,
            'last_maintenance': self.last_maintenance,
            'next_maintenance': self.next_maintenance,
        }
    
    def get_connection_analytics(self):
        """Get connection analytics"""
        return {
            'total_queries': self.total_queries,
            'successful_queries': self.successful_queries,
            'failed_queries': self.failed_queries,
            'response_time': self.response_time,
            'current_connections': self.current_connections,
            'max_connections': self.max_connections,
            'total_connections': self.total_connections,
            'average_connection_time': self.average_connection_time,
            'error_count': self.error_count,
            'last_activity': self.last_activity,
            'last_error': self.last_error,
            'maintenance_required': self.maintenance_required,
            'last_maintenance': self.last_maintenance,
            'next_maintenance': self.next_maintenance,
        }
    
    @api.model
    def get_connections_by_database(self, database_id):
        """Get connections by database"""
        return self.search([
            ('database_id', '=', database_id),
            ('status', '=', 'active'),
        ])
    
    @api.model
    def get_connections_by_type(self, connection_type):
        """Get connections by type"""
        return self.search([
            ('connection_type', '=', connection_type),
            ('status', '=', 'active'),
        ])
    
    @api.model
    def get_active_connections(self):
        """Get active connections"""
        return self.search([('status', '=', 'active')])
    
    @api.model
    def get_connection_analytics_summary(self):
        """Get connection analytics summary"""
        total_connections = self.search_count([])
        active_connections = self.search_count([('status', '=', 'active')])
        error_connections = self.search_count([('status', '=', 'error')])
        timeout_connections = self.search_count([('status', '=', 'timeout')])
        
        return {
            'total_connections': total_connections,
            'active_connections': active_connections,
            'error_connections': error_connections,
            'timeout_connections': timeout_connections,
            'inactive_connections': total_connections - active_connections,
            'active_percentage': (active_connections / total_connections * 100) if total_connections > 0 else 0,
        }
    
    @api.constrains('name')
    def _check_name(self):
        """Validate connection name"""
        for connection in self:
            if connection.name:
                # Check for duplicate names
                existing = self.search([
                    ('name', '=', connection.name),
                    ('id', '!=', connection.id),
                ])
                if existing:
                    raise ValidationError(_('Connection name must be unique'))
    
    @api.constrains('max_connections', 'current_connections')
    def _check_connections(self):
        """Validate connections"""
        for connection in self:
            if connection.current_connections > connection.max_connections:
                raise ValidationError(_('Current connections exceed maximum connections'))
    
    @api.constrains('pool_size')
    def _check_pool_size(self):
        """Validate pool size"""
        for connection in self:
            if connection.pool_size <= 0:
                raise ValidationError(_('Pool size must be greater than 0'))
    
    def action_duplicate(self):
        """Duplicate connection"""
        self.ensure_one()
        
        new_connection = self.copy({
            'name': f'{self.name} (Copy)',
            'status': 'inactive',
        })
        
        return {
            'type': 'ir.actions.act_window',
            'name': 'Duplicated Connection',
            'res_model': 'database.connection',
            'res_id': new_connection.id,
            'view_mode': 'form',
            'target': 'current',
        }
    
    def action_export_connection(self):
        """Export connection configuration"""
        self.ensure_one()
        
        return {
            'name': self.name,
            'description': self.description,
            'database_id': self.database_id.id,
            'connection_type': self.connection_type,
            'host': self.host,
            'port': self.port,
            'user': self.user,
            'database_name': self.database_name,
            'connection_timeout': self.connection_timeout,
            'max_connections': self.max_connections,
            'ssl_enabled': self.ssl_enabled,
            'encryption_enabled': self.encryption_enabled,
            'enable_pooling': self.enable_pooling,
            'pool_size': self.pool_size,
            'pool_timeout': self.pool_timeout,
        }
    
    def action_import_connection(self, connection_data):
        """Import connection configuration"""
        self.ensure_one()
        
        self.write(connection_data)
        return True