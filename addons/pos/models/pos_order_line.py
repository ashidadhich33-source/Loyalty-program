# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - POS Order Line
==================================

POS order line management for kids clothing retail.
"""

from core_framework.orm import BaseModel, CharField, TextField, BooleanField, IntegerField, DateTimeField, Many2OneField, SelectionField, FloatField, One2ManyField, Many2ManyField
from core_framework.orm import Field
from typing import Dict, Any, Optional
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class PosOrderLine(BaseModel):
    """POS order line for individual products"""
    
    _name = 'pos.order.line'
    _description = 'POS Order Line'
    _table = 'pos_order_line'
    
    # Basic Information
    order_id = Many2OneField(
        'pos.order',
        string='Order',
        required=True,
        help='POS order for this line'
    )
    
    session_id = Many2OneField(
        'pos.session',
        string='Session',
        related='order_id.session_id',
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
        help='Product for this line'
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
    qty = FloatField(
        string='Quantity',
        digits=(12, 3),
        default=1.0,
        help='Quantity ordered'
    )
    
    price_unit = FloatField(
        string='Unit Price',
        digits=(12, 2),
        help='Unit price of the product'
    )
    
    # Discount Information
    discount_type = SelectionField(
        string='Discount Type',
        selection=[
            ('percentage', 'Percentage'),
            ('fixed', 'Fixed Amount')
        ],
        help='Type of discount applied'
    )
    
    discount_rate = FloatField(
        string='Discount Rate',
        digits=(5, 2),
        help='Discount rate (percentage or amount)'
    )
    
    discount_amount = FloatField(
        string='Discount Amount',
        digits=(12, 2),
        default=0.0,
        help='Total discount amount for this line'
    )
    
    # Tax Information
    tax_ids = Many2ManyField(
        'account.tax',
        string='Taxes',
        help='Taxes applied to this line'
    )
    
    # Calculated Amounts
    price_subtotal = FloatField(
        string='Subtotal',
        digits=(12, 2),
        default=0.0,
        help='Subtotal without tax'
    )
    
    price_tax = FloatField(
        string='Tax Amount',
        digits=(12, 2),
        default=0.0,
        help='Tax amount for this line'
    )
    
    price_total = FloatField(
        string='Total',
        digits=(12, 2),
        default=0.0,
        help='Total amount including tax'
    )
    
    # Age-based Information
    customer_age = IntegerField(
        string='Customer Age',
        help='Age of the customer (for age-based discounts)'
    )
    
    age_discount_applied = BooleanField(
        string='Age Discount Applied',
        default=False,
        help='Whether age-based discount was applied'
    )
    
    age_discount_percentage = FloatField(
        string='Age Discount %',
        digits=(5, 2),
        help='Age-based discount percentage'
    )
    
    # Product Attributes
    product_attributes = TextField(
        string='Product Attributes',
        help='Product attributes (size, color, etc.)'
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
            vals['price_unit'] = product.list_price
        
        return super().create(vals)
    
    def write(self, vals):
        """Override write to update amounts"""
        result = super().write(vals)
        
        # Update amounts when pricing changes
        if any(field in vals for field in ['qty', 'price_unit', 'discount_rate', 'discount_type', 'tax_ids']):
            self._update_amounts()
        
        return result
    
    def _update_amounts(self):
        """Update line amounts"""
        for line in self:
            # Calculate base amount
            base_amount = line.qty * line.price_unit
            
            # Apply discount
            discount_amount = 0.0
            if line.discount_type == 'percentage' and line.discount_rate:
                discount_amount = base_amount * (line.discount_rate / 100)
            elif line.discount_type == 'fixed' and line.discount_rate:
                discount_amount = line.discount_rate
            
            line.discount_amount = discount_amount
            
            # Calculate subtotal
            subtotal = base_amount - discount_amount
            line.price_subtotal = subtotal
            
            # Calculate tax
            tax_amount = 0.0
            if line.tax_ids:
                # This would calculate tax based on tax configuration
                # For now, assume 18% GST
                tax_amount = subtotal * 0.18
            
            line.price_tax = tax_amount
            
            # Calculate total
            line.price_total = subtotal + tax_amount
    
    def action_apply_age_discount(self):
        """Apply age-based discount to this line"""
        if not self.customer_age:
            raise ValueError("Customer age is required for age-based discount")
        
        # Get age discount percentage from POS config
        pos_config = self.order_id.config_id
        if not pos_config.enable_age_discount:
            raise ValueError("Age-based discount is not enabled for this POS")
        
        age_discount = pos_config.age_discount_percentage
        
        # Apply discount based on age
        if self.customer_age <= 3:  # Toddler
            age_discount = age_discount * 1.2  # 20% extra discount
        elif self.customer_age <= 12:  # Child
            age_discount = age_discount * 1.1  # 10% extra discount
        
        # Apply the discount
        self.discount_type = 'percentage'
        self.discount_rate = age_discount
        self.age_discount_applied = True
        self.age_discount_percentage = age_discount
        
        # Update amounts
        self._update_amounts()
        
        return True
    
    def action_remove_age_discount(self):
        """Remove age-based discount from this line"""
        if self.age_discount_applied:
            self.discount_type = False
            self.discount_rate = 0.0
            self.age_discount_applied = False
            self.age_discount_percentage = 0.0
            
            # Update amounts
            self._update_amounts()
        
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
            'quantity': self.qty,
            'unit_price': self.price_unit,
            'discount_amount': self.discount_amount,
            'subtotal': self.price_subtotal,
            'tax_amount': self.price_tax,
            'total': self.price_total,
            'age_discount_applied': self.age_discount_applied,
            'customer_age': self.customer_age
        }
    
    def validate_line(self):
        """Validate line data"""
        errors = []
        
        # Check required fields
        if not self.product_id:
            errors.append("Product is required")
        
        if not self.qty or self.qty <= 0:
            errors.append("Quantity must be greater than 0")
        
        if not self.price_unit or self.price_unit < 0:
            errors.append("Unit price must be greater than or equal to 0")
        
        # Check discount
        if self.discount_type == 'percentage' and (self.discount_rate < 0 or self.discount_rate > 100):
            errors.append("Discount percentage must be between 0 and 100")
        
        if self.discount_type == 'fixed' and self.discount_rate < 0:
            errors.append("Discount amount must be greater than or equal to 0")
        
        if errors:
            raise ValueError('\n'.join(errors))
        
        return True