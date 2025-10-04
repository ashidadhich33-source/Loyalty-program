#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Notification Model
=====================================

Notification management for multi-channel alerts.
"""

from core_framework.orm import (
    BaseModel, CharField, TextField, SelectionField, Many2OneField,
    BooleanField, One2ManyField, IntegerField, DateTimeField, FloatField
)
from addons.core_base.models.base_mixins import KidsClothingMixin


class Notification(BaseModel, KidsClothingMixin):
    """Notification Model"""
    
    _name = 'notification.notification'
    _description = 'Notification'
    _order = 'create_date desc'
    
    # Basic Information
    name = CharField('Subject', required=True, size=200)
    message = TextField('Message', required=True)
    notification_type = SelectionField([
        ('info', 'Information'),
        ('warning', 'Warning'),
        ('error', 'Error'),
        ('success', 'Success'),
        ('urgent', 'Urgent'),
    ], 'Type', required=True, default='info')
    
    # Recipients
    user_ids = One2ManyField('users.user', 'notification_ids', 'Recipients')
    group_ids = One2ManyField('users.group', 'notification_ids', 'Groups')
    
    # Notification Channels
    channel_ids = One2ManyField('notification.channel', 'notification_ids', 'Channels')
    
    # Content
    template_id = Many2OneField('notification.template', 'Template')
    context_data = TextField('Context Data', help='JSON data for template rendering')
    
    # Scheduling
    scheduled_date = DateTimeField('Scheduled Date')
    priority = SelectionField([
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ], 'Priority', default='medium')
    
    # Status
    status = SelectionField([
        ('draft', 'Draft'),
        ('queued', 'Queued'),
        ('sending', 'Sending'),
        ('sent', 'Sent'),
        ('delivered', 'Delivered'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    ], 'Status', default='draft')
    
    # Delivery Tracking
    delivery_attempts = IntegerField('Delivery Attempts', default=0)
    max_attempts = IntegerField('Max Attempts', default=3)
    last_attempt = DateTimeField('Last Attempt')
    delivery_log = TextField('Delivery Log')
    
    # Access Control
    user_id = Many2OneField('users.user', 'Created By', required=True)
    company_id = Many2OneField('res.company', 'Company')
    
    def send_notification(self):
        """Send notification through all channels"""
        try:
            self.write({'status': 'sending'})
            
            # Get recipients
            recipients = self._get_recipients()
            
            # Send through each channel
            for channel in self.channel_ids:
                self._send_through_channel(channel, recipients)
            
            # Update status
            self.write({
                'status': 'sent',
                'last_attempt': self.env.cr.now(),
                'delivery_attempts': self.delivery_attempts + 1,
            })
            
            return True
            
        except Exception as e:
            self.write({
                'status': 'failed',
                'delivery_log': f"Error: {str(e)}",
                'last_attempt': self.env.cr.now(),
            })
            raise e
    
    def _get_recipients(self):
        """Get all recipients for the notification"""
        recipients = []
        
        # Add individual users
        for user in self.user_ids:
            recipients.append({
                'type': 'user',
                'id': user.id,
                'name': user.name,
                'email': user.email,
                'phone': user.phone,
            })
        
        # Add users from groups
        for group in self.group_ids:
            for user in group.user_ids:
                if user.id not in [r['id'] for r in recipients]:
                    recipients.append({
                        'type': 'user',
                        'id': user.id,
                        'name': user.name,
                        'email': user.email,
                        'phone': user.phone,
                    })
        
        return recipients
    
    def _send_through_channel(self, channel, recipients):
        """Send notification through specific channel"""
        try:
            if channel.channel_type == 'email':
                self._send_email(channel, recipients)
            elif channel.channel_type == 'sms':
                self._send_sms(channel, recipients)
            elif channel.channel_type == 'whatsapp':
                self._send_whatsapp(channel, recipients)
            elif channel.channel_type == 'push':
                self._send_push(channel, recipients)
            elif channel.channel_type == 'in_app':
                self._send_in_app(channel, recipients)
            
        except Exception as e:
            self.write({
                'delivery_log': f"{channel.name} failed: {str(e)}",
            })
            raise e
    
    def _send_email(self, channel, recipients):
        """Send email notification"""
        # Implementation for email sending
        for recipient in recipients:
            if recipient.get('email'):
                # Send email logic here
                pass
    
    def _send_sms(self, channel, recipients):
        """Send SMS notification"""
        # Implementation for SMS sending
        for recipient in recipients:
            if recipient.get('phone'):
                # Send SMS logic here
                pass
    
    def _send_whatsapp(self, channel, recipients):
        """Send WhatsApp notification"""
        # Implementation for WhatsApp sending
        for recipient in recipients:
            if recipient.get('phone'):
                # Send WhatsApp logic here
                pass
    
    def _send_push(self, channel, recipients):
        """Send push notification"""
        # Implementation for push notification
        for recipient in recipients:
            # Send push notification logic here
            pass
    
    def _send_in_app(self, channel, recipients):
        """Send in-app notification"""
        # Implementation for in-app notification
        for recipient in recipients:
            # Create in-app notification record
            self.env['notification.in_app'].create({
                'user_id': recipient['id'],
                'subject': self.name,
                'message': self.message,
                'notification_type': self.notification_type,
                'priority': self.priority,
                'notification_id': self.id,
            })
    
    def schedule_notification(self, scheduled_date):
        """Schedule notification for later delivery"""
        self.write({
            'scheduled_date': scheduled_date,
            'status': 'queued',
        })
    
    def cancel_notification(self):
        """Cancel notification"""
        self.write({'status': 'cancelled'})
    
    def retry_delivery(self):
        """Retry failed notification delivery"""
        if self.status == 'failed' and self.delivery_attempts < self.max_attempts:
            self.send_notification()
    
    def get_notification_summary(self):
        """Get notification summary"""
        return {
            'id': self.id,
            'name': self.name,
            'type': self.notification_type,
            'status': self.status,
            'priority': self.priority,
            'recipients_count': len(self._get_recipients()),
            'channels_count': len(self.channel_ids),
            'create_date': self.create_date,
            'scheduled_date': self.scheduled_date,
        }


class NotificationInApp(BaseModel, KidsClothingMixin):
    """In-App Notification Model"""
    
    _name = 'notification.in_app'
    _description = 'In-App Notification'
    _order = 'create_date desc'
    
    # Basic Information
    user_id = Many2OneField('users.user', 'User', required=True)
    subject = CharField('Subject', required=True, size=200)
    message = TextField('Message', required=True)
    notification_type = SelectionField([
        ('info', 'Information'),
        ('warning', 'Warning'),
        ('error', 'Error'),
        ('success', 'Success'),
        ('urgent', 'Urgent'),
    ], 'Type', default='info')
    
    # Status
    is_read = BooleanField('Is Read', default=False)
    is_archived = BooleanField('Is Archived', default=False)
    priority = SelectionField([
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ], 'Priority', default='medium')
    
    # Related Data
    notification_id = Many2OneField('notification.notification', 'Parent Notification')
    related_model = CharField('Related Model', size=100)
    related_id = IntegerField('Related Record ID')
    
    # Actions
    action_url = CharField('Action URL', size=500)
    action_text = CharField('Action Text', size=100)
    
    def mark_as_read(self):
        """Mark notification as read"""
        self.write({'is_read': True})
    
    def archive(self):
        """Archive notification"""
        self.write({'is_archived': True})
    
    def get_user_notifications(self, user_id, limit=50):
        """Get notifications for user"""
        return self.search([
            ('user_id', '=', user_id),
            ('is_archived', '=', False),
        ], limit=limit, order='create_date desc')
    
    def get_unread_count(self, user_id):
        """Get unread notification count for user"""
        return self.search_count([
            ('user_id', '=', user_id),
            ('is_read', '=', False),
            ('is_archived', '=', False),
        ])