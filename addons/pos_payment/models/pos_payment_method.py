# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - POS Payment Method
======================================

POS payment method management for kids clothing retail.
"""

from core_framework.orm import BaseModel, CharField, TextField, BooleanField, IntegerField, DateTimeField, Many2OneField, SelectionField, FloatField, One2ManyField, Many2ManyField
from core_framework.orm import Field
from typing import Dict, Any, Optional
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class PosPaymentMethod(BaseModel):
    """POS payment method configuration"""
    
    _name = 'pos.payment.method'
    _description = 'POS Payment Method'
    _table = 'pos_payment_method'
    
    # Basic Information
    name = CharField(
        string='Payment Method Name',
        size=100,
        required=True,
        help='Name of the payment method'
    )
    
    code = CharField(
        string='Payment Method Code',
        size=20,
        required=True,
        help='Short code for the payment method'
    )
    
    description = TextField(
        string='Description',
        help='Description of the payment method'
    )
    
    # Payment Type
    payment_type = SelectionField(
        string='Payment Type',
        selection=[
            ('cash', 'Cash'),
            ('card', 'Card'),
            ('digital', 'Digital Payment'),
            ('upi', 'UPI'),
            ('wallet', 'Wallet'),
            ('netbanking', 'Net Banking'),
            ('emi', 'EMI'),
            ('loyalty', 'Loyalty Points'),
            ('gift_card', 'Gift Card'),
            ('store_credit', 'Store Credit'),
            ('other', 'Other')
        ],
        required=True,
        help='Type of payment method'
    )
    
    # Configuration
    is_active = BooleanField(
        string='Active',
        default=True,
        help='Whether this payment method is active'
    )
    
    is_default = BooleanField(
        string='Default',
        default=False,
        help='Whether this is the default payment method'
    )
    
    requires_confirmation = BooleanField(
        string='Requires Confirmation',
        default=False,
        help='Whether this payment method requires confirmation'
    )
    
    # POS Configuration
    config_ids = Many2ManyField(
        'pos.config',
        string='POS Configurations',
        help='POS configurations where this payment method is available'
    )
    
    # Payment Processing
    payment_provider = SelectionField(
        string='Payment Provider',
        selection=[
            ('manual', 'Manual'),
            ('razorpay', 'Razorpay'),
            ('payu', 'PayU'),
            ('paytm', 'Paytm'),
            ('phonepe', 'PhonePe'),
            ('google_pay', 'Google Pay'),
            ('other', 'Other')
        ],
        default='manual',
        help='Payment processing provider'
    )
    
    # Fees and Charges
    has_fees = BooleanField(
        string='Has Fees',
        default=False,
        help='Whether this payment method has processing fees'
    )
    
    fee_type = SelectionField(
        string='Fee Type',
        selection=[
            ('fixed', 'Fixed Amount'),
            ('percentage', 'Percentage'),
            ('tiered', 'Tiered')
        ],
        help='Type of fee calculation'
    )
    
    fee_amount = FloatField(
        string='Fee Amount',
        digits=(12, 2),
        default=0.0,
        help='Fixed fee amount'
    )
    
    fee_percentage = FloatField(
        string='Fee Percentage',
        digits=(5, 2),
        default=0.0,
        help='Fee percentage'
    )
    
    # Limits and Restrictions
    min_amount = FloatField(
        string='Minimum Amount',
        digits=(12, 2),
        default=0.0,
        help='Minimum transaction amount'
    )
    
    max_amount = FloatField(
        string='Maximum Amount',
        digits=(12, 2),
        default=0.0,
        help='Maximum transaction amount'
    )
    
    daily_limit = FloatField(
        string='Daily Limit',
        digits=(12, 2),
        default=0.0,
        help='Daily transaction limit'
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
        help='Age group restriction for this payment method'
    )
    
    requires_adult_supervision = BooleanField(
        string='Requires Adult Supervision',
        default=False,
        help='Whether this payment method requires adult supervision'
    )
    
    # Security Settings
    requires_pin = BooleanField(
        string='Requires PIN',
        default=False,
        help='Whether this payment method requires PIN verification'
    )
    
    requires_signature = BooleanField(
        string='Requires Signature',
        default=False,
        help='Whether this payment method requires signature'
    )
    
    # Integration Settings
    api_endpoint = CharField(
        string='API Endpoint',
        size=200,
        help='API endpoint for payment processing'
    )
    
    api_key = CharField(
        string='API Key',
        size=100,
        help='API key for payment processing'
    )
    
    webhook_url = CharField(
        string='Webhook URL',
        size=200,
        help='Webhook URL for payment notifications'
    )
    
    # Display Settings
    icon = CharField(
        string='Icon',
        size=50,
        help='Icon for display'
    )
    
    color = CharField(
        string='Color',
        size=20,
        default='#007bff',
        help='Color for display'
    )
    
    sequence = IntegerField(
        string='Sequence',
        default=10,
        help='Display sequence'
    )
    
    # Usage Statistics
    usage_count = IntegerField(
        string='Usage Count',
        default=0,
        help='Number of times this payment method has been used'
    )
    
    total_amount = FloatField(
        string='Total Amount',
        digits=(12, 2),
        default=0.0,
        help='Total amount processed through this payment method'
    )
    
    last_used = DateTimeField(
        string='Last Used',
        help='When this payment method was last used'
    )
    
    # Notes
    note = TextField(
        string='Notes',
        help='Additional notes about this payment method'
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
        
        # Update usage count if payment method is used
        if 'usage_count' in vals:
            self.last_used = datetime.now()
        
        return result
    
    def action_view_transactions(self):
        """View transactions for this payment method"""
        return {
            'type': 'ir.actions.act_window',
            'name': f'Transactions - {self.name}',
            'res_model': 'pos.payment.transaction',
            'view_mode': 'tree,form',
            'domain': [('payment_method_id', '=', self.id)],
            'context': {'default_payment_method_id': self.id}
        }
    
    def get_payment_method_summary(self):
        """Get payment method summary data"""
        return {
            'payment_method_name': self.name,
            'payment_method_code': self.code,
            'payment_type': self.payment_type,
            'is_active': self.is_active,
            'is_default': self.is_default,
            'requires_confirmation': self.requires_confirmation,
            'payment_provider': self.payment_provider,
            'has_fees': self.has_fees,
            'fee_type': self.fee_type,
            'fee_amount': self.fee_amount,
            'fee_percentage': self.fee_percentage,
            'min_amount': self.min_amount,
            'max_amount': self.max_amount,
            'daily_limit': self.daily_limit,
            'age_group_restriction': self.age_group_restriction,
            'requires_adult_supervision': self.requires_adult_supervision,
            'requires_pin': self.requires_pin,
            'requires_signature': self.requires_signature,
            'usage_count': self.usage_count,
            'total_amount': self.total_amount,
            'last_used': self.last_used
        }
    
    def validate_age_group(self, customer_age):
        """Validate if payment method applies to customer age group"""
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
    
    def validate_amount(self, amount):
        """Validate transaction amount"""
        if self.min_amount > 0 and amount < self.min_amount:
            return False, f"Amount must be at least {self.min_amount}"
        
        if self.max_amount > 0 and amount > self.max_amount:
            return False, f"Amount cannot exceed {self.max_amount}"
        
        return True, "Valid amount"
    
    def calculate_fee(self, amount):
        """Calculate processing fee for amount"""
        if not self.has_fees:
            return 0.0
        
        if self.fee_type == 'fixed':
            return self.fee_amount
        elif self.fee_type == 'percentage':
            return amount * (self.fee_percentage / 100)
        elif self.fee_type == 'tiered':
            # Implement tiered fee calculation
            return 0.0
        
        return 0.0
    
    def process_payment(self, amount, transaction_data=None):
        """Process payment through this method"""
        # Validate amount
        is_valid, message = self.validate_amount(amount)
        if not is_valid:
            raise ValueError(message)
        
        # Calculate fee
        fee = self.calculate_fee(amount)
        
        # Process payment based on provider
        if self.payment_provider == 'manual':
            return self._process_manual_payment(amount, fee, transaction_data)
        elif self.payment_provider == 'razorpay':
            return self._process_razorpay_payment(amount, fee, transaction_data)
        elif self.payment_provider == 'payu':
            return self._process_payu_payment(amount, fee, transaction_data)
        else:
            return self._process_manual_payment(amount, fee, transaction_data)
    
    def _process_manual_payment(self, amount, fee, transaction_data):
        """Process manual payment"""
        return {
            'status': 'success',
            'transaction_id': f"MANUAL_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            'amount': amount,
            'fee': fee,
            'net_amount': amount - fee,
            'provider_response': 'Manual payment processed'
        }
    
    def _process_razorpay_payment(self, amount, fee, transaction_data):
        """Process Razorpay payment"""
        # This would integrate with Razorpay API
        return {
            'status': 'success',
            'transaction_id': f"RAZORPAY_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            'amount': amount,
            'fee': fee,
            'net_amount': amount - fee,
            'provider_response': 'Razorpay payment processed'
        }
    
    def _process_payu_payment(self, amount, fee, transaction_data):
        """Process PayU payment"""
        # This would integrate with PayU API
        return {
            'status': 'success',
            'transaction_id': f"PAYU_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            'amount': amount,
            'fee': fee,
            'net_amount': amount - fee,
            'provider_response': 'PayU payment processed'
        }