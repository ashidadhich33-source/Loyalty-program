#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - CRM Activity Model
=====================================

Activity management for kids clothing retail.
"""

import logging
from datetime import datetime, timedelta
from core_framework.orm import BaseModel, CharField, TextField, BooleanField, IntegerField, DateTimeField, Many2OneField, SelectionField, FloatField, One2ManyField, Many2ManyField
from core_framework.exceptions import ValidationError

logger = logging.getLogger(__name__)

class CrmActivity(BaseModel):
    """CRM activities for kids clothing retail"""
    
    _name = 'crm.activity'
    _description = 'CRM Activity'
    _table = 'crm_activity'
    _order = 'date_deadline asc, id desc'
    
    # Basic Information
    name = CharField(
        string='Activity Name',
        size=100,
        required=True,
        help='Name of the activity'
    )
    
    # Activity Details
    activity_type = SelectionField(
        string='Activity Type',
        selection=[
            ('call', 'Call'),
            ('email', 'Email'),
            ('meeting', 'Meeting'),
            ('demo', 'Demo'),
            ('presentation', 'Presentation'),
            ('follow_up', 'Follow Up'),
            ('visit', 'Visit'),
            ('other', 'Other')
        ],
        required=True,
        help='Type of activity'
    )
    
    description = TextField(
        string='Description',
        help='Description of the activity'
    )
    
    # Activity Scheduling
    date_deadline = DateTimeField(
        string='Deadline',
        required=True,
        help='Deadline for this activity'
    )
    
    date_start = DateTimeField(
        string='Start Date',
        help='Start date of the activity'
    )
    
    date_end = DateTimeField(
        string='End Date',
        help='End date of the activity'
    )
    
    duration = FloatField(
        string='Duration (hours)',
        digits=(5, 2),
        default=1.0,
        help='Duration of the activity in hours'
    )
    
    # Activity Status
    state = SelectionField(
        string='Status',
        selection=[
            ('planned', 'Planned'),
            ('in_progress', 'In Progress'),
            ('completed', 'Completed'),
            ('cancelled', 'Cancelled')
        ],
        default='planned',
        help='Current status of the activity'
    )
    
    # Activity Assignment
    user_id = Many2OneField(
        'res.users',
        string='Assigned To',
        required=True,
        help='User assigned to this activity'
    )
    
    # Activity Relations
    lead_id = Many2OneField(
        'crm.lead',
        string='Lead',
        help='Lead related to this activity'
    )
    
    opportunity_id = Many2OneField(
        'crm.opportunity',
        string='Opportunity',
        help='Opportunity related to this activity'
    )
    
    partner_id = Many2OneField(
        'contact.customer',
        string='Customer',
        help='Customer related to this activity'
    )
    
    # Activity Location
    location = CharField(
        string='Location',
        size=100,
        help='Location of the activity'
    )
    
    # Activity Priority
    priority = SelectionField(
        string='Priority',
        selection=[
            ('0', 'Low'),
            ('1', 'Normal'),
            ('2', 'High'),
            ('3', 'Very High')
        ],
        default='1',
        help='Priority of the activity'
    )
    
    # Activity Results
    result = TextField(
        string='Result',
        help='Result of the activity'
    )
    
    outcome = SelectionField(
        string='Outcome',
        selection=[
            ('positive', 'Positive'),
            ('neutral', 'Neutral'),
            ('negative', 'Negative'),
            ('pending', 'Pending')
        ],
        help='Outcome of the activity'
    )
    
    # Activity Follow-up
    follow_up_required = BooleanField(
        string='Follow-up Required',
        default=False,
        help='Whether follow-up is required'
    )
    
    follow_up_date = DateTimeField(
        string='Follow-up Date',
        help='Date for follow-up activity'
    )
    
    follow_up_notes = TextField(
        string='Follow-up Notes',
        help='Notes for follow-up activity'
    )
    
    # Activity Reminders
    reminder_enabled = BooleanField(
        string='Reminder Enabled',
        default=True,
        help='Whether reminder is enabled'
    )
    
    reminder_time = IntegerField(
        string='Reminder Time (minutes)',
        default=15,
        help='Reminder time in minutes before deadline'
    )
    
    # Activity Notes
    note = TextField(
        string='Notes',
        help='Internal notes about the activity'
    )
    
    # Activity Status
    is_active = BooleanField(
        string='Active',
        default=True,
        help='Whether this activity is active'
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
        
        # Update status based on dates
        if 'date_start' in vals or 'date_end' in vals:
            self._update_status()
        
        return result
    
    def _update_status(self):
        """Update activity status based on dates"""
        for activity in self:
            now = datetime.now()
            
            if activity.date_start and activity.date_start <= now:
                if activity.date_end and activity.date_end <= now:
                    activity.state = 'completed'
                else:
                    activity.state = 'in_progress'
    
    def action_start(self):
        """Start the activity"""
        for activity in self:
            if activity.state != 'planned':
                raise ValidationError("Only planned activities can be started")
            
            activity.state = 'in_progress'
            activity.date_start = datetime.now()
    
    def action_complete(self):
        """Complete the activity"""
        for activity in self:
            if activity.state not in ['planned', 'in_progress']:
                raise ValidationError("Only planned or in-progress activities can be completed")
            
            activity.state = 'completed'
            activity.date_end = datetime.now()
    
    def action_cancel(self):
        """Cancel the activity"""
        for activity in self:
            if activity.state == 'completed':
                raise ValidationError("Cannot cancel completed activities")
            
            activity.state = 'cancelled'
    
    def action_reschedule(self):
        """Reschedule the activity"""
        for activity in self:
            if activity.state == 'completed':
                raise ValidationError("Cannot reschedule completed activities")
            
            activity.state = 'planned'
            activity.date_start = False
            activity.date_end = False
    
    def action_create_follow_up(self):
        """Create follow-up activity"""
        for activity in self:
            if not activity.follow_up_required:
                raise ValidationError("Follow-up is not required for this activity")
            
            # Create follow-up activity
            follow_up_vals = {
                'name': f"Follow-up: {activity.name}",
                'activity_type': 'follow_up',
                'description': activity.follow_up_notes,
                'date_deadline': activity.follow_up_date,
                'user_id': activity.user_id.id,
                'lead_id': activity.lead_id.id,
                'opportunity_id': activity.opportunity_id.id,
                'partner_id': activity.partner_id.id,
                'priority': activity.priority,
                'location': activity.location
            }
            
            follow_up = self.env['crm.activity'].create(follow_up_vals)
            return follow_up
    
    def action_view_related(self):
        """View related record"""
        for activity in self:
            if activity.lead_id:
                return activity.lead_id.action_view_activities()
            elif activity.opportunity_id:
                return activity.opportunity_id.action_view_activities()
            elif activity.partner_id:
                return {
                    'type': 'ocean.actions.act_window',
                    'name': f'Customer - {activity.partner_id.name}',
                    'res_model': 'contact.customer',
                    'res_id': activity.partner_id.id,
                    'view_mode': 'form',
                    'target': 'current'
                }
    
    def action_send_reminder(self):
        """Send reminder for activity"""
        for activity in self:
            if not activity.reminder_enabled:
                return
            
            # This would integrate with notification system
            # For now, just log the reminder
            logger.info(f"Reminder sent for activity: {activity.name}")
    
    def get_overdue_activities(self):
        """Get overdue activities"""
        now = datetime.now()
        return self.search([
            ('date_deadline', '<', now),
            ('state', 'in', ['planned', 'in_progress'])
        ])
    
    def get_today_activities(self):
        """Get today's activities"""
        today = datetime.now().date()
        return self.search([
            ('date_deadline', '>=', today),
            ('date_deadline', '<', today + timedelta(days=1)),
            ('state', 'in', ['planned', 'in_progress'])
        ])
    
    def get_this_week_activities(self):
        """Get this week's activities"""
        today = datetime.now().date()
        week_start = today - timedelta(days=today.weekday())
        week_end = week_start + timedelta(days=6)
        
        return self.search([
            ('date_deadline', '>=', week_start),
            ('date_deadline', '<=', week_end),
            ('state', 'in', ['planned', 'in_progress'])
        ])