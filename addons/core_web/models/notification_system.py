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
    name = fields.Char(
        string='Title',
        required=True,
        help='Notification title'
    )
    
    message = fields.Text(
        string='Message',
        required=True,
        help='Notification message'
    )
    
    type = fields.Selection([
        ('info', 'Information'),
        ('success', 'Success'),
        ('warning', 'Warning'),
        ('error', 'Error'),
        ('reminder', 'Reminder'),
        ('alert', 'Alert'),
    ], string='Type', default='info', help='Notification type')
    
    priority = fields.Selection([
        ('low', 'Low'),
        ('normal', 'Normal'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ], string='Priority', default='normal', help='Notification priority')
    
    # User and recipient fields
    user_id = fields.Many2one(
        'res.users',
        string='User',
        default=lambda self: self.env.user,
        help='User who created the notification'
    )
    
    recipient_ids = fields.Many2many(
        'res.users',
        'notification_recipient_rel',
        'notification_id',
        'user_id',
        string='Recipients',
        help='Users who will receive this notification'
    )
    
    # Status and delivery
    status = fields.Selection([
        ('draft', 'Draft'),
        ('sent', 'Sent'),
        ('delivered', 'Delivered'),
        ('read', 'Read'),
        ('failed', 'Failed'),
    ], string='Status', default='draft', help='Notification status')
    
    delivery_method = fields.Selection([
        ('in_app', 'In-App'),
        ('email', 'Email'),
        ('sms', 'SMS'),
        ('whatsapp', 'WhatsApp'),
        ('push', 'Push Notification'),
    ], string='Delivery Method', default='in_app', help='How to deliver the notification')
    
    # Timestamps
    sent_date = fields.Datetime(
        string='Sent Date',
        help='When the notification was sent'
    )
    
    delivered_date = fields.Datetime(
        string='Delivered Date',
        help='When the notification was delivered'
    )
    
    read_date = fields.Datetime(
        string='Read Date',
        help='When the notification was read'
    )
    
    # Additional fields
    icon = fields.Char(
        string='Icon',
        help='Icon class for the notification'
    )
    
    action_url = fields.Char(
        string='Action URL',
        help='URL to navigate to when notification is clicked'
    )
    
    action_text = fields.Char(
        string='Action Text',
        help='Text for the action button'
    )
    
    expires_date = fields.Datetime(
        string='Expires Date',
        help='When the notification expires'
    )
    
    is_auto_dismiss = fields.Boolean(
        string='Auto Dismiss',
        default=True,
        help='Automatically dismiss after a certain time'
    )
    
    auto_dismiss_delay = fields.Integer(
        string='Auto Dismiss Delay (seconds)',
        default=5,
        help='Delay before auto dismiss in seconds'
    )
    
    # Related record fields
    model_name = fields.Char(
        string='Model',
        help='Related model name'
    )
    
    record_id = fields.Integer(
        string='Record ID',
        help='Related record ID'
    )
    
    # Grouping and categorization
    category = fields.Char(
        string='Category',
        help='Notification category for grouping'
    )
    
    group_id = fields.Many2one(
        'notification.group',
        string='Group',
        help='Notification group'
    )
    
    # Template and content
    template_id = fields.Many2one(
        'notification.template',
        string='Template',
        help='Notification template'
    )
    
    template_data = fields.Text(
        string='Template Data',
        help='JSON data for template rendering'
    )
    
    # Delivery tracking
    delivery_attempts = fields.Integer(
        string='Delivery Attempts',
        default=0,
        help='Number of delivery attempts'
    )
    
    last_delivery_attempt = fields.Datetime(
        string='Last Delivery Attempt',
        help='Last delivery attempt timestamp'
    )
    
    delivery_error = fields.Text(
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
            vals['expires_date'] = fields.Datetime.now() + timedelta(seconds=delay)
        
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
                notification.sent_date = fields.Datetime.now()
                notification.delivery_attempts += 1
                notification.last_delivery_attempt = fields.Datetime.now()
                
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
                notification.delivered_date = fields.Datetime.now()
                
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
                'delivered_date': fields.Datetime.now(),
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
        self.read_date = fields.Datetime.now()
    
    def mark_as_delivered(self):
        """Mark notification as delivered"""
        self.status = 'delivered'
        self.delivered_date = fields.Datetime.now()
    
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
            ('expires_date', '<', fields.Datetime.now()),
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
    
    notification_id = fields.Many2one(
        'notification.system',
        string='Notification',
        required=True,
        ondelete='cascade'
    )
    
    user_id = fields.Many2one(
        'res.users',
        string='User',
        required=True
    )
    
    status = fields.Selection([
        ('pending', 'Pending'),
        ('delivered', 'Delivered'),
        ('read', 'Read'),
        ('failed', 'Failed'),
    ], string='Status', default='pending')
    
    delivered_date = fields.Datetime(
        string='Delivered Date'
    )
    
    read_date = fields.Datetime(
        string='Read Date'
    )
    
    error_message = fields.Text(
        string='Error Message'
    )
    
    def mark_as_read(self):
        """Mark notification as read for this recipient"""
        self.status = 'read'
        self.read_date = fields.Datetime.now()
        
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
    
    name = fields.Char(
        string='Template Name',
        required=True
    )
    
    subject = fields.Char(
        string='Subject',
        help='Notification subject template'
    )
    
    body = fields.Text(
        string='Body',
        help='Notification body template'
    )
    
    type = fields.Selection([
        ('info', 'Information'),
        ('success', 'Success'),
        ('warning', 'Warning'),
        ('error', 'Error'),
        ('reminder', 'Reminder'),
        ('alert', 'Alert'),
    ], string='Type', default='info')
    
    delivery_method = fields.Selection([
        ('in_app', 'In-App'),
        ('email', 'Email'),
        ('sms', 'SMS'),
        ('whatsapp', 'WhatsApp'),
        ('push', 'Push Notification'),
    ], string='Delivery Method', default='in_app')
    
    is_active = fields.Boolean(
        string='Active',
        default=True
    )
    
    variables = fields.Text(
        string='Variables',
        help='Available variables for this template'
    )
    
    def render_template(self, data):
        """Render template with data"""
        # This would implement template rendering logic
        pass