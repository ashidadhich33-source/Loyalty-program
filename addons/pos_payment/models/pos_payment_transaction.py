# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - POS Payment Transaction
==========================================

POS payment transaction management for kids clothing retail.
"""

from core_framework.orm import BaseModel, CharField, TextField, BooleanField, IntegerField, DateTimeField, Many2OneField, SelectionField, FloatField, One2ManyField, Many2ManyField
from core_framework.orm import Field
from typing import Dict, Any, Optional
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class PosPaymentTransaction(BaseModel):
    """POS payment transaction record"""
    
    _name = 'pos.payment.transaction'
    _description = 'POS Payment Transaction'
    _table = 'pos_payment_transaction'
    
    # Basic Information
    name = CharField(
        string='Transaction Reference',
        size=100,
        required=True,
        help='Transaction reference number'
    )
    
    transaction_id = CharField(
        string='Transaction ID',
        size=100,
        help='External transaction ID from payment provider'
    )
    
    # Related Records
    session_id = Many2OneField(
        'pos.session',
        string='Session',
        required=True,
        help='POS session for this transaction'
    )
    
    order_id = Many2OneField(
        'pos.order',
        string='Order',
        help='POS order for this transaction'
    )
    
    payment_method_id = Many2OneField(
        'pos.payment.method',
        string='Payment Method',
        required=True,
        help='Payment method used'
    )
    
    terminal_id = Many2OneField(
        'pos.payment.terminal',
        string='Terminal',
        help='Payment terminal used'
    )
    
    # Transaction Details
    amount = FloatField(
        string='Amount',
        digits=(12, 2),
        required=True,
        help='Transaction amount'
    )
    
    fee = FloatField(
        string='Fee',
        digits=(12, 2),
        default=0.0,
        help='Processing fee'
    )
    
    net_amount = FloatField(
        string='Net Amount',
        digits=(12, 2),
        help='Net amount after fees'
    )
    
    # Transaction State
    state = SelectionField(
        string='State',
        selection=[
            ('draft', 'Draft'),
            ('pending', 'Pending'),
            ('processing', 'Processing'),
            ('success', 'Success'),
            ('failed', 'Failed'),
            ('cancelled', 'Cancelled'),
            ('refunded', 'Refunded'),
            ('partially_refunded', 'Partially Refunded')
        ],
        default='draft',
        help='Current state of the transaction'
    )
    
    # Transaction Type
    transaction_type = SelectionField(
        string='Transaction Type',
        selection=[
            ('payment', 'Payment'),
            ('refund', 'Refund'),
            ('void', 'Void'),
            ('settlement', 'Settlement'),
            ('reversal', 'Reversal')
        ],
        default='payment',
        help='Type of transaction'
    )
    
    # Customer Information
    partner_id = Many2OneField(
        'res.partner',
        string='Customer',
        help='Customer for this transaction'
    )
    
    customer_age = IntegerField(
        string='Customer Age',
        help='Age of the customer'
    )
    
    # Payment Details
    payment_reference = CharField(
        string='Payment Reference',
        size=100,
        help='Payment reference from customer'
    )
    
    card_number = CharField(
        string='Card Number',
        size=20,
        help='Last 4 digits of card number'
    )
    
    card_type = CharField(
        string='Card Type',
        size=50,
        help='Type of card used'
    )
    
    card_holder_name = CharField(
        string='Card Holder Name',
        size=100,
        help='Name on the card'
    )
    
    # Digital Payment Details
    upi_id = CharField(
        string='UPI ID',
        size=100,
        help='UPI ID used for payment'
    )
    
    wallet_provider = CharField(
        string='Wallet Provider',
        size=50,
        help='Digital wallet provider'
    )
    
    wallet_transaction_id = CharField(
        string='Wallet Transaction ID',
        size=100,
        help='Wallet transaction ID'
    )
    
    # Transaction Timing
    transaction_date = DateTimeField(
        string='Transaction Date',
        required=True,
        help='Date and time of transaction'
    )
    
    processing_time = FloatField(
        string='Processing Time',
        digits=(8, 2),
        default=0.0,
        help='Transaction processing time in seconds'
    )
    
    # Provider Response
    provider_response = TextField(
        string='Provider Response',
        help='Response from payment provider'
    )
    
    provider_status = CharField(
        string='Provider Status',
        size=50,
        help='Status from payment provider'
    )
    
    provider_error_code = CharField(
        string='Provider Error Code',
        size=50,
        help='Error code from payment provider'
    )
    
    provider_error_message = TextField(
        string='Provider Error Message',
        help='Error message from payment provider'
    )
    
    # Security Information
    requires_pin = BooleanField(
        string='Requires PIN',
        default=False,
        help='Whether transaction required PIN verification'
    )
    
    requires_signature = BooleanField(
        string='Requires Signature',
        default=False,
        help='Whether transaction required signature'
    )
    
    pin_verified = BooleanField(
        string='PIN Verified',
        default=False,
        help='Whether PIN was verified'
    )
    
    signature_verified = BooleanField(
        string='Signature Verified',
        default=False,
        help='Whether signature was verified'
    )
    
    # Refund Information
    refund_amount = FloatField(
        string='Refund Amount',
        digits=(12, 2),
        default=0.0,
        help='Amount refunded'
    )
    
    refund_reference = CharField(
        string='Refund Reference',
        size=100,
        help='Refund reference number'
    )
    
    refund_date = DateTimeField(
        string='Refund Date',
        help='Date of refund'
    )
    
    refund_reason = TextField(
        string='Refund Reason',
        help='Reason for refund'
    )
    
    # Settlement Information
    settlement_date = DateTimeField(
        string='Settlement Date',
        help='Date of settlement'
    )
    
    settlement_reference = CharField(
        string='Settlement Reference',
        size=100,
        help='Settlement reference number'
    )
    
    settlement_amount = FloatField(
        string='Settlement Amount',
        digits=(12, 2),
        help='Settlement amount'
    )
    
    # Notes
    note = TextField(
        string='Notes',
        help='Transaction notes and comments'
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
            vals['name'] = self._generate_transaction_name()
        
        if 'transaction_date' not in vals:
            vals['transaction_date'] = datetime.now()
        
        if 'net_amount' not in vals and 'amount' in vals and 'fee' in vals:
            vals['net_amount'] = vals['amount'] - vals['fee']
        
        return super().create(vals)
    
    def write(self, vals):
        """Override write to update net amount"""
        result = super().write(vals)
        
        # Update net amount when amount or fee changes
        if any(field in vals for field in ['amount', 'fee']):
            self._update_net_amount()
        
        return result
    
    def _generate_transaction_name(self):
        """Generate unique transaction name"""
        return f"TXN-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    def _update_net_amount(self):
        """Update net amount"""
        for transaction in self:
            transaction.net_amount = transaction.amount - transaction.fee
    
    def action_process_payment(self):
        """Process payment transaction"""
        if self.state != 'draft':
            raise ValueError("Only draft transactions can be processed")
        
        self.state = 'processing'
        
        try:
            # Process payment through payment method
            result = self.payment_method_id.process_payment(
                self.amount, 
                {
                    'transaction_id': self.id,
                    'customer_age': self.customer_age,
                    'partner_id': self.partner_id.id if self.partner_id else None
                }
            )
            
            # Update transaction with result
            self.transaction_id = result['transaction_id']
            self.provider_response = result['provider_response']
            self.provider_status = result['status']
            self.fee = result['fee']
            self.net_amount = result['net_amount']
            
            if result['status'] == 'success':
                self.state = 'success'
            else:
                self.state = 'failed'
                self.provider_error_message = result.get('error_message', 'Payment failed')
            
        except Exception as e:
            self.state = 'failed'
            self.provider_error_message = str(e)
            logger.error(f"Payment processing error: {e}")
        
        return True
    
    def action_refund(self, refund_amount=None, refund_reason=None):
        """Process refund for transaction"""
        if self.state != 'success':
            raise ValueError("Only successful transactions can be refunded")
        
        if refund_amount is None:
            refund_amount = self.amount
        
        if refund_amount > self.amount:
            raise ValueError("Refund amount cannot exceed transaction amount")
        
        # Process refund through payment method
        try:
            result = self.payment_method_id.process_payment(
                refund_amount,
                {
                    'transaction_id': self.id,
                    'refund': True,
                    'original_transaction_id': self.transaction_id
                }
            )
            
            # Update transaction
            self.refund_amount = refund_amount
            self.refund_reference = result['transaction_id']
            self.refund_date = datetime.now()
            self.refund_reason = refund_reason or 'Customer refund'
            
            if refund_amount == self.amount:
                self.state = 'refunded'
            else:
                self.state = 'partially_refunded'
            
        except Exception as e:
            logger.error(f"Refund processing error: {e}")
            raise ValueError(f"Refund failed: {e}")
        
        return True
    
    def action_void(self):
        """Void transaction"""
        if self.state not in ['draft', 'pending', 'processing']:
            raise ValueError("Only draft, pending, or processing transactions can be voided")
        
        self.state = 'cancelled'
        return True
    
    def action_view_order(self):
        """View related order"""
        if not self.order_id:
            return None
        
        return {
            'type': 'ir.actions.act_window',
            'name': f'Order - {self.order_id.name}',
            'res_model': 'pos.order',
            'res_id': self.order_id.id,
            'view_mode': 'form',
            'target': 'new'
        }
    
    def action_view_session(self):
        """View related session"""
        return {
            'type': 'ir.actions.act_window',
            'name': f'Session - {self.session_id.name}',
            'res_model': 'pos.session',
            'res_id': self.session_id.id,
            'view_mode': 'form',
            'target': 'new'
        }
    
    def get_transaction_summary(self):
        """Get transaction summary data"""
        return {
            'transaction_name': self.name,
            'transaction_id': self.transaction_id,
            'session': self.session_id.name,
            'order': self.order_id.name if self.order_id else 'Not specified',
            'payment_method': self.payment_method_id.name,
            'terminal': self.terminal_id.name if self.terminal_id else 'Not specified',
            'amount': self.amount,
            'fee': self.fee,
            'net_amount': self.net_amount,
            'state': self.state,
            'transaction_type': self.transaction_type,
            'customer': self.partner_id.name if self.partner_id else 'Not specified',
            'customer_age': self.customer_age,
            'transaction_date': self.transaction_date,
            'processing_time': self.processing_time,
            'provider_status': self.provider_status,
            'refund_amount': self.refund_amount,
            'refund_reference': self.refund_reference,
            'refund_date': self.refund_date,
            'settlement_date': self.settlement_date,
            'settlement_amount': self.settlement_amount
        }