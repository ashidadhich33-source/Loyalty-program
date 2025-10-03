#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Sale Order Line Model
=========================================

Sales order line management for kids clothing retail.
"""

import logging
from core_framework.orm import BaseModel, CharField, TextField, BooleanField, IntegerField, DateTimeField, Many2OneField, SelectionField, FloatField, One2ManyField, Many2ManyField
from core_framework.exceptions import ValidationError

logger = logging.getLogger(__name__)

class SaleOrderLine(BaseModel):
    """Sales order lines for kids clothing retail"""
    
    _name = 'sale.order.line'
    _description = 'Sales Order Line'
    _table = 'sale_order_line'
    _order = 'order_id, sequence, id'
    
    # Basic Information
    name = CharField(
        string='Description',
        size=256,
        required=True,
        help='Description of the order line'
    )
    
    order_id = Many2OneField(
        'sale.order',
        string='Order',
        required=True,
        help='Sales order for this line'
    )
    
    sequence = IntegerField(
        string='Sequence',
        default=10,
        help='Display order'
    )
    
    # Product Information
    product_id = Many2OneField(
        'product.template',
        string='Product',
        required=True,
        help='Product for this line'
    )
    
    product_template_id = Many2OneField(
        'product.template',
        string='Product Template',
        related='product_id',
        help='Product template for this line'
    )
    
    # Product Variants
    product_variant_ids = Many2ManyField(
        'product.variant',
        string='Product Variants',
        help='Product variants for this line'
    )
    
    # Size and Color
    size = CharField(
        string='Size',
        size=20,
        help='Size of the product'
    )
    
    color = CharField(
        string='Color',
        size=50,
        help='Color of the product'
    )
    
    # Quantity and Pricing
    product_uom_qty = FloatField(
        string='Quantity',
        digits=(12, 3),
        default=1.0,
        required=True,
        help='Quantity ordered'
    )
    
    qty_delivered = FloatField(
        string='Delivered Quantity',
        digits=(12, 3),
        default=0.0,
        help='Quantity delivered'
    )
    
    qty_invoiced = FloatField(
        string='Invoiced Quantity',
        digits=(12, 3),
        default=0.0,
        help='Quantity invoiced'
    )
    
    qty_returned = FloatField(
        string='Returned Quantity',
        digits=(12, 3),
        default=0.0,
        help='Quantity returned'
    )
    
    # Pricing
    price_unit = FloatField(
        string='Unit Price',
        digits=(12, 2),
        required=True,
        help='Unit price of the product'
    )
    
    price_subtotal = FloatField(
        string='Subtotal',
        digits=(12, 2),
        compute='_compute_amount',
        help='Subtotal without taxes'
    )
    
    price_total = FloatField(
        string='Total',
        digits=(12, 2),
        compute='_compute_amount',
        help='Total with taxes'
    )
    
    # Discount Information
    discount = FloatField(
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
    
    # Kids Clothing Specific Fields
    age_group = SelectionField(
        string='Age Group',
        selection=[
            ('newborn', 'Newborn (0-6 months)'),
            ('infant', 'Infant (6-12 months)'),
            ('toddler', 'Toddler (1-3 years)'),
            ('preschool', 'Preschool (3-5 years)'),
            ('school', 'School (5-12 years)'),
            ('teen', 'Teen (12+ years)'),
            ('all', 'All Ages')
        ],
        help='Target age group for this product'
    )
    
    gender = SelectionField(
        string='Gender',
        selection=[
            ('boys', 'Boys'),
            ('girls', 'Girls'),
            ('unisex', 'Unisex'),
            ('all', 'All Genders')
        ],
        help='Target gender for this product'
    )
    
    season = SelectionField(
        string='Season',
        selection=[
            ('summer', 'Summer'),
            ('winter', 'Winter'),
            ('monsoon', 'Monsoon'),
            ('all_season', 'All Season'),
            ('festive', 'Festive'),
            ('party', 'Party Wear')
        ],
        help='Seasonal classification for this product'
    )
    
    # Special Requirements
    is_gift = BooleanField(
        string='Gift Item',
        default=False,
        help='Whether this is a gift item'
    )
    
    gift_message = TextField(
        string='Gift Message',
        help='Gift message for this item'
    )
    
    is_exchange = BooleanField(
        string='Exchange Item',
        default=False,
        help='Whether this is an exchange item'
    )
    
    exchange_reason = CharField(
        string='Exchange Reason',
        size=100,
        help='Reason for exchange'
    )
    
    # Customer Preferences
    customer_notes = TextField(
        string='Customer Notes',
        help='Customer notes for this line'
    )
    
    special_instructions = TextField(
        string='Special Instructions',
        help='Special instructions for this line'
    )
    
    # Status
    state = SelectionField(
        string='Status',
        selection=[
            ('draft', 'Draft'),
            ('confirmed', 'Confirmed'),
            ('delivered', 'Delivered'),
            ('invoiced', 'Invoiced'),
            ('returned', 'Returned'),
            ('cancelled', 'Cancelled')
        ],
        default='draft',
        help='Status of this order line'
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
        if 'product_id' in vals and 'name' not in vals:
            product = self.env['product.template'].browse(vals['product_id'])
            vals['name'] = product.name
        
        if 'product_id' in vals and 'price_unit' not in vals:
            product = self.env['product.template'].browse(vals['product_id'])
            vals['price_unit'] = product.list_price
        
        return super().create(vals)
    
    def write(self, vals):
        """Override write to update amounts"""
        result = super().write(vals)
        
        # Update amounts if pricing changed
        if any(field in vals for field in ['product_uom_qty', 'price_unit', 'discount', 'discount_amount']):
            self._compute_amount()
        
        return result
    
    def _compute_amount(self):
        """Compute line amounts"""
        for line in self:
            # Calculate subtotal
            subtotal = line.product_uom_qty * line.price_unit
            
            # Apply discount
            if line.discount > 0:
                discount_amount = subtotal * (line.discount / 100)
            else:
                discount_amount = line.discount_amount
            
            line.price_subtotal = subtotal - discount_amount
            
            # Calculate tax (simplified 18% GST)
            tax_amount = line.price_subtotal * 0.18
            line.price_total = line.price_subtotal + tax_amount
    
    def action_confirm(self):
        """Confirm order line"""
        for line in self:
            if line.state == 'draft':
                line.state = 'confirmed'
    
    def action_deliver(self):
        """Mark line as delivered"""
        for line in self:
            if line.state == 'confirmed':
                line.state = 'delivered'
                line.qty_delivered = line.product_uom_qty
    
    def action_invoice(self):
        """Mark line as invoiced"""
        for line in self:
            if line.state == 'delivered':
                line.state = 'invoiced'
                line.qty_invoiced = line.product_uom_qty
    
    def action_return(self):
        """Mark line as returned"""
        for line in self:
            if line.state in ['delivered', 'invoiced']:
                line.state = 'returned'
                line.qty_returned = line.product_uom_qty
    
    def action_cancel(self):
        """Cancel order line"""
        for line in self:
            if line.state not in ['delivered', 'invoiced', 'returned']:
                line.state = 'cancelled'
    
    def get_product_recommendations(self):
        """Get product recommendations based on age group and gender"""
        recommendations = []
        
        if self.age_group and self.gender:
            # Find similar products
            domain = [
                ('age_group', '=', self.age_group),
                ('gender', 'in', [self.gender, 'all']),
                ('id', '!=', self.product_id.id)
            ]
            
            products = self.env['product.template'].search(domain, limit=5)
            recommendations = products.read(['name', 'list_price', 'image'])
        
        return recommendations
    
    def action_view_product(self):
        """View product details"""
        return {
            'type': 'ocean.actions.act_window',
            'name': f'Product - {self.product_id.name}',
            'res_model': 'product.template',
            'res_id': self.product_id.id,
            'view_mode': 'form',
            'target': 'current'
        }