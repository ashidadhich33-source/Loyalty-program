# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - POS Return
==============================

POS return management for kids clothing retail.
"""

from core_framework.orm import BaseModel, CharField, TextField, BooleanField, IntegerField, DateTimeField, Many2OneField, SelectionField, FloatField, One2ManyField, Many2ManyField
from core_framework.orm import Field
from typing import Dict, Any, Optional
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class PosReturn(BaseModel):
    """POS return for product returns"""
    
    _name = 'pos.return'
    _description = 'POS Return'
    _table = 'pos_return'
    
    # Basic Information
    name = CharField(
        string='Return Reference',
        size=100,
        required=True,
        help='Return reference number'
    )
    
    session_id = Many2OneField(
        'pos.session',
        string='Session',
        required=True,
        help='POS session for this return'
    )
    
    config_id = Many2OneField(
        'pos.config',
        string='POS Configuration',
        related='session_id.config_id',
        store=True,
        help='POS configuration'
    )
    
    user_id = Many2OneField(
        'res.users',
        string='Cashier',
        required=True,
        help='Cashier who processed this return'
    )
    
    # Customer Information
    partner_id = Many2OneField(
        'res.partner',
        string='Customer',
        required=True,
        help='Customer for this return'
    )
    
    # Original Order Information
    original_order_id = Many2OneField(
        'pos.order',
        string='Original Order',
        required=True,
        help='Original order being returned'
    )
    
    # Return State
    state = SelectionField(
        string='State',
        selection=[
            ('draft', 'Draft'),
            ('confirmed', 'Confirmed'),
            ('done', 'Done'),
            ('cancel', 'Cancelled')
        ],
        default='draft',
        help='Current state of the return'
    )
    
    # Return Timing
    return_date = DateTimeField(
        string='Return Date',
        required=True,
        help='Date and time of the return'
    )
    
    # Return Lines
    return_lines = One2ManyField(
        string='Return Lines',
        comodel_name='pos.return.line',
        inverse_name='return_id',
        help='Return line items'
    )
    
    # Return Reason
    return_reason_id = Many2OneField(
        'pos.return.reason',
        string='Return Reason',
        help='Reason for the return'
    )
    
    reason_note = TextField(
        string='Reason Note',
        help='Additional notes about the return reason'
    )
    
    # Amounts
    amount_returned = FloatField(
        string='Amount Returned',
        digits=(12, 2),
        default=0.0,
        help='Amount returned to customer'
    )
    
    amount_refunded = FloatField(
        string='Amount Refunded',
        digits=(12, 2),
        default=0.0,
        help='Amount refunded to customer'
    )
    
    refund_method = SelectionField(
        string='Refund Method',
        selection=[
            ('cash', 'Cash Refund'),
            ('card', 'Card Refund'),
            ('store_credit', 'Store Credit'),
            ('exchange', 'Exchange'),
            ('other', 'Other')
        ],
        help='Method of refund'
    )
    
    # Return Type
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
        default='full_return',
        help='Type of return'
    )
    
    # Age-based Information
    customer_age = IntegerField(
        string='Customer Age',
        help='Age of the customer (for age-based policies)'
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
    
    # Refund Policy
    refund_percentage = FloatField(
        string='Refund Percentage',
        digits=(5, 2),
        default=100.0,
        help='Percentage of original price that can be refunded'
    )
    
    # Store Credit
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
    
    # Receipt Information
    return_receipt_number = CharField(
        string='Return Receipt Number',
        size=50,
        help='Return receipt number'
    )
    
    print_return_receipt = BooleanField(
        string='Print Return Receipt',
        default=True,
        help='Whether to print return receipt'
    )
    
    # Notes
    note = TextField(
        string='Notes',
        help='Return notes and comments'
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
        if 'name' not in vals:
            vals['name'] = self._generate_return_name()
        
        if 'return_date' not in vals:
            vals['return_date'] = datetime.now()
        
        if 'user_id' not in vals:
            vals['user_id'] = self.env.user.id
        
        return super().create(vals)
    
    def write(self, vals):
        """Override write to update amounts"""
        result = super().write(vals)
        
        # Update amounts when lines change
        if 'return_lines' in vals:
            self._update_amounts()
        
        return result
    
    def _generate_return_name(self):
        """Generate unique return name"""
        return f"RET-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    def _update_amounts(self):
        """Update return amounts based on lines"""
        for return_record in self:
            # Calculate amounts from lines
            amount_returned = sum(line.return_amount for line in return_record.return_lines)
            amount_refunded = sum(line.refund_amount for line in return_record.return_lines)
            
            # Update amounts
            return_record.amount_returned = amount_returned
            return_record.amount_refunded = amount_refunded
    
    def action_confirm(self):
        """Confirm the return"""
        if self.state != 'draft':
            raise ValueError("Only draft returns can be confirmed")
        
        # Validate return
        self._validate_return()
        
        # Update state
        self.state = 'confirmed'
        
        # Generate return receipt number
        if not self.return_receipt_number:
            self.return_receipt_number = self._generate_return_receipt_number()
        
        return True
    
    def action_done(self):
        """Mark return as done"""
        if self.state not in ['confirmed', 'draft']:
            raise ValueError("Return must be confirmed or draft to mark as done")
        
        self.state = 'done'
        
        # Update inventory
        self._update_inventory()
        
        # Process refund
        self._process_refund()
        
        return True
    
    def action_cancel(self):
        """Cancel the return"""
        if self.state == 'done':
            raise ValueError("Cannot cancel completed returns")
        
        self.state = 'cancel'
        return True
    
    def _validate_return(self):
        """Validate return before confirmation"""
        errors = []
        
        # Check if return has lines
        if not self.return_lines:
            errors.append("Return must have at least one line")
        
        # Check return period
        if not self.within_return_period:
            errors.append("Return is outside the allowed period")
        
        # Check customer age for age-based policies
        if self.customer_age and self.customer_age < 3:
            # Special policy for toddlers
            if self.return_period_days > 14:
                errors.append("Return period exceeds limit for toddler items")
        
        # Check refund percentage
        if self.refund_percentage < 0 or self.refund_percentage > 100:
            errors.append("Refund percentage must be between 0 and 100")
        
        if errors:
            raise ValueError('\n'.join(errors))
    
    def _generate_return_receipt_number(self):
        """Generate return receipt number"""
        return f"RET-RCP-{self.id:06d}"
    
    def _update_inventory(self):
        """Update inventory for returned products"""
        # This would integrate with inventory addon
        for line in self.return_lines:
            # Return product to stock
            pass
    
    def _process_refund(self):
        """Process refund based on refund method"""
        if self.refund_method == 'cash':
            # Process cash refund
            pass
        elif self.refund_method == 'card':
            # Process card refund
            pass
        elif self.refund_method == 'store_credit':
            # Create store credit
            self._create_store_credit()
        elif self.refund_method == 'exchange':
            # This would integrate with exchange addon
            pass
    
    def _create_store_credit(self):
        """Create store credit for customer"""
        # This would integrate with loyalty/addon system
        pass
    
    def action_view_lines(self):
        """View return lines"""
        return {
            'type': 'ir.actions.act_window',
            'name': f'Return Lines - {self.name}',
            'res_model': 'pos.return.line',
            'view_mode': 'tree,form',
            'domain': [('return_id', '=', self.id)],
            'context': {'default_return_id': self.id}
        }
    
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
    
    def action_print_return_receipt(self):
        """Print return receipt"""
        return {
            'type': 'ir.actions.report',
            'report_name': 'pos_return.report_return_receipt',
            'report_type': 'qweb-pdf',
            'data': {'ids': [self.id]},
            'target': 'new'
        }
    
    def get_return_summary(self):
        """Get return summary data"""
        return {
            'return_name': self.name,
            'customer': self.partner_id.name,
            'cashier': self.user_id.name,
            'return_date': self.return_date,
            'state': self.state,
            'return_type': self.return_type,
            'line_count': len(self.return_lines),
            'amount_returned': self.amount_returned,
            'amount_refunded': self.amount_refunded,
            'refund_method': self.refund_method,
            'original_order': self.original_order_id.name,
            'return_reason': self.return_reason_id.name if self.return_reason_id else 'Not specified',
            'store_credit_amount': self.store_credit_amount
        }