#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - POS Order Models
================================

POS order and order line management.
"""

import logging
from datetime import datetime
from core_framework.orm import BaseModel, CharField, TextField, BooleanField, IntegerField, DateTimeField, Many2OneField, SelectionField, FloatField, One2ManyField, Many2ManyField
from core_framework.exceptions import ValidationError

logger = logging.getLogger(__name__)

class PosOrder(BaseModel):
    """POS order for sales transactions"""
    
    _name = 'pos.order'
    _description = 'POS Order'
    _table = 'pos_order'
    _order = 'create_date desc'
    
    # Basic Information
    name = CharField(
        string='Order Reference',
        size=100,
        required=True,
        help='Order reference number'
    )
    
    session_id = Many2OneField(
        'pos.session',
        string='POS Session',
        required=True,
        help='POS session for this order'
    )
    
    config_id = Many2OneField(
        'pos.config',
        string='POS Configuration',
        related='session_id.config_id',
        help='POS configuration'
    )
    
    user_id = Many2OneField(
        'res.users',
        string='Cashier',
        required=True,
        help='Cashier who processed the order'
    )
    
    # Customer Information
    partner_id = Many2OneField(
        'res.partner',
        string='Customer',
        help='Customer for this order'
    )
    
    customer_name = CharField(
        string='Customer Name',
        size=100,
        help='Customer name if no customer record'
    )
    
    customer_phone = CharField(
        string='Customer Phone',
        size=20,
        help='Customer phone number'
    )
    
    customer_email = CharField(
        string='Customer Email',
        size=100,
        help='Customer email address'
    )
    
    # Order Status
    state = SelectionField(
        string='Status',
        selection=[
            ('draft', 'Draft'),
            ('confirmed', 'Confirmed'),
            ('paid', 'Paid'),
            ('done', 'Done'),
            ('cancelled', 'Cancelled')
        ],
        default='draft',
        help='Order status'
    )
    
    # Order Lines
    order_line_ids = One2ManyField(
        string='Order Lines',
        comodel_name='pos.order.line',
        inverse_name='order_id',
        help='Order lines'
    )
    
    # Pricing Information
    amount_untaxed = FloatField(
        string='Untaxed Amount',
        digits=(12, 2),
        default=0.0,
        help='Amount without tax'
    )
    
    amount_tax = FloatField(
        string='Tax Amount',
        digits=(12, 2),
        default=0.0,
        help='Tax amount'
    )
    
    amount_total = FloatField(
        string='Total Amount',
        digits=(12, 2),
        default=0.0,
        help='Total amount including tax'
    )
    
    # Discount Information
    discount_type = SelectionField(
        string='Discount Type',
        selection=[
            ('percentage', 'Percentage'),
            ('fixed', 'Fixed Amount')
        ],
        default='percentage',
        help='Type of discount applied'
    )
    
    discount_percentage = FloatField(
        string='Discount %',
        digits=(5, 2),
        default=0.0,
        help='Discount percentage'
    )
    
    discount_amount = FloatField(
        string='Discount Amount',
        digits=(12, 2),
        default=0.0,
        help='Discount amount'
    )
    
    # Payment Information
    payment_method = SelectionField(
        string='Payment Method',
        selection=[
            ('cash', 'Cash'),
            ('card', 'Card'),
            ('upi', 'UPI'),
            ('wallet', 'Wallet'),
            ('mixed', 'Mixed Payment')
        ],
        help='Primary payment method'
    )
    
    cash_amount = FloatField(
        string='Cash Amount',
        digits=(12, 2),
        default=0.0,
        help='Cash payment amount'
    )
    
    card_amount = FloatField(
        string='Card Amount',
        digits=(12, 2),
        default=0.0,
        help='Card payment amount'
    )
    
    upi_amount = FloatField(
        string='UPI Amount',
        digits=(12, 2),
        default=0.0,
        help='UPI payment amount'
    )
    
    wallet_amount = FloatField(
        string='Wallet Amount',
        digits=(12, 2),
        default=0.0,
        help='Wallet payment amount'
    )
    
    # Loyalty Information
    loyalty_points_earned = IntegerField(
        string='Loyalty Points Earned',
        default=0,
        help='Loyalty points earned from this order'
    )
    
    loyalty_points_redeemed = IntegerField(
        string='Loyalty Points Redeemed',
        default=0,
        help='Loyalty points redeemed in this order'
    )
    
    loyalty_discount_amount = FloatField(
        string='Loyalty Discount',
        digits=(12, 2),
        default=0.0,
        help='Discount amount from loyalty points'
    )
    
    # Order Statistics
    total_items = IntegerField(
        string='Total Items',
        default=0,
        help='Total number of items in order'
    )
    
    total_quantity = IntegerField(
        string='Total Quantity',
        default=0,
        help='Total quantity of items'
    )
    
    # Receipt Information
    receipt_number = CharField(
        string='Receipt Number',
        size=50,
        help='Receipt number'
    )
    
    receipt_printed = BooleanField(
        string='Receipt Printed',
        default=False,
        help='Whether receipt has been printed'
    )
    
    # Notes
    notes = TextField(
        string='Notes',
        help='Order notes'
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
            vals['name'] = self._generate_order_reference()
        
        return super().create(vals)
    
    def write(self, vals):
        """Override write to update calculations"""
        result = super().write(vals)
        
        # Update calculations if order lines changed
        if 'order_line_ids' in vals:
            for record in self:
                record._update_order_calculations()
        
        return result
    
    def _generate_order_reference(self):
        """Generate order reference"""
        # This would use sequence generation
        return f"POS{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    def _update_order_calculations(self):
        """Update order calculations"""
        for record in self:
            # Calculate totals from order lines
            total_untaxed = 0.0
            total_tax = 0.0
            total_items = 0
            total_quantity = 0
            
            for line in record.order_line_ids:
                total_untaxed += line.price_subtotal
                total_tax += line.price_tax
                total_items += 1
                total_quantity += line.quantity
            
            # Apply discount
            if record.discount_type == 'percentage':
                discount_amount = (total_untaxed * record.discount_percentage) / 100
            else:
                discount_amount = record.discount_amount
            
            # Update fields
            record.amount_untaxed = total_untaxed - discount_amount
            record.amount_tax = total_tax
            record.amount_total = record.amount_untaxed + record.amount_tax
            record.total_items = total_items
            record.total_quantity = total_quantity
            record.discount_amount = discount_amount
    
    def action_confirm_order(self):
        """Confirm the order"""
        for record in self:
            if record.state == 'draft':
                record.state = 'confirmed'
                record._update_order_calculations()
    
    def action_pay_order(self):
        """Mark order as paid"""
        for record in self:
            if record.state == 'confirmed':
                record.state = 'paid'
                record._process_payment()
    
    def action_done_order(self):
        """Mark order as done"""
        for record in self:
            if record.state == 'paid':
                record.state = 'done'
                record._process_loyalty_points()
                record._create_stock_moves()
    
    def action_cancel_order(self):
        """Cancel the order"""
        for record in self:
            if record.state in ['draft', 'confirmed']:
                record.state = 'cancelled'
    
    def _process_payment(self):
        """Process payment for the order"""
        for record in self:
            # Calculate payment amounts
            total_payment = record.cash_amount + record.card_amount + record.upi_amount + record.wallet_amount
            
            # Validate payment amount
            if abs(total_payment - record.amount_total) > 0.01:
                raise ValidationError("Payment amount does not match order total")
    
    def _process_loyalty_points(self):
        """Process loyalty points for the order"""
        for record in self:
            if record.partner_id and record.config_id.enable_loyalty:
                # Calculate points earned
                points_earned = int(record.amount_total * record.config_id.loyalty_points_per_rupee)
                record.loyalty_points_earned = points_earned
                
                # Update customer loyalty points
                if hasattr(record.partner_id, 'loyalty_points'):
                    record.partner_id.loyalty_points += points_earned
    
    def _create_stock_moves(self):
        """Create stock moves for the order"""
        for record in self:
            if record.config_id.auto_create_picking:
                # This would create stock moves for inventory
                pass
    
    def get_order_summary(self):
        """Get order summary"""
        return {
            'order_info': {
                'name': self.name,
                'customer': self.partner_id.name if self.partner_id else self.customer_name,
                'cashier': self.user_id.name,
                'status': self.state,
                'date': self.create_date
            },
            'pricing': {
                'untaxed_amount': self.amount_untaxed,
                'tax_amount': self.amount_tax,
                'total_amount': self.amount_total,
                'discount_amount': self.discount_amount
            },
            'payment': {
                'method': self.payment_method,
                'cash': self.cash_amount,
                'card': self.card_amount,
                'upi': self.upi_amount,
                'wallet': self.wallet_amount
            },
            'loyalty': {
                'points_earned': self.loyalty_points_earned,
                'points_redeemed': self.loyalty_points_redeemed,
                'discount_amount': self.loyalty_discount_amount
            },
            'items': {
                'total_items': self.total_items,
                'total_quantity': self.total_quantity
            }
        }
    
    def action_print_receipt(self):
        """Print receipt for the order"""
        for record in self:
            record.receipt_printed = True
            # This would trigger receipt printing
            return {
                'type': 'ocean.actions.act_url',
                'url': f'/pos/receipt/{record.id}',
                'target': 'new'
            }
    
    def action_view_order_lines(self):
        """View order lines"""
        return {
            'type': 'ocean.actions.act_window',
            'name': f'Order Lines - {self.name}',
            'res_model': 'pos.order.line',
            'view_mode': 'tree,form',
            'domain': [('order_id', '=', self.id)],
            'context': {'default_order_id': self.id}
        }


class PosOrderLine(BaseModel):
    """POS order line for individual items"""
    
    _name = 'pos.order.line'
    _description = 'POS Order Line'
    _table = 'pos_order_line'
    _order = 'sequence, id'
    
    # Basic Information
    order_id = Many2OneField(
        'pos.order',
        string='Order',
        required=True,
        help='Parent order'
    )
    
    product_id = Many2OneField(
        'product.product',
        string='Product',
        required=True,
        help='Product for this line'
    )
    
    product_name = CharField(
        string='Product Name',
        size=200,
        help='Product name'
    )
    
    product_code = CharField(
        string='Product Code',
        size=50,
        help='Product code'
    )
    
    # Quantity and Pricing
    quantity = FloatField(
        string='Quantity',
        digits=(10, 3),
        default=1.0,
        help='Quantity ordered'
    )
    
    price_unit = FloatField(
        string='Unit Price',
        digits=(12, 2),
        help='Unit price'
    )
    
    price_subtotal = FloatField(
        string='Subtotal',
        digits=(12, 2),
        help='Subtotal without tax'
    )
    
    price_tax = FloatField(
        string='Tax Amount',
        digits=(12, 2),
        help='Tax amount'
    )
    
    price_total = FloatField(
        string='Total',
        digits=(12, 2),
        help='Total price including tax'
    )
    
    # Discount Information
    discount_type = SelectionField(
        string='Discount Type',
        selection=[
            ('percentage', 'Percentage'),
            ('fixed', 'Fixed Amount')
        ],
        default='percentage',
        help='Type of discount'
    )
    
    discount_percentage = FloatField(
        string='Discount %',
        digits=(5, 2),
        default=0.0,
        help='Discount percentage'
    )
    
    discount_amount = FloatField(
        string='Discount Amount',
        digits=(12, 2),
        default=0.0,
        help='Discount amount'
    )
    
    # Product Attributes
    size = CharField(
        string='Size',
        size=20,
        help='Product size'
    )
    
    color = CharField(
        string='Color',
        size=50,
        help='Product color'
    )
    
    age_group = SelectionField(
        string='Age Group',
        selection=[
            ('newborn', 'Newborn (0-6 months)'),
            ('infant', 'Infant (6-12 months)'),
            ('toddler', 'Toddler (1-3 years)'),
            ('preschool', 'Preschool (3-5 years)'),
            ('school', 'School (5-12 years)'),
            ('teen', 'Teen (12+ years)')
        ],
        help='Target age group'
    )
    
    gender = SelectionField(
        string='Gender',
        selection=[
            ('boys', 'Boys'),
            ('girls', 'Girls'),
            ('unisex', 'Unisex')
        ],
        help='Target gender'
    )
    
    # Display Order
    sequence = IntegerField(
        string='Sequence',
        default=10,
        help='Display order'
    )
    
    # Notes
    notes = TextField(
        string='Notes',
        help='Line notes'
    )
    
    def create(self, vals):
        """Override create to set defaults"""
        result = super().create(vals)
        
        # Update calculations
        for record in result:
            record._update_line_calculations()
        
        return result
    
    def write(self, vals):
        """Override write to update calculations"""
        result = super().write(vals)
        
        # Update calculations if pricing changed
        if any(field in vals for field in ['quantity', 'price_unit', 'discount_percentage', 'discount_amount']):
            for record in self:
                record._update_line_calculations()
        
        return result
    
    def _update_line_calculations(self):
        """Update line calculations"""
        for record in self:
            # Calculate subtotal
            subtotal = record.quantity * record.price_unit
            
            # Apply discount
            if record.discount_type == 'percentage':
                discount_amount = (subtotal * record.discount_percentage) / 100
            else:
                discount_amount = record.discount_amount
            
            # Update fields
            record.price_subtotal = subtotal - discount_amount
            record.discount_amount = discount_amount
            
            # Calculate tax (simplified)
            tax_rate = 0.18  # 18% GST
            record.price_tax = record.price_subtotal * tax_rate
            record.price_total = record.price_subtotal + record.price_tax
    
    def get_line_summary(self):
        """Get line summary"""
        return {
            'product_info': {
                'name': self.product_name,
                'code': self.product_code,
                'size': self.size,
                'color': self.color,
                'age_group': self.age_group,
                'gender': self.gender
            },
            'pricing': {
                'quantity': self.quantity,
                'unit_price': self.price_unit,
                'subtotal': self.price_subtotal,
                'tax': self.price_tax,
                'total': self.price_total,
                'discount': self.discount_amount
            }
        }