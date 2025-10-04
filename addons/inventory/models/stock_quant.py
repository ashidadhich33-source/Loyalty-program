# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Stock Quant
===============================

Stock quant management for kids clothing retail.
"""

from core_framework.orm import BaseModel, CharField, TextField, BooleanField, IntegerField, DateTimeField, Many2OneField, SelectionField, FloatField, One2ManyField, Many2ManyField
from core_framework.orm import Field
from typing import Dict, Any, Optional
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class StockQuant(BaseModel):
    """Stock quant for inventory tracking"""
    
    _name = 'stock.quant'
    _description = 'Stock Quant'
    _table = 'stock_quant'
    
    # Basic Information
    product_id = Many2OneField(
        'product.template',
        string='Product',
        required=True,
        help='Product for this quant'
    )
    
    location_id = Many2OneField(
        'stock.location',
        string='Location',
        required=True,
        help='Location of this quant'
    )
    
    lot_id = Many2OneField(
        'stock.lot',
        string='Lot/Serial Number',
        help='Lot or serial number'
    )
    
    package_id = Many2OneField(
        'stock.quant.package',
        string='Package',
        help='Package this quant belongs to'
    )
    
    owner_id = Many2OneField(
        'res.partner',
        string='Owner',
        help='Owner of this quant'
    )
    
    # Quantities
    quantity = FloatField(
        string='Quantity',
        digits=(12, 3),
        default=0.0,
        help='Available quantity'
    )
    
    reserved_quantity = FloatField(
        string='Reserved Quantity',
        digits=(12, 3),
        default=0.0,
        help='Reserved quantity'
    )
    
    # Pricing
    value = FloatField(
        string='Value',
        digits=(12, 2),
        default=0.0,
        help='Total value of this quant'
    )
    
    cost = FloatField(
        string='Cost',
        digits=(12, 2),
        default=0.0,
        help='Unit cost of this quant'
    )
    
    # Company
    company_id = Many2OneField(
        'res.company',
        string='Company',
        required=True,
        help='Company this quant belongs to'
    )
    
    # Kids Clothing Specific
    product_age_group = SelectionField(
        string='Product Age Group',
        selection=[
            ('toddler', 'Toddler (0-3 years)'),
            ('child', 'Child (3-12 years)'),
            ('teen', 'Teen (12+ years)')
        ],
        help='Age group of the product'
    )
    
    product_size = CharField(
        string='Product Size',
        size=20,
        help='Size of the product'
    )
    
    product_color = CharField(
        string='Product Color',
        size=50,
        help='Color of the product'
    )
    
    # Quality Information
    quality_status = SelectionField(
        string='Quality Status',
        selection=[
            ('good', 'Good'),
            ('damaged', 'Damaged'),
            ('defective', 'Defective'),
            ('expired', 'Expired'),
            ('recalled', 'Recalled')
        ],
        default='good',
        help='Quality status of this quant'
    )
    
    quality_notes = TextField(
        string='Quality Notes',
        help='Quality notes for this quant'
    )
    
    # Expiry Information
    expiry_date = DateTimeField(
        string='Expiry Date',
        help='Expiry date of the product'
    )
    
    days_to_expiry = IntegerField(
        string='Days to Expiry',
        help='Days remaining until expiry'
    )
    
    # Batch Information
    batch_number = CharField(
        string='Batch Number',
        size=50,
        help='Batch number of the product'
    )
    
    manufacturing_date = DateTimeField(
        string='Manufacturing Date',
        help='Manufacturing date of the product'
    )
    
    # Location Specific
    shelf_location = CharField(
        string='Shelf Location',
        size=50,
        help='Specific shelf location'
    )
    
    bin_location = CharField(
        string='Bin Location',
        size=50,
        help='Specific bin location'
    )
    
    # Movement Tracking
    last_move_date = DateTimeField(
        string='Last Move Date',
        help='Date of last movement'
    )
    
    last_move_type = SelectionField(
        string='Last Move Type',
        selection=[
            ('incoming', 'Incoming'),
            ('outgoing', 'Outgoing'),
            ('internal', 'Internal'),
            ('adjustment', 'Adjustment')
        ],
        help='Type of last movement'
    )
    
    # Inventory Aging
    inventory_age_days = IntegerField(
        string='Inventory Age (Days)',
        default=0,
        help='Age of inventory in days'
    )
    
    # Notes
    note = TextField(
        string='Notes',
        help='Additional notes about this quant'
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
        if 'company_id' not in vals:
            vals['company_id'] = self.env.user.company_id.id
        
        return super().create(vals)
    
    def write(self, vals):
        """Override write to update calculations"""
        result = super().write(vals)
        
        # Update calculations when quantities change
        if any(field in vals for field in ['quantity', 'cost']):
            self._update_calculations()
        
        # Update expiry information
        if 'expiry_date' in vals:
            self._update_expiry_info()
        
        return result
    
    def _update_calculations(self):
        """Update calculated fields"""
        for quant in self:
            # Update value
            quant.value = quant.quantity * quant.cost
            
            # Update inventory age
            if quant.create_date:
                age_delta = datetime.now() - quant.create_date
                quant.inventory_age_days = age_delta.days
    
    def _update_expiry_info(self):
        """Update expiry information"""
        for quant in self:
            if quant.expiry_date:
                expiry_delta = quant.expiry_date - datetime.now()
                quant.days_to_expiry = expiry_delta.days
            else:
                quant.days_to_expiry = 0
    
    def action_reserve(self, quantity):
        """Reserve quantity from this quant"""
        if quantity > self.quantity:
            raise ValueError(f"Cannot reserve {quantity}. Available: {self.quantity}")
        
        self.reserved_quantity += quantity
        return True
    
    def action_unreserve(self, quantity):
        """Unreserve quantity from this quant"""
        if quantity > self.reserved_quantity:
            raise ValueError(f"Cannot unreserve {quantity}. Reserved: {self.reserved_quantity}")
        
        self.reserved_quantity -= quantity
        return True
    
    def action_adjust(self, new_quantity, reason=None):
        """Adjust quantity of this quant"""
        old_quantity = self.quantity
        quantity_diff = new_quantity - old_quantity
        
        # Update quantity
        self.quantity = new_quantity
        
        # Update value
        self._update_calculations()
        
        # Create adjustment move
        if quantity_diff != 0:
            self._create_adjustment_move(quantity_diff, reason)
        
        return True
    
    def _create_adjustment_move(self, quantity_diff, reason=None):
        """Create adjustment move for quantity change"""
        move_vals = {
            'name': f'Adjustment: {self.product_id.name}',
            'product_id': self.product_id.id,
            'location_id': self.location_id.id,
            'location_dest_id': self.location_id.id,
            'product_uom_qty': abs(quantity_diff),
            'quantity_done': abs(quantity_diff),
            'move_type': 'internal',
            'origin': f'Adjustment - {reason or "Manual"}',
            'reference': f'ADJ-{datetime.now().strftime("%Y%m%d%H%M%S")}',
            'company_id': self.company_id.id,
            'date': datetime.now(),
            'state': 'done',
            'date_done': datetime.now()
        }
        
        self.env['stock.move'].create(move_vals)
    
    def action_view_product(self):
        """View product details"""
        return {
            'type': 'ir.actions.act_window',
            'name': f'Product - {self.product_id.name}',
            'res_model': 'product.template',
            'res_id': self.product_id.id,
            'view_mode': 'form',
            'target': 'new'
        }
    
    def action_view_location(self):
        """View location details"""
        return {
            'type': 'ir.actions.act_window',
            'name': f'Location - {self.location_id.name}',
            'res_model': 'stock.location',
            'res_id': self.location_id.id,
            'view_mode': 'form',
            'target': 'new'
        }
    
    def action_view_moves(self):
        """View moves for this quant"""
        return {
            'type': 'ir.actions.act_window',
            'name': f'Moves - {self.product_id.name}',
            'res_model': 'stock.move',
            'view_mode': 'tree,form',
            'domain': [
                '&',
                ('product_id', '=', self.product_id.id),
                '|',
                ('location_id', '=', self.location_id.id),
                ('location_dest_id', '=', self.location_id.id)
            ],
            'context': {'default_product_id': self.product_id.id}
        }
    
    def get_quant_summary(self):
        """Get quant summary data"""
        return {
            'product': self.product_id.name,
            'location': self.location_id.name,
            'lot_number': self.lot_id.name if self.lot_id else 'None',
            'package': self.package_id.name if self.package_id else 'None',
            'owner': self.owner_id.name if self.owner_id else 'None',
            'quantity': self.quantity,
            'reserved_quantity': self.reserved_quantity,
            'available_quantity': self.quantity - self.reserved_quantity,
            'value': self.value,
            'cost': self.cost,
            'product_age_group': self.product_age_group,
            'product_size': self.product_size,
            'product_color': self.product_color,
            'quality_status': self.quality_status,
            'expiry_date': self.expiry_date,
            'days_to_expiry': self.days_to_expiry,
            'batch_number': self.batch_number,
            'manufacturing_date': self.manufacturing_date,
            'shelf_location': self.shelf_location,
            'bin_location': self.bin_location,
            'last_move_date': self.last_move_date,
            'last_move_type': self.last_move_type,
            'inventory_age_days': self.inventory_age_days
        }
    
    def check_expiry_alert(self, days_threshold=30):
        """Check if quant is approaching expiry"""
        if not self.expiry_date:
            return False, "No expiry date set"
        
        if self.days_to_expiry <= 0:
            return True, "Product has expired"
        elif self.days_to_expiry <= days_threshold:
            return True, f"Product expires in {self.days_to_expiry} days"
        
        return False, "Product is not approaching expiry"
    
    def check_quality_alert(self):
        """Check if quant has quality issues"""
        if self.quality_status in ['damaged', 'defective', 'expired', 'recalled']:
            return True, f"Quality issue: {self.quality_status}"
        
        return False, "No quality issues"
    
    def check_age_alert(self, age_threshold=365):
        """Check if quant is aging"""
        if self.inventory_age_days > age_threshold:
            return True, f"Inventory is {self.inventory_age_days} days old"
        
        return False, "Inventory is not aging"