#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - CRM Opportunity Model
=========================================

Opportunity management for kids clothing retail.
"""

import logging
from datetime import datetime, timedelta
from core_framework.orm import BaseModel, CharField, TextField, BooleanField, IntegerField, DateTimeField, Many2OneField, SelectionField, FloatField, One2ManyField, Many2ManyField
from core_framework.exceptions import ValidationError

logger = logging.getLogger(__name__)

class CrmOpportunity(BaseModel):
    """CRM opportunities for kids clothing retail"""
    
    _name = 'crm.opportunity'
    _description = 'CRM Opportunity'
    _table = 'crm_opportunity'
    _order = 'create_date desc'
    
    # Basic Information
    name = CharField(
        string='Opportunity Name',
        size=100,
        required=True,
        help='Name of the opportunity'
    )
    
    partner_name = CharField(
        string='Contact Name',
        size=100,
        help='Name of the contact person'
    )
    
    # Contact Information
    email = CharField(
        string='Email',
        size=100,
        help='Email address of the opportunity'
    )
    
    phone = CharField(
        string='Phone',
        size=20,
        help='Phone number of the opportunity'
    )
    
    mobile = CharField(
        string='Mobile',
        size=20,
        help='Mobile number of the opportunity'
    )
    
    # Opportunity Details
    expected_revenue = FloatField(
        string='Expected Revenue',
        digits=(12, 2),
        default=0.0,
        help='Expected revenue from this opportunity'
    )
    
    probability = FloatField(
        string='Probability %',
        digits=(5, 2),
        default=0.0,
        help='Probability of closing this opportunity'
    )
    
    weighted_revenue = FloatField(
        string='Weighted Revenue',
        digits=(12, 2),
        compute='_compute_weighted_revenue',
        help='Weighted revenue based on probability'
    )
    
    # Opportunity Status
    stage_id = Many2OneField(
        'crm.stage',
        string='Stage',
        help='Current stage of the opportunity'
    )
    
    # Kids Clothing Specific Fields
    child_count = IntegerField(
        string='Number of Children',
        default=0,
        help='Number of children in the family'
    )
    
    child_ages = TextField(
        string='Child Ages',
        help='Ages of the children'
    )
    
    age_group_interest = SelectionField(
        string='Age Group Interest',
        selection=[
            ('newborn', 'Newborn (0-6 months)'),
            ('infant', 'Infant (6-12 months)'),
            ('toddler', 'Toddler (1-3 years)'),
            ('preschool', 'Preschool (3-5 years)'),
            ('school', 'School (5-12 years)'),
            ('teen', 'Teen (12+ years)'),
            ('all', 'All Ages')
        ],
        help='Primary age group interest'
    )
    
    gender_preference = SelectionField(
        string='Gender Preference',
        selection=[
            ('boys', 'Boys'),
            ('girls', 'Girls'),
            ('unisex', 'Unisex'),
            ('all', 'All Genders')
        ],
        help='Gender preference for clothing'
    )
    
    seasonal_interest = SelectionField(
        string='Seasonal Interest',
        selection=[
            ('summer', 'Summer'),
            ('winter', 'Winter'),
            ('monsoon', 'Monsoon'),
            ('all_season', 'All Season'),
            ('festive', 'Festive'),
            ('party', 'Party Wear')
        ],
        help='Seasonal preference for clothing'
    )
    
    # Opportunity Source
    source_id = Many2OneField(
        'crm.source',
        string='Source',
        help='Source of the opportunity'
    )
    
    medium_id = Many2OneField(
        'crm.medium',
        string='Medium',
        help='Medium of the opportunity'
    )
    
    campaign_id = Many2OneField(
        'crm.campaign',
        string='Campaign',
        help='Campaign that generated the opportunity'
    )
    
    # Opportunity Assignment
    user_id = Many2OneField(
        'res.users',
        string='Salesperson',
        help='Salesperson assigned to this opportunity'
    )
    
    team_id = Many2OneField(
        'sales.team',
        string='Sales Team',
        help='Sales team assigned to this opportunity'
    )
    
    # Opportunity Activities
    activity_ids = One2ManyField(
        string='Activities',
        comodel_name='crm.activity',
        inverse_name='opportunity_id',
        help='Activities related to this opportunity'
    )
    
    communication_ids = One2ManyField(
        string='Communications',
        comodel_name='crm.communication',
        inverse_name='opportunity_id',
        help='Communications with this opportunity'
    )
    
    # Opportunity Conversion
    partner_id = Many2OneField(
        'contact.customer',
        string='Customer',
        help='Customer for this opportunity'
    )
    
    sale_order_id = Many2OneField(
        'sale.order',
        string='Sales Order',
        help='Sales order created from this opportunity'
    )
    
    # Opportunity Dates
    date_open = DateTimeField(
        string='Open Date',
        default=datetime.now,
        help='Date when opportunity was opened'
    )
    
    date_closed = DateTimeField(
        string='Closed Date',
        help='Date when opportunity was closed'
    )
    
    date_deadline = DateTimeField(
        string='Deadline',
        help='Deadline for closing this opportunity'
    )
    
    # Opportunity Priority
    priority = SelectionField(
        string='Priority',
        selection=[
            ('0', 'Low'),
            ('1', 'Normal'),
            ('2', 'High'),
            ('3', 'Very High')
        ],
        default='1',
        help='Priority of the opportunity'
    )
    
    # Opportunity Notes
    description = TextField(
        string='Description',
        help='Description of the opportunity'
    )
    
    note = TextField(
        string='Notes',
        help='Internal notes about the opportunity'
    )
    
    # Opportunity Status
    is_active = BooleanField(
        string='Active',
        default=True,
        help='Whether this opportunity is active'
    )
    
    is_won = BooleanField(
        string='Won',
        default=False,
        help='Whether this opportunity was won'
    )
    
    is_lost = BooleanField(
        string='Lost',
        default=False,
        help='Whether this opportunity was lost'
    )
    
    lost_reason = CharField(
        string='Lost Reason',
        size=100,
        help='Reason why opportunity was lost'
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
        """Override write to update weighted revenue"""
        result = super().write(vals)
        
        # Update weighted revenue if probability or expected revenue changed
        if any(field in vals for field in ['probability', 'expected_revenue']):
            self._compute_weighted_revenue()
        
        return result
    
    def _compute_weighted_revenue(self):
        """Compute weighted revenue based on probability"""
        for opportunity in self:
            opportunity.weighted_revenue = opportunity.expected_revenue * (opportunity.probability / 100)
    
    def action_convert_to_sale(self):
        """Convert opportunity to sales order"""
        for opportunity in self:
            if opportunity.is_won or opportunity.is_lost:
                raise ValidationError("Cannot convert won or lost opportunities")
            
            # Create sales order
            sale_order_vals = {
                'name': f"SO-{opportunity.name}",
                'partner_id': opportunity.partner_id.id if opportunity.partner_id else False,
                'user_id': opportunity.user_id.id,
                'team_id': opportunity.team_id.id,
                'expected_revenue': opportunity.expected_revenue,
                'age_group': opportunity.age_group_interest,
                'gender_preference': opportunity.gender_preference,
                'season': opportunity.seasonal_interest,
                'note': opportunity.description
            }
            
            sale_order = self.env['sale.order'].create(sale_order_vals)
            opportunity.sale_order_id = sale_order.id
            opportunity.is_won = True
            opportunity.date_closed = datetime.now()
    
    def action_mark_won(self):
        """Mark opportunity as won"""
        for opportunity in self:
            if opportunity.is_lost:
                raise ValidationError("Cannot mark lost opportunity as won")
            
            opportunity.is_won = True
            opportunity.is_lost = False
            opportunity.date_closed = datetime.now()
    
    def action_mark_lost(self):
        """Mark opportunity as lost"""
        for opportunity in self:
            if opportunity.is_won:
                raise ValidationError("Cannot mark won opportunity as lost")
            
            opportunity.is_lost = True
            opportunity.is_won = False
            opportunity.date_closed = datetime.now()
    
    def action_schedule_activity(self):
        """Schedule activity for opportunity"""
        return {
            'type': 'ocean.actions.act_window',
            'name': f'Schedule Activity - {self.name}',
            'res_model': 'crm.activity',
            'view_mode': 'form',
            'context': {
                'default_opportunity_id': self.id,
                'default_user_id': self.user_id.id
            },
            'target': 'new'
        }
    
    def action_send_communication(self):
        """Send communication to opportunity"""
        return {
            'type': 'ocean.actions.act_window',
            'name': f'Send Communication - {self.name}',
            'res_model': 'crm.communication',
            'view_mode': 'form',
            'context': {
                'default_opportunity_id': self.id,
                'default_user_id': self.user_id.id
            },
            'target': 'new'
        }
    
    def action_view_activities(self):
        """View activities for this opportunity"""
        return {
            'type': 'ocean.actions.act_window',
            'name': f'Activities - {self.name}',
            'res_model': 'crm.activity',
            'view_mode': 'tree,form',
            'domain': [('opportunity_id', '=', self.id)],
            'context': {'default_opportunity_id': self.id}
        }
    
    def action_view_communications(self):
        """View communications for this opportunity"""
        return {
            'type': 'ocean.actions.act_window',
            'name': f'Communications - {self.name}',
            'res_model': 'crm.communication',
            'view_mode': 'tree,form',
            'domain': [('opportunity_id', '=', self.id)],
            'context': {'default_opportunity_id': self.id}
        }