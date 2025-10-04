# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - POS Exchange Line
=====================================

POS exchange line management for kids clothing retail.
"""

from core_framework.orm import BaseModel, CharField, TextField, BooleanField, IntegerField, DateTimeField, Many2OneField, SelectionField, FloatField, One2ManyField, Many2ManyField
from core_framework.orm import Field
from typing import Dict, Any, Optional
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class PosExchangeLine(BaseModel):
    """POS exchange line for individual product exchanges"""
    
    _name = 'pos.exchange.line'
    _description = 'POS Exchange Line'
    _table = 'pos_exchange_line'
    
    # Basic Information
    exchange_id = Many2OneField(
        'pos.exchange',
        string='Exchange',
        required=True,
        help='POS exchange for this line'
    )
    
    session_id = Many2OneField(
        'pos.session',
        string='Session',
        related='exchange_id.session_id',
        store=True,
        help='POS session'
    )
    
    sequence = IntegerField(
        string='Sequence',
        default=10,
        help='Line sequence'
    )
    
    # Original Product Information
    original_product_id = Many2OneField(
        'product.template',
        string='Original Product',
        required=True,
        help='Product being returned'
    )
    
    original_product_name = CharField(
        string='Original Product Name',
        size=200,
        help='Original product name (for display)'
    )
    
    original_product_code = CharField(
        string='Original Product Code',
        size=50,
        help='Original product code (for display)'
    )
    
    # New Product Information
    new_product_id = Many2OneField(
        'product.template',
        string='New Product',
        required=True,
        help='Product being exchanged for'
    )
    
    new_product_name = CharField(
        string='New Product Name',
        size=200,
        help='New product name (for display)'
    )
    
    new_product_code = CharField(
        string='New Product Code',
        size=50,
        help='New product code (for display)'
    )
    
    # Quantities
    return_qty = FloatField(
        string='Return Quantity',
        digits=(12, 3),
        default=1.0,
        help='Quantity being returned'
    )
    
    exchange_qty = FloatField(
        string='Exchange Quantity',
        digits=(12, 3),
        default=1.0,
        help='Quantity being exchanged for'
    )
    
    # Pricing
    original_price = FloatField(
        string='Original Price',
        digits=(12, 2),
        help='Original product price'
    )
    
    new_price = FloatField(
        string='New Price',
        digits=(12, 2),
        help='New product price'
    )
    
    # Amounts
    return_amount = FloatField(
        string='Return Amount',
        digits=(12, 2),
        default=0.0,
        help='Amount returned to customer'
    )
    
    charge_amount = FloatField(
        string='Charge Amount',
        digits=(12, 2),
        default=0.0,
        help='Amount charged to customer'
    )
    
    line_difference = FloatField(
        string='Line Difference',
        digits=(12, 2),
        default=0.0,
        help='Difference amount for this line'
    )
    
    # Exchange Details
    exchange_reason = SelectionField(
        string='Exchange Reason',
        selection=[
            ('size_too_small', 'Size Too Small'),
            ('size_too_large', 'Size Too Large'),
            ('wrong_color', 'Wrong Color'),
            ('wrong_style', 'Wrong Style'),
            ('defective', 'Defective'),
            ('damaged', 'Damaged'),
            ('not_as_expected', 'Not As Expected'),
            ('customer_preference', 'Customer Preference'),
            ('other', 'Other')
        ],
        help='Reason for this specific exchange'
    )
    
    # Size Information
    original_size = CharField(
        string='Original Size',
        size=20,
        help='Size of original product'
    )
    
    new_size = CharField(
        string='New Size',
        size=20,
        help='Size of new product'
    )
    
    # Color Information
    original_color = CharField(
        string='Original Color',
        size=50,
        help='Color of original product'
    )
    
    new_color = CharField(
        string='New Color',
        size=50,
        help='Color of new product'
    )
    
    # Age-based Information
    customer_age = IntegerField(
        string='Customer Age',
        help='Age of the customer'
    )
    
    # Exchange Policy
    within_policy = BooleanField(
        string='Within Policy',
        default=True,
        help='Whether this exchange is within policy'
    )
    
    policy_notes = TextField(
        string='Policy Notes',
        help='Notes about exchange policy application'
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
        if 'original_product_id' in vals:
            product = self.env['product.template'].browse(vals['original_product_id'])
            vals['original_product_name'] = product.name
            vals['original_product_code'] = product.default_code or ''
            vals['original_price'] = product.list_price
        
        if 'new_product_id' in vals:
            product = self.env['product.template'].browse(vals['new_product_id'])
            vals['new_product_name'] = product.name
            vals['new_product_code'] = product.default_code or ''
            vals['new_price'] = product.list_price
        
        return super().create(vals)
    
    def write(self, vals):
        """Override write to update amounts"""
        result = super().write(vals)
        
        # Update amounts when pricing changes
        if any(field in vals for field in ['return_qty', 'exchange_qty', 'original_price', 'new_price']):
            self._update_amounts()
        
        return result
    
    def _update_amounts(self):
        """Update line amounts"""
        for line in self:
            # Calculate return amount
            return_amount = line.return_qty * line.original_price
            line.return_amount = return_amount
            
            # Calculate charge amount
            charge_amount = line.exchange_qty * line.new_price
            line.charge_amount = charge_amount
            
            # Calculate difference
            line.line_difference = charge_amount - return_amount
    
    def action_validate_exchange(self):
        """Validate this exchange line"""
        errors = []
        
        # Check required fields
        if not self.original_product_id:
            errors.append("Original product is required")
        
        if not self.new_product_id:
            errors.append("New product is required")
        
        if not self.return_qty or self.return_qty <= 0:
            errors.append("Return quantity must be greater than 0")
        
        if not self.exchange_qty or self.exchange_qty <= 0:
            errors.append("Exchange quantity must be greater than 0")
        
        # Check if products are different
        if self.original_product_id == self.new_product_id:
            errors.append("Original and new products must be different")
        
        # Check age-based policies
        if self.customer_age and self.customer_age < 3:
            # Special policy for toddlers
            if self.exchange_reason in ['defective', 'damaged']:
                self.policy_notes = "Toddler item exchange - special policy applied"
        
        if errors:
            raise ValueError('\n'.join(errors))
        
        return True
    
    def action_view_original_product(self):
        """View original product details"""
        return {
            'type': 'ir.actions.act_window',
            'name': f'Original Product - {self.original_product_name}',
            'res_model': 'product.template',
            'res_id': self.original_product_id.id,
            'view_mode': 'form',
            'target': 'new'
        }
    
    def action_view_new_product(self):
        """View new product details"""
        return {
            'type': 'ir.actions.act_window',
            'name': f'New Product - {self.new_product_name}',
            'res_model': 'product.template',
            'res_id': self.new_product_id.id,
            'view_mode': 'form',
            'target': 'new'
        }
    
    def get_line_summary(self):
        """Get line summary data"""
        return {
            'original_product': self.original_product_name,
            'new_product': self.new_product_name,
            'return_qty': self.return_qty,
            'exchange_qty': self.exchange_qty,
            'original_price': self.original_price,
            'new_price': self.new_price,
            'return_amount': self.return_amount,
            'charge_amount': self.charge_amount,
            'line_difference': self.line_difference,
            'exchange_reason': self.exchange_reason,
            'original_size': self.original_size,
            'new_size': self.new_size,
            'original_color': self.original_color,
            'new_color': self.new_color,
            'customer_age': self.customer_age,
            'within_policy': self.within_policy
        }