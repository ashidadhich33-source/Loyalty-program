#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Notification Template Model
==============================================

Notification template management for reusable message formats.
"""

from core_framework.orm import (
    BaseModel, CharField, TextField, SelectionField, Many2OneField,
    BooleanField, One2ManyField, IntegerField
)
from addons.core_base.models.base_mixins import KidsClothingMixin


class NotificationTemplate(BaseModel, KidsClothingMixin):
    """Notification Template Model"""
    
    _name = 'notification.template'
    _description = 'Notification Template'
    _order = 'sequence, name'
    
    # Basic Information
    name = CharField('Template Name', required=True, size=200)
    description = TextField('Description')
    code = CharField('Template Code', required=True, size=50)
    
    # Template Configuration
    template_type = SelectionField([
        ('email', 'Email Template'),
        ('sms', 'SMS Template'),
        ('whatsapp', 'WhatsApp Template'),
        ('push', 'Push Notification Template'),
        ('in_app', 'In-App Template'),
        ('universal', 'Universal Template'),
    ], 'Template Type', required=True)
    
    # Template Content
    subject_template = TextField('Subject Template', help='Template for notification subject')
    body_template = TextField('Body Template', help='Template for notification body')
    html_template = TextField('HTML Template', help='HTML template for email notifications')
    
    # Template Settings
    sequence = IntegerField('Sequence', default=10)
    active = BooleanField('Active', default=True)
    is_public = BooleanField('Public Template', default=False)
    
    # Usage Tracking
    usage_count = IntegerField('Usage Count', default=0)
    
    # Access Control
    user_id = Many2OneField('users.user', 'Created By', required=True)
    group_ids = One2ManyField('users.group', 'template_group_ids', 'Access Groups')
    
    def render_template(self, context_data=None):
        """Render template with context data"""
        try:
            context = context_data or {}
            
            # Render subject
            subject = self._render_text(self.subject_template, context)
            
            # Render body
            body = self._render_text(self.body_template, context)
            
            # Render HTML if available
            html_body = None
            if self.html_template:
                html_body = self._render_text(self.html_template, context)
            
            return {
                'subject': subject,
                'body': body,
                'html_body': html_body,
            }
            
        except Exception as e:
            raise e
    
    def _render_text(self, template_text, context):
        """Render text template with context"""
        if not template_text:
            return ""
        
        try:
            # Simple template rendering using string formatting
            # In a real implementation, you might use Jinja2 or similar
            rendered_text = template_text.format(**context)
            return rendered_text
        except KeyError as e:
            # Handle missing context variables
            return template_text.replace(f"{{{e.args[0]}}}", f"[{e.args[0]}]")
        except Exception as e:
            return template_text
    
    def create_notification(self, recipients, context_data=None, **kwargs):
        """Create notification using this template"""
        try:
            # Render template
            rendered_content = self.render_template(context_data)
            
            # Create notification
            notification_data = {
                'name': rendered_content['subject'],
                'message': rendered_content['body'],
                'template_id': self.id,
                'context_data': str(context_data) if context_data else None,
                'user_id': self.env.uid,
            }
            
            # Add additional parameters
            notification_data.update(kwargs)
            
            notification = self.env['notification.notification'].create(notification_data)
            
            # Add recipients
            if isinstance(recipients, list):
                notification.write({'user_ids': [(6, 0, recipients)]})
            else:
                notification.write({'user_ids': [(4, recipients)]})
            
            # Update usage count
            self.write({'usage_count': self.usage_count + 1})
            
            return notification
            
        except Exception as e:
            raise e
    
    def duplicate_template(self, new_name=None):
        """Duplicate template"""
        new_name = new_name or f"{self.name} (Copy)"
        
        new_template = self.create({
            'name': new_name,
            'description': self.description,
            'code': f"{self.code}_copy",
            'template_type': self.template_type,
            'subject_template': self.subject_template,
            'body_template': self.body_template,
            'html_template': self.html_template,
            'sequence': self.sequence,
            'active': self.active,
            'is_public': False,  # Duplicated templates are private
            'user_id': self.user_id.id,
        })
        
        return new_template
    
    def get_template_summary(self):
        """Get template summary"""
        return {
            'id': self.id,
            'name': self.name,
            'code': self.code,
            'type': self.template_type,
            'usage_count': self.usage_count,
            'active': self.active,
            'is_public': self.is_public,
        }