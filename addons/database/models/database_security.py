# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging
from datetime import datetime, timedelta

_logger = logging.getLogger(__name__)


class DatabaseSecurity(models.Model):
    """Database security model for Kids Clothing ERP"""
    
    _name = 'database.security'
    _description = 'Database Security'
    _order = 'create_date desc'
    
    # Basic fields
    name = fields.Char(
        string='Security Name',
        required=True,
        help='Name of the security record'
    )
    
    description = fields.Text(
        string='Description',
        help='Description of the security record'
    )
    
    # Database relationship
    database_id = fields.Many2one(
        'database.info',
        string='Database',
        required=True,
        help='Database this security belongs to'
    )
    
    # Security details
    security_type = fields.Selection([
        ('access_control', 'Access Control'),
        ('authentication', 'Authentication'),
        ('authorization', 'Authorization'),
        ('encryption', 'Encryption'),
        ('audit', 'Audit'),
        ('firewall', 'Firewall'),
        ('ssl', 'SSL/TLS'),
        ('backup_security', 'Backup Security'),
        ('custom', 'Custom Security'),
    ], string='Security Type', default='access_control', help='Type of security')
    
    # Security status
    status = fields.Selection([
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('warning', 'Warning'),
        'critical', 'Critical'),
    ], string='Status', default='active', help='Status of the security')
    
    # Access control
    user_access = fields.Boolean(
        string='User Access',
        default=True,
        help='Whether user access is enabled'
    )
    
    role_based_access = fields.Boolean(
        string='Role-Based Access',
        default=True,
        help='Whether role-based access is enabled'
    )
    
    ip_restrictions = fields.Boolean(
        string='IP Restrictions',
        default=False,
        help='Whether IP restrictions are enabled'
    )
    
    allowed_ips = fields.Text(
        string='Allowed IPs',
        help='List of allowed IP addresses'
    )
    
    blocked_ips = fields.Text(
        string='Blocked IPs',
        help='List of blocked IP addresses'
    )
    
    # Authentication
    password_policy = fields.Boolean(
        string='Password Policy',
        default=True,
        help='Whether password policy is enabled'
    )
    
    min_password_length = fields.Integer(
        string='Min Password Length',
        default=8,
        help='Minimum password length'
    )
    
    password_complexity = fields.Boolean(
        string='Password Complexity',
        default=True,
        help='Whether password complexity is required'
    )
    
    account_lockout = fields.Boolean(
        string='Account Lockout',
        default=True,
        help='Whether account lockout is enabled'
    )
    
    max_login_attempts = fields.Integer(
        string='Max Login Attempts',
        default=5,
        help='Maximum login attempts before lockout'
    )
    
    lockout_duration = fields.Integer(
        string='Lockout Duration (minutes)',
        default=30,
        help='Account lockout duration in minutes'
    )
    
    # Authorization
    permission_level = fields.Selection([
        ('read', 'Read Only'),
        ('write', 'Read/Write'),
        ('admin', 'Administrative'),
        ('custom', 'Custom'),
    ], string='Permission Level', default='read', help='Permission level')
    
    custom_permissions = fields.Text(
        string='Custom Permissions',
        help='Custom permissions configuration'
    )
    
    # Encryption
    encryption_enabled = fields.Boolean(
        string='Encryption Enabled',
        default=False,
        help='Whether encryption is enabled'
    )
    
    encryption_algorithm = fields.Selection([
        ('aes256', 'AES-256'),
        ('aes128', 'AES-128'),
        ('des', 'DES'),
        ('3des', '3DES'),
        ('custom', 'Custom'),
    ], string='Encryption Algorithm', help='Encryption algorithm')
    
    encryption_key = fields.Char(
        string='Encryption Key',
        help='Encryption key'
    )
    
    # SSL/TLS
    ssl_enabled = fields.Boolean(
        string='SSL Enabled',
        default=False,
        help='Whether SSL is enabled'
    )
    
    ssl_certificate = fields.Char(
        string='SSL Certificate',
        help='SSL certificate path'
    )
    
    ssl_key = fields.Char(
        string='SSL Key',
        help='SSL key path'
    )
    
    ssl_ca = fields.Char(
        string='SSL CA',
        help='SSL CA certificate path'
    )
    
    # Audit
    audit_enabled = fields.Boolean(
        string='Audit Enabled',
        default=True,
        help='Whether audit is enabled'
    )
    
    audit_level = fields.Selection([
        ('basic', 'Basic'),
        ('detailed', 'Detailed'),
        ('comprehensive', 'Comprehensive'),
    ], string='Audit Level', default='basic', help='Audit level')
    
    audit_retention_days = fields.Integer(
        string='Audit Retention Days',
        default=90,
        help='Audit log retention days'
    )
    
    # Firewall
    firewall_enabled = fields.Boolean(
        string='Firewall Enabled',
        default=False,
        help='Whether firewall is enabled'
    )
    
    firewall_rules = fields.Text(
        string='Firewall Rules',
        help='Firewall rules configuration'
    )
    
    # Security metrics
    failed_logins = fields.Integer(
        string='Failed Logins',
        default=0,
        help='Number of failed login attempts'
    )
    
    security_violations = fields.Integer(
        string='Security Violations',
        default=0,
        help='Number of security violations'
    )
    
    blocked_attempts = fields.Integer(
        string='Blocked Attempts',
        default=0,
        help='Number of blocked access attempts'
    )
    
    # Security monitoring
    last_security_check = fields.Datetime(
        string='Last Security Check',
        help='Last security check time'
    )
    
    next_security_check = fields.Datetime(
        string='Next Security Check',
        compute='_compute_next_security_check',
        store=True,
        help='Next security check time'
    )
    
    security_score = fields.Float(
        string='Security Score',
        compute='_compute_security_score',
        store=True,
        help='Security score (0-100)'
    )
    
    # Security alerts
    alert_enabled = fields.Boolean(
        string='Alert Enabled',
        default=True,
        help='Whether security alerts are enabled'
    )
    
    alert_email = fields.Char(
        string='Alert Email',
        help='Email address for security alerts'
    )
    
    alert_sms = fields.Char(
        string='Alert SMS',
        help='SMS number for security alerts'
    )
    
    # Security metadata
    metadata = fields.Text(
        string='Metadata',
        help='Security metadata (JSON format)'
    )
    
    # Security logs
    log_file = fields.Char(
        string='Log File',
        help='Path to security log file'
    )
    
    error_message = fields.Text(
        string='Error Message',
        help='Error message if security check failed'
    )
    
    @api.depends('last_security_check')
    def _compute_next_security_check(self):
        """Compute next security check time"""
        for security in self:
            if security.last_security_check:
                last_check = fields.Datetime.from_string(security.last_security_check)
                security.next_security_check = last_check + timedelta(hours=24)
            else:
                security.next_security_check = fields.Datetime.now()
    
    @api.depends('failed_logins', 'security_violations', 'blocked_attempts', 'encryption_enabled', 'ssl_enabled')
    def _compute_security_score(self):
        """Compute security score"""
        for security in self:
            # Calculate security score based on security metrics
            login_score = max(0, 100 - (security.failed_logins * 5))
            violation_score = max(0, 100 - (security.security_violations * 10))
            blocked_score = max(0, 100 - (security.blocked_attempts * 2))
            encryption_score = 100 if security.encryption_enabled else 0
            ssl_score = 100 if security.ssl_enabled else 0
            
            security.security_score = (login_score + violation_score + blocked_score + encryption_score + ssl_score) / 5
    
    @api.model
    def create(self, vals):
        """Override create to set default values"""
        # Set default values
        if 'last_security_check' not in vals:
            vals['last_security_check'] = fields.Datetime.now()
        
        return super(DatabaseSecurity, self).create(vals)
    
    def write(self, vals):
        """Override write to handle security updates"""
        result = super(DatabaseSecurity, self).write(vals)
        
        # Update last security check if security settings changed
        if any(field in vals for field in ['user_access', 'role_based_access', 'ip_restrictions', 'encryption_enabled', 'ssl_enabled']):
            for security in self:
                security.last_security_check = fields.Datetime.now()
        
        return result
    
    def unlink(self):
        """Override unlink to prevent deletion of active security"""
        for security in self:
            if security.status == 'active':
                raise ValidationError(_('Cannot delete active security. Please deactivate first.'))
        
        return super(DatabaseSecurity, self).unlink()
    
    def action_activate(self):
        """Activate security"""
        self.status = 'active'
        return True
    
    def action_deactivate(self):
        """Deactivate security"""
        self.status = 'inactive'
        return True
    
    def action_check_security(self):
        """Perform security check"""
        self.ensure_one()
        
        # This would need actual implementation to perform security check
        self.last_security_check = fields.Datetime.now()
        
        # Update security metrics
        self._update_security_metrics()
        
        return True
    
    def action_analyze_security(self):
        """Analyze security"""
        self.ensure_one()
        
        # This would need actual implementation to analyze security
        return True
    
    def action_generate_security_report(self):
        """Generate security report"""
        self.ensure_one()
        
        # This would need actual implementation to generate security report
        return True
    
    def action_send_security_alert(self, alert_type, message):
        """Send security alert"""
        self.ensure_one()
        
        if not self.alert_enabled:
            return True
        
        # This would need actual implementation to send security alerts
        if self.alert_email:
            # Send email alert
            pass
        
        if self.alert_sms:
            # Send SMS alert
            pass
        
        return True
    
    def _update_security_metrics(self):
        """Update security metrics"""
        # This would need actual implementation to update security metrics
        pass
    
    def get_security_info(self):
        """Get security information"""
        return {
            'name': self.name,
            'description': self.description,
            'database_id': self.database_id.id,
            'security_type': self.security_type,
            'status': self.status,
            'user_access': self.user_access,
            'role_based_access': self.role_based_access,
            'ip_restrictions': self.ip_restrictions,
            'allowed_ips': self.allowed_ips,
            'blocked_ips': self.blocked_ips,
            'password_policy': self.password_policy,
            'min_password_length': self.min_password_length,
            'password_complexity': self.password_complexity,
            'account_lockout': self.account_lockout,
            'max_login_attempts': self.max_login_attempts,
            'lockout_duration': self.lockout_duration,
            'permission_level': self.permission_level,
            'custom_permissions': self.custom_permissions,
            'encryption_enabled': self.encryption_enabled,
            'encryption_algorithm': self.encryption_algorithm,
            'ssl_enabled': self.ssl_enabled,
            'ssl_certificate': self.ssl_certificate,
            'ssl_key': self.ssl_key,
            'ssl_ca': self.ssl_ca,
            'audit_enabled': self.audit_enabled,
            'audit_level': self.audit_level,
            'audit_retention_days': self.audit_retention_days,
            'firewall_enabled': self.firewall_enabled,
            'firewall_rules': self.firewall_rules,
            'failed_logins': self.failed_logins,
            'security_violations': self.security_violations,
            'blocked_attempts': self.blocked_attempts,
            'last_security_check': self.last_security_check,
            'next_security_check': self.next_security_check,
            'security_score': self.security_score,
            'alert_enabled': self.alert_enabled,
            'alert_email': self.alert_email,
            'alert_sms': self.alert_sms,
            'error_message': self.error_message,
        }
    
    def get_security_analytics(self):
        """Get security analytics"""
        return {
            'security_score': self.security_score,
            'failed_logins': self.failed_logins,
            'security_violations': self.security_violations,
            'blocked_attempts': self.blocked_attempts,
            'last_security_check': self.last_security_check,
            'next_security_check': self.next_security_check,
            'encryption_enabled': self.encryption_enabled,
            'ssl_enabled': self.ssl_enabled,
            'audit_enabled': self.audit_enabled,
            'firewall_enabled': self.firewall_enabled,
            'alert_enabled': self.alert_enabled,
        }
    
    @api.model
    def get_security_by_database(self, database_id):
        """Get security by database"""
        return self.search([
            ('database_id', '=', database_id),
            ('status', '=', 'active'),
        ])
    
    @api.model
    def get_security_by_type(self, security_type):
        """Get security by type"""
        return self.search([
            ('security_type', '=', security_type),
            ('status', '=', 'active'),
        ])
    
    @api.model
    def get_active_security(self):
        """Get active security"""
        return self.search([('status', '=', 'active')])
    
    @api.model
    def get_critical_security(self):
        """Get critical security"""
        return self.search([('status', '=', 'critical')])
    
    @api.model
    def get_security_analytics_summary(self):
        """Get security analytics summary"""
        total_security = self.search_count([])
        active_security = self.search_count([('status', '=', 'active')])
        critical_security = self.search_count([('status', '=', 'critical')])
        warning_security = self.search_count([('status', '=', 'warning')])
        
        return {
            'total_security': total_security,
            'active_security': active_security,
            'critical_security': critical_security,
            'warning_security': warning_security,
            'inactive_security': total_security - active_security,
            'active_percentage': (active_security / total_security * 100) if total_security > 0 else 0,
        }
    
    @api.constrains('name')
    def _check_name(self):
        """Validate security name"""
        for security in self:
            if security.name:
                # Check for duplicate names
                existing = self.search([
                    ('name', '=', security.name),
                    ('id', '!=', security.id),
                ])
                if existing:
                    raise ValidationError(_('Security name must be unique'))
    
    @api.constrains('min_password_length')
    def _check_min_password_length(self):
        """Validate minimum password length"""
        for security in self:
            if security.min_password_length < 6:
                raise ValidationError(_('Minimum password length must be at least 6'))
    
    @api.constrains('max_login_attempts')
    def _check_max_login_attempts(self):
        """Validate maximum login attempts"""
        for security in self:
            if security.max_login_attempts <= 0:
                raise ValidationError(_('Maximum login attempts must be greater than 0'))
    
    @api.constrains('lockout_duration')
    def _check_lockout_duration(self):
        """Validate lockout duration"""
        for security in self:
            if security.lockout_duration <= 0:
                raise ValidationError(_('Lockout duration must be greater than 0'))
    
    def action_duplicate(self):
        """Duplicate security"""
        self.ensure_one()
        
        new_security = self.copy({
            'name': f'{self.name} (Copy)',
            'status': 'inactive',
        })
        
        return {
            'type': 'ir.actions.act_window',
            'name': 'Duplicated Security',
            'res_model': 'database.security',
            'res_id': new_security.id,
            'view_mode': 'form',
            'target': 'current',
        }
    
    def action_export_security(self):
        """Export security configuration"""
        self.ensure_one()
        
        return {
            'name': self.name,
            'description': self.description,
            'database_id': self.database_id.id,
            'security_type': self.security_type,
            'user_access': self.user_access,
            'role_based_access': self.role_based_access,
            'ip_restrictions': self.ip_restrictions,
            'password_policy': self.password_policy,
            'min_password_length': self.min_password_length,
            'password_complexity': self.password_complexity,
            'account_lockout': self.account_lockout,
            'max_login_attempts': self.max_login_attempts,
            'lockout_duration': self.lockout_duration,
            'permission_level': self.permission_level,
            'encryption_enabled': self.encryption_enabled,
            'encryption_algorithm': self.encryption_algorithm,
            'ssl_enabled': self.ssl_enabled,
            'audit_enabled': self.audit_enabled,
            'audit_level': self.audit_level,
            'firewall_enabled': self.firewall_enabled,
            'alert_enabled': self.alert_enabled,
        }
    
    def action_import_security(self, security_data):
        """Import security configuration"""
        self.ensure_one()
        
        self.write(security_data)
        return True