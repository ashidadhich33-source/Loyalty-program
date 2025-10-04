# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Purchase Order Line
=======================================

Purchase order line management for kids clothing retail.
"""

from core_framework.orm import BaseModel, CharField, TextField, BooleanField, IntegerField, DateTimeField, Many2OneField, SelectionField, FloatField, One2ManyField, Many2ManyField
from core_framework.orm import Field
from typing import Dict, Any, Optional
import logging
from datetime import datetime
from core_framework.exceptions import ValidationError

logger = logging.getLogger(__name__)

class PurchaseOrderLine(BaseModel):
    """Purchase order line for individual product procurement"""
    
    _name = 'purchase.order.line'
    _description = 'Purchase Order Line'
    _table = 'purchase_order_line'
    
    # Basic Information
    order_id = Many2OneField(
        'purchase.order',
        string='Purchase Order',
        required=True,
        help='Purchase order for this line'
    )
    
    product_id = Many2OneField(
        'product.template',
        string='Product',
        required=True,
        help='Product for this line'
    )
    
    product_qty = FloatField(
        string='Quantity',
        digits=(16, 3),
        required=True,
        help='Quantity to purchase'
    )
    
    product_uom = Many2OneField(
        'product.uom',
        string='Unit of Measure',
        required=True,
        help='Unit of measure for the product'
    )
    
    # Pricing Information
    price_unit = FloatField(
        string='Unit Price',
        digits=(16, 2),
        required=True,
        help='Unit price for the product'
    )
    
    price_subtotal = FloatField(
        string='Subtotal',
        digits=(16, 2),
        help='Subtotal without taxes'
    )
    
    price_tax = FloatField(
        string='Tax Amount',
        digits=(16, 2),
        help='Tax amount for this line'
    )
    
    price_total = FloatField(
        string='Total',
        digits=(16, 2),
        help='Total amount including taxes'
    )
    
    # Kids Clothing Specific Fields
    age_group = SelectionField(
        string='Age Group',
        selection=[
            ('infant', 'Infant (0-2 years)'),
            ('toddler', 'Toddler (2-4 years)'),
            ('child', 'Child (4-8 years)'),
            ('teen', 'Teen (8-16 years)'),
        ],
        help='Target age group for this product'
    )
    
    season = SelectionField(
        string='Season',
        selection=[
            ('summer', 'Summer'),
            ('winter', 'Winter'),
            ('monsoon', 'Monsoon'),
            ('all_season', 'All Season'),
        ],
        help='Season for this product'
    )
    
    size_range = SelectionField(
        string='Size Range',
        selection=[
            ('xs', 'XS'),
            ('s', 'S'),
            ('m', 'M'),
            ('l', 'L'),
            ('xl', 'XL'),
            ('xxl', 'XXL'),
        ],
        help='Size range for this product'
    )
    
    gender = SelectionField(
        string='Gender',
        selection=[
            ('unisex', 'Unisex'),
            ('boys', 'Boys'),
            ('girls', 'Girls'),
        ],
        help='Gender category for this product'
    )
    
    special_occasion = SelectionField(
        string='Special Occasion',
        selection=[
            ('daily_wear', 'Daily Wear'),
            ('party_wear', 'Party Wear'),
            ('festival', 'Festival'),
            ('school', 'School'),
            ('sports', 'Sports'),
            ('formal', 'Formal'),
        ],
        help='Special occasion for this product'
    )
    
    # Additional Information
    notes = TextField(
        string='Notes',
        help='Additional notes for this line'
    )
    
    # Timestamps
    create_date = DateTimeField(
        string='Created On',
        default=datetime.now,
        help='Date when the record was created'
    )
    
    write_date = DateTimeField(
        string='Last Updated On',
        default=datetime.now,
        help='Date when the record was last updated'
    )
    
    def create(self, vals):
        """Override create to set default values"""
        if 'product_uom' not in vals and 'product_id' in vals:
            product = self.env['product.template'].browse(vals['product_id'])
            vals['product_uom'] = product.uom_id.id
        
        return super().create(vals)
    
    def write(self, vals):
        """Override write to update timestamps and calculations"""
        vals['write_date'] = datetime.now()
        result = super().write(vals)
        
        # Recalculate totals if price or quantity changed
        if 'price_unit' in vals or 'product_qty' in vals:
            self._calculate_totals()
        
        return result
    
    def _calculate_totals(self):
        """Calculate line totals"""
        for line in self:
            line.price_subtotal = line.product_qty * line.price_unit
            # Simple tax calculation - in production, use proper tax system
            line.price_tax = line.price_subtotal * 0.18  # 18% GST
            line.price_total = line.price_subtotal + line.price_tax
    
    def action_view_product(self):
        """View product details"""
        return {
            'type': 'ocean.actions.act_window',
            'name': 'Product Details',
            'res_model': 'product.template',
            'view_mode': 'form',
            'res_id': self.product_id.id,
        }
    
    def action_view_order(self):
        """View purchase order"""
        return {
            'type': 'ocean.actions.act_window',
            'name': 'Purchase Order',
            'res_model': 'purchase.order',
            'view_mode': 'form',
            'res_id': self.order_id.id,
        }
    
    def get_line_summary(self):
        """Get line summary"""
        return {
            'product_name': self.product_id.name,
            'quantity': self.product_qty,
            'unit_price': self.price_unit,
            'subtotal': self.price_subtotal,
            'total': self.price_total,
        }
    
    def _validate_line(self):
        """Validate purchase order line"""
        if self.product_qty <= 0:
            raise ValidationError("Product quantity must be greater than 0")
        
        if self.price_unit <= 0:
            raise ValidationError("Unit price must be greater than 0")
    
    def _update_order_totals(self):
        """Update parent order totals"""
        if self.order_id:
            self.order_id._calculate_totals()