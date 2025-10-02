# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging
from datetime import datetime, timedelta

_logger = logging.getLogger(__name__)


class DatabaseMonitoring(models.Model):
    """Database monitoring model for Kids Clothing ERP"""
    
    _name = 'database.monitoring'
    _description = 'Database Monitoring'
    _order = 'create_date desc'
    
    # Basic fields
    name = fields.Char(
        string='Monitoring Name',
        required=True,
        help='Name of the monitoring record'
    )
    
    description = fields.Text(
        string='Description',
        help='Description of the monitoring record'
    )
    
    # Database relationship
    database_id = fields.Many2one(
        'database.info',
        string='Database',
        required=True,
        help='Database this monitoring belongs to'
    )
    
    # Monitoring details
    monitoring_type = fields.Selection([
        ('health_check', 'Health Check'),
        ('performance', 'Performance Monitoring'),
        ('security', 'Security Monitoring'),
        ('backup', 'Backup Monitoring'),
        ('connection', 'Connection Monitoring'),
        ('storage', 'Storage Monitoring'),
        ('query', 'Query Monitoring'),
        ('error', 'Error Monitoring'),
        ('custom', 'Custom Monitoring'),
    ], string='Monitoring Type', default='health_check', help='Type of monitoring')
    
    # Monitoring status
    status = fields.Selection([
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('error', 'Error'),
        ('warning', 'Warning'),
        ('critical', 'Critical'),
    ], string='Status', default='active', help='Status of the monitoring')
    
    # Monitoring metrics
    cpu_usage = fields.Float(
        string='CPU Usage (%)',
        help='CPU usage percentage'
    )
    
    memory_usage = fields.Float(
        string='Memory Usage (%)',
        help='Memory usage percentage'
    )
    
    disk_usage = fields.Float(
        string='Disk Usage (%)',
        help='Disk usage percentage'
    )
    
    connection_count = fields.Integer(
        string='Connection Count',
        help='Number of active connections'
    )
    
    query_count = fields.Integer(
        string='Query Count',
        help='Number of queries executed'
    )
    
    slow_query_count = fields.Integer(
        string='Slow Query Count',
        help='Number of slow queries'
    )
    
    error_count = fields.Integer(
        string='Error Count',
        help='Number of errors'
    )
    
    # Performance metrics
    response_time = fields.Float(
        string='Response Time (ms)',
        help='Average response time in milliseconds'
    )
    
    throughput = fields.Float(
        string='Throughput (queries/sec)',
        help='Queries per second'
    )
    
    latency = fields.Float(
        string='Latency (ms)',
        help='Average latency in milliseconds'
    )
    
    # Storage metrics
    database_size = fields.Float(
        string='Database Size (MB)',
        help='Database size in MB'
    )
    
    table_count = fields.Integer(
        string='Table Count',
        help='Number of tables'
    )
    
    record_count = fields.Integer(
        string='Record Count',
        help='Total number of records'
    )
    
    # Security metrics
    failed_logins = fields.Integer(
        string='Failed Logins',
        help='Number of failed login attempts'
    )
    
    security_violations = fields.Integer(
        string='Security Violations',
        help='Number of security violations'
    )
    
    # Monitoring settings
    monitoring_interval = fields.Integer(
        string='Monitoring Interval (minutes)',
        default=5,
        help='Monitoring interval in minutes'
    )
    
    alert_threshold = fields.Float(
        string='Alert Threshold (%)',
        default=80.0,
        help='Alert threshold percentage'
    )
    
    critical_threshold = fields.Float(
        string='Critical Threshold (%)',
        default=95.0,
        help='Critical threshold percentage'
    )
    
    # Monitoring alerts
    alert_enabled = fields.Boolean(
        string='Alert Enabled',
        default=True,
        help='Whether alerts are enabled'
    )
    
    alert_email = fields.Char(
        string='Alert Email',
        help='Email address for alerts'
    )
    
    alert_sms = fields.Char(
        string='Alert SMS',
        help='SMS number for alerts'
    )
    
    # Monitoring history
    last_check = fields.Datetime(
        string='Last Check',
        help='Last monitoring check time'
    )
    
    next_check = fields.Datetime(
        string='Next Check',
        compute='_compute_next_check',
        store=True,
        help='Next monitoring check time'
    )
    
    check_count = fields.Integer(
        string='Check Count',
        default=0,
        help='Number of monitoring checks performed'
    )
    
    # Monitoring results
    health_score = fields.Float(
        string='Health Score',
        compute='_compute_health_score',
        store=True,
        help='Overall health score (0-100)'
    )
    
    performance_score = fields.Float(
        string='Performance Score',
        compute='_compute_performance_score',
        store=True,
        help='Performance score (0-100)'
    )
    
    security_score = fields.Float(
        string='Security Score',
        compute='_compute_security_score',
        store=True,
        help='Security score (0-100)'
    )
    
    # Monitoring analytics
    average_cpu_usage = fields.Float(
        string='Average CPU Usage (%)',
        compute='_compute_average_cpu_usage',
        store=True,
        help='Average CPU usage percentage'
    )
    
    average_memory_usage = fields.Float(
        string='Average Memory Usage (%)',
        compute='_compute_average_memory_usage',
        store=True,
        help='Average memory usage percentage'
    )
    
    average_response_time = fields.Float(
        string='Average Response Time (ms)',
        compute='_compute_average_response_time',
        store=True,
        help='Average response time in milliseconds'
    )
    
    # Monitoring trends
    cpu_trend = fields.Selection([
        ('increasing', 'Increasing'),
        ('decreasing', 'Decreasing'),
        ('stable', 'Stable'),
    ], string='CPU Trend', help='CPU usage trend')
    
    memory_trend = fields.Selection([
        ('increasing', 'Increasing'),
        ('decreasing', 'Decreasing'),
        ('stable', 'Stable'),
    ], string='Memory Trend', help='Memory usage trend')
    
    performance_trend = fields.Selection([
        ('improving', 'Improving'),
        ('degrading', 'Degrading'),
        ('stable', 'Stable'),
    ], string='Performance Trend', help='Performance trend')
    
    # Monitoring metadata
    metadata = fields.Text(
        string='Metadata',
        help='Monitoring metadata (JSON format)'
    )
    
    # Monitoring logs
    log_file = fields.Char(
        string='Log File',
        help='Path to monitoring log file'
    )
    
    error_message = fields.Text(
        string='Error Message',
        help='Error message if monitoring failed'
    )
    
    @api.depends('monitoring_interval', 'last_check')
    def _compute_next_check(self):
        """Compute next check time"""
        for monitoring in self:
            if monitoring.last_check:
                last_check = fields.Datetime.from_string(monitoring.last_check)
                monitoring.next_check = last_check + timedelta(minutes=monitoring.monitoring_interval)
            else:
                monitoring.next_check = fields.Datetime.now()
    
    @api.depends('cpu_usage', 'memory_usage', 'disk_usage', 'response_time', 'error_count')
    def _compute_health_score(self):
        """Compute health score"""
        for monitoring in self:
            # Calculate health score based on various metrics
            cpu_score = max(0, 100 - monitoring.cpu_usage)
            memory_score = max(0, 100 - monitoring.memory_usage)
            disk_score = max(0, 100 - monitoring.disk_usage)
            response_score = max(0, 100 - (monitoring.response_time / 10))  # Normalize response time
            error_score = max(0, 100 - (monitoring.error_count * 10))  # Penalize errors
            
            monitoring.health_score = (cpu_score + memory_score + disk_score + response_score + error_score) / 5
    
    @api.depends('response_time', 'throughput', 'latency', 'slow_query_count')
    def _compute_performance_score(self):
        """Compute performance score"""
        for monitoring in self:
            # Calculate performance score based on performance metrics
            response_score = max(0, 100 - (monitoring.response_time / 10))
            throughput_score = min(100, monitoring.throughput * 10)  # Normalize throughput
            latency_score = max(0, 100 - (monitoring.latency / 10))
            slow_query_score = max(0, 100 - (monitoring.slow_query_count * 5))
            
            monitoring.performance_score = (response_score + throughput_score + latency_score + slow_query_score) / 4
    
    @api.depends('failed_logins', 'security_violations', 'error_count')
    def _compute_security_score(self):
        """Compute security score"""
        for monitoring in self:
            # Calculate security score based on security metrics
            login_score = max(0, 100 - (monitoring.failed_logins * 5))
            violation_score = max(0, 100 - (monitoring.security_violations * 10))
            error_score = max(0, 100 - (monitoring.error_count * 2))
            
            monitoring.security_score = (login_score + violation_score + error_score) / 3
    
    @api.depends('database_id')
    def _compute_average_cpu_usage(self):
        """Compute average CPU usage"""
        for monitoring in self:
            # This would need actual implementation to get average CPU usage
            monitoring.average_cpu_usage = monitoring.cpu_usage
    
    @api.depends('database_id')
    def _compute_average_memory_usage(self):
        """Compute average memory usage"""
        for monitoring in self:
            # This would need actual implementation to get average memory usage
            monitoring.average_memory_usage = monitoring.memory_usage
    
    @api.depends('database_id')
    def _compute_average_response_time(self):
        """Compute average response time"""
        for monitoring in self:
            # This would need actual implementation to get average response time
            monitoring.average_response_time = monitoring.response_time
    
    @api.model
    def create(self, vals):
        """Override create to set default values"""
        # Set default values
        if 'last_check' not in vals:
            vals['last_check'] = fields.Datetime.now()
        
        return super(DatabaseMonitoring, self).create(vals)
    
    def write(self, vals):
        """Override write to handle monitoring updates"""
        result = super(DatabaseMonitoring, self).write(vals)
        
        # Update last check if monitoring metrics changed
        if any(field in vals for field in ['cpu_usage', 'memory_usage', 'disk_usage', 'response_time']):
            for monitoring in self:
                monitoring.last_check = fields.Datetime.now()
                monitoring.check_count += 1
        
        return result
    
    def unlink(self):
        """Override unlink to prevent deletion of active monitoring"""
        for monitoring in self:
            if monitoring.status == 'active':
                raise ValidationError(_('Cannot delete active monitoring. Please deactivate first.'))
        
        return super(DatabaseMonitoring, self).unlink()
    
    def action_activate(self):
        """Activate monitoring"""
        self.status = 'active'
        return True
    
    def action_deactivate(self):
        """Deactivate monitoring"""
        self.status = 'inactive'
        return True
    
    def action_start_monitoring(self):
        """Start monitoring process"""
        self.ensure_one()
        
        self.status = 'active'
        self.last_check = fields.Datetime.now()
        
        # This would need actual implementation to start monitoring
        return True
    
    def action_stop_monitoring(self):
        """Stop monitoring process"""
        self.ensure_one()
        
        self.status = 'inactive'
        return True
    
    def action_check_monitoring(self):
        """Perform monitoring check"""
        self.ensure_one()
        
        # This would need actual implementation to perform monitoring check
        self.last_check = fields.Datetime.now()
        self.check_count += 1
        
        # Update metrics (this would be done by actual monitoring implementation)
        self._update_monitoring_metrics()
        
        return True
    
    def action_analyze_monitoring(self):
        """Analyze monitoring data"""
        self.ensure_one()
        
        # This would need actual implementation to analyze monitoring data
        return True
    
    def action_generate_report(self):
        """Generate monitoring report"""
        self.ensure_one()
        
        # This would need actual implementation to generate monitoring report
        return True
    
    def action_send_alert(self, alert_type, message):
        """Send monitoring alert"""
        self.ensure_one()
        
        if not self.alert_enabled:
            return True
        
        # This would need actual implementation to send alerts
        if self.alert_email:
            # Send email alert
            pass
        
        if self.alert_sms:
            # Send SMS alert
            pass
        
        return True
    
    def _update_monitoring_metrics(self):
        """Update monitoring metrics"""
        # This would need actual implementation to update metrics
        pass
    
    def get_monitoring_info(self):
        """Get monitoring information"""
        return {
            'name': self.name,
            'description': self.description,
            'database_id': self.database_id.id,
            'monitoring_type': self.monitoring_type,
            'status': self.status,
            'cpu_usage': self.cpu_usage,
            'memory_usage': self.memory_usage,
            'disk_usage': self.disk_usage,
            'connection_count': self.connection_count,
            'query_count': self.query_count,
            'slow_query_count': self.slow_query_count,
            'error_count': self.error_count,
            'response_time': self.response_time,
            'throughput': self.throughput,
            'latency': self.latency,
            'database_size': self.database_size,
            'table_count': self.table_count,
            'record_count': self.record_count,
            'failed_logins': self.failed_logins,
            'security_violations': self.security_violations,
            'monitoring_interval': self.monitoring_interval,
            'alert_threshold': self.alert_threshold,
            'critical_threshold': self.critical_threshold,
            'alert_enabled': self.alert_enabled,
            'alert_email': self.alert_email,
            'alert_sms': self.alert_sms,
            'last_check': self.last_check,
            'next_check': self.next_check,
            'check_count': self.check_count,
            'health_score': self.health_score,
            'performance_score': self.performance_score,
            'security_score': self.security_score,
            'average_cpu_usage': self.average_cpu_usage,
            'average_memory_usage': self.average_memory_usage,
            'average_response_time': self.average_response_time,
            'cpu_trend': self.cpu_trend,
            'memory_trend': self.memory_trend,
            'performance_trend': self.performance_trend,
            'error_message': self.error_message,
        }
    
    def get_monitoring_analytics(self):
        """Get monitoring analytics"""
        return {
            'health_score': self.health_score,
            'performance_score': self.performance_score,
            'security_score': self.security_score,
            'cpu_usage': self.cpu_usage,
            'memory_usage': self.memory_usage,
            'disk_usage': self.disk_usage,
            'response_time': self.response_time,
            'throughput': self.throughput,
            'latency': self.latency,
            'connection_count': self.connection_count,
            'query_count': self.query_count,
            'slow_query_count': self.slow_query_count,
            'error_count': self.error_count,
            'database_size': self.database_size,
            'table_count': self.table_count,
            'record_count': self.record_count,
            'failed_logins': self.failed_logins,
            'security_violations': self.security_violations,
            'average_cpu_usage': self.average_cpu_usage,
            'average_memory_usage': self.average_memory_usage,
            'average_response_time': self.average_response_time,
            'cpu_trend': self.cpu_trend,
            'memory_trend': self.memory_trend,
            'performance_trend': self.performance_trend,
            'check_count': self.check_count,
            'last_check': self.last_check,
            'next_check': self.next_check,
        }
    
    @api.model
    def get_monitoring_by_database(self, database_id):
        """Get monitoring by database"""
        return self.search([
            ('database_id', '=', database_id),
            ('status', '=', 'active'),
        ])
    
    @api.model
    def get_monitoring_by_type(self, monitoring_type):
        """Get monitoring by type"""
        return self.search([
            ('monitoring_type', '=', monitoring_type),
            ('status', '=', 'active'),
        ])
    
    @api.model
    def get_active_monitoring(self):
        """Get active monitoring"""
        return self.search([('status', '=', 'active')])
    
    @api.model
    def get_critical_monitoring(self):
        """Get critical monitoring"""
        return self.search([('status', '=', 'critical')])
    
    @api.model
    def get_monitoring_analytics_summary(self):
        """Get monitoring analytics summary"""
        total_monitoring = self.search_count([])
        active_monitoring = self.search_count([('status', '=', 'active')])
        critical_monitoring = self.search_count([('status', '=', 'critical')])
        warning_monitoring = self.search_count([('status', '=', 'warning')])
        error_monitoring = self.search_count([('status', '=', 'error')])
        
        return {
            'total_monitoring': total_monitoring,
            'active_monitoring': active_monitoring,
            'critical_monitoring': critical_monitoring,
            'warning_monitoring': warning_monitoring,
            'error_monitoring': error_monitoring,
            'inactive_monitoring': total_monitoring - active_monitoring,
            'active_percentage': (active_monitoring / total_monitoring * 100) if total_monitoring > 0 else 0,
        }
    
    @api.constrains('name')
    def _check_name(self):
        """Validate monitoring name"""
        for monitoring in self:
            if monitoring.name:
                # Check for duplicate names
                existing = self.search([
                    ('name', '=', monitoring.name),
                    ('id', '!=', monitoring.id),
                ])
                if existing:
                    raise ValidationError(_('Monitoring name must be unique'))
    
    @api.constrains('monitoring_interval')
    def _check_monitoring_interval(self):
        """Validate monitoring interval"""
        for monitoring in self:
            if monitoring.monitoring_interval <= 0:
                raise ValidationError(_('Monitoring interval must be greater than 0'))
    
    @api.constrains('alert_threshold', 'critical_threshold')
    def _check_thresholds(self):
        """Validate alert thresholds"""
        for monitoring in self:
            if monitoring.alert_threshold >= monitoring.critical_threshold:
                raise ValidationError(_('Alert threshold must be less than critical threshold'))
    
    def action_duplicate(self):
        """Duplicate monitoring"""
        self.ensure_one()
        
        new_monitoring = self.copy({
            'name': f'{self.name} (Copy)',
            'status': 'inactive',
            'last_check': False,
            'check_count': 0,
        })
        
        return {
            'type': 'ir.actions.act_window',
            'name': 'Duplicated Monitoring',
            'res_model': 'database.monitoring',
            'res_id': new_monitoring.id,
            'view_mode': 'form',
            'target': 'current',
        }
    
    def action_export_monitoring(self):
        """Export monitoring configuration"""
        self.ensure_one()
        
        return {
            'name': self.name,
            'description': self.description,
            'database_id': self.database_id.id,
            'monitoring_type': self.monitoring_type,
            'monitoring_interval': self.monitoring_interval,
            'alert_threshold': self.alert_threshold,
            'critical_threshold': self.critical_threshold,
            'alert_enabled': self.alert_enabled,
            'alert_email': self.alert_email,
            'alert_sms': self.alert_sms,
        }
    
    def action_import_monitoring(self, monitoring_data):
        """Import monitoring configuration"""
        self.ensure_one()
        
        self.write(monitoring_data)
        return True