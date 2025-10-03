#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - CRM Campaign Model
======================================

Campaign management for kids clothing retail.
"""

import logging
from datetime import datetime, timedelta
from core_framework.orm import BaseModel, CharField, TextField, BooleanField, IntegerField, DateTimeField, Many2OneField, SelectionField, FloatField, One2ManyField, Many2ManyField
from core_framework.exceptions import ValidationError

logger = logging.getLogger(__name__)

class CrmCampaign(BaseModel):
    """CRM campaigns for kids clothing retail"""
    
    _name = 'crm.campaign'
    _description = 'CRM Campaign'
    _table = 'crm_campaign'
    _order = 'date_start desc, id desc'
    
    # Basic Information
    name = CharField(
        string='Campaign Name',
        size=100,
        required=True,
        help='Name of the campaign'
    )
    
    description = TextField(
        string='Description',
        help='Description of the campaign'
    )
    
    # Campaign Details
    campaign_type = SelectionField(
        string='Campaign Type',
        selection=[
            ('email', 'Email Campaign'),
            ('sms', 'SMS Campaign'),
            ('whatsapp', 'WhatsApp Campaign'),
            ('social_media', 'Social Media Campaign'),
            ('print', 'Print Campaign'),
            ('digital', 'Digital Campaign'),
            ('event', 'Event Campaign'),
            ('loyalty', 'Loyalty Campaign'),
            ('seasonal', 'Seasonal Campaign'),
            ('other', 'Other')
        ],
        required=True,
        help='Type of campaign'
    )
    
    # Campaign Status
    state = SelectionField(
        string='Status',
        selection=[
            ('draft', 'Draft'),
            ('running', 'Running'),
            ('paused', 'Paused'),
            ('completed', 'Completed'),
            ('cancelled', 'Cancelled')
        ],
        default='draft',
        help='Current status of the campaign'
    )
    
    # Campaign Dates
    date_start = DateTimeField(
        string='Start Date',
        required=True,
        help='Start date of the campaign'
    )
    
    date_end = DateTimeField(
        string='End Date',
        help='End date of the campaign'
    )
    
    # Campaign Budget
    budget = FloatField(
        string='Budget',
        digits=(12, 2),
        default=0.0,
        help='Budget for the campaign'
    )
    
    actual_cost = FloatField(
        string='Actual Cost',
        digits=(12, 2),
        default=0.0,
        help='Actual cost of the campaign'
    )
    
    # Campaign Assignment
    user_id = Many2OneField(
        'res.users',
        string='Campaign Manager',
        required=True,
        help='User managing this campaign'
    )
    
    team_id = Many2OneField(
        'sales.team',
        string='Sales Team',
        help='Sales team for this campaign'
    )
    
    # Campaign Target
    target_audience = SelectionField(
        string='Target Audience',
        selection=[
            ('all', 'All Customers'),
            ('new', 'New Customers'),
            ('existing', 'Existing Customers'),
            ('loyal', 'Loyal Customers'),
            ('age_group', 'Specific Age Group'),
            ('gender', 'Specific Gender'),
            ('seasonal', 'Seasonal Customers'),
            ('custom', 'Custom Segment')
        ],
        default='all',
        help='Target audience for the campaign'
    )
    
    # Kids Clothing Specific Targeting
    age_group_target = SelectionField(
        string='Age Group Target',
        selection=[
            ('newborn', 'Newborn (0-6 months)'),
            ('infant', 'Infant (6-12 months)'),
            ('toddler', 'Toddler (1-3 years)'),
            ('preschool', 'Preschool (3-5 years)'),
            ('school', 'School (5-12 years)'),
            ('teen', 'Teen (12+ years)'),
            ('all', 'All Ages')
        ],
        help='Target age group for the campaign'
    )
    
    gender_target = SelectionField(
        string='Gender Target',
        selection=[
            ('boys', 'Boys'),
            ('girls', 'Girls'),
            ('unisex', 'Unisex'),
            ('all', 'All Genders')
        ],
        help='Target gender for the campaign'
    )
    
    seasonal_target = SelectionField(
        string='Seasonal Target',
        selection=[
            ('summer', 'Summer'),
            ('winter', 'Winter'),
            ('monsoon', 'Monsoon'),
            ('all_season', 'All Season'),
            ('festive', 'Festive'),
            ('party', 'Party Wear')
        ],
        help='Target season for the campaign'
    )
    
    # Campaign Content
    subject = CharField(
        string='Subject',
        size=200,
        help='Subject line for the campaign'
    )
    
    body = TextField(
        string='Message',
        help='Message content for the campaign'
    )
    
    # Campaign Metrics
    total_sent = IntegerField(
        string='Total Sent',
        default=0,
        help='Total number of messages sent'
    )
    
    total_delivered = IntegerField(
        string='Total Delivered',
        default=0,
        help='Total number of messages delivered'
    )
    
    total_opened = IntegerField(
        string='Total Opened',
        default=0,
        help='Total number of messages opened'
    )
    
    total_clicked = IntegerField(
        string='Total Clicked',
        default=0,
        help='Total number of clicks'
    )
    
    total_replied = IntegerField(
        string='Total Replied',
        default=0,
        help='Total number of replies'
    )
    
    total_converted = IntegerField(
        string='Total Converted',
        default=0,
        help='Total number of conversions'
    )
    
    # Campaign Performance
    delivery_rate = FloatField(
        string='Delivery Rate %',
        digits=(5, 2),
        compute='_compute_delivery_rate',
        help='Delivery rate percentage'
    )
    
    open_rate = FloatField(
        string='Open Rate %',
        digits=(5, 2),
        compute='_compute_open_rate',
        help='Open rate percentage'
    )
    
    click_rate = FloatField(
        string='Click Rate %',
        digits=(5, 2),
        compute='_compute_click_rate',
        help='Click rate percentage'
    )
    
    reply_rate = FloatField(
        string='Reply Rate %',
        digits=(5, 2),
        compute='_compute_reply_rate',
        help='Reply rate percentage'
    )
    
    conversion_rate = FloatField(
        string='Conversion Rate %',
        digits=(5, 2),
        compute='_compute_conversion_rate',
        help='Conversion rate percentage'
    )
    
    # Campaign Relations
    lead_ids = One2ManyField(
        string='Leads',
        comodel_name='crm.lead',
        inverse_name='campaign_id',
        help='Leads generated from this campaign'
    )
    
    opportunity_ids = One2ManyField(
        string='Opportunities',
        comodel_name='crm.opportunity',
        inverse_name='campaign_id',
        help='Opportunities generated from this campaign'
    )
    
    # Campaign Notes
    note = TextField(
        string='Notes',
        help='Internal notes about the campaign'
    )
    
    # Campaign Status
    is_active = BooleanField(
        string='Active',
        default=True,
        help='Whether this campaign is active'
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
        """Override write to update metrics"""
        result = super().write(vals)
        
        # Update performance metrics
        if any(field in vals for field in ['total_sent', 'total_delivered', 'total_opened', 'total_clicked', 'total_replied', 'total_converted']):
            self._compute_performance_metrics()
        
        return result
    
    def _compute_delivery_rate(self):
        """Compute delivery rate"""
        for campaign in self:
            if campaign.total_sent > 0:
                campaign.delivery_rate = (campaign.total_delivered / campaign.total_sent) * 100
            else:
                campaign.delivery_rate = 0.0
    
    def _compute_open_rate(self):
        """Compute open rate"""
        for campaign in self:
            if campaign.total_delivered > 0:
                campaign.open_rate = (campaign.total_opened / campaign.total_delivered) * 100
            else:
                campaign.open_rate = 0.0
    
    def _compute_click_rate(self):
        """Compute click rate"""
        for campaign in self:
            if campaign.total_delivered > 0:
                campaign.click_rate = (campaign.total_clicked / campaign.total_delivered) * 100
            else:
                campaign.click_rate = 0.0
    
    def _compute_reply_rate(self):
        """Compute reply rate"""
        for campaign in self:
            if campaign.total_delivered > 0:
                campaign.reply_rate = (campaign.total_replied / campaign.total_delivered) * 100
            else:
                campaign.reply_rate = 0.0
    
    def _compute_conversion_rate(self):
        """Compute conversion rate"""
        for campaign in self:
            if campaign.total_delivered > 0:
                campaign.conversion_rate = (campaign.total_converted / campaign.total_delivered) * 100
            else:
                campaign.conversion_rate = 0.0
    
    def _compute_performance_metrics(self):
        """Compute all performance metrics"""
        self._compute_delivery_rate()
        self._compute_open_rate()
        self._compute_click_rate()
        self._compute_reply_rate()
        self._compute_conversion_rate()
    
    def action_start(self):
        """Start the campaign"""
        for campaign in self:
            if campaign.state != 'draft':
                raise ValidationError("Only draft campaigns can be started")
            
            campaign.state = 'running'
            campaign.date_start = datetime.now()
    
    def action_pause(self):
        """Pause the campaign"""
        for campaign in self:
            if campaign.state != 'running':
                raise ValidationError("Only running campaigns can be paused")
            
            campaign.state = 'paused'
    
    def action_resume(self):
        """Resume the campaign"""
        for campaign in self:
            if campaign.state != 'paused':
                raise ValidationError("Only paused campaigns can be resumed")
            
            campaign.state = 'running'
    
    def action_complete(self):
        """Complete the campaign"""
        for campaign in self:
            if campaign.state not in ['running', 'paused']:
                raise ValidationError("Only running or paused campaigns can be completed")
            
            campaign.state = 'completed'
            campaign.date_end = datetime.now()
    
    def action_cancel(self):
        """Cancel the campaign"""
        for campaign in self:
            if campaign.state in ['completed', 'cancelled']:
                raise ValidationError("Cannot cancel completed or cancelled campaigns")
            
            campaign.state = 'cancelled'
    
    def action_send_campaign(self):
        """Send the campaign"""
        for campaign in self:
            if campaign.state != 'running':
                raise ValidationError("Only running campaigns can be sent")
            
            # This would integrate with the actual sending system
            # For now, just update the metrics
            campaign.total_sent += 1
            campaign.total_delivered += 1
    
    def action_view_leads(self):
        """View leads generated from this campaign"""
        return {
            'type': 'ocean.actions.act_window',
            'name': f'Leads - {self.name}',
            'res_model': 'crm.lead',
            'view_mode': 'tree,form',
            'domain': [('campaign_id', '=', self.id)],
            'context': {'default_campaign_id': self.id}
        }
    
    def action_view_opportunities(self):
        """View opportunities generated from this campaign"""
        return {
            'type': 'ocean.actions.act_window',
            'name': f'Opportunities - {self.name}',
            'res_model': 'crm.opportunity',
            'view_mode': 'tree,form',
            'domain': [('campaign_id', '=', self.id)],
            'context': {'default_campaign_id': self.id}
        }
    
    def action_analyze_performance(self):
        """Analyze campaign performance"""
        return {
            'type': 'ocean.actions.act_window',
            'name': f'Campaign Analytics - {self.name}',
            'res_model': 'crm.analytics',
            'view_mode': 'form',
            'domain': [('campaign_id', '=', self.id)],
            'context': {'default_campaign_id': self.id}
        }