#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - CRM Communication Model
============================================

Communication management for kids clothing retail.
"""

import logging
from datetime import datetime, timedelta
from core_framework.orm import BaseModel, CharField, TextField, BooleanField, IntegerField, DateTimeField, Many2OneField, SelectionField, FloatField, One2ManyField, Many2ManyField
from core_framework.exceptions import ValidationError

logger = logging.getLogger(__name__)

class CrmCommunication(BaseModel):
    """CRM communications for kids clothing retail"""
    
    _name = 'crm.communication'
    _description = 'CRM Communication'
    _table = 'crm_communication'
    _order = 'date desc, id desc'
    
    # Basic Information
    name = CharField(
        string='Subject',
        size=200,
        required=True,
        help='Subject of the communication'
    )
    
    # Communication Details
    communication_type = SelectionField(
        string='Communication Type',
        selection=[
            ('email', 'Email'),
            ('phone', 'Phone'),
            ('sms', 'SMS'),
            ('whatsapp', 'WhatsApp'),
            ('letter', 'Letter'),
            ('meeting', 'Meeting'),
            ('other', 'Other')
        ],
        required=True,
        help='Type of communication'
    )
    
    direction = SelectionField(
        string='Direction',
        selection=[
            ('inbound', 'Inbound'),
            ('outbound', 'Outbound')
        ],
        required=True,
        help='Direction of communication'
    )
    
    # Communication Content
    body = TextField(
        string='Message',
        help='Content of the communication'
    )
    
    # Communication Relations
    lead_id = Many2OneField(
        'crm.lead',
        string='Lead',
        help='Lead related to this communication'
    )
    
    opportunity_id = Many2OneField(
        'crm.opportunity',
        string='Opportunity',
        help='Opportunity related to this communication'
    )
    
    partner_id = Many2OneField(
        'contact.customer',
        string='Customer',
        help='Customer related to this communication'
    )
    
    # Communication Assignment
    user_id = Many2OneField(
        'res.users',
        string='Author',
        required=True,
        help='User who created this communication'
    )
    
    # Communication Details
    email_from = CharField(
        string='From Email',
        size=100,
        help='Sender email address'
    )
    
    email_to = CharField(
        string='To Email',
        size=100,
        help='Recipient email address'
    )
    
    phone_number = CharField(
        string='Phone Number',
        size=20,
        help='Phone number used for communication'
    )
    
    # Communication Status
    state = SelectionField(
        string='Status',
        selection=[
            ('draft', 'Draft'),
            ('sent', 'Sent'),
            ('delivered', 'Delivered'),
            ('read', 'Read'),
            ('replied', 'Replied'),
            ('failed', 'Failed')
        ],
        default='draft',
        help='Status of the communication'
    )
    
    # Communication Priority
    priority = SelectionField(
        string='Priority',
        selection=[
            ('0', 'Low'),
            ('1', 'Normal'),
            ('2', 'High'),
            ('3', 'Very High')
        ],
        default='1',
        help='Priority of the communication'
    )
    
    # Communication Dates
    date = DateTimeField(
        string='Date',
        default=datetime.now,
        required=True,
        help='Date of the communication'
    )
    
    date_sent = DateTimeField(
        string='Sent Date',
        help='Date when communication was sent'
    )
    
    date_delivered = DateTimeField(
        string='Delivered Date',
        help='Date when communication was delivered'
    )
    
    date_read = DateTimeField(
        string='Read Date',
        help='Date when communication was read'
    )
    
    # Communication Results
    result = TextField(
        string='Result',
        help='Result of the communication'
    )
    
    outcome = SelectionField(
        string='Outcome',
        selection=[
            ('positive', 'Positive'),
            ('neutral', 'Neutral'),
            ('negative', 'Negative'),
            ('pending', 'Pending')
        ],
        help='Outcome of the communication'
    )
    
    # Communication Follow-up
    follow_up_required = BooleanField(
        string='Follow-up Required',
        default=False,
        help='Whether follow-up is required'
    )
    
    follow_up_date = DateTimeField(
        string='Follow-up Date',
        help='Date for follow-up communication'
    )
    
    follow_up_notes = TextField(
        string='Follow-up Notes',
        help='Notes for follow-up communication'
    )
    
    # Communication Attachments
    attachment_ids = One2ManyField(
        string='Attachments',
        comodel_name='crm.attachment',
        inverse_name='communication_id',
        help='Attachments for this communication'
    )
    
    # Communication Tags
    tag_ids = Many2ManyField(
        'crm.tag',
        string='Tags',
        help='Tags for this communication'
    )
    
    # Communication Notes
    note = TextField(
        string='Notes',
        help='Internal notes about the communication'
    )
    
    # Communication Status
    is_active = BooleanField(
        string='Active',
        default=True,
        help='Whether this communication is active'
    )
    
    # Timestamps
    create_date = DateTimeField(
        string='Created On',
        auto_now_add=True
    )
    
    write_date = DateTimeField(
        string='Updated On',
        auto_now=True
    )
    
    def create(self, vals):
        """Override create to set defaults"""
        if 'user_id' not in vals:
            vals['user_id'] = self.env.user.id
        
        return super().create(vals)
    
    def write(self, vals):
        """Override write to update status"""
        result = super().write(vals)
        
        # Update status based on state changes
        if 'state' in vals:
            self._update_status_dates()
        
        return result
    
    def _update_status_dates(self):
        """Update status dates based on state"""
        for communication in self:
            now = datetime.now()
            
            if communication.state == 'sent' and not communication.date_sent:
                communication.date_sent = now
            elif communication.state == 'delivered' and not communication.date_delivered:
                communication.date_delivered = now
            elif communication.state == 'read' and not communication.date_read:
                communication.date_read = now
    
    def action_send(self):
        """Send the communication"""
        for communication in self:
            if communication.state != 'draft':
                raise ValidationError("Only draft communications can be sent")
            
            # Update status
            communication.state = 'sent'
            communication.date_sent = datetime.now()
            
            # Send based on type
            if communication.communication_type == 'email':
                self._send_email(communication)
            elif communication.communication_type == 'sms':
                self._send_sms(communication)
            elif communication.communication_type == 'whatsapp':
                self._send_whatsapp(communication)
    
    def _send_email(self, communication):
        """Send email communication"""
        # This would integrate with email system
        logger.info(f"Email sent: {communication.name}")
    
    def _send_sms(self, communication):
        """Send SMS communication"""
        # This would integrate with SMS system
        logger.info(f"SMS sent: {communication.name}")
    
    def _send_whatsapp(self, communication):
        """Send WhatsApp communication"""
        # This would integrate with WhatsApp API
        logger.info(f"WhatsApp sent: {communication.name}")
    
    def action_mark_delivered(self):
        """Mark communication as delivered"""
        for communication in self:
            if communication.state not in ['sent', 'delivered']:
                raise ValidationError("Only sent communications can be marked as delivered")
            
            communication.state = 'delivered'
            communication.date_delivered = datetime.now()
    
    def action_mark_read(self):
        """Mark communication as read"""
        for communication in self:
            if communication.state not in ['sent', 'delivered', 'read']:
                raise ValidationError("Only sent or delivered communications can be marked as read")
            
            communication.state = 'read'
            communication.date_read = datetime.now()
    
    def action_mark_replied(self):
        """Mark communication as replied"""
        for communication in self:
            if communication.state != 'read':
                raise ValidationError("Only read communications can be marked as replied")
            
            communication.state = 'replied'
    
    def action_mark_failed(self):
        """Mark communication as failed"""
        for communication in self:
            if communication.state not in ['draft', 'sent']:
                raise ValidationError("Only draft or sent communications can be marked as failed")
            
            communication.state = 'failed'
    
    def action_create_follow_up(self):
        """Create follow-up communication"""
        for communication in self:
            if not communication.follow_up_required:
                raise ValidationError("Follow-up is not required for this communication")
            
            # Create follow-up communication
            follow_up_vals = {
                'name': f"Follow-up: {communication.name}",
                'communication_type': communication.communication_type,
                'direction': 'outbound',
                'body': communication.follow_up_notes,
                'date': communication.follow_up_date,
                'user_id': communication.user_id.id,
                'lead_id': communication.lead_id.id,
                'opportunity_id': communication.opportunity_id.id,
                'partner_id': communication.partner_id.id,
                'priority': communication.priority,
                'email_from': communication.email_from,
                'email_to': communication.email_to,
                'phone_number': communication.phone_number
            }
            
            follow_up = self.env['crm.communication'].create(follow_up_vals)
            return follow_up
    
    def action_view_related(self):
        """View related record"""
        for communication in self:
            if communication.lead_id:
                return communication.lead_id.action_view_communications()
            elif communication.opportunity_id:
                return communication.opportunity_id.action_view_communications()
            elif communication.partner_id:
                return {
                    'type': 'ocean.actions.act_window',
                    'name': f'Customer - {communication.partner_id.name}',
                    'res_model': 'contact.customer',
                    'res_id': communication.partner_id.id,
                    'view_mode': 'form',
                    'target': 'current'
                }
    
    def get_communication_history(self, partner_id):
        """Get communication history for a partner"""
        return self.search([
            ('partner_id', '=', partner_id)
        ], order='date desc')
    
    def get_recent_communications(self, days=7):
        """Get recent communications"""
        date_limit = datetime.now() - timedelta(days=days)
        return self.search([
            ('date', '>=', date_limit)
        ], order='date desc')