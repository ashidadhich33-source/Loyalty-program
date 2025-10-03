# -*- coding: utf-8 -*-

from core_framework.orm import BaseModel, CharField, TextField, BooleanField, IntegerField, DateTimeField, Many2OneField, SelectionField, FloatField, One2ManyField, Many2ManyField
from core_framework.exceptions import ValidationError
import logging
import json
from datetime import datetime, timedelta

_logger = logging.getLogger(__name__)


class NotificationSystem(BaseModel):
    """Notification system for Kids Clothing ERP"""
    
    _name = 'notification.system'
    _description = 'Notification System'
    _order = 'create_date desc'
    
    # Basic fields
    name = CharField(
        string='Title',
        size=255,
        required=True,
        help='Notification title'
    )
    
    message = TextField(
        string='Message',
        required=True,
        help='Notification message'
    )
    
    type = SelectionField(
        string='Type',
        selection=[
        ('info', 'Information'),
        ('success', 'Success'),
        ('warning', 'Warning'),
        ('error', 'Error'),
        ('reminder', 'Reminder'),
        ('alert', 'Alert'),
    ],
        default='info',
        help='Notification type'
    )
    
    priority = SelectionField(
        string='Priority',
        selection=[
        ('low', 'Low'),
        ('normal', 'Normal'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ],
        default='normal',
        help='Notification priority'
    )
    
    # User and recipient fields
    user_id = Many2OneField('res.users', string='User', default=lambda self: self.env.user, help='User who created the notification'
    )
    
    recipient_ids = Many2ManyField('res.users', string='Recipients', help='Users who will receive this notification'
    )
    
    # Status and delivery
    status = SelectionField(
        string='Status',
        selection=[
        ('draft', 'Draft'),
        ('sent', 'Sent'),
        ('delivered', 'Delivered'),
        ('read', 'Read'),
        ('failed', 'Failed'),
    ],
        default='draft',
        help='Notification status'
    )
    
    delivery_method = SelectionField(
        string='Delivery Method',
        selection=[
        ('in_app', 'In-App'),
        ('email', 'Email'),
        ('sms', 'SMS'),
        ('whatsapp', 'WhatsApp'),
        ('push', 'Push Notification'),
    ],
        default='in_app',
        help='How to deliver the notification'
    )
    
    # Timestamps
    sent_date = DateFieldtime(
        string='Sent Date',
        help='When the notification was sent'
    )
    
    delivered_date = DateFieldtime(
        string='Delivered Date',
        help='When the notification was delivered'
    )
    
    read_date = DateFieldtime(
        string='Read Date',
        help='When the notification was read'
    )
    
    # Additional fields
    icon = CharField(
        string='Icon',
        help='Icon class for the notification'
    )
    
    action_url = CharField(
        string='Action URL',
        help='URL to navigate to when notification is clicked'
    )
    
    action_text = CharField(
        string='Action Text',
        help='Text for the action button'
    )
    
    expires_date = DateFieldtime(
        string='Expires Date',
        help='When the notification expires'
    )
    
    is_auto_dismiss = BooleanField(
        string='Auto Dismiss',
        default=True,
        help='Automatically dismiss after a certain time'
    )
    
    auto_dismiss_delay = IntegerField(
        string='Auto Dismiss Delay (seconds)',
        default=5,
        help='Delay before auto dismiss in seconds'
    )
    
    # Related record fields
    model_name = CharField(
        string='Model',
        help='Related model name'
    )
    
    record_id = IntegerField(
        string='Record ID',
        help='Related record ID'
    )
    
    # Grouping and categorization
    category = CharField(
        string='Category',
        help='Notification category for grouping'
    )
    
    group_id = Many2OneField(
        'notification.group',
        string='Group',
        help='Notification group'
    )
    
    # Template and content
    template_id = Many2OneField(
        'notification.template',
        string='Template',
        help='Notification template'
    )
    
    template_data = TextField(
        string='Template Data',
        help='JSON data for template rendering'
    )
    
    # Delivery tracking
    delivery_attempts = IntegerField(
        string='Delivery Attempts',
        default=0,
        help='Number of delivery attempts'
    )
    
    last_delivery_attempt = DateFieldtime(
        string='Last Delivery Attempt',
        help='Last delivery attempt timestamp'
    )
    
    delivery_error = TextField(
        string='Delivery Error',
        help='Error message from last delivery attempt'
    )
    
    @api.model
    def create(self, vals):
        """Override create to set default values"""
        if 'icon' not in vals:
            vals['icon'] = self._get_default_icon(vals.get('type', 'info'))
        
        if 'expires_date' not in vals and vals.get('is_auto_dismiss', True):
            delay = vals.get('auto_dismiss_delay', 5)
            vals['expires_date'] = DateFieldtime.now() + timedelta(seconds=delay)
        
        return super(NotificationSystem, self).create(vals)
    
    def _get_default_icon(self, notification_type):
        """Get default icon for notification type"""
        icon_mapping = {
            'info': 'fa-info-circle',
            'success': 'fa-check-circle',
            'warning': 'fa-exclamation-triangle',
            'error': 'fa-exclamation-circle',
            'reminder': 'fa-clock',
            'alert': 'fa-bell',
        }
        return icon_mapping.get(notification_type, 'fa-info-circle')
    
    def send_notification(self):
        """Send the notification to recipients"""
        for notification in self:
            if notification.status != 'draft':
                continue
            
            try:
                # Update status to sent
                notification.status = 'sent'
                notification.sent_date = DateFieldtime.now()
                notification.delivery_attempts += 1
                notification.last_delivery_attempt = DateFieldtime.now()
                
                # Send based on delivery method
                if notification.delivery_method == 'in_app':
                    self._send_in_app_notification(notification)
                elif notification.delivery_method == 'email':
                    self._send_email_notification(notification)
                elif notification.delivery_method == 'sms':
                    self._send_sms_notification(notification)
                elif notification.delivery_method == 'whatsapp':
                    self._send_whatsapp_notification(notification)
                elif notification.delivery_method == 'push':
                    self._send_push_notification(notification)
                
                # Mark as delivered
                notification.status = 'delivered'
                notification.delivered_date = DateFieldtime.now()
                
            except Exception as e:
                _logger.error(f"Failed to send notification {notification.id}: {str(e)}")
                notification.status = 'failed'
                notification.delivery_error = str(e)
    
    def _send_in_app_notification(self, notification):
        """Send in-app notification"""
        # Create notification records for each recipient
        for recipient in notification.recipient_ids:
            self.env['notification.recipient'].create({
                'notification_id': notification.id,
                'user_id': recipient.id,
                'status': 'delivered',
                'delivered_date': DateFieldtime.now(),
            })
    
    def _send_email_notification(self, notification):
        """Send email notification"""
        # This would integrate with email system
        pass
    
    def _send_sms_notification(self, notification):
        """Send SMS notification"""
        # This would integrate with SMS gateway
        pass
    
    def _send_whatsapp_notification(self, notification):
        """Send WhatsApp notification"""
        # This would integrate with WhatsApp API
        pass
    
    def _send_push_notification(self, notification):
        """Send push notification"""
        # This would integrate with push notification service
        pass
    
    def mark_as_read(self):
        """Mark notification as read"""
        self.status = 'read'
        self.read_date = DateFieldtime.now()
    
    def mark_as_delivered(self):
        """Mark notification as delivered"""
        self.status = 'delivered'
        self.delivered_date = DateFieldtime.now()
    
    def dismiss_notification(self):
        """Dismiss the notification"""
        self.unlink()
    
    def resend_notification(self):
        """Resend the notification"""
        self.status = 'draft'
        self.delivery_error = False
        self.send_notification()
    
    @api.model
    def create_notification(self, title, message, recipients=None, notification_type='info', **kwargs):
        """Create and send a notification"""
        if not recipients:
            recipients = [self.env.user.id]
        
        notification = self.create({
            'name': title,
            'message': message,
            'type': notification_type,
            'recipient_ids': [(6, 0, recipients)],
            **kwargs
        })
        
        notification.send_notification()
        return notification
    
    @api.model
    def get_user_notifications(self, user_id=None, limit=50):
        """Get notifications for a user"""
        if not user_id:
            user_id = self.env.user.id
        
        return self.search([
            ('recipient_ids', 'in', [user_id]),
            ('status', 'in', ['delivered', 'read']),
        ], limit=limit)
    
    @api.model
    def get_unread_count(self, user_id=None):
        """Get unread notification count for a user"""
        if not user_id:
            user_id = self.env.user.id
        
        return self.search_count([
            ('recipient_ids', 'in', [user_id]),
            ('status', '=', 'delivered'),
        ])
    
    @api.model
    def mark_all_as_read(self, user_id=None):
        """Mark all notifications as read for a user"""
        if not user_id:
            user_id = self.env.user.id
        
        notifications = self.search([
            ('recipient_ids', 'in', [user_id]),
            ('status', '=', 'delivered'),
        ])
        
        notifications.mark_as_read()
        return len(notifications)
    
    @api.model
    def cleanup_expired_notifications(self):
        """Clean up expired notifications"""
        expired_notifications = self.search([
            ('expires_date', '<', DateFieldtime.now()),
            ('status', 'in', ['delivered', 'read']),
        ])
        
        count = len(expired_notifications)
        expired_notifications.unlink()
        
        _logger.info(f"Cleaned up {count} expired notifications")
        return count
    
    @api.model
    def send_bulk_notification(self, title, message, user_ids, notification_type='info', **kwargs):
        """Send notification to multiple users"""
        notifications = []
        
        for user_id in user_ids:
            notification = self.create_notification(
                title=title,
                message=message,
                recipients=[user_id],
                notification_type=notification_type,
                **kwargs
            )
            notifications.append(notification)
        
        return notifications
    
    @api.model
    def send_system_notification(self, title, message, notification_type='info', **kwargs):
        """Send system-wide notification"""
        all_users = self.env['res.users'].search([('active', '=', True)])
        user_ids = all_users.ids
        
        return self.send_bulk_notification(
            title=title,
            message=message,
            user_ids=user_ids,
            notification_type=notification_type,
            **kwargs
        )


class NotificationRecipient(models.Model):
    """Notification recipient tracking"""
    
    _name = 'notification.recipient'
    _description = 'Notification Recipient'
    _order = 'create_date desc'
    
    notification_id = Many2OneField(
        'notification.system',
        string='Notification',
        required=True,
        ondelete='cascade'
    )
    
    user_id = Many2OneField(
        'res.users',
        string='User',
        required=True
    )
    
    status = SelectionField(
        string='Status',
        selection=[
        ('pending', 'Pending'),
        ('delivered', 'Delivered'),
        ('read', 'Read'),
        ('failed', 'Failed'),
    ],
        default='pending'
    )
    
    delivered_date = DateFieldtime(
        string='Delivered Date'
    )
    
    read_date = DateFieldtime(
        string='Read Date'
    )
    
    error_message = TextField(
        string='Error Message'
    )
    
    def mark_as_read(self):
        """Mark notification as read for this recipient"""
        self.status = 'read'
        self.read_date = DateFieldtime.now()
        
        # Update main notification status if all recipients have read
        notification = self.notification_id
        all_recipients = notification.recipient_ids
        read_recipients = self.search([
            ('notification_id', '=', notification.id),
            ('status', '=', 'read')
        ])
        
        if len(read_recipients) == len(all_recipients):
            notification.mark_as_read()


class NotificationTemplate(models.Model):
    """Notification templates"""
    
    _name = 'notification.template'
    _description = 'Notification Template'
    
    name = CharField(
        string='Template Name',
        required=True
    )
    
    subject = CharField(
        string='Subject',
        help='Notification subject template'
    )
    
    body = TextField(
        string='Body',
        help='Notification body template'
    )
    
    type = SelectionField(
        string='Type',
        selection=[
        ('info', 'Information'),
        ('success', 'Success'),
        ('warning', 'Warning'),
        ('error', 'Error'),
        ('reminder', 'Reminder'),
        ('alert', 'Alert'),
    ],
        default='info'
    )
    
    delivery_method = SelectionField(
        string='Delivery Method',
        selection=[
        ('in_app', 'In-App'),
        ('email', 'Email'),
        ('sms', 'SMS'),
        ('whatsapp', 'WhatsApp'),
        ('push', 'Push Notification'),
    ],
        default='in_app'
    )
    
    is_active = BooleanField(
        string='Active',
        default=True
    )
    
    variables = TextField(
        string='Variables',
        help='Available variables for this template'
    )
    
    def render_template(self, data):
        """Render template with data"""
        # This would implement template rendering logic
        pass