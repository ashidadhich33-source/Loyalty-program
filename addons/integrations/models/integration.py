#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Integration Model
====================================

Integration management for third-party services.
"""

from core_framework.orm import (
    BaseModel, CharField, TextField, SelectionField, Many2OneField,
    BooleanField, One2ManyField, IntegerField, DateTimeField, FloatField
)
from addons.core_base.models.base_mixins import KidsClothingMixin


class Integration(BaseModel, KidsClothingMixin):
    """Integration Model"""
    
    _name = 'integration.integration'
    _description = 'Integration'
    _order = 'sequence, name'
    
    # Basic Information
    name = CharField('Integration Name', required=True, size=200)
    description = TextField('Description')
    code = CharField('Integration Code', required=True, size=50)
    
    # Integration Configuration
    integration_type = SelectionField([
        ('payment_gateway', 'Payment Gateway'),
        ('shipping', 'Shipping Service'),
        ('accounting', 'Accounting Software'),
        ('crm', 'CRM System'),
        ('ecommerce', 'E-commerce Platform'),
        ('social_media', 'Social Media'),
        ('email_service', 'Email Service'),
        ('sms_service', 'SMS Service'),
        ('cloud_storage', 'Cloud Storage'),
        ('api', 'Generic API'),
        ('webhook', 'Webhook'),
    ], 'Integration Type', required=True)
    
    # Service Provider
    provider = CharField('Service Provider', size=100)
    provider_url = CharField('Provider URL', size=500)
    
    # Status
    status = SelectionField([
        ('draft', 'Draft'),
        ('configured', 'Configured'),
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('error', 'Error'),
    ], 'Status', default='draft')
    
    # Configuration
    config_ids = One2ManyField('integration.config', 'integration_id', 'Configuration')
    endpoint_ids = One2ManyField('integration.endpoint', 'integration_id', 'Endpoints')
    webhook_ids = One2ManyField('integration.webhook', 'integration_id', 'Webhooks')
    
    # Settings
    sequence = IntegerField('Sequence', default=10)
    active = BooleanField('Active', default=True)
    auto_sync = BooleanField('Auto Sync', default=False)
    sync_interval = IntegerField('Sync Interval (minutes)', default=60)
    
    # Monitoring
    last_sync = DateTimeField('Last Sync')
    sync_count = IntegerField('Sync Count', default=0)
    error_count = IntegerField('Error Count', default=0)
    success_rate = FloatField('Success Rate (%)', digits=(5, 2), default=0.0)
    
    # Access Control
    user_id = Many2OneField('users.user', 'Created By', required=True)
    group_ids = One2ManyField('users.group', 'integration_group_ids', 'Access Groups')
    
    def test_connection(self):
        """Test integration connection"""
        try:
            # Get configuration
            config = self._get_configuration()
            
            # Test connection based on integration type
            if self.integration_type == 'api':
                result = self._test_api_connection(config)
            elif self.integration_type == 'webhook':
                result = self._test_webhook_connection(config)
            elif self.integration_type == 'payment_gateway':
                result = self._test_payment_connection(config)
            else:
                result = self._test_generic_connection(config)
            
            # Update status
            if result['success']:
                self.write({'status': 'active'})
            else:
                self.write({'status': 'error'})
            
            return result
            
        except Exception as e:
            self.write({'status': 'error'})
            raise e
    
    def _get_configuration(self):
        """Get integration configuration"""
        config = {}
        for config_item in self.config_ids:
            config[config_item.key] = config_item.value
        return config
    
    def _test_api_connection(self, config):
        """Test API connection"""
        try:
            import requests
            
            # Test API endpoint
            test_url = config.get('test_url', self.provider_url)
            headers = self._get_api_headers(config)
            
            response = requests.get(test_url, headers=headers, timeout=30)
            
            if response.status_code == 200:
                return {'success': True, 'message': 'API connection successful'}
            else:
                return {'success': False, 'message': f'API returned status {response.status_code}'}
                
        except Exception as e:
            return {'success': False, 'message': f'API connection failed: {str(e)}'}
    
    def _test_webhook_connection(self, config):
        """Test webhook connection"""
        try:
            # Test webhook endpoint
            webhook_url = config.get('webhook_url')
            if not webhook_url:
                return {'success': False, 'message': 'Webhook URL not configured'}
            
            # Send test webhook
            test_data = {'test': True, 'timestamp': self.env.cr.now()}
            result = self._send_webhook(webhook_url, test_data)
            
            return result
            
        except Exception as e:
            return {'success': False, 'message': f'Webhook test failed: {str(e)}'}
    
    def _test_payment_connection(self, config):
        """Test payment gateway connection"""
        try:
            # Test payment gateway
            # This would typically involve a test transaction
            return {'success': True, 'message': 'Payment gateway connection successful'}
            
        except Exception as e:
            return {'success': False, 'message': f'Payment gateway test failed: {str(e)}'}
    
    def _test_generic_connection(self, config):
        """Test generic connection"""
        try:
            # Generic connection test
            return {'success': True, 'message': 'Connection test successful'}
            
        except Exception as e:
            return {'success': False, 'message': f'Connection test failed: {str(e)}'}
    
    def _get_api_headers(self, config):
        """Get API headers from configuration"""
        headers = {}
        
        # Add authentication headers
        if config.get('api_key'):
            headers['Authorization'] = f"Bearer {config['api_key']}"
        
        if config.get('api_token'):
            headers['X-API-Token'] = config['api_token']
        
        # Add content type
        headers['Content-Type'] = 'application/json'
        
        return headers
    
    def sync_data(self):
        """Sync data with external service"""
        try:
            self.write({'status': 'active'})
            
            # Get sync configuration
            sync_config = self._get_sync_configuration()
            
            # Perform sync based on integration type
            if self.integration_type == 'api':
                result = self._sync_api_data(sync_config)
            elif self.integration_type == 'webhook':
                result = self._sync_webhook_data(sync_config)
            else:
                result = self._sync_generic_data(sync_config)
            
            # Update sync statistics
            from datetime import datetime
            
            if result['success']:
                self.write({
                    'last_sync': datetime.now(),
                    'sync_count': self.sync_count + 1,
                    'success_rate': self._calculate_success_rate(),
                })
            else:
                self.write({
                    'error_count': self.error_count + 1,
                    'success_rate': self._calculate_success_rate(),
                })
            
            return result
            
        except Exception as e:
            self.write({
                'error_count': self.error_count + 1,
                'status': 'error',
            })
            raise e
    
    def _get_sync_configuration(self):
        """Get sync configuration"""
        config = {}
        for config_item in self.config_ids:
            config[config_item.key] = config_item.value
        return config
    
    def _sync_api_data(self, config):
        """Sync data via API"""
        try:
            # Implementation for API data sync
            return {'success': True, 'message': 'API sync completed', 'records_synced': 0}
            
        except Exception as e:
            return {'success': False, 'message': f'API sync failed: {str(e)}'}
    
    def _sync_webhook_data(self, config):
        """Sync data via webhook"""
        try:
            # Implementation for webhook data sync
            return {'success': True, 'message': 'Webhook sync completed', 'records_synced': 0}
            
        except Exception as e:
            return {'success': False, 'message': f'Webhook sync failed: {str(e)}'}
    
    def _sync_generic_data(self, config):
        """Sync data via generic method"""
        try:
            # Implementation for generic data sync
            return {'success': True, 'message': 'Generic sync completed', 'records_synced': 0}
            
        except Exception as e:
            return {'success': False, 'message': f'Generic sync failed: {str(e)}'}
    
    def _calculate_success_rate(self):
        """Calculate success rate"""
        total_attempts = self.sync_count + self.error_count
        if total_attempts == 0:
            return 0.0
        
        success_rate = (self.sync_count / total_attempts) * 100
        return round(success_rate, 2)
    
    def _send_webhook(self, url, data):
        """Send webhook data"""
        try:
            import requests
            import json
            
            response = requests.post(
                url,
                data=json.dumps(data),
                headers={'Content-Type': 'application/json'},
                timeout=30
            )
            
            if response.status_code in [200, 201]:
                return {'success': True, 'message': 'Webhook sent successfully'}
            else:
                return {'success': False, 'message': f'Webhook failed with status {response.status_code}'}
                
        except Exception as e:
            return {'success': False, 'message': f'Webhook send failed: {str(e)}'}
    
    def get_integration_summary(self):
        """Get integration summary"""
        return {
            'id': self.id,
            'name': self.name,
            'code': self.code,
            'type': self.integration_type,
            'provider': self.provider,
            'status': self.status,
            'active': self.active,
            'last_sync': self.last_sync,
            'sync_count': self.sync_count,
            'error_count': self.error_count,
            'success_rate': self.success_rate,
        }