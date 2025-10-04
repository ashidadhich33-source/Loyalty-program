# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Stock Move
===============================

Stock move management for kids clothing retail.
"""

from core_framework.orm import BaseModel, CharField, TextField, BooleanField, IntegerField, DateTimeField, Many2OneField, SelectionField, FloatField, One2ManyField, Many2ManyField
from core_framework.orm import Field
from typing import Dict, Any, Optional
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class StockMove(BaseModel):
    """Stock move for inventory operations"""
    
    _name = 'stock.move'
    _description = 'Stock Move'
    _table = 'stock_move'
    
    # Basic Information
    name = CharField(
        string='Description',
        size=200,
        required=True,
        help='Description of the stock move'
    )
    
    sequence = IntegerField(
        string='Sequence',
        default=10,
        help='Sequence of the move'
    )
    
    # Product Information
    product_id = Many2OneField(
        'product.template',
        string='Product',
        required=True,
        help='Product being moved'
    )
    
    product_uom_id = Many2OneField(
        'product.uom',
        string='Unit of Measure',
        help='Unit of measure for the product'
    )
    
    # Location Information
    location_id = Many2OneField(
        'stock.location',
        string='Source Location',
        required=True,
        help='Source location'
    )
    
    location_dest_id = Many2OneField(
        'stock.location',
        string='Destination Location',
        required=True,
        help='Destination location'
    )
    
    # Quantities
    product_uom_qty = FloatField(
        string='Demand',
        digits=(12, 3),
        required=True,
        help='Quantity demanded'
    )
    
    quantity_done = FloatField(
        string='Done',
        digits=(12, 3),
        default=0.0,
        help='Quantity done'
    )
    
    reserved_availability = FloatField(
        string='Reserved',
        digits=(12, 3),
        default=0.0,
        help='Reserved quantity'
    )
    
    availability = FloatField(
        string='Available',
        digits=(12, 3),
        default=0.0,
        help='Available quantity'
    )
    
    # Pricing
    price_unit = FloatField(
        string='Unit Price',
        digits=(12, 2),
        default=0.0,
        help='Unit price of the product'
    )
    
    # Move State
    state = SelectionField(
        string='State',
        selection=[
            ('draft', 'New'),
            ('waiting', 'Waiting Another Move'),
            ('confirmed', 'Waiting Availability'),
            ('assigned', 'Available'),
            ('done', 'Done'),
            ('cancel', 'Cancelled')
        ],
        default='draft',
        help='Current state of the move'
    )
    
    # Move Type
    move_type = SelectionField(
        string='Move Type',
        selection=[
            ('incoming', 'Incoming'),
            ('outgoing', 'Outgoing'),
            ('internal', 'Internal')
        ],
        help='Type of stock move'
    )
    
    # Origin Information
    origin = CharField(
        string='Source Document',
        size=200,
        help='Source document reference'
    )
    
    reference = CharField(
        string='Reference',
        size=100,
        help='Reference of the move'
    )
    
    # Related Records
    picking_id = Many2OneField(
        'stock.picking',
        string='Transfer',
        help='Stock picking this move belongs to'
    )
    
    inventory_id = Many2OneField(
        'stock.inventory',
        string='Inventory Adjustment',
        help='Inventory adjustment this move belongs to'
    )
    
    # Company
    company_id = Many2OneField(
        'res.company',
        string='Company',
        required=True,
        help='Company this move belongs to'
    )
    
    # Date Information
    date = DateTimeField(
        string='Date',
        required=True,
        help='Scheduled date of the move'
    )
    
    date_done = DateTimeField(
        string='Date Done',
        help='Date when move was completed'
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
    
    # Quality Control
    quality_check_required = BooleanField(
        string='Quality Check Required',
        default=False,
        help='Whether quality check is required'
    )
    
    quality_check_done = BooleanField(
        string='Quality Check Done',
        default=False,
        help='Whether quality check is completed'
    )
    
    quality_notes = TextField(
        string='Quality Notes',
        help='Quality check notes'
    )
    
    # Batch/Serial Tracking
    lot_id = Many2OneField(
        'stock.lot',
        string='Lot/Serial Number',
        help='Lot or serial number'
    )
    
    # Package Information
    package_id = Many2OneField(
        'stock.quant.package',
        string='Package',
        help='Package this move belongs to'
    )
    
    # Scrap Information
    scrap_ids = One2ManyField(
        'stock.scrap',
        string='Scrap',
        inverse_name='move_id',
        help='Scrap records for this move'
    )
    
    # Notes
    note = TextField(
        string='Notes',
        help='Additional notes about this move'
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
        if 'date' not in vals:
            vals['date'] = datetime.now()
        
        if 'company_id' not in vals:
            vals['company_id'] = self.env.user.company_id.id
        
        return super().create(vals)
    
    def write(self, vals):
        """Override write to update state"""
        result = super().write(vals)
        
        # Update state when quantities change
        if any(field in vals for field in ['quantity_done', 'product_uom_qty']):
            self._update_state()
        
        return result
    
    def _update_state(self):
        """Update move state based on quantities"""
        for move in self:
            if move.quantity_done >= move.product_uom_qty:
                move.state = 'done'
                if not move.date_done:
                    move.date_done = datetime.now()
            elif move.quantity_done > 0:
                move.state = 'assigned'
            elif move.reserved_availability > 0:
                move.state = 'confirmed'
            else:
                move.state = 'draft'
    
    def action_confirm(self):
        """Confirm the stock move"""
        if self.state != 'draft':
            raise ValueError("Only draft moves can be confirmed")
        
        # Check availability
        self._check_availability()
        
        # Reserve quantity
        self._reserve_quantity()
        
        self.state = 'confirmed'
        return True
    
    def action_assign(self):
        """Assign the stock move"""
        if self.state not in ['confirmed', 'waiting']:
            raise ValueError("Move must be confirmed or waiting to be assigned")
        
        # Check availability again
        self._check_availability()
        
        # Reserve quantity
        self._reserve_quantity()
        
        self.state = 'assigned'
        return True
    
    def action_done(self):
        """Mark move as done"""
        if self.state not in ['assigned', 'confirmed']:
            raise ValueError("Move must be assigned or confirmed to be done")
        
        # Validate move
        self._validate_move()
        
        # Update quantities
        self._update_quantities()
        
        # Update state
        self.state = 'done'
        self.date_done = datetime.now()
        
        return True
    
    def action_cancel(self):
        """Cancel the stock move"""
        if self.state == 'done':
            raise ValueError("Cannot cancel completed moves")
        
        # Unreserve quantity
        self._unreserve_quantity()
        
        self.state = 'cancel'
        return True
    
    def _check_availability(self):
        """Check if product is available in source location"""
        if self.move_type == 'incoming':
            return True
        
        # Check available quantity in source location
        available_qty = self._get_available_quantity()
        
        if available_qty < self.product_uom_qty:
            raise ValueError(f"Insufficient quantity. Available: {available_qty}, Required: {self.product_uom_qty}")
    
    def _get_available_quantity(self):
        """Get available quantity in source location"""
        quants = self.env['stock.quant'].search([
            ('product_id', '=', self.product_id.id),
            ('location_id', '=', self.location_id.id)
        ])
        
        return sum(quant.quantity for quant in quants)
    
    def _reserve_quantity(self):
        """Reserve quantity for this move"""
        if self.move_type == 'incoming':
            return
        
        # Reserve quantity in source location
        self.reserved_availability = self.product_uom_qty
    
    def _unreserve_quantity(self):
        """Unreserve quantity for this move"""
        self.reserved_availability = 0.0
    
    def _validate_move(self):
        """Validate move before completion"""
        errors = []
        
        # Check if move has required fields
        if not self.product_id:
            errors.append("Product is required")
        
        if not self.location_id:
            errors.append("Source location is required")
        
        if not self.location_dest_id:
            errors.append("Destination location is required")
        
        if not self.product_uom_qty or self.product_uom_qty <= 0:
            errors.append("Quantity must be greater than 0")
        
        # Check age group compatibility
        if self.product_age_group and self.location_dest_id:
            if not self.location_dest_id.validate_age_group(self.product_age_group):
                errors.append(f"Product age group '{self.product_age_group}' not allowed in destination location")
        
        # Check quality requirements
        if self.quality_check_required and not self.quality_check_done:
            errors.append("Quality check is required but not completed")
        
        if errors:
            raise ValueError('\n'.join(errors))
    
    def _update_quantities(self):
        """Update quantities in source and destination locations"""
        # Update source location (decrease)
        if self.move_type != 'incoming':
            self._update_location_quantity(self.location_id, -self.quantity_done)
        
        # Update destination location (increase)
        if self.move_type != 'outgoing':
            self._update_location_quantity(self.location_dest_id, self.quantity_done)
    
    def _update_location_quantity(self, location, quantity_change):
        """Update quantity in a specific location"""
        # Find or create quant for this product and location
        quant = self.env['stock.quant'].search([
            ('product_id', '=', self.product_id.id),
            ('location_id', '=', location.id)
        ], limit=1)
        
        if not quant:
            # Create new quant
            quant_vals = {
                'product_id': self.product_id.id,
                'location_id': location.id,
                'quantity': quantity_change,
                'reserved_quantity': 0.0,
                'value': quantity_change * self.price_unit
            }
            self.env['stock.quant'].create(quant_vals)
        else:
            # Update existing quant
            quant.quantity += quantity_change
            quant.value += quantity_change * self.price_unit
    
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
    
    def action_view_picking(self):
        """View related picking"""
        if not self.picking_id:
            return None
        
        return {
            'type': 'ir.actions.act_window',
            'name': f'Transfer - {self.picking_id.name}',
            'res_model': 'stock.picking',
            'res_id': self.picking_id.id,
            'view_mode': 'form',
            'target': 'new'
        }
    
    def get_move_summary(self):
        """Get move summary data"""
        return {
            'move_name': self.name,
            'product': self.product_id.name,
            'source_location': self.location_id.name,
            'destination_location': self.location_dest_id.name,
            'demand_quantity': self.product_uom_qty,
            'done_quantity': self.quantity_done,
            'reserved_quantity': self.reserved_availability,
            'available_quantity': self.availability,
            'unit_price': self.price_unit,
            'state': self.state,
            'move_type': self.move_type,
            'origin': self.origin,
            'reference': self.reference,
            'date': self.date,
            'date_done': self.date_done,
            'product_age_group': self.product_age_group,
            'product_size': self.product_size,
            'product_color': self.product_color,
            'quality_check_required': self.quality_check_required,
            'quality_check_done': self.quality_check_done,
            'lot_number': self.lot_id.name if self.lot_id else 'None'
        }