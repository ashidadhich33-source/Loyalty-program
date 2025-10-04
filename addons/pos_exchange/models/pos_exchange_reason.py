# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - POS Exchange Reason
=======================================

POS exchange reason management for kids clothing retail.
"""

from core_framework.orm import BaseModel, CharField, TextField, BooleanField, IntegerField, DateTimeField, Many2OneField, SelectionField, FloatField, One2ManyField, Many2ManyField
from core_framework.orm import Field
from typing import Dict, Any, Optional
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class PosExchangeReason(BaseModel):
    """POS exchange reason for categorization"""
    
    _name = 'pos.exchange.reason'
    _description = 'POS Exchange Reason'
    _table = 'pos_exchange_reason'
    
    # Basic Information
    name = CharField(
        string='Reason Name',
        size=100,
        required=True,
        help='Name of the exchange reason'
    )
    
    code = CharField(
        string='Reason Code',
        size=20,
        required=True,
        help='Short code for the exchange reason'
    )
    
    description = TextField(
        string='Description',
        help='Description of the exchange reason'
    )
    
    # Reason Category
    category = SelectionField(
        string='Category',
        selection=[
            ('size_issue', 'Size Issue'),
            ('color_preference', 'Color Preference'),
            ('style_preference', 'Style Preference'),
            ('quality_issue', 'Quality Issue'),
            ('defective', 'Defective Product'),
            ('wrong_item', 'Wrong Item'),
            ('customer_preference', 'Customer Preference'),
            ('other', 'Other')
        ],
        default='size_issue',
        help='Category of the exchange reason'
    )
    
    # Policy Settings
    is_active = BooleanField(
        string='Active',
        default=True,
        help='Whether this reason is active'
    )
    
    requires_approval = BooleanField(
        string='Requires Approval',
        default=False,
        help='Whether exchanges with this reason require approval'
    )
    
    approval_user_id = Many2OneField(
        'res.users',
        string='Approval User',
        help='User who can approve exchanges with this reason'
    )
    
    # Age-based Settings
    age_group_restriction = SelectionField(
        string='Age Group Restriction',
        selection=[
            ('none', 'No Restriction'),
            ('toddler', 'Toddler Only (0-3 years)'),
            ('child', 'Child Only (3-12 years)'),
            ('teen', 'Teen Only (12+ years)'),
            ('toddler_child', 'Toddler & Child (0-12 years)'),
            ('child_teen', 'Child & Teen (3+ years)')
        ],
        default='none',
        help='Age group restriction for this reason'
    )
    
    # Exchange Policy
    max_exchange_period = IntegerField(
        string='Max Exchange Period (Days)',
        default=7,
        help='Maximum number of days allowed for exchange'
    )
    
    allow_size_change = BooleanField(
        string='Allow Size Change',
        default=True,
        help='Whether this reason allows size changes'
    )
    
    allow_color_change = BooleanField(
        string='Allow Color Change',
        default=True,
        help='Whether this reason allows color changes'
    )
    
    allow_style_change = BooleanField(
        string='Allow Style Change',
        default=False,
        help='Whether this reason allows style changes'
    )
    
    # Refund Policy
    allow_refund = BooleanField(
        string='Allow Refund',
        default=False,
        help='Whether this reason allows refunds'
    )
    
    refund_percentage = FloatField(
        string='Refund Percentage',
        digits=(5, 2),
        default=100.0,
        help='Percentage of original price that can be refunded'
    )
    
    # Usage Statistics
    usage_count = IntegerField(
        string='Usage Count',
        default=0,
        help='Number of times this reason has been used'
    )
    
    last_used = DateTimeField(
        string='Last Used',
        help='When this reason was last used'
    )
    
    # Notes
    note = TextField(
        string='Notes',
        help='Additional notes about this reason'
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
        if 'code' not in vals and 'name' in vals:
            vals['code'] = vals['name'].upper().replace(' ', '_')
        
        return super().create(vals)
    
    def write(self, vals):
        """Override write to update usage statistics"""
        result = super().write(vals)
        
        # Update usage count if reason is used
        if 'usage_count' in vals:
            self.last_used = datetime.now()
        
        return result
    
    def action_view_exchanges(self):
        """View exchanges with this reason"""
        return {
            'type': 'ir.actions.act_window',
            'name': f'Exchanges - {self.name}',
            'res_model': 'pos.exchange',
            'view_mode': 'tree,form',
            'domain': [('exchange_reason_id', '=', self.id)],
            'context': {'default_exchange_reason_id': self.id}
        }
    
    def get_reason_summary(self):
        """Get reason summary data"""
        return {
            'reason_name': self.name,
            'reason_code': self.code,
            'category': self.category,
            'is_active': self.is_active,
            'requires_approval': self.requires_approval,
            'age_group_restriction': self.age_group_restriction,
            'max_exchange_period': self.max_exchange_period,
            'allow_size_change': self.allow_size_change,
            'allow_color_change': self.allow_color_change,
            'allow_style_change': self.allow_style_change,
            'allow_refund': self.allow_refund,
            'refund_percentage': self.refund_percentage,
            'usage_count': self.usage_count,
            'last_used': self.last_used
        }
    
    def validate_age_group(self, customer_age):
        """Validate if reason applies to customer age group"""
        if self.age_group_restriction == 'none':
            return True
        
        if self.age_group_restriction == 'toddler' and customer_age <= 3:
            return True
        elif self.age_group_restriction == 'child' and 3 < customer_age <= 12:
            return True
        elif self.age_group_restriction == 'teen' and customer_age > 12:
            return True
        elif self.age_group_restriction == 'toddler_child' and customer_age <= 12:
            return True
        elif self.age_group_restriction == 'child_teen' and customer_age > 3:
            return True
        
        return False
    
    def validate_exchange_type(self, exchange_type):
        """Validate if reason allows the exchange type"""
        if exchange_type == 'size_change' and not self.allow_size_change:
            return False
        elif exchange_type == 'color_change' and not self.allow_color_change:
            return False
        elif exchange_type == 'style_change' and not self.allow_style_change:
            return False
        
        return True