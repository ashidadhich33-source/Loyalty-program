# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - POS Return Wizard
====================================

Return processing wizard for POS sessions.
"""

from core_framework.orm import BaseModel, CharField, TextField, BooleanField, IntegerField, DateTimeField, Many2OneField, SelectionField, FloatField, One2ManyField, Many2ManyField
from core_framework.orm import Field
from typing import Dict, Any, Optional
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class PosReturnWizard(BaseModel):
    """Return processing wizard"""
    
    _name = 'pos.return.wizard'
    _description = 'POS Return Wizard'
    _table = 'pos_return_wizard'
    
    # Basic Information
    session_id = Many2OneField(
        'pos.session',
        string='Session',
        required=True,
        help='POS session for this return'
    )
    
    partner_id = Many2OneField(
        'res.partner',
        string='Customer',
        required=True,
        help='Customer for this return'
    )
    
    original_order_id = Many2OneField(
        'pos.order',
        string='Original Order',
        required=True,
        help='Original order being returned'
    )
    
    # Return Information
    return_reason_id = Many2OneField(
        'pos.return.reason',
        string='Return Reason',
        required=True,
        help='Reason for the return'
    )
    
    return_type = SelectionField(
        string='Return Type',
        selection=[
            ('full_return', 'Full Return'),
            ('partial_return', 'Partial Return'),
            ('defective', 'Defective Product'),
            ('wrong_item', 'Wrong Item'),
            ('customer_preference', 'Customer Preference'),
            ('other', 'Other')
        ],
        required=True,
        help='Type of return'
    )
    
    # Customer Information
    customer_age = IntegerField(
        string='Customer Age',
        help='Age of the customer'
    )
    
    # Return Policy
    within_return_period = BooleanField(
        string='Within Return Period',
        default=True,
        help='Whether return is within allowed period'
    )
    
    return_period_days = IntegerField(
        string='Return Period (Days)',
        default=7,
        help='Number of days allowed for return'
    )
    
    # Refund Information
    refund_method = SelectionField(
        string='Refund Method',
        selection=[
            ('cash', 'Cash Refund'),
            ('card', 'Card Refund'),
            ('store_credit', 'Store Credit'),
            ('exchange', 'Exchange'),
            ('other', 'Other')
        ],
        required=True,
        help='Method of refund'
    )
    
    refund_percentage = FloatField(
        string='Refund Percentage',
        digits=(5, 2),
        default=100.0,
        help='Percentage of original price to refund'
    )
    
    # Store Credit Information
    store_credit_amount = FloatField(
        string='Store Credit Amount',
        digits=(12, 2),
        default=0.0,
        help='Amount given as store credit'
    )
    
    store_credit_expiry = DateTimeField(
        string='Store Credit Expiry',
        help='Expiry date for store credit'
    )
    
    # Notes
    reason_note = TextField(
        string='Reason Note',
        help='Additional notes about the return reason'
    )
    
    note = TextField(
        string='Notes',
        help='Return notes and comments'
    )
    
    # Timestamps
    create_date = DateTimeField(
        string='Created On',
        auto_now_add=True
    )
    
    def action_process_return(self):
        """Process the return"""
        for wizard in self:
            # Validate wizard data
            wizard._validate_wizard()
            
            # Create return
            return_record = wizard._create_return()
            
            # Confirm return
            return_record.action_confirm()
            return_record.action_done()
        
        return {
            'type': 'ir.actions.act_window',
            'name': 'Return Processed',
            'res_model': 'pos.return',
            'res_id': return_record.id,
            'view_mode': 'form',
            'target': 'new'
        }
    
    def _validate_wizard(self):
        """Validate wizard data"""
        errors = []
        
        # Check required fields
        if not self.partner_id:
            errors.append("Customer is required")
        
        if not self.original_order_id:
            errors.append("Original order is required")
        
        if not self.return_reason_id:
            errors.append("Return reason is required")
        
        if not self.return_type:
            errors.append("Return type is required")
        
        if not self.refund_method:
            errors.append("Refund method is required")
        
        # Check return period
        if not self.within_return_period:
            errors.append("Return is outside the allowed period")
        
        # Check age-based policies
        if self.customer_age and self.return_reason_id:
            if not self.return_reason_id.validate_age_group(self.customer_age):
                errors.append(f"Return reason '{self.return_reason_id.name}' does not apply to customer age {self.customer_age}")
        
        # Check return type validation
        if self.return_reason_id and self.return_type:
            if not self.return_reason_id.validate_return_type(self.return_type):
                errors.append(f"Return reason '{self.return_reason_id.name}' does not allow '{self.return_type}' returns")
        
        # Check refund percentage
        if self.refund_percentage < 0 or self.refund_percentage > 100:
            errors.append("Refund percentage must be between 0 and 100")
        
        # Check store credit expiry
        if self.refund_method == 'store_credit' and not self.store_credit_expiry:
            # Set default expiry based on reason policy
            if self.return_reason_id:
                validity_days = self.return_reason_id.store_credit_validity_days
                self.store_credit_expiry = datetime.now() + timedelta(days=validity_days)
        
        if errors:
            raise ValueError('\n'.join(errors))
    
    def _create_return(self):
        """Create return from wizard data"""
        # Create return
        return_vals = {
            'session_id': self.session_id.id,
            'partner_id': self.partner_id.id,
            'original_order_id': self.original_order_id.id,
            'return_reason_id': self.return_reason_id.id,
            'return_type': self.return_type,
            'customer_age': self.customer_age,
            'within_return_period': self.within_return_period,
            'return_period_days': self.return_period_days,
            'refund_method': self.refund_method,
            'refund_percentage': self.refund_percentage,
            'store_credit_amount': self.store_credit_amount,
            'store_credit_expiry': self.store_credit_expiry,
            'reason_note': self.reason_note,
            'note': self.note,
            'state': 'draft',
            'return_date': datetime.now()
        }
        
        return_record = self.env['pos.return'].create(return_vals)
        
        return return_record
    
    def action_view_original_order(self):
        """View original order"""
        return {
            'type': 'ir.actions.act_window',
            'name': f'Original Order - {self.original_order_id.name}',
            'res_model': 'pos.order',
            'res_id': self.original_order_id.id,
            'view_mode': 'form',
            'target': 'new'
        }
    
    def action_view_customer(self):
        """View customer details"""
        return {
            'type': 'ir.actions.act_window',
            'name': f'Customer - {self.partner_id.name}',
            'res_model': 'res.partner',
            'res_id': self.partner_id.id,
            'view_mode': 'form',
            'target': 'new'
        }
    
    def action_calculate_refund(self):
        """Calculate refund amounts based on reason policy"""
        if not self.return_reason_id or not self.original_order_id:
            return
        
        # Get original order amount
        original_amount = self.original_order_id.amount_total
        
        # Calculate refund amount based on reason policy
        refund_amount = self.return_reason_id.calculate_refund_amount(
            original_amount, 
            self.return_type
        )
        
        # Calculate store credit amount
        store_credit_amount = self.return_reason_id.calculate_store_credit_amount(
            original_amount
        )
        
        # Update wizard fields
        self.refund_percentage = (refund_amount / original_amount) * 100
        self.store_credit_amount = store_credit_amount
        
        return True
    
    def get_wizard_summary(self):
        """Get wizard summary data"""
        return {
            'customer': self.partner_id.name,
            'original_order': self.original_order_id.name,
            'return_reason': self.return_reason_id.name if self.return_reason_id else 'Not specified',
            'return_type': self.return_type,
            'customer_age': self.customer_age,
            'within_return_period': self.within_return_period,
            'return_period_days': self.return_period_days,
            'refund_method': self.refund_method,
            'refund_percentage': self.refund_percentage,
            'store_credit_amount': self.store_credit_amount,
            'store_credit_expiry': self.store_credit_expiry,
            'session': self.session_id.name
        }