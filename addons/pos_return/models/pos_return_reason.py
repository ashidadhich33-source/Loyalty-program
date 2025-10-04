# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - POS Return Reason
=====================================

POS return reason management for kids clothing retail.
"""

from core_framework.orm import BaseModel, CharField, TextField, BooleanField, IntegerField, DateTimeField, Many2OneField, SelectionField, FloatField, One2ManyField, Many2ManyField
from core_framework.orm import Field
from typing import Dict, Any, Optional
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class PosReturnReason(BaseModel):
    """POS return reason for categorization"""
    
    _name = 'pos.return.reason'
    _description = 'POS Return Reason'
    _table = 'pos_return_reason'
    
    # Basic Information
    name = CharField(
        string='Reason Name',
        size=100,
        required=True,
        help='Name of the return reason'
    )
    
    code = CharField(
        string='Reason Code',
        size=20,
        required=True,
        help='Short code for the return reason'
    )
    
    description = TextField(
        string='Description',
        help='Description of the return reason'
    )
    
    # Reason Category
    category = SelectionField(
        string='Category',
        selection=[
            ('quality_issue', 'Quality Issue'),
            ('size_issue', 'Size Issue'),
            ('color_preference', 'Color Preference'),
            ('style_preference', 'Style Preference'),
            ('defective', 'Defective Product'),
            ('wrong_item', 'Wrong Item'),
            ('customer_preference', 'Customer Preference'),
            ('other', 'Other')
        ],
        default='quality_issue',
        help='Category of the return reason'
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
        help='Whether returns with this reason require approval'
    )
    
    approval_user_id = Many2OneField(
        'res.users',
        string='Approval User',
        help='User who can approve returns with this reason'
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
    
    # Return Policy
    max_return_period = IntegerField(
        string='Max Return Period (Days)',
        default=7,
        help='Maximum number of days allowed for return'
    )
    
    allow_full_refund = BooleanField(
        string='Allow Full Refund',
        default=True,
        help='Whether this reason allows full refunds'
    )
    
    allow_partial_refund = BooleanField(
        string='Allow Partial Refund',
        default=True,
        help='Whether this reason allows partial refunds'
    )
    
    allow_store_credit = BooleanField(
        string='Allow Store Credit',
        default=True,
        help='Whether this reason allows store credit'
    )
    
    allow_exchange = BooleanField(
        string='Allow Exchange',
        default=True,
        help='Whether this reason allows exchanges'
    )
    
    # Refund Policy
    default_refund_percentage = FloatField(
        string='Default Refund Percentage',
        digits=(5, 2),
        default=100.0,
        help='Default percentage of original price that can be refunded'
    )
    
    max_refund_percentage = FloatField(
        string='Max Refund Percentage',
        digits=(5, 2),
        default=100.0,
        help='Maximum percentage of original price that can be refunded'
    )
    
    # Store Credit Policy
    store_credit_percentage = FloatField(
        string='Store Credit Percentage',
        digits=(5, 2),
        default=0.0,
        help='Percentage given as store credit'
    )
    
    store_credit_validity_days = IntegerField(
        string='Store Credit Validity (Days)',
        default=365,
        help='Number of days store credit is valid'
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
    
    def action_view_returns(self):
        """View returns with this reason"""
        return {
            'type': 'ir.actions.act_window',
            'name': f'Returns - {self.name}',
            'res_model': 'pos.return',
            'view_mode': 'tree,form',
            'domain': [('return_reason_id', '=', self.id)],
            'context': {'default_return_reason_id': self.id}
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
            'max_return_period': self.max_return_period,
            'allow_full_refund': self.allow_full_refund,
            'allow_partial_refund': self.allow_partial_refund,
            'allow_store_credit': self.allow_store_credit,
            'allow_exchange': self.allow_exchange,
            'default_refund_percentage': self.default_refund_percentage,
            'max_refund_percentage': self.max_refund_percentage,
            'store_credit_percentage': self.store_credit_percentage,
            'store_credit_validity_days': self.store_credit_validity_days,
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
    
    def validate_return_type(self, return_type):
        """Validate if reason allows the return type"""
        if return_type == 'full_return' and not self.allow_full_refund:
            return False
        elif return_type == 'partial_return' and not self.allow_partial_refund:
            return False
        
        return True
    
    def calculate_refund_amount(self, original_amount, return_type='full_return'):
        """Calculate refund amount based on reason policy"""
        if return_type == 'full_return':
            refund_percentage = self.default_refund_percentage
        elif return_type == 'partial_return':
            refund_percentage = self.default_refund_percentage * 0.5  # 50% for partial
        else:
            refund_percentage = 0
        
        # Ensure it doesn't exceed max refund percentage
        refund_percentage = min(refund_percentage, self.max_refund_percentage)
        
        return original_amount * (refund_percentage / 100)
    
    def calculate_store_credit_amount(self, original_amount):
        """Calculate store credit amount based on reason policy"""
        if not self.allow_store_credit:
            return 0
        
        return original_amount * (self.store_credit_percentage / 100)