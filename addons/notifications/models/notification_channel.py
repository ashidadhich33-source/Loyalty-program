#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Notification Channel Model
=============================================

Notification channel management for multi-channel delivery.
"""

from core_framework.orm import (
    BaseModel, CharField, TextField, SelectionField, Many2OneField,
    BooleanField, One2ManyField, IntegerField, FloatField
)
from addons.core_base.models.base_mixins import KidsClothingMixin


class NotificationChannel(BaseModel, KidsClothingMixin):
    """Notification Channel Model"""
    
    _name = 'notification.channel'
    _description = 'Notification Channel'
    _order = 'sequence, name'
    
    # Basic Information
    name = CharField('Channel Name', required=True, size=200)
    description = TextField('Description')
    code = CharField('Channel Code', required=True, size=50)
    
    # Channel Configuration
    channel_type = SelectionField([
        ('email', 'Email'),
        ('sms', 'SMS'),
        ('whatsapp', 'WhatsApp'),
        ('push', 'Push Notification'),
        ('in_app', 'In-App Notification'),
        ('webhook', 'Webhook'),
        ('slack', 'Slack'),
        ('teams', 'Microsoft Teams'),
    ], 'Channel Type', required=True)
    
    # Channel Settings
    sequence = IntegerField('Sequence', default=10)
    active = BooleanField('Active', default=True)
    is_default = BooleanField('Default Channel', default=False)
    
    # Delivery Configuration
    priority = SelectionField([
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ], 'Priority', default='medium')
    
    delivery_timeout = IntegerField('Delivery Timeout (seconds)', default=30)
    retry_attempts = IntegerField('Retry Attempts', default=3)
    retry_interval = IntegerField('Retry Interval (minutes)', default=5)
    
    # Channel Statistics
    total_sent = IntegerField('Total Sent', default=0)
    total_delivered = IntegerField('Total Delivered', default=0)
    total_failed = IntegerField('Total Failed', default=0)
    success_rate = FloatField('Success Rate (%)', digits=(5, 2), default=0.0)
    
    # Channel Configuration
    config_ids = One2ManyField('notification.channel.config', 'channel_id', 'Configuration')
    
    # Access Control
    user_id = Many2OneField('users.user', 'Created By', required=True)
    group_ids = One2ManyField('users.group', 'channel_group_ids', 'Access Groups')
    
    def send_notification(self, notification_data, recipients):
        """Send notification through this channel"""
        try:
            # Validate channel configuration
            if not self._validate_configuration():
                raise ValueError(f"Channel {self.name} is not properly configured")
            
            # Send based on channel type
            if self.channel_type == 'email':
                result = self._send_email(notification_data, recipients)
            elif self.channel_type == 'sms':
                result = self._send_sms(notification_data, recipients)
            elif self.channel_type == 'whatsapp':
                result = self._send_whatsapp(notification_data, recipients)
            elif self.channel_type == 'push':
                result = self._send_push(notification_data, recipients)
            elif self.channel_type == 'in_app':
                result = self._send_in_app(notification_data, recipients)
            elif self.channel_type == 'webhook':
                result = self._send_webhook(notification_data, recipients)
            elif self.channel_type == 'slack':
                result = self._send_slack(notification_data, recipients)
            elif self.channel_type == 'teams':
                result = self._send_teams(notification_data, recipients)
            else:
                raise ValueError(f"Unsupported channel type: {self.channel_type}")
            
            # Update statistics
            self._update_statistics(result)
            
            return result
            
        except Exception as e:
            # Update failure statistics
            self.write({
                'total_failed': self.total_failed + 1,
                'success_rate': self._calculate_success_rate(),
            })
            raise e
    
    def _validate_configuration(self):
        """Validate channel configuration"""
        required_configs = self._get_required_configs()
        
        for config_key in required_configs:
            config = self.config_ids.filtered(lambda c: c.key == config_key)
            if not config or not config.value:
                return False
        
        return True
    
    def _get_required_configs(self):
        """Get required configuration keys for channel type"""
        config_map = {
            'email': ['smtp_host', 'smtp_port', 'smtp_user', 'smtp_password'],
            'sms': ['sms_provider', 'api_key', 'api_secret'],
            'whatsapp': ['whatsapp_api_url', 'access_token'],
            'push': ['firebase_server_key', 'firebase_project_id'],
            'webhook': ['webhook_url'],
            'slack': ['slack_webhook_url'],
            'teams': ['teams_webhook_url'],
        }
        
        return config_map.get(self.channel_type, [])
    
    def _send_email(self, notification_data, recipients):
        """Send email notification"""
        try:
            import smtplib
            from email.mime.text import MIMEText
            from email.mime.multipart import MIMEMultipart
            
            # Get email configuration
            config = self._get_configuration()
            
            # Create email message
            msg = MIMEMultipart()
            msg['From'] = config.get('smtp_user')
            msg['Subject'] = notification_data.get('subject', 'Notification')
            
            # Add body
            body = notification_data.get('body', '')
            if notification_data.get('html_body'):
                msg.attach(MIMEText(notification_data['html_body'], 'html'))
            else:
                msg.attach(MIMEText(body, 'plain'))
            
            # Send to recipients
            sent_count = 0
            for recipient in recipients:
                if recipient.get('email'):
                    msg['To'] = recipient['email']
                    
                    # Send email
                    server = smtplib.SMTP(config['smtp_host'], int(config['smtp_port']))
                    server.starttls()
                    server.login(config['smtp_user'], config['smtp_password'])
                    server.send_message(msg)
                    server.quit()
                    
                    sent_count += 1
            
            return {
                'success': True,
                'sent_count': sent_count,
                'message': f'Email sent to {sent_count} recipients',
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Email sending failed: {str(e)}',
            }
    
    def _send_sms(self, notification_data, recipients):
        """Send SMS notification"""
        try:
            # Get SMS configuration
            config = self._get_configuration()
            
            # Implementation for SMS sending
            # This would integrate with SMS providers like Twilio, AWS SNS, etc.
            sent_count = 0
            for recipient in recipients:
                if recipient.get('phone'):
                    # Send SMS logic here
                    sent_count += 1
            
            return {
                'success': True,
                'sent_count': sent_count,
                'message': f'SMS sent to {sent_count} recipients',
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'SMS sending failed: {str(e)}',
            }
    
    def _send_whatsapp(self, notification_data, recipients):
        """Send WhatsApp notification"""
        try:
            # Get WhatsApp configuration
            config = self._get_configuration()
            
            # Implementation for WhatsApp sending
            # This would integrate with WhatsApp Business API
            sent_count = 0
            for recipient in recipients:
                if recipient.get('phone'):
                    # Send WhatsApp logic here
                    sent_count += 1
            
            return {
                'success': True,
                'sent_count': sent_count,
                'message': f'WhatsApp message sent to {sent_count} recipients',
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'WhatsApp sending failed: {str(e)}',
            }
    
    def _send_push(self, notification_data, recipients):
        """Send push notification"""
        try:
            # Get push configuration
            config = self._get_configuration()
            
            # Implementation for push notification
            # This would integrate with Firebase, OneSignal, etc.
            sent_count = 0
            for recipient in recipients:
                # Send push notification logic here
                sent_count += 1
            
            return {
                'success': True,
                'sent_count': sent_count,
                'message': f'Push notification sent to {sent_count} recipients',
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Push notification failed: {str(e)}',
            }
    
    def _send_in_app(self, notification_data, recipients):
        """Send in-app notification"""
        try:
            # Create in-app notifications
            sent_count = 0
            for recipient in recipients:
                self.env['notification.in_app'].create({
                    'user_id': recipient['id'],
                    'subject': notification_data.get('subject', ''),
                    'message': notification_data.get('body', ''),
                    'notification_type': notification_data.get('type', 'info'),
                    'priority': notification_data.get('priority', 'medium'),
                })
                sent_count += 1
            
            return {
                'success': True,
                'sent_count': sent_count,
                'message': f'In-app notification sent to {sent_count} recipients',
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'In-app notification failed: {str(e)}',
            }
    
    def _send_webhook(self, notification_data, recipients):
        """Send webhook notification"""
        try:
            import requests
            import json
            
            # Get webhook configuration
            config = self._get_configuration()
            webhook_url = config.get('webhook_url')
            
            if not webhook_url:
                raise ValueError("Webhook URL not configured")
            
            # Prepare webhook data
            webhook_data = {
                'notification': notification_data,
                'recipients': recipients,
                'channel': self.name,
                'timestamp': self.env.cr.now(),
            }
            
            # Send webhook
            response = requests.post(
                webhook_url,
                data=json.dumps(webhook_data),
                headers={'Content-Type': 'application/json'},
                timeout=self.delivery_timeout
            )
            
            if response.status_code in [200, 201]:
                return {
                    'success': True,
                    'sent_count': len(recipients),
                    'message': 'Webhook sent successfully',
                }
            else:
                return {
                    'success': False,
                    'message': f'Webhook failed with status {response.status_code}',
                }
                
        except Exception as e:
            return {
                'success': False,
                'message': f'Webhook sending failed: {str(e)}',
            }
    
    def _send_slack(self, notification_data, recipients):
        """Send Slack notification"""
        try:
            import requests
            import json
            
            # Get Slack configuration
            config = self._get_configuration()
            webhook_url = config.get('slack_webhook_url')
            
            if not webhook_url:
                raise ValueError("Slack webhook URL not configured")
            
            # Prepare Slack message
            slack_data = {
                'text': notification_data.get('subject', ''),
                'attachments': [{
                    'color': self._get_slack_color(notification_data.get('type', 'info')),
                    'fields': [{
                        'title': 'Message',
                        'value': notification_data.get('body', ''),
                        'short': False
                    }]
                }]
            }
            
            # Send to Slack
            response = requests.post(
                webhook_url,
                data=json.dumps(slack_data),
                headers={'Content-Type': 'application/json'},
                timeout=self.delivery_timeout
            )
            
            if response.status_code == 200:
                return {
                    'success': True,
                    'sent_count': 1,
                    'message': 'Slack message sent successfully',
                }
            else:
                return {
                    'success': False,
                    'message': f'Slack sending failed with status {response.status_code}',
                }
                
        except Exception as e:
            return {
                'success': False,
                'message': f'Slack sending failed: {str(e)}',
            }
    
    def _send_teams(self, notification_data, recipients):
        """Send Microsoft Teams notification"""
        try:
            import requests
            import json
            
            # Get Teams configuration
            config = self._get_configuration()
            webhook_url = config.get('teams_webhook_url')
            
            if not webhook_url:
                raise ValueError("Teams webhook URL not configured")
            
            # Prepare Teams message
            teams_data = {
                '@type': 'MessageCard',
                '@context': 'http://schema.org/extensions',
                'themeColor': self._get_teams_color(notification_data.get('type', 'info')),
                'summary': notification_data.get('subject', ''),
                'sections': [{
                    'activityTitle': notification_data.get('subject', ''),
                    'activitySubtitle': 'Notification',
                    'text': notification_data.get('body', ''),
                }]
            }
            
            # Send to Teams
            response = requests.post(
                webhook_url,
                data=json.dumps(teams_data),
                headers={'Content-Type': 'application/json'},
                timeout=self.delivery_timeout
            )
            
            if response.status_code == 200:
                return {
                    'success': True,
                    'sent_count': 1,
                    'message': 'Teams message sent successfully',
                }
            else:
                return {
                    'success': False,
                    'message': f'Teams sending failed with status {response.status_code}',
                }
                
        except Exception as e:
            return {
                'success': False,
                'message': f'Teams sending failed: {str(e)}',
            }
    
    def _get_configuration(self):
        """Get channel configuration"""
        config = {}
        for config_item in self.config_ids:
            config[config_item.key] = config_item.value
        return config
    
    def _get_slack_color(self, notification_type):
        """Get Slack color for notification type"""
        color_map = {
            'info': '#36a64f',
            'warning': '#ff9500',
            'error': '#ff0000',
            'success': '#36a64f',
            'urgent': '#ff0000',
        }
        return color_map.get(notification_type, '#36a64f')
    
    def _get_teams_color(self, notification_type):
        """Get Teams color for notification type"""
        color_map = {
            'info': '0078D4',
            'warning': 'FF8C00',
            'error': 'D13438',
            'success': '107C10',
            'urgent': 'D13438',
        }
        return color_map.get(notification_type, '0078D4')
    
    def _update_statistics(self, result):
        """Update channel statistics"""
        if result['success']:
            self.write({
                'total_sent': self.total_sent + result.get('sent_count', 1),
                'total_delivered': self.total_delivered + result.get('sent_count', 1),
                'success_rate': self._calculate_success_rate(),
            })
        else:
            self.write({
                'total_sent': self.total_sent + 1,
                'total_failed': self.total_failed + 1,
                'success_rate': self._calculate_success_rate(),
            })
    
    def _calculate_success_rate(self):
        """Calculate success rate"""
        total_attempts = self.total_delivered + self.total_failed
        if total_attempts == 0:
            return 0.0
        
        success_rate = (self.total_delivered / total_attempts) * 100
        return round(success_rate, 2)
    
    def get_channel_summary(self):
        """Get channel summary"""
        return {
            'id': self.id,
            'name': self.name,
            'code': self.code,
            'type': self.channel_type,
            'active': self.active,
            'is_default': self.is_default,
            'total_sent': self.total_sent,
            'total_delivered': self.total_delivered,
            'total_failed': self.total_failed,
            'success_rate': self.success_rate,
        }


class NotificationChannelConfig(BaseModel, KidsClothingMixin):
    """Notification Channel Configuration Model"""
    
    _name = 'notification.channel.config'
    _description = 'Notification Channel Configuration'
    
    channel_id = Many2OneField('notification.channel', 'Channel', required=True)
    key = CharField('Configuration Key', required=True, size=100)
    value = TextField('Configuration Value')
    description = TextField('Description')
    is_encrypted = BooleanField('Encrypted', default=False)