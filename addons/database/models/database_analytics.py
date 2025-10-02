# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging
from datetime import datetime, timedelta

_logger = logging.getLogger(__name__)


class DatabaseAnalytics(models.Model):
    """Database analytics model for Kids Clothing ERP"""
    
    _name = 'database.analytics'
    _description = 'Database Analytics'
    _order = 'create_date desc'
    
    # Basic fields
    name = fields.Char(
        string='Analytics Name',
        required=True,
        help='Name of the analytics record'
    )
    
    description = fields.Text(
        string='Description',
        help='Description of the analytics record'
    )
    
    # Database relationship
    database_id = fields.Many2one(
        'database.info',
        string='Database',
        required=True,
        help='Database this analytics belongs to'
    )
    
    # Analytics details
    analytics_type = fields.Selection([
        ('performance', 'Performance Analytics'),
        ('usage', 'Usage Analytics'),
        ('security', 'Security Analytics'),
        ('storage', 'Storage Analytics'),
        ('query', 'Query Analytics'),
        ('connection', 'Connection Analytics'),
        ('backup', 'Backup Analytics'),
        ('migration', 'Migration Analytics'),
        ('custom', 'Custom Analytics'),
    ], string='Analytics Type', default='performance', help='Type of analytics')
    
    # Analytics status
    status = fields.Selection([
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='pending', help='Status of the analytics')
    
    # Analytics period
    date_from = fields.Date(
        string='From Date',
        help='Start date for analytics'
    )
    
    date_to = fields.Date(
        string='To Date',
        help='End date for analytics'
    )
    
    # Performance analytics
    total_queries = fields.Integer(
        string='Total Queries',
        help='Total number of queries executed'
    )
    
    slow_queries = fields.Integer(
        string='Slow Queries',
        help='Number of slow queries'
    )
    
    average_response_time = fields.Float(
        string='Average Response Time (ms)',
        help='Average response time in milliseconds'
    )
    
    peak_response_time = fields.Float(
        string='Peak Response Time (ms)',
        help='Peak response time in milliseconds'
    )
    
    throughput = fields.Float(
        string='Throughput (queries/sec)',
        help='Queries per second'
    )
    
    # Usage analytics
    total_connections = fields.Integer(
        string='Total Connections',
        help='Total number of connections'
    )
    
    peak_connections = fields.Integer(
        string='Peak Connections',
        help='Peak number of connections'
    )
    
    average_connections = fields.Float(
        string='Average Connections',
        help='Average number of connections'
    )
    
    connection_duration = fields.Float(
        string='Connection Duration (minutes)',
        help='Average connection duration in minutes'
    )
    
    # Security analytics
    failed_logins = fields.Integer(
        string='Failed Logins',
        help='Number of failed login attempts'
    )
    
    security_violations = fields.Integer(
        string='Security Violations',
        help='Number of security violations'
    )
    
    blocked_ips = fields.Integer(
        string='Blocked IPs',
        help='Number of blocked IP addresses'
    )
    
    # Storage analytics
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
    
    index_count = fields.Integer(
        string='Index Count',
        help='Number of indexes'
    )
    
    # Query analytics
    most_used_tables = fields.Text(
        string='Most Used Tables',
        help='Most frequently used tables'
    )
    
    slowest_queries = fields.Text(
        string='Slowest Queries',
        help='Slowest queries identified'
    )
    
    query_patterns = fields.Text(
        string='Query Patterns',
        help='Common query patterns identified'
    )
    
    # Connection analytics
    connection_sources = fields.Text(
        string='Connection Sources',
        help='Sources of database connections'
    )
    
    connection_times = fields.Text(
        string='Connection Times',
        help='Peak connection times'
    )
    
    # Backup analytics
    backup_frequency = fields.Float(
        string='Backup Frequency (days)',
        help='Average backup frequency in days'
    )
    
    backup_success_rate = fields.Float(
        string='Backup Success Rate (%)',
        help='Backup success rate percentage'
    )
    
    backup_size_trend = fields.Selection([
        ('increasing', 'Increasing'),
        ('decreasing', 'Decreasing'),
        ('stable', 'Stable'),
    ], string='Backup Size Trend', help='Backup size trend')
    
    # Migration analytics
    migration_frequency = fields.Float(
        string='Migration Frequency (days)',
        help='Average migration frequency in days'
    )
    
    migration_success_rate = fields.Float(
        string='Migration Success Rate (%)',
        help='Migration success rate percentage'
    )
    
    migration_duration = fields.Float(
        string='Migration Duration (minutes)',
        help='Average migration duration in minutes'
    )
    
    # Analytics insights
    insights = fields.Text(
        string='Insights',
        help='Analytics insights and recommendations'
    )
    
    recommendations = fields.Text(
        string='Recommendations',
        help='Recommendations based on analytics'
    )
    
    # Analytics trends
    performance_trend = fields.Selection([
        ('improving', 'Improving'),
        ('degrading', 'Degrading'),
        ('stable', 'Stable'),
    ], string='Performance Trend', help='Performance trend')
    
    usage_trend = fields.Selection([
        ('increasing', 'Increasing'),
        ('decreasing', 'Decreasing'),
        ('stable', 'Stable'),
    ], string='Usage Trend', help='Usage trend')
    
    security_trend = fields.Selection([
        ('improving', 'Improving'),
        ('degrading', 'Degrading'),
        ('stable', 'Stable'),
    ], string='Security Trend', help='Security trend')
    
    # Analytics metrics
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
    
    # Analytics timing
    start_time = fields.Datetime(
        string='Start Time',
        help='Analytics start time'
    )
    
    end_time = fields.Datetime(
        string='End Time',
        help='Analytics end time'
    )
    
    duration = fields.Float(
        string='Duration (minutes)',
        compute='_compute_duration',
        store=True,
        help='Analytics duration in minutes'
    )
    
    # Analytics metadata
    metadata = fields.Text(
        string='Metadata',
        help='Analytics metadata (JSON format)'
    )
    
    # Analytics logs
    log_file = fields.Char(
        string='Log File',
        help='Path to analytics log file'
    )
    
    error_message = fields.Text(
        string='Error Message',
        help='Error message if analytics failed'
    )
    
    @api.depends('start_time', 'end_time')
    def _compute_duration(self):
        """Compute analytics duration"""
        for analytics in self:
            if analytics.start_time and analytics.end_time:
                start = fields.Datetime.from_string(analytics.start_time)
                end = fields.Datetime.from_string(analytics.end_time)
                duration = (end - start).total_seconds() / 60  # Convert to minutes
                analytics.duration = duration
            else:
                analytics.duration = 0.0
    
    @api.depends('total_queries', 'slow_queries', 'average_response_time', 'throughput')
    def _compute_health_score(self):
        """Compute health score"""
        for analytics in self:
            # Calculate health score based on performance metrics
            query_score = max(0, 100 - (analytics.slow_queries / max(1, analytics.total_queries) * 100))
            response_score = max(0, 100 - (analytics.average_response_time / 10))
            throughput_score = min(100, analytics.throughput * 10)
            
            analytics.health_score = (query_score + response_score + throughput_score) / 3
    
    @api.depends('average_response_time', 'peak_response_time', 'throughput', 'slow_queries')
    def _compute_performance_score(self):
        """Compute performance score"""
        for analytics in self:
            # Calculate performance score based on performance metrics
            response_score = max(0, 100 - (analytics.average_response_time / 10))
            peak_score = max(0, 100 - (analytics.peak_response_time / 10))
            throughput_score = min(100, analytics.throughput * 10)
            slow_query_score = max(0, 100 - (analytics.slow_queries / max(1, analytics.total_queries) * 100))
            
            analytics.performance_score = (response_score + peak_score + throughput_score + slow_query_score) / 4
    
    @api.depends('failed_logins', 'security_violations', 'blocked_ips')
    def _compute_security_score(self):
        """Compute security score"""
        for analytics in self:
            # Calculate security score based on security metrics
            login_score = max(0, 100 - (analytics.failed_logins * 5))
            violation_score = max(0, 100 - (analytics.security_violations * 10))
            ip_score = max(0, 100 - (analytics.blocked_ips * 2))
            
            analytics.security_score = (login_score + violation_score + ip_score) / 3
    
    @api.model
    def create(self, vals):
        """Override create to set default values"""
        # Set default values
        if 'start_time' not in vals:
            vals['start_time'] = fields.Datetime.now()
        
        return super(DatabaseAnalytics, self).create(vals)
    
    def write(self, vals):
        """Override write to handle analytics updates"""
        result = super(DatabaseAnalytics, self).write(vals)
        
        # Update end time if status changed to completed or failed
        if 'status' in vals and vals['status'] in ['completed', 'failed']:
            for analytics in self:
                analytics.end_time = fields.Datetime.now()
        
        return result
    
    def unlink(self):
        """Override unlink to prevent deletion of completed analytics"""
        for analytics in self:
            if analytics.status == 'completed':
                raise ValidationError(_('Cannot delete completed analytics'))
        
        return super(DatabaseAnalytics, self).unlink()
    
    def action_start_analytics(self):
        """Start analytics process"""
        self.ensure_one()
        
        self.status = 'in_progress'
        self.start_time = fields.Datetime.now()
        
        # This would need actual implementation to start analytics
        return True
    
    def action_complete_analytics(self):
        """Complete analytics process"""
        self.ensure_one()
        
        self.status = 'completed'
        self.end_time = fields.Datetime.now()
        
        return True
    
    def action_fail_analytics(self, error_message):
        """Fail analytics process"""
        self.ensure_one()
        
        self.status = 'failed'
        self.end_time = fields.Datetime.now()
        self.error_message = error_message
        
        return True
    
    def action_cancel_analytics(self):
        """Cancel analytics process"""
        self.ensure_one()
        
        self.status = 'cancelled'
        self.end_time = fields.Datetime.now()
        
        return True
    
    def action_generate_report(self):
        """Generate analytics report"""
        self.ensure_one()
        
        if self.status != 'completed':
            raise ValidationError(_('Only completed analytics can generate reports'))
        
        # This would need actual implementation to generate report
        return True
    
    def action_export_analytics(self):
        """Export analytics data"""
        self.ensure_one()
        
        # This would need actual implementation to export analytics
        return True
    
    def action_analyze_trends(self):
        """Analyze trends"""
        self.ensure_one()
        
        # This would need actual implementation to analyze trends
        return True
    
    def get_analytics_info(self):
        """Get analytics information"""
        return {
            'name': self.name,
            'description': self.description,
            'database_id': self.database_id.id,
            'analytics_type': self.analytics_type,
            'status': self.status,
            'date_from': self.date_from,
            'date_to': self.date_to,
            'total_queries': self.total_queries,
            'slow_queries': self.slow_queries,
            'average_response_time': self.average_response_time,
            'peak_response_time': self.peak_response_time,
            'throughput': self.throughput,
            'total_connections': self.total_connections,
            'peak_connections': self.peak_connections,
            'average_connections': self.average_connections,
            'connection_duration': self.connection_duration,
            'failed_logins': self.failed_logins,
            'security_violations': self.security_violations,
            'blocked_ips': self.blocked_ips,
            'database_size': self.database_size,
            'table_count': self.table_count,
            'record_count': self.record_count,
            'index_count': self.index_count,
            'most_used_tables': self.most_used_tables,
            'slowest_queries': self.slowest_queries,
            'query_patterns': self.query_patterns,
            'connection_sources': self.connection_sources,
            'connection_times': self.connection_times,
            'backup_frequency': self.backup_frequency,
            'backup_success_rate': self.backup_success_rate,
            'backup_size_trend': self.backup_size_trend,
            'migration_frequency': self.migration_frequency,
            'migration_success_rate': self.migration_success_rate,
            'migration_duration': self.migration_duration,
            'insights': self.insights,
            'recommendations': self.recommendations,
            'performance_trend': self.performance_trend,
            'usage_trend': self.usage_trend,
            'security_trend': self.security_trend,
            'health_score': self.health_score,
            'performance_score': self.performance_score,
            'security_score': self.security_score,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'duration': self.duration,
            'error_message': self.error_message,
        }
    
    def get_analytics_summary(self):
        """Get analytics summary"""
        return {
            'health_score': self.health_score,
            'performance_score': self.performance_score,
            'security_score': self.security_score,
            'total_queries': self.total_queries,
            'slow_queries': self.slow_queries,
            'average_response_time': self.average_response_time,
            'throughput': self.throughput,
            'total_connections': self.total_connections,
            'peak_connections': self.peak_connections,
            'database_size': self.database_size,
            'table_count': self.table_count,
            'record_count': self.record_count,
            'failed_logins': self.failed_logins,
            'security_violations': self.security_violations,
            'backup_success_rate': self.backup_success_rate,
            'migration_success_rate': self.migration_success_rate,
            'performance_trend': self.performance_trend,
            'usage_trend': self.usage_trend,
            'security_trend': self.security_trend,
            'insights': self.insights,
            'recommendations': self.recommendations,
        }
    
    @api.model
    def get_analytics_by_database(self, database_id):
        """Get analytics by database"""
        return self.search([
            ('database_id', '=', database_id),
            ('status', '=', 'completed'),
        ])
    
    @api.model
    def get_analytics_by_type(self, analytics_type):
        """Get analytics by type"""
        return self.search([
            ('analytics_type', '=', analytics_type),
            ('status', '=', 'completed'),
        ])
    
    @api.model
    def get_analytics_by_period(self, date_from, date_to):
        """Get analytics by period"""
        return self.search([
            ('date_from', '>=', date_from),
            ('date_to', '<=', date_to),
            ('status', '=', 'completed'),
        ])
    
    @api.model
    def get_analytics_analytics_summary(self):
        """Get analytics analytics summary"""
        total_analytics = self.search_count([])
        completed_analytics = self.search_count([('status', '=', 'completed')])
        failed_analytics = self.search_count([('status', '=', 'failed')])
        pending_analytics = self.search_count([('status', '=', 'pending')])
        
        return {
            'total_analytics': total_analytics,
            'completed_analytics': completed_analytics,
            'failed_analytics': failed_analytics,
            'pending_analytics': pending_analytics,
            'in_progress_analytics': total_analytics - completed_analytics - failed_analytics - pending_analytics,
            'success_rate': (completed_analytics / total_analytics * 100) if total_analytics > 0 else 0,
        }
    
    @api.constrains('name')
    def _check_name(self):
        """Validate analytics name"""
        for analytics in self:
            if analytics.name:
                # Check for duplicate names
                existing = self.search([
                    ('name', '=', analytics.name),
                    ('id', '!=', analytics.id),
                ])
                if existing:
                    raise ValidationError(_('Analytics name must be unique'))
    
    @api.constrains('date_from', 'date_to')
    def _check_dates(self):
        """Validate analytics dates"""
        for analytics in self:
            if analytics.date_from and analytics.date_to:
                if analytics.date_from > analytics.date_to:
                    raise ValidationError(_('From date must be before to date'))
    
    def action_duplicate(self):
        """Duplicate analytics"""
        self.ensure_one()
        
        new_analytics = self.copy({
            'name': f'{self.name} (Copy)',
            'status': 'pending',
            'start_time': False,
            'end_time': False,
        })
        
        return {
            'type': 'ir.actions.act_window',
            'name': 'Duplicated Analytics',
            'res_model': 'database.analytics',
            'res_id': new_analytics.id,
            'view_mode': 'form',
            'target': 'current',
        }
    
    def action_export_analytics_config(self):
        """Export analytics configuration"""
        self.ensure_one()
        
        return {
            'name': self.name,
            'description': self.description,
            'database_id': self.database_id.id,
            'analytics_type': self.analytics_type,
            'date_from': self.date_from,
            'date_to': self.date_to,
        }
    
    def action_import_analytics_config(self, analytics_data):
        """Import analytics configuration"""
        self.ensure_one()
        
        self.write(analytics_data)
        return True