#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - CRM Lead Model
===================================

Lead management for kids clothing retail.
"""

import logging
from datetime import datetime, timedelta
from core_framework.orm import BaseModel, CharField, TextField, BooleanField, IntegerField, DateTimeField, Many2OneField, SelectionField, FloatField, One2ManyField, Many2ManyField
from core_framework.exceptions import ValidationError

logger = logging.getLogger(__name__)

class CrmLead(BaseModel):
    """CRM leads for kids clothing retail"""
    
    _name = 'crm.lead'
    _description = 'CRM Lead'
    _table = 'crm_lead'
    _order = 'create_date desc'
    
    # Basic Information
    name = CharField(
        string='Lead Name',
        size=100,
        required=True,
        help='Name of the lead'
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
        help='Email address of the lead'
    )
    
    phone = CharField(
        string='Phone',
        size=20,
        help='Phone number of the lead'
    )
    
    mobile = CharField(
        string='Mobile',
        size=20,
        help='Mobile number of the lead'
    )
    
    # Address Information
    street = CharField(
        string='Street',
        size=100,
        help='Street address'
    )
    
    city = CharField(
        string='City',
        size=50,
        help='City'
    )
    
    state = CharField(
        string='State',
        size=50,
        help='State'
    )
    
    zip = CharField(
        string='ZIP Code',
        size=20,
        help='ZIP code'
    )
    
    country = CharField(
        string='Country',
        size=50,
        help='Country'
    )
    
    # Lead Details
    title = CharField(
        string='Title',
        size=100,
        help='Job title of the contact'
    )
    
    function = CharField(
        string='Function',
        size=100,
        help='Function of the contact'
    )
    
    website = CharField(
        string='Website',
        size=100,
        help='Website of the lead'
    )
    
    # Lead Status
    type = SelectionField(
        string='Type',
        selection=[
            ('lead', 'Lead'),
            ('opportunity', 'Opportunity'),
            ('customer', 'Customer')
        ],
        default='lead',
        help='Type of the lead'
    )
    
    stage_id = Many2OneField(
        'crm.stage',
        string='Stage',
        help='Current stage of the lead'
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
    
    # Lead Source
    source_id = Many2OneField(
        'crm.source',
        string='Source',
        help='Source of the lead'
    )
    
    medium_id = Many2OneField(
        'crm.medium',
        string='Medium',
        help='Medium of the lead'
    )
    
    campaign_id = Many2OneField(
        'crm.campaign',
        string='Campaign',
        help='Campaign that generated the lead'
    )
    
    # Lead Quality
    priority = SelectionField(
        string='Priority',
        selection=[
            ('0', 'Low'),
            ('1', 'Normal'),
            ('2', 'High'),
            ('3', 'Very High')
        ],
        default='1',
        help='Priority of the lead'
    )
    
    probability = FloatField(
        string='Probability %',
        digits=(5, 2),
        default=0.0,
        help='Probability of conversion'
    )
    
    expected_revenue = FloatField(
        string='Expected Revenue',
        digits=(12, 2),
        default=0.0,
        help='Expected revenue from this lead'
    )
    
    # Lead Assignment
    user_id = Many2OneField(
        'res.users',
        string='Salesperson',
        help='Salesperson assigned to this lead'
    )
    
    team_id = Many2OneField(
        'sales.team',
        string='Sales Team',
        help='Sales team assigned to this lead'
    )
    
    # Lead Activities
    activity_ids = One2ManyField(
        string='Activities',
        comodel_name='crm.activity',
        inverse_name='lead_id',
        help='Activities related to this lead'
    )
    
    communication_ids = One2ManyField(
        string='Communications',
        comodel_name='crm.communication',
        inverse_name='lead_id',
        help='Communications with this lead'
    )
    
    # Lead Conversion
    partner_id = Many2OneField(
        'contact.customer',
        string='Customer',
        help='Customer created from this lead'
    )
    
    opportunity_id = Many2OneField(
        'crm.opportunity',
        string='Opportunity',
        help='Opportunity created from this lead'
    )
    
    # Lead Notes
    description = TextField(
        string='Description',
        help='Description of the lead'
    )
    
    note = TextField(
        string='Notes',
        help='Internal notes about the lead'
    )
    
    # Lead Status
    is_active = BooleanField(
        string='Active',
        default=True,
        help='Whether this lead is active'
    )
    
    is_converted = BooleanField(
        string='Converted',
        default=False,
        help='Whether this lead has been converted'
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
        
        # Update conversion status
        if 'partner_id' in vals and vals['partner_id']:
            self.is_converted = True
            self.type = 'customer'
        
        return result
    
    def action_convert_to_customer(self):
        """Convert lead to customer"""
        for lead in self:
            if lead.is_converted:
                raise ValidationError("Lead has already been converted")
            
            # Create customer
            customer_vals = {
                'name': lead.partner_name or lead.name,
                'email': lead.email,
                'phone': lead.phone,
                'mobile': lead.mobile,
                'street': lead.street,
                'city': lead.city,
                'state': lead.state,
                'zip': lead.zip,
                'country': lead.country,
                'title': lead.title,
                'function': lead.function,
                'website': lead.website,
                'child_count': lead.child_count,
                'child_ages': lead.child_ages,
                'age_group_interest': lead.age_group_interest,
                'gender_preference': lead.gender_preference,
                'seasonal_interest': lead.seasonal_interest
            }
            
            customer = self.env['contact.customer'].create(customer_vals)
            lead.partner_id = customer.id
            lead.is_converted = True
            lead.type = 'customer'
    
    def action_convert_to_opportunity(self):
        """Convert lead to opportunity"""
        for lead in self:
            if lead.is_converted:
                raise ValidationError("Lead has already been converted")
            
            # Create opportunity
            opportunity_vals = {
                'name': lead.name,
                'partner_name': lead.partner_name,
                'email': lead.email,
                'phone': lead.phone,
                'expected_revenue': lead.expected_revenue,
                'probability': lead.probability,
                'user_id': lead.user_id.id,
                'team_id': lead.team_id.id,
                'source_id': lead.source_id.id,
                'campaign_id': lead.campaign_id.id,
                'child_count': lead.child_count,
                'child_ages': lead.child_ages,
                'age_group_interest': lead.age_group_interest,
                'gender_preference': lead.gender_preference,
                'seasonal_interest': lead.seasonal_interest,
                'description': lead.description
            }
            
            opportunity = self.env['crm.opportunity'].create(opportunity_vals)
            lead.opportunity_id = opportunity.id
            lead.type = 'opportunity'
    
    def action_schedule_activity(self):
        """Schedule activity for lead"""
        return {
            'type': 'ocean.actions.act_window',
            'name': f'Schedule Activity - {self.name}',
            'res_model': 'crm.activity',
            'view_mode': 'form',
            'context': {
                'default_lead_id': self.id,
                'default_user_id': self.user_id.id
            },
            'target': 'new'
        }
    
    def action_send_communication(self):
        """Send communication to lead"""
        return {
            'type': 'ocean.actions.act_window',
            'name': f'Send Communication - {self.name}',
            'res_model': 'crm.communication',
            'view_mode': 'form',
            'context': {
                'default_lead_id': self.id,
                'default_user_id': self.user_id.id
            },
            'target': 'new'
        }
    
    def action_view_activities(self):
        """View activities for this lead"""
        return {
            'type': 'ocean.actions.act_window',
            'name': f'Activities - {self.name}',
            'res_model': 'crm.activity',
            'view_mode': 'tree,form',
            'domain': [('lead_id', '=', self.id)],
            'context': {'default_lead_id': self.id}
        }
    
    def action_view_communications(self):
        """View communications for this lead"""
        return {
            'type': 'ocean.actions.act_window',
            'name': f'Communications - {self.name}',
            'res_model': 'crm.communication',
            'view_mode': 'tree,form',
            'domain': [('lead_id', '=', self.id)],
            'context': {'default_lead_id': self.id}
        }