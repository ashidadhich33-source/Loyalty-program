#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - POS Quick Sale Wizard
=========================================

Quick sale wizard for fast POS transactions.
"""

import logging
from core_framework.orm import BaseModel, CharField, TextField, BooleanField, IntegerField, DateTimeField, Many2OneField, SelectionField, FloatField, One2ManyField, Many2ManyField
from core_framework.exceptions import ValidationError

logger = logging.getLogger(__name__)

class PosQuickSaleWizard(BaseModel):
    """Quick sale wizard for fast transactions"""
    
    _name = 'pos.quick.sale.wizard'
    _description = 'POS Quick Sale Wizard'
    _table = 'pos_quick_sale_wizard'
    
    # Product Information
    product_id = Many2OneField(
        'product.template',
        string='Product',
        required=True,
        help='Product for quick sale'
    )
    
    quantity = FloatField(
        string='Quantity',
        digits=(12, 3),
        default=1.0,
        help='Quantity to sell'
    )
    
    unit_price = FloatField(
        string='Unit Price',
        digits=(12, 2),
        help='Unit price of the product'
    )
    
    # Customer Information
    customer_id = Many2OneField(
        'res.partner',
        string='Customer',
        help='Customer for this sale'
    )
    
    # Discount Information
    discount_type = SelectionField(
        string='Discount Type',
        selection=[
            ('percentage', 'Percentage'),
            ('fixed', 'Fixed Amount')
        ],
        help='Type of discount'
    )
    
    discount_rate = FloatField(
        string='Discount Rate',
        digits=(5, 2),
        help='Discount rate (percentage or amount)'
    )
    
    # Payment Information
    payment_method_id = Many2OneField(
        'pos.payment.method',
        string='Payment Method',
        required=True,
        help='Payment method for this sale'
    )
    
    # Calculated Amounts
    subtotal = FloatField(
        string='Subtotal',
        digits=(12, 2),
        readonly=True,
        help='Subtotal amount'
    )
    
    tax_amount = FloatField(
        string='Tax Amount',
        digits=(12, 2),
        readonly=True,
        help='Tax amount'
    )
    
    total_amount = FloatField(
        string='Total Amount',
        digits=(12, 2),
        readonly=True,
        help='Total amount'
    )
    
    # Notes
    notes = TextField(
        string='Notes',
        help='Additional notes for this sale'
    )
    
    # Timestamps
    create_date = DateTimeField(
        string='Created On',
        auto_now_add=True
    )
    
    def create(self, vals):
        """Override create to set defaults"""
        if 'product_id' in vals:
            product = self.env['product.template'].browse(vals['product_id'])
            vals['unit_price'] = product.list_price
        
        return super().create(vals)
    
    def write(self, vals):
        """Override write to update amounts"""
        result = super().write(vals)
        
        # Update amounts when pricing changes
        if any(field in vals for field in ['quantity', 'unit_price', 'discount_rate', 'discount_type']):
            self._update_amounts()
        
        return result
    
    def _update_amounts(self):
        """Update calculated amounts"""
        for wizard in self:
            # Calculate base amount
            base_amount = wizard.quantity * wizard.unit_price
            
            # Apply discount
            discount_amount = 0.0
            if wizard.discount_type == 'percentage' and wizard.discount_rate:
                discount_amount = base_amount * (wizard.discount_rate / 100)
            elif wizard.discount_type == 'fixed' and wizard.discount_rate:
                discount_amount = wizard.discount_rate
            
            # Calculate subtotal
            subtotal = base_amount - discount_amount
            wizard.subtotal = subtotal
            
            # Calculate tax (assuming 18% GST)
            tax_amount = subtotal * 0.18
            wizard.tax_amount = tax_amount
            
            # Calculate total
            wizard.total_amount = subtotal + tax_amount
    
    def action_process_sale(self):
        """Process the quick sale"""
        for wizard in self:
            # Validate wizard data
            wizard._validate_wizard()
            
            # Create POS order
            order = wizard._create_pos_order()
            
            # Create payment
            wizard._create_payment(order)
            
            # Confirm order
            order.action_confirm()
            order.action_done()
        
        return {
            'type': 'ocean.actions.act_window',
            'name': 'Sale Completed',
            'res_model': 'pos.order',
            'res_id': order.id,
            'view_mode': 'form',
            'target': 'new'
        }
    
    def _validate_wizard(self):
        """Validate wizard data"""
        errors = []
        
        # Check required fields
        if not self.product_id:
            errors.append("Product is required")
        
        if not self.quantity or self.quantity <= 0:
            errors.append("Quantity must be greater than 0")
        
        if not self.unit_price or self.unit_price < 0:
            errors.append("Unit price must be greater than or equal to 0")
        
        if not self.payment_method_id:
            errors.append("Payment method is required")
        
        # Check discount
        if self.discount_type == 'percentage' and (self.discount_rate < 0 or self.discount_rate > 100):
            errors.append("Discount percentage must be between 0 and 100")
        
        if self.discount_type == 'fixed' and self.discount_rate < 0:
            errors.append("Discount amount must be greater than or equal to 0")
        
        if errors:
            raise ValidationError('\n'.join(errors))
    
    def _create_pos_order(self):
        """Create POS order from wizard data"""
        # Get active session
        session = self.env['pos.session'].search([
            ('state', '=', 'opened'),
            ('user_id', '=', self.env.user.id)
        ], limit=1)
        
        if not session:
            raise ValidationError("No active POS session found")
        
        # Create order
        order_vals = {
            'session_id': session.id,
            'user_id': self.env.user.id,
            'partner_id': self.customer_id.id if self.customer_id else False,
            'state': 'draft',
            'date_order': self.env['datetime'].now(),
            'amount_untaxed': self.subtotal,
            'amount_tax': self.tax_amount,
            'amount_discount': self._calculate_discount_amount(),
            'amount_total': self.total_amount,
            'note': self.notes
        }
        
        order = self.env['pos.order'].create(order_vals)
        
        # Create order line
        line_vals = {
            'order_id': order.id,
            'product_id': self.product_id.id,
            'product_name': self.product_id.name,
            'product_code': self.product_id.default_code or '',
            'qty': self.quantity,
            'price_unit': self.unit_price,
            'discount_type': self.discount_type,
            'discount_rate': self.discount_rate,
            'price_subtotal': self.subtotal,
            'price_tax': self.tax_amount,
            'price_total': self.total_amount
        }
        
        self.env['pos.order.line'].create(line_vals)
        
        return order
    
    def _create_payment(self, order):
        """Create payment for the order"""
        payment_vals = {
            'order_id': order.id,
            'payment_method_id': self.payment_method_id.id,
            'amount': self.total_amount,
            'state': 'draft',
            'payment_date': self.env['datetime'].now()
        }
        
        # Add payment method specific fields
        if self.payment_method_id.is_cash:
            payment_vals['cash_amount'] = self.total_amount
        elif self.payment_method_id.is_digital:
            payment_vals['digital_payment_id'] = f"DIGITAL_{order.id}"
            payment_vals['digital_payment_status'] = 'success'
        
        payment = self.env['pos.payment'].create(payment_vals)
        payment.action_confirm()
        
        return payment
    
    def _calculate_discount_amount(self):
        """Calculate total discount amount"""
        base_amount = self.quantity * self.unit_price
        
        if self.discount_type == 'percentage' and self.discount_rate:
            return base_amount * (self.discount_rate / 100)
        elif self.discount_type == 'fixed' and self.discount_rate:
            return self.discount_rate
        
        return 0.0