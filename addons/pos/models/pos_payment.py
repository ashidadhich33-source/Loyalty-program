# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - POS Payment
===============================

POS payment management for kids clothing retail.
"""

from core_framework.orm import BaseModel, CharField, TextField, BooleanField, IntegerField, DateTimeField, Many2OneField, SelectionField, FloatField, One2ManyField, Many2ManyField
from core_framework.orm import Field
from typing import Dict, Any, Optional
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class PosPayment(BaseModel):
    """POS payment for order transactions"""
    
    _name = 'pos.payment'
    _description = 'POS Payment'
    _table = 'pos_payment'
    
    # Basic Information
    name = CharField(
        string='Payment Reference',
        size=100,
        help='Payment reference number'
    )
    
    order_id = Many2OneField(
        'pos.order',
        string='Order',
        required=True,
        help='POS order for this payment'
    )
    
    session_id = Many2OneField(
        'pos.session',
        string='Session',
        related='order_id.session_id',
        store=True,
        help='POS session'
    )
    
    # Payment Information
    payment_method_id = Many2OneField(
        'pos.payment.method',
        string='Payment Method',
        required=True,
        help='Payment method used'
    )
    
    amount = FloatField(
        string='Amount',
        digits=(12, 2),
        required=True,
        help='Payment amount'
    )
    
    # Payment State
    state = SelectionField(
        string='State',
        selection=[
            ('draft', 'Draft'),
            ('done', 'Done'),
            ('cancel', 'Cancelled')
        ],
        default='draft',
        help='Payment state'
    )
    
    # Payment Details
    payment_date = DateTimeField(
        string='Payment Date',
        required=True,
        help='Date and time of payment'
    )
    
    payment_reference = CharField(
        string='Payment Reference',
        size=100,
        help='External payment reference (transaction ID, etc.)'
    )
    
    # Digital Payment Details
    digital_payment_id = CharField(
        string='Digital Payment ID',
        size=100,
        help='Digital payment transaction ID'
    )
    
    digital_payment_status = SelectionField(
        string='Digital Payment Status',
        selection=[
            ('pending', 'Pending'),
            ('success', 'Success'),
            ('failed', 'Failed'),
            ('cancelled', 'Cancelled')
        ],
        help='Status of digital payment'
    )
    
    # Cash Payment Details
    cash_register_id = Many2OneField(
        'pos.cash.register',
        string='Cash Register',
        help='Cash register used for cash payment'
    )
    
    cash_amount = FloatField(
        string='Cash Amount',
        digits=(12, 2),
        help='Cash amount (for cash payments)'
    )
    
    change_amount = FloatField(
        string='Change Amount',
        digits=(12, 2),
        help='Change given to customer'
    )
    
    # Notes
    note = TextField(
        string='Notes',
        help='Payment notes and comments'
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
        if 'payment_date' not in vals:
            vals['payment_date'] = datetime.now()
        
        if 'name' not in vals:
            vals['name'] = self._generate_payment_name()
        
        return super().create(vals)
    
    def write(self, vals):
        """Override write to validate payment"""
        result = super().write(vals)
        
        # Validate payment amount
        if 'amount' in vals:
            self._validate_payment_amount()
        
        return result
    
    def _generate_payment_name(self):
        """Generate unique payment name"""
        return f"PAY-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    def _validate_payment_amount(self):
        """Validate payment amount"""
        for payment in self:
            if payment.amount <= 0:
                raise ValueError("Payment amount must be greater than 0")
            
            # Check if payment method is cash and validate cash amount
            if payment.payment_method_id.is_cash:
                if payment.cash_amount and payment.cash_amount < payment.amount:
                    raise ValueError("Cash amount cannot be less than payment amount")
    
    def action_confirm(self):
        """Confirm the payment"""
        if self.state != 'draft':
            raise ValueError("Only draft payments can be confirmed")
        
        # Validate payment
        self._validate_payment()
        
        # Process payment based on method
        if self.payment_method_id.is_cash:
            self._process_cash_payment()
        elif self.payment_method_id.is_digital:
            self._process_digital_payment()
        
        # Update state
        self.state = 'done'
        
        return True
    
    def action_cancel(self):
        """Cancel the payment"""
        if self.state == 'done':
            raise ValueError("Cannot cancel completed payments")
        
        self.state = 'cancel'
        return True
    
    def _validate_payment(self):
        """Validate payment before confirmation"""
        errors = []
        
        # Check required fields
        if not self.payment_method_id:
            errors.append("Payment method is required")
        
        if not self.amount or self.amount <= 0:
            errors.append("Payment amount must be greater than 0")
        
        # Validate cash payment
        if self.payment_method_id.is_cash:
            if not self.cash_amount or self.cash_amount < self.amount:
                errors.append("Cash amount must be greater than or equal to payment amount")
        
        # Validate digital payment
        if self.payment_method_id.is_digital:
            if not self.digital_payment_id:
                errors.append("Digital payment ID is required for digital payments")
        
        if errors:
            raise ValueError('\n'.join(errors))
    
    def _process_cash_payment(self):
        """Process cash payment"""
        # Update cash register
        if self.cash_register_id:
            self.cash_register_id.cash_amount += self.amount
        
        # Calculate change
        if self.cash_amount and self.cash_amount > self.amount:
            self.change_amount = self.cash_amount - self.amount
    
    def _process_digital_payment(self):
        """Process digital payment"""
        # This would integrate with payment gateways
        # For now, just mark as success
        self.digital_payment_status = 'success'
    
    def action_view_order(self):
        """View associated order"""
        return {
            'type': 'ir.actions.act_window',
            'name': f'Order - {self.order_id.name}',
            'res_model': 'pos.order',
            'res_id': self.order_id.id,
            'view_mode': 'form',
            'target': 'new'
        }
    
    def action_view_session(self):
        """View associated session"""
        return {
            'type': 'ir.actions.act_window',
            'name': f'Session - {self.session_id.name}',
            'res_model': 'pos.session',
            'res_id': self.session_id.id,
            'view_mode': 'form',
            'target': 'new'
        }
    
    def get_payment_summary(self):
        """Get payment summary data"""
        return {
            'payment_name': self.name,
            'payment_method': self.payment_method_id.name,
            'amount': self.amount,
            'state': self.state,
            'payment_date': self.payment_date,
            'payment_reference': self.payment_reference,
            'digital_payment_status': self.digital_payment_status,
            'cash_amount': self.cash_amount,
            'change_amount': self.change_amount,
            'order_name': self.order_id.name,
            'session_name': self.session_id.name
        }