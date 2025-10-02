# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Contacts - Contact Communication Management
===========================================================

Standalone version of the contact communication management model.
"""

from core_framework.orm import BaseModel, CharField, TextField, BooleanField, IntegerField, DateTimeField, Many2OneField, SelectionField, DateField
from core_framework.orm import Field
from typing import Dict, Any, Optional
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class ContactCommunication(BaseModel):
    """Contact communication model for Kids Clothing ERP"""
    
    _name = 'contact.communication'
    _description = 'Contact Communication'
    _table = 'contact_communication'
    
    # Basic communication information
    contact_id = IntegerField(
        string='Contact ID',
        required=True,
        help='Contact this communication belongs to'
    )
    
    communication_type = SelectionField(
        string='Communication Type',
        selection=[
            ('email', 'Email'),
            ('phone', 'Phone'),
            ('sms', 'SMS'),
            ('whatsapp', 'WhatsApp'),
            ('letter', 'Letter'),
            ('meeting', 'Meeting'),
            ('other', 'Other'),
        ],
        required=True,
        help='Type of communication'
    )
    
    subject = CharField(
        string='Subject',
        size=255,
        help='Subject of the communication'
    )
    
    message = TextField(
        string='Message',
        help='Message content'
    )
    
    # Communication details
    date_time = DateTimeField(
        string='Date & Time',
        default=datetime.now,
        help='Date and time of the communication'
    )
    
    direction = SelectionField(
        string='Direction',
        selection=[
            ('incoming', 'Incoming'),
            ('outgoing', 'Outgoing'),
        ],
        required=True,
        help='Direction of communication'
    )
    
    # Contact information
    contact_number = CharField(
        string='Contact Number',
        size=20,
        help='Phone number used for communication'
    )
    
    email_address = CharField(
        string='Email Address',
        size=255,
        help='Email address used for communication'
    )
    
    # Communication status
    status = SelectionField(
        string='Status',
        selection=[
            ('sent', 'Sent'),
            ('delivered', 'Delivered'),
            ('read', 'Read'),
            ('replied', 'Replied'),
            ('failed', 'Failed'),
            ('pending', 'Pending'),
        ],
        default='sent',
        help='Status of the communication'
    )
    
    # User information
    user_id = IntegerField(
        string='User ID',
        help='User who handled this communication'
    )
    
    # Follow-up
    requires_follow_up = BooleanField(
        string='Requires Follow-up',
        default=False,
        help='Whether this communication requires follow-up'
    )
    
    follow_up_date = DateField(
        string='Follow-up Date',
        help='Date for follow-up'
    )
    
    follow_up_notes = TextField(
        string='Follow-up Notes',
        help='Notes for follow-up'
    )
    
    # Company relationship
    company_id = IntegerField(
        string='Company ID',
        default=1,
        help='Company this communication belongs to'
    )
    
    def create(self, vals: Dict[str, Any]):
        """Override create to set default values"""
        # Set date and time if not provided
        if 'date_time' not in vals:
            vals['date_time'] = datetime.now()
        
        return super().create(vals)
    
    def write(self, vals: Dict[str, Any]):
        """Override write to handle communication updates"""
        result = super().write(vals)
        
        # Log communication updates
        for communication in self:
            if vals:
                logger.info(f"Communication for contact {communication.contact_id} updated: {', '.join(vals.keys())}")
        
        return result
    
    def get_communication_info(self):
        """Get communication information"""
        return {
            'contact_id': self.contact_id,
            'communication_type': self.communication_type,
            'subject': self.subject,
            'message': self.message,
            'date_time': self.date_time,
            'direction': self.direction,
            'contact_number': self.contact_number,
            'email_address': self.email_address,
            'status': self.status,
            'user_id': self.user_id,
            'requires_follow_up': self.requires_follow_up,
            'follow_up_date': self.follow_up_date,
            'follow_up_notes': self.follow_up_notes,
        }
    
    @classmethod
    def get_communications_by_contact(cls, contact_id: int):
        """Get communications by contact"""
        return cls.search([
            ('contact_id', '=', contact_id),
        ], order='date_time desc')
    
    @classmethod
    def get_communications_by_type(cls, communication_type: str):
        """Get communications by type"""
        return cls.search([
            ('communication_type', '=', communication_type),
        ], order='date_time desc')
    
    @classmethod
    def get_communications_by_direction(cls, direction: str):
        """Get communications by direction"""
        return cls.search([
            ('direction', '=', direction),
        ], order='date_time desc')
    
    @classmethod
    def get_communications_by_status(cls, status: str):
        """Get communications by status"""
        return cls.search([
            ('status', '=', status),
        ], order='date_time desc')
    
    @classmethod
    def get_communications_by_user(cls, user_id: int):
        """Get communications by user"""
        return cls.search([
            ('user_id', '=', user_id),
        ], order='date_time desc')
    
    @classmethod
    def get_follow_up_communications(cls, date_from: str = None, date_to: str = None):
        """Get communications requiring follow-up"""
        domain = [('requires_follow_up', '=', True)]
        
        if date_from:
            domain.append(('follow_up_date', '>=', date_from))
        if date_to:
            domain.append(('follow_up_date', '<=', date_to))
        
        return cls.search(domain, order='follow_up_date asc')
    
    @classmethod
    def get_communication_analytics(cls, contact_id: int):
        """Get communication analytics for contact"""
        communications = cls.search([('contact_id', '=', contact_id)])
        
        if not communications:
            return {
                'total_communications': 0,
                'by_type': {},
                'by_direction': {},
                'by_status': {},
                'follow_up_communications': 0,
            }
        
        # Count by type
        by_type = {}
        for comm in communications:
            comm_type = comm.communication_type
            by_type[comm_type] = by_type.get(comm_type, 0) + 1
        
        # Count by direction
        by_direction = {}
        for comm in communications:
            direction = comm.direction
            by_direction[direction] = by_direction.get(direction, 0) + 1
        
        # Count by status
        by_status = {}
        for comm in communications:
            status = comm.status
            by_status[status] = by_status.get(status, 0) + 1
        
        return {
            'total_communications': len(communications),
            'by_type': by_type,
            'by_direction': by_direction,
            'by_status': by_status,
            'follow_up_communications': len([c for c in communications if c.requires_follow_up]),
        }
    
    @classmethod
    def get_communication_analytics_summary(cls):
        """Get communication analytics summary"""
        # In standalone version, we'll return mock data
        return {
            'total_communications': 0,
            'by_type': {},
            'by_direction': {},
            'by_status': {},
            'follow_up_communications': 0,
        }
    
    def _check_follow_up_date(self):
        """Validate follow-up date"""
        if self.follow_up_date and self.date_time:
            follow_up = datetime.strptime(self.follow_up_date, '%Y-%m-%d').date()
            comm_date = datetime.strptime(self.date_time, '%Y-%m-%d %H:%M:%S').date()
            
            if follow_up < comm_date:
                raise ValueError('Follow-up date cannot be before communication date')
    
    def action_mark_sent(self):
        """Mark as sent"""
        self.status = 'sent'
        return True
    
    def action_mark_delivered(self):
        """Mark as delivered"""
        self.status = 'delivered'
        return True
    
    def action_mark_read(self):
        """Mark as read"""
        self.status = 'read'
        return True
    
    def action_mark_replied(self):
        """Mark as replied"""
        self.status = 'replied'
        return True
    
    def action_mark_failed(self):
        """Mark as failed"""
        self.status = 'failed'
        return True
    
    def action_set_follow_up(self, follow_up_date: str, notes: str = None):
        """Set follow-up"""
        self.requires_follow_up = True
        self.follow_up_date = follow_up_date
        if notes:
            self.follow_up_notes = notes
        return True
    
    def action_clear_follow_up(self):
        """Clear follow-up"""
        self.requires_follow_up = False
        self.follow_up_date = None
        self.follow_up_notes = None
        return True
    
    def action_duplicate(self):
        """Duplicate communication"""
        self.ensure_one()
        
        new_communication = self.copy({
            'date_time': datetime.now(),
        })
        
        return new_communication
    
    def action_export_communication(self):
        """Export communication data"""
        self.ensure_one()
        
        return {
            'contact_id': self.contact_id,
            'communication_type': self.communication_type,
            'subject': self.subject,
            'message': self.message,
            'date_time': self.date_time,
            'direction': self.direction,
            'contact_number': self.contact_number,
            'email_address': self.email_address,
            'status': self.status,
            'user_id': self.user_id,
            'requires_follow_up': self.requires_follow_up,
            'follow_up_date': self.follow_up_date,
            'follow_up_notes': self.follow_up_notes,
        }
    
    def action_import_communication(self, communication_data: Dict[str, Any]):
        """Import communication data"""
        self.ensure_one()
        
        self.write(communication_data)
        return True