# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Database - Database Security Management
=========================================================

Standalone version of the database security management model.
"""

from core_framework.orm import BaseModel, CharField, TextField, BooleanField, IntegerField, DateTimeField, Many2OneField, SelectionField, FloatField
from core_framework.orm import Field
from typing import Dict, Any, Optional
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class DatabaseSecurity(BaseModel):
    """Database security model for Kids Clothing ERP"""
    
    _name = 'database.security'
    _description = 'Database Security'
    _table = 'database_security'
    
    # Basic fields
    name = CharField(
        string='Security Name',
        size=255,
        required=True,
        help='Name of the security'
    )
    
    description = TextField(
        string='Description',
        help='Description of the security'
    )
    
    # Database relationship
    database_id = IntegerField(
        string='Database ID',
        required=True,
        help='Database this security belongs to'
    )
    
    # Security details
    security_type = SelectionField(
        string='Security Type',
        selection=[
            ('authentication', 'Authentication'),
            ('authorization', 'Authorization'),
            ('encryption', 'Encryption'),
            ('audit', 'Audit'),
            ('firewall', 'Firewall'),
            ('backup', 'Backup Security'),
        ],
        default='authentication',
        help='Type of security'
    )
    
    # Security status
    status = SelectionField(
        string='Status',
        selection=[
            ('active', 'Active'),
            ('inactive', 'Inactive'),
            ('error', 'Error'),
            ('warning', 'Warning'),
        ],
        default='active',
        help='Status of the security'
    )
    
    # Security settings
    is_enabled = BooleanField(
        string='Enabled',
        default=True,
        help='Whether security is enabled'
    )
    
    is_required = BooleanField(
        string='Required',
        default=False,
        help='Whether security is required'
    )
    
    # Security level
    security_level = SelectionField(
        string='Security Level',
        selection=[
            ('low', 'Low'),
            ('medium', 'Medium'),
            ('high', 'High'),
            ('critical', 'Critical'),
        ],
        default='medium',
        help='Security level'
    )
    
    # Security metrics
    failed_attempts = IntegerField(
        string='Failed Attempts',
        default=0,
        help='Number of failed security attempts'
    )
    
    successful_attempts = IntegerField(
        string='Successful Attempts',
        default=0,
        help='Number of successful security attempts'
    )
    
    blocked_attempts = IntegerField(
        string='Blocked Attempts',
        default=0,
        help='Number of blocked security attempts'
    )
    
    # Security timing
    last_attempt = DateTimeField(
        string='Last Attempt',
        help='Last security attempt time'
    )
    
    last_success = DateTimeField(
        string='Last Success',
        help='Last successful security time'
    )
    
    last_failure = DateTimeField(
        string='Last Failure',
        help='Last failed security time'
    )
    
    # Security configuration
    max_attempts = IntegerField(
        string='Max Attempts',
        default=3,
        help='Maximum number of attempts allowed'
    )
    
    lockout_duration = IntegerField(
        string='Lockout Duration (minutes)',
        default=30,
        help='Lockout duration in minutes'
    )
    
    password_policy = TextField(
        string='Password Policy',
        help='Password policy configuration'
    )
    
    # Security encryption
    encryption_enabled = BooleanField(
        string='Encryption Enabled',
        default=False,
        help='Whether encryption is enabled'
    )
    
    encryption_algorithm = CharField(
        string='Encryption Algorithm',
        size=50,
        help='Encryption algorithm used'
    )
    
    encryption_key = CharField(
        string='Encryption Key',
        size=255,
        help='Encryption key'
    )
    
    # Security audit
    audit_enabled = BooleanField(
        string='Audit Enabled',
        default=True,
        help='Whether audit is enabled'
    )
    
    audit_level = SelectionField(
        string='Audit Level',
        selection=[
            ('basic', 'Basic'),
            ('detailed', 'Detailed'),
            ('comprehensive', 'Comprehensive'),
        ],
        default='basic',
        help='Audit level'
    )
    
    # Security alerts
    alert_enabled = BooleanField(
        string='Alert Enabled',
        default=True,
        help='Whether alerts are enabled'
    )
    
    alert_threshold = IntegerField(
        string='Alert Threshold',
        default=5,
        help='Alert threshold for failed attempts'
    )
    
    # Security logs
    log_file = CharField(
        string='Log File',
        size=255,
        help='Path to security log file'
    )
    
    error_message = TextField(
        string='Error Message',
        help='Error message if security failed'
    )
    
    # Security metadata
    metadata = TextField(
        string='Metadata',
        help='Security metadata (JSON format)'
    )
    
    # Security analytics
    success_rate = FloatField(
        string='Success Rate (%)',
        default=100.0,
        help='Security success rate percentage'
    )
    
    threat_level = SelectionField(
        string='Threat Level',
        selection=[
            ('low', 'Low'),
            ('medium', 'Medium'),
            ('high', 'High'),
            ('critical', 'Critical'),
        ],
        default='low',
        help='Current threat level'
    )
    
    def create(self, vals: Dict[str, Any]):
        """Override create to set default values"""
        return super().create(vals)
    
    def write(self, vals: Dict[str, Any]):
        """Override write to handle security updates"""
        result = super().write(vals)
        
        # Update success rate
        if 'failed_attempts' in vals or 'successful_attempts' in vals:
            for security in self:
                security._calculate_success_rate()
        
        return result
    
    def action_activate(self):
        """Activate security"""
        self.is_enabled = True
        self.status = 'active'
        return True
    
    def action_deactivate(self):
        """Deactivate security"""
        self.is_enabled = False
        self.status = 'inactive'
        return True
    
    def action_test_security(self):
        """Test security configuration"""
        self.ensure_one()
        
        try:
            # In standalone version, we'll do basic security tests
            if not self.is_enabled:
                raise ValueError('Security is not enabled')
            
            # Test encryption
            if self.encryption_enabled and not self.encryption_algorithm:
                raise ValueError('Encryption algorithm is required when encryption is enabled')
            
            # Test audit
            if self.audit_enabled and not self.audit_level:
                raise ValueError('Audit level is required when audit is enabled')
            
            self.status = 'active'
            return True
        except Exception as e:
            self.status = 'error'
            self.error_message = str(e)
            raise ValueError(f'Security test failed: {str(e)}')
    
    def action_authenticate(self, credentials: Dict[str, Any]):
        """Authenticate user"""
        self.ensure_one()
        
        try:
            # In standalone version, we'll do basic authentication
            if not credentials.get('username') or not credentials.get('password'):
                raise ValueError('Username and password are required')
            
            # Simulate authentication
            if credentials['username'] == 'admin' and credentials['password'] == 'admin':
                self.successful_attempts += 1
                self.last_success = datetime.now()
                self.status = 'active'
                return True
            else:
                self.failed_attempts += 1
                self.last_failure = datetime.now()
                
                # Check if max attempts exceeded
                if self.failed_attempts >= self.max_attempts:
                    self.blocked_attempts += 1
                    self.status = 'error'
                    raise ValueError('Maximum attempts exceeded. Account locked.')
                
                raise ValueError('Invalid credentials')
        except Exception as e:
            self.error_message = str(e)
            raise ValueError(f'Authentication failed: {str(e)}')
    
    def action_authorize(self, user_id: int, resource: str, action: str):
        """Authorize user action"""
        self.ensure_one()
        
        try:
            # In standalone version, we'll do basic authorization
            if not user_id or not resource or not action:
                raise ValueError('User ID, resource, and action are required')
            
            # Simulate authorization check
            if user_id == 1:  # Admin user
                return True
            else:
                raise ValueError('Access denied')
        except Exception as e:
            self.error_message = str(e)
            raise ValueError(f'Authorization failed: {str(e)}')
    
    def action_encrypt_data(self, data: str):
        """Encrypt data"""
        self.ensure_one()
        
        if not self.encryption_enabled:
            raise ValueError('Encryption is not enabled')
        
        if not self.encryption_algorithm:
            raise ValueError('Encryption algorithm is not configured')
        
        # In standalone version, we'll do basic encryption simulation
        encrypted_data = f"encrypted_{data}"
        return encrypted_data
    
    def action_decrypt_data(self, encrypted_data: str):
        """Decrypt data"""
        self.ensure_one()
        
        if not self.encryption_enabled:
            raise ValueError('Encryption is not enabled')
        
        if not self.encryption_algorithm:
            raise ValueError('Encryption algorithm is not configured')
        
        # In standalone version, we'll do basic decryption simulation
        if encrypted_data.startswith('encrypted_'):
            decrypted_data = encrypted_data[10:]  # Remove 'encrypted_' prefix
            return decrypted_data
        else:
            raise ValueError('Invalid encrypted data')
    
    def action_audit_event(self, event_type: str, event_data: Dict[str, Any]):
        """Audit security event"""
        self.ensure_one()
        
        if not self.audit_enabled:
            return True
        
        # Log audit event
        audit_message = f"Security audit: {event_type} - {event_data}"
        logger.info(audit_message)
        
        # Check for security threats
        if event_type == 'failed_login':
            self.failed_attempts += 1
            if self.failed_attempts >= self.alert_threshold:
                self.threat_level = 'high'
                if self.alert_enabled:
                    self._send_security_alert('High number of failed login attempts')
        
        return True
    
    def _send_security_alert(self, message: str):
        """Send security alert"""
        logger.warning(f'Security alert: {message}')
        
        # This would need actual implementation to send alerts
        # For now, we'll just log the alert
    
    def _calculate_success_rate(self):
        """Calculate security success rate"""
        total_attempts = self.successful_attempts + self.failed_attempts
        if total_attempts > 0:
            self.success_rate = (self.successful_attempts / total_attempts) * 100
        else:
            self.success_rate = 100.0
    
    def get_security_info(self):
        """Get security information"""
        return {
            'name': self.name,
            'description': self.description,
            'database_id': self.database_id,
            'security_type': self.security_type,
            'status': self.status,
            'is_enabled': self.is_enabled,
            'is_required': self.is_required,
            'security_level': self.security_level,
            'failed_attempts': self.failed_attempts,
            'successful_attempts': self.successful_attempts,
            'blocked_attempts': self.blocked_attempts,
            'last_attempt': self.last_attempt,
            'last_success': self.last_success,
            'last_failure': self.last_failure,
            'max_attempts': self.max_attempts,
            'lockout_duration': self.lockout_duration,
            'password_policy': self.password_policy,
            'encryption_enabled': self.encryption_enabled,
            'encryption_algorithm': self.encryption_algorithm,
            'audit_enabled': self.audit_enabled,
            'audit_level': self.audit_level,
            'alert_enabled': self.alert_enabled,
            'alert_threshold': self.alert_threshold,
            'log_file': self.log_file,
            'error_message': self.error_message,
            'success_rate': self.success_rate,
            'threat_level': self.threat_level,
        }
    
    def get_security_analytics(self):
        """Get security analytics"""
        return {
            'status': self.status,
            'security_level': self.security_level,
            'threat_level': self.threat_level,
            'failed_attempts': self.failed_attempts,
            'successful_attempts': self.successful_attempts,
            'blocked_attempts': self.blocked_attempts,
            'success_rate': self.success_rate,
            'last_attempt': self.last_attempt,
            'last_success': self.last_success,
            'last_failure': self.last_failure,
            'encryption_enabled': self.encryption_enabled,
            'audit_enabled': self.audit_enabled,
            'alert_enabled': self.alert_enabled,
        }
    
    @classmethod
    def get_security_by_database(cls, database_id: int):
        """Get security by database"""
        return cls.search([
            ('database_id', '=', database_id),
        ])
    
    @classmethod
    def get_security_by_type(cls, security_type: str):
        """Get security by type"""
        return cls.search([
            ('security_type', '=', security_type),
        ])
    
    @classmethod
    def get_security_by_status(cls, status: str):
        """Get security by status"""
        return cls.search([
            ('status', '=', status),
        ])
    
    @classmethod
    def get_active_security(cls):
        """Get active security"""
        return cls.search([
            ('is_enabled', '=', True),
            ('status', '=', 'active'),
        ])
    
    @classmethod
    def get_security_analytics_summary(cls):
        """Get security analytics summary"""
        # In standalone version, we'll return mock data
        return {
            'total_security': 0,
            'active_security': 0,
            'error_security': 0,
            'warning_security': 0,
            'average_success_rate': 0.0,
            'total_failed_attempts': 0,
            'total_blocked_attempts': 0,
            'high_threat_level': 0,
        }
    
    def _check_name(self):
        """Validate security name"""
        if self.name:
            # Check for duplicate names
            existing = self.search([
                ('name', '=', self.name),
                ('id', '!=', self.id),
            ])
            if existing:
                raise ValueError('Security name must be unique')
    
    def _check_attempts(self):
        """Validate security attempts"""
        if self.max_attempts <= 0:
            raise ValueError('Max attempts must be greater than 0')
        
        if self.lockout_duration < 0:
            raise ValueError('Lockout duration cannot be negative')
    
    def _check_threshold(self):
        """Validate alert threshold"""
        if self.alert_threshold <= 0:
            raise ValueError('Alert threshold must be greater than 0')
    
    def action_duplicate(self):
        """Duplicate security"""
        self.ensure_one()
        
        new_security = self.copy({
            'name': f'{self.name} (Copy)',
            'status': 'inactive',
            'failed_attempts': 0,
            'successful_attempts': 0,
            'blocked_attempts': 0,
        })
        
        return new_security
    
    def action_export_security(self):
        """Export security configuration"""
        self.ensure_one()
        
        return {
            'name': self.name,
            'description': self.description,
            'database_id': self.database_id,
            'security_type': self.security_type,
            'is_enabled': self.is_enabled,
            'is_required': self.is_required,
            'security_level': self.security_level,
            'max_attempts': self.max_attempts,
            'lockout_duration': self.lockout_duration,
            'password_policy': self.password_policy,
            'encryption_enabled': self.encryption_enabled,
            'encryption_algorithm': self.encryption_algorithm,
            'audit_enabled': self.audit_enabled,
            'audit_level': self.audit_level,
            'alert_enabled': self.alert_enabled,
            'alert_threshold': self.alert_threshold,
        }
    
    def action_import_security(self, security_data: Dict[str, Any]):
        """Import security configuration"""
        self.ensure_one()
        
        self.write(security_data)
        return True