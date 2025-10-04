# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - POS Return Line
===================================

POS return line management for kids clothing retail.
"""

from core_framework.orm import BaseModel, CharField, TextField, BooleanField, IntegerField, DateTimeField, Many2OneField, SelectionField, FloatField, One2ManyField, Many2ManyField
from core_framework.orm import Field
from typing import Dict, Any, Optional
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class PosReturnLine(BaseModel):
    """POS return line for individual product returns"""
    
    _name = 'pos.return.line'
    _description = 'POS Return Line'
    _table = 'pos_return_line'
    
    # Basic Information
    return_id = Many2OneField(
        'pos.return',
        string='Return',
        required=True,
        help='POS return for this line'
    )
    
    session_id = Many2OneField(
        'pos.session',
        string='Session',
        related='return_id.session_id',
        store=True,
        help='POS session'
    )
    
    sequence = IntegerField(
        string='Sequence',
        default=10,
        help='Line sequence'
    )
    
    # Product Information
    product_id = Many2OneField(
        'product.template',
        string='Product',
        required=True,
        help='Product being returned'
    )
    
    product_name = CharField(
        string='Product Name',
        size=200,
        help='Product name (for display)'
    )
    
    product_code = CharField(
        string='Product Code',
        size=50,
        help='Product code (for display)'
    )
    
    # Quantity and Pricing
    return_qty = FloatField(
        string='Return Quantity',
        digits=(12, 3),
        default=1.0,
        help='Quantity being returned'
    )
    
    original_qty = FloatField(
        string='Original Quantity',
        digits=(12, 3),
        help='Original quantity purchased'
    )
    
    original_price = FloatField(
        string='Original Price',
        digits=(12, 2),
        help='Original product price'
    )
    
    # Return Amounts
    return_amount = FloatField(
        string='Return Amount',
        digits=(12, 2),
        default=0.0,
        help='Amount for this return line'
    )
    
    refund_amount = FloatField(
        string='Refund Amount',
        digits=(12, 2),
        default=0.0,
        help='Amount refunded for this line'
    )
    
    # Return Details
    return_reason = SelectionField(
        string='Return Reason',
        selection=[
            ('defective', 'Defective'),
            ('damaged', 'Damaged'),
            ('wrong_size', 'Wrong Size'),
            ('wrong_color', 'Wrong Color'),
            ('wrong_item', 'Wrong Item'),
            ('not_as_expected', 'Not As Expected'),
            ('customer_preference', 'Customer Preference'),
            ('quality_issue', 'Quality Issue'),
            ('other', 'Other')
        ],
        help='Reason for this specific return'
    )
    
    # Product Condition
    product_condition = SelectionField(
        string='Product Condition',
        selection=[
            ('new', 'New'),
            ('used', 'Used'),
            ('defective', 'Defective'),
            ('damaged', 'Damaged'),
            ('worn', 'Worn')
        ],
        default='new',
        help='Condition of returned product'
    )
    
    # Size Information
    product_size = CharField(
        string='Product Size',
        size=20,
        help='Size of returned product'
    )
    
    # Color Information
    product_color = CharField(
        string='Product Color',
        size=50,
        help='Color of returned product'
    )
    
    # Age-based Information
    customer_age = IntegerField(
        string='Customer Age',
        help='Age of the customer'
    )
    
    # Return Policy
    within_policy = BooleanField(
        string='Within Policy',
        default=True,
        help='Whether this return is within policy'
    )
    
    policy_notes = TextField(
        string='Policy Notes',
        help='Notes about return policy application'
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
    
    # Notes
    note = TextField(
        string='Notes',
        help='Line notes and comments'
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
        if 'product_id' in vals:
            product = self.env['product.template'].browse(vals['product_id'])
            vals['product_name'] = product.name
            vals['product_code'] = product.default_code or ''
            vals['original_price'] = product.list_price
        
        return super().create(vals)
    
    def write(self, vals):
        """Override write to update amounts"""
        result = super().write(vals)
        
        # Update amounts when pricing changes
        if any(field in vals for field in ['return_qty', 'original_price', 'refund_percentage']):
            self._update_amounts()
        
        return result
    
    def _update_amounts(self):
        """Update line amounts"""
        for line in self:
            # Calculate return amount
            return_amount = line.return_qty * line.original_price
            line.return_amount = return_amount
            
            # Calculate refund amount based on percentage
            refund_amount = return_amount * (line.refund_percentage / 100)
            line.refund_amount = refund_amount
            
            # Calculate store credit amount
            store_credit_amount = return_amount - refund_amount
            line.store_credit_amount = store_credit_amount
    
    def action_validate_return(self):
        """Validate this return line"""
        errors = []
        
        # Check required fields
        if not self.product_id:
            errors.append("Product is required")
        
        if not self.return_qty or self.return_qty <= 0:
            errors.append("Return quantity must be greater than 0")
        
        if not self.original_price or self.original_price < 0:
            errors.append("Original price must be greater than or equal to 0")
        
        # Check if return quantity exceeds original quantity
        if self.original_qty and self.return_qty > self.original_qty:
            errors.append("Return quantity cannot exceed original quantity")
        
        # Check refund percentage
        if self.refund_percentage < 0 or self.refund_percentage > 100:
            errors.append("Refund percentage must be between 0 and 100")
        
        # Check age-based policies
        if self.customer_age and self.customer_age < 3:
            # Special policy for toddlers
            if self.product_condition in ['defective', 'damaged']:
                self.policy_notes = "Toddler item return - special policy applied"
                self.refund_percentage = 100.0
        
        if errors:
            raise ValueError('\n'.join(errors))
        
        return True
    
    def action_view_product(self):
        """View product details"""
        return {
            'type': 'ir.actions.act_window',
            'name': f'Product - {self.product_name}',
            'res_model': 'product.template',
            'res_id': self.product_id.id,
            'view_mode': 'form',
            'target': 'new'
        }
    
    def get_line_summary(self):
        """Get line summary data"""
        return {
            'product_name': self.product_name,
            'product_code': self.product_code,
            'return_qty': self.return_qty,
            'original_qty': self.original_qty,
            'original_price': self.original_price,
            'return_amount': self.return_amount,
            'refund_amount': self.refund_amount,
            'return_reason': self.return_reason,
            'product_condition': self.product_condition,
            'product_size': self.product_size,
            'product_color': self.product_color,
            'customer_age': self.customer_age,
            'within_policy': self.within_policy,
            'refund_percentage': self.refund_percentage,
            'store_credit_amount': self.store_credit_amount
        }