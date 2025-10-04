# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - POS Payment Wizard
=====================================

Payment processing wizard for POS sessions.
"""

from core_framework.orm import BaseModel, CharField, TextField, BooleanField, IntegerField, DateTimeField, Many2OneField, SelectionField, FloatField, One2ManyField, Many2ManyField
from core_framework.orm import Field
from typing import Dict, Any, Optional
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class PosPaymentWizard(BaseModel):
    """Payment processing wizard"""
    
    _name = 'pos.payment.wizard'
    _description = 'POS Payment Wizard'
    _table = 'pos_payment_wizard'
    
    # Basic Information
    session_id = Many2OneField(
        'pos.session',
        string='Session',
        required=True,
        help='POS session for this payment'
    )
    
    order_id = Many2OneField(
        'pos.order',
        string='Order',
        required=True,
        help='POS order for this payment'
    )
    
    partner_id = Many2OneField(
        'res.partner',
        string='Customer',
        help='Customer for this payment'
    )
    
    # Payment Method
    payment_method_id = Many2OneField(
        'pos.payment.method',
        string='Payment Method',
        required=True,
        help='Payment method to use'
    )
    
    terminal_id = Many2OneField(
        'pos.payment.terminal',
        string='Terminal',
        help='Payment terminal to use'
    )
    
    # Payment Amount
    amount = FloatField(
        string='Amount',
        digits=(12, 2),
        required=True,
        help='Payment amount'
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
    
    # Customer Information
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
    
    # Card Payment Details
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
    
    # Security Information
    requires_pin = BooleanField(
        string='Requires PIN',
        default=False,
        help='Whether payment requires PIN verification'
    )
    
    requires_signature = BooleanField(
        string='Requires Signature',
        default=False,
        help='Whether payment requires signature'
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
    
    def action_process_payment(self):
        """Process the payment"""
        for wizard in self:
            # Validate wizard data
            wizard._validate_wizard()
            
            # Calculate fee
            wizard._calculate_fee()
            
            # Create transaction
            transaction = wizard._create_transaction()
            
            # Process payment
            transaction.action_process_payment()
        
        return {
            'type': 'ir.actions.act_window',
            'name': 'Payment Processed',
            'res_model': 'pos.payment.transaction',
            'res_id': transaction.id,
            'view_mode': 'form',
            'target': 'new'
        }
    
    def _validate_wizard(self):
        """Validate wizard data"""
        errors = []
        
        # Check required fields
        if not self.payment_method_id:
            errors.append("Payment method is required")
        
        if not self.amount or self.amount <= 0:
            errors.append("Payment amount must be greater than 0")
        
        # Validate payment method
        if self.payment_method_id:
            is_valid, message = self.payment_method_id.validate_amount(self.amount)
            if not is_valid:
                errors.append(message)
            
            # Check age group restriction
            if self.customer_age and not self.payment_method_id.validate_age_group(self.customer_age):
                errors.append(f"Payment method '{self.payment_method_id.name}' does not apply to customer age {self.customer_age}")
        
        # Validate terminal
        if self.terminal_id and self.payment_method_id:
            try:
                self.terminal_id.validate_transaction(self.amount, self.payment_method_id)
            except ValueError as e:
                errors.append(str(e))
        
        # Check security requirements
        if self.payment_method_id.requires_pin and not self.pin_verified:
            errors.append("PIN verification is required for this payment method")
        
        if self.payment_method_id.requires_signature and not self.signature_verified:
            errors.append("Signature verification is required for this payment method")
        
        if errors:
            raise ValueError('\n'.join(errors))
    
    def _calculate_fee(self):
        """Calculate processing fee"""
        if self.payment_method_id:
            self.fee = self.payment_method_id.calculate_fee(self.amount)
            self.net_amount = self.amount - self.fee
    
    def _create_transaction(self):
        """Create payment transaction from wizard data"""
        # Create transaction
        transaction_vals = {
            'session_id': self.session_id.id,
            'order_id': self.order_id.id,
            'payment_method_id': self.payment_method_id.id,
            'terminal_id': self.terminal_id.id if self.terminal_id else None,
            'amount': self.amount,
            'fee': self.fee,
            'net_amount': self.net_amount,
            'partner_id': self.partner_id.id if self.partner_id else None,
            'customer_age': self.customer_age,
            'payment_reference': self.payment_reference,
            'card_number': self.card_number,
            'card_type': self.card_type,
            'card_holder_name': self.card_holder_name,
            'upi_id': self.upi_id,
            'wallet_provider': self.wallet_provider,
            'wallet_transaction_id': self.wallet_transaction_id,
            'requires_pin': self.requires_pin,
            'requires_signature': self.requires_signature,
            'pin_verified': self.pin_verified,
            'signature_verified': self.signature_verified,
            'note': self.note,
            'state': 'draft',
            'transaction_date': datetime.now()
        }
        
        transaction = self.env['pos.payment.transaction'].create(transaction_vals)
        
        return transaction
    
    def action_view_order(self):
        """View related order"""
        return {
            'type': 'ir.actions.act_window',
            'name': f'Order - {self.order_id.name}',
            'res_model': 'pos.order',
            'res_id': self.order_id.id,
            'view_mode': 'form',
            'target': 'new'
        }
    
    def action_view_customer(self):
        """View customer details"""
        if not self.partner_id:
            return None
        
        return {
            'type': 'ir.actions.act_window',
            'name': f'Customer - {self.partner_id.name}',
            'res_model': 'res.partner',
            'res_id': self.partner_id.id,
            'view_mode': 'form',
            'target': 'new'
        }
    
    def action_view_payment_method(self):
        """View payment method details"""
        return {
            'type': 'ir.actions.act_window',
            'name': f'Payment Method - {self.payment_method_id.name}',
            'res_model': 'pos.payment.method',
            'res_id': self.payment_method_id.id,
            'view_mode': 'form',
            'target': 'new'
        }
    
    def action_view_terminal(self):
        """View terminal details"""
        if not self.terminal_id:
            return None
        
        return {
            'type': 'ir.actions.act_window',
            'name': f'Terminal - {self.terminal_id.name}',
            'res_model': 'pos.payment.terminal',
            'res_id': self.terminal_id.id,
            'view_mode': 'form',
            'target': 'new'
        }
    
    def action_calculate_fee(self):
        """Calculate fee for current payment method and amount"""
        if not self.payment_method_id or not self.amount:
            return
        
        self.fee = self.payment_method_id.calculate_fee(self.amount)
        self.net_amount = self.amount - self.fee
        
        return True
    
    def action_verify_pin(self):
        """Verify PIN for payment"""
        # This would integrate with PIN verification system
        self.pin_verified = True
        return True
    
    def action_verify_signature(self):
        """Verify signature for payment"""
        # This would integrate with signature verification system
        self.signature_verified = True
        return True
    
    def get_wizard_summary(self):
        """Get wizard summary data"""
        return {
            'session': self.session_id.name,
            'order': self.order_id.name,
            'customer': self.partner_id.name if self.partner_id else 'Not specified',
            'payment_method': self.payment_method_id.name,
            'terminal': self.terminal_id.name if self.terminal_id else 'Not specified',
            'amount': self.amount,
            'fee': self.fee,
            'net_amount': self.net_amount,
            'customer_age': self.customer_age,
            'payment_reference': self.payment_reference,
            'card_number': self.card_number,
            'card_type': self.card_type,
            'card_holder_name': self.card_holder_name,
            'upi_id': self.upi_id,
            'wallet_provider': self.wallet_provider,
            'wallet_transaction_id': self.wallet_transaction_id,
            'requires_pin': self.requires_pin,
            'requires_signature': self.requires_signature,
            'pin_verified': self.pin_verified,
            'signature_verified': self.signature_verified
        }