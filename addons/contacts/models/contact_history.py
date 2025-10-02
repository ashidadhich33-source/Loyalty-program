# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Contacts - Contact History Management
=====================================================

Standalone version of the contact history management model.
"""

from core_framework.orm import BaseModel, CharField, TextField, BooleanField, IntegerField, DateTimeField, Many2OneField, SelectionField, DateField
from core_framework.orm import Field
from typing import Dict, Any, Optional
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class ContactHistory(BaseModel):
    """Contact history model for Kids Clothing ERP"""
    
    _name = 'contact.history'
    _description = 'Contact History'
    _table = 'contact_history'
    
    # Basic history information
    contact_id = IntegerField(
        string='Contact ID',
        required=True,
        help='Contact this history belongs to'
    )
    
    history_type = SelectionField(
        string='History Type',
        selection=[
            ('note', 'Note'),
            ('call', 'Call'),
            ('email', 'Email'),
            ('meeting', 'Meeting'),
            ('order', 'Order'),
            ('payment', 'Payment'),
            ('complaint', 'Complaint'),
            ('feedback', 'Feedback'),
            ('other', 'Other'),
        ],
        required=True,
        help='Type of history entry'
    )
    
    subject = CharField(
        string='Subject',
        size=255,
        help='Subject of the history entry'
    )
    
    description = TextField(
        string='Description',
        help='Description of the history entry'
    )
    
    # History details
    date_time = DateTimeField(
        string='Date & Time',
        default=datetime.now,
        help='Date and time of the history entry'
    )
    
    duration = IntegerField(
        string='Duration (minutes)',
        default=0,
        help='Duration in minutes'
    )
    
    # User information
    user_id = IntegerField(
        string='User ID',
        help='User who created this history entry'
    )
    
    # History status
    is_important = BooleanField(
        string='Important',
        default=False,
        help='Whether this history entry is important'
    )
    
    is_private = BooleanField(
        string='Private',
        default=False,
        help='Whether this history entry is private'
    )
    
    # Follow-up
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
        help='Company this history belongs to'
    )
    
    def create(self, vals: Dict[str, Any]):
        """Override create to set default values"""
        # Set date and time if not provided
        if 'date_time' not in vals:
            vals['date_time'] = datetime.now()
        
        return super().create(vals)
    
    def write(self, vals: Dict[str, Any]):
        """Override write to handle history updates"""
        result = super().write(vals)
        
        # Log history updates
        for history in self:
            if vals:
                logger.info(f"History entry for contact {history.contact_id} updated: {', '.join(vals.keys())}")
        
        return result
    
    def get_history_info(self):
        """Get history information"""
        return {
            'contact_id': self.contact_id,
            'history_type': self.history_type,
            'subject': self.subject,
            'description': self.description,
            'date_time': self.date_time,
            'duration': self.duration,
            'user_id': self.user_id,
            'is_important': self.is_important,
            'is_private': self.is_private,
            'follow_up_date': self.follow_up_date,
            'follow_up_notes': self.follow_up_notes,
        }
    
    @classmethod
    def get_history_by_contact(cls, contact_id: int):
        """Get history by contact"""
        return cls.search([
            ('contact_id', '=', contact_id),
        ], order='date_time desc')
    
    @classmethod
    def get_history_by_type(cls, history_type: str):
        """Get history by type"""
        return cls.search([
            ('history_type', '=', history_type),
        ], order='date_time desc')
    
    @classmethod
    def get_history_by_user(cls, user_id: int):
        """Get history by user"""
        return cls.search([
            ('user_id', '=', user_id),
        ], order='date_time desc')
    
    @classmethod
    def get_important_history(cls, contact_id: int):
        """Get important history for contact"""
        return cls.search([
            ('contact_id', '=', contact_id),
            ('is_important', '=', True),
        ], order='date_time desc')
    
    @classmethod
    def get_follow_up_history(cls, date_from: str = None, date_to: str = None):
        """Get history with follow-up dates"""
        domain = [('follow_up_date', '!=', None)]
        
        if date_from:
            domain.append(('follow_up_date', '>=', date_from))
        if date_to:
            domain.append(('follow_up_date', '<=', date_to))
        
        return cls.search(domain, order='follow_up_date asc')
    
    @classmethod
    def get_history_analytics(cls, contact_id: int):
        """Get history analytics for contact"""
        history = cls.search([('contact_id', '=', contact_id)])
        
        if not history:
            return {
                'total_entries': 0,
                'by_type': {},
                'important_entries': 0,
                'private_entries': 0,
                'follow_up_entries': 0,
            }
        
        # Count by type
        by_type = {}
        for entry in history:
            entry_type = entry.history_type
            by_type[entry_type] = by_type.get(entry_type, 0) + 1
        
        return {
            'total_entries': len(history),
            'by_type': by_type,
            'important_entries': len([h for h in history if h.is_important]),
            'private_entries': len([h for h in history if h.is_private]),
            'follow_up_entries': len([h for h in history if h.follow_up_date]),
        }
    
    @classmethod
    def get_history_analytics_summary(cls):
        """Get history analytics summary"""
        # In standalone version, we'll return mock data
        return {
            'total_history_entries': 0,
            'by_type': {},
            'important_entries': 0,
            'private_entries': 0,
            'follow_up_entries': 0,
        }
    
    def _check_follow_up_date(self):
        """Validate follow-up date"""
        if self.follow_up_date and self.date_time:
            follow_up = datetime.strptime(self.follow_up_date, '%Y-%m-%d').date()
            history_date = datetime.strptime(self.date_time, '%Y-%m-%d %H:%M:%S').date()
            
            if follow_up < history_date:
                raise ValueError('Follow-up date cannot be before history date')
    
    def action_mark_important(self):
        """Mark as important"""
        self.is_important = True
        return True
    
    def action_unmark_important(self):
        """Unmark as important"""
        self.is_important = False
        return True
    
    def action_mark_private(self):
        """Mark as private"""
        self.is_private = True
        return True
    
    def action_unmark_private(self):
        """Unmark as private"""
        self.is_private = False
        return True
    
    def action_set_follow_up(self, follow_up_date: str, notes: str = None):
        """Set follow-up"""
        self.follow_up_date = follow_up_date
        if notes:
            self.follow_up_notes = notes
        return True
    
    def action_clear_follow_up(self):
        """Clear follow-up"""
        self.follow_up_date = None
        self.follow_up_notes = None
        return True
    
    def action_duplicate(self):
        """Duplicate history entry"""
        self.ensure_one()
        
        new_history = self.copy({
            'date_time': datetime.now(),
        })
        
        return new_history
    
    def action_export_history(self):
        """Export history data"""
        self.ensure_one()
        
        return {
            'contact_id': self.contact_id,
            'history_type': self.history_type,
            'subject': self.subject,
            'description': self.description,
            'date_time': self.date_time,
            'duration': self.duration,
            'user_id': self.user_id,
            'is_important': self.is_important,
            'is_private': self.is_private,
            'follow_up_date': self.follow_up_date,
            'follow_up_notes': self.follow_up_notes,
        }
    
    def action_import_history(self, history_data: Dict[str, Any]):
        """Import history data"""
        self.ensure_one()
        
        self.write(history_data)
        return True