# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Stock Inventory
===================================

Stock inventory management for kids clothing retail.
"""

from core_framework.orm import BaseModel, CharField, TextField, BooleanField, IntegerField, DateTimeField, Many2OneField, SelectionField, FloatField, One2ManyField, Many2ManyField
from core_framework.orm import Field
from typing import Dict, Any, Optional
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class StockInventory(BaseModel):
    """Stock inventory for inventory adjustments"""
    
    _name = 'stock.inventory'
    _description = 'Stock Inventory'
    _table = 'stock_inventory'
    
    # Basic Information
    name = CharField(
        string='Inventory Reference',
        size=100,
        required=True,
        help='Reference of the inventory adjustment'
    )
    
    # Inventory Type
    inventory_type = SelectionField(
        string='Inventory Type',
        selection=[
            ('full', 'Full Inventory'),
            ('partial', 'Partial Inventory'),
            ('cycle', 'Cycle Count'),
            ('spot', 'Spot Check'),
            ('damage', 'Damage Check'),
            ('expiry', 'Expiry Check')
        ],
        default='full',
        help='Type of inventory adjustment'
    )
    
    # Location Information
    location_ids = Many2ManyField(
        'stock.location',
        string='Locations',
        help='Locations to include in inventory'
    )
    
    # Product Information
    product_ids = Many2ManyField(
        'product.template',
        string='Products',
        help='Products to include in inventory'
    )
    
    # Inventory State
    state = SelectionField(
        string='State',
        selection=[
            ('draft', 'Draft'),
            ('in_progress', 'In Progress'),
            ('done', 'Done'),
            ('cancel', 'Cancelled')
        ],
        default='draft',
        help='Current state of the inventory'
    )
    
    # Move Lines
    move_ids = One2ManyField(
        'stock.move',
        string='Inventory Moves',
        inverse_name='inventory_id',
        help='Moves created by this inventory'
    )
    
    # Company
    company_id = Many2OneField(
        'res.company',
        string='Company',
        required=True,
        help='Company this inventory belongs to'
    )
    
    # Date Information
    date = DateTimeField(
        string='Inventory Date',
        required=True,
        help='Date of the inventory'
    )
    
    date_done = DateTimeField(
        string='Date Done',
        help='Date when inventory was completed'
    )
    
    # Kids Clothing Specific
    age_group_filter = SelectionField(
        string='Age Group Filter',
        selection=[
            ('none', 'No Filter'),
            ('toddler', 'Toddler Only (0-3 years)'),
            ('child', 'Child Only (3-12 years)'),
            ('teen', 'Teen Only (12+ years)'),
            ('toddler_child', 'Toddler & Child (0-12 years)'),
            ('child_teen', 'Child & Teen (3+ years)')
        ],
        default='none',
        help='Age group filter for inventory'
    )
    
    # Quality Check
    quality_check_required = BooleanField(
        string='Quality Check Required',
        default=False,
        help='Whether quality check is required'
    )
    
    # Results
    total_products = IntegerField(
        string='Total Products',
        default=0,
        help='Total number of products counted'
    )
    
    total_quantity = FloatField(
        string='Total Quantity',
        digits=(12, 3),
        default=0.0,
        help='Total quantity counted'
    )
    
    total_value = FloatField(
        string='Total Value',
        digits=(12, 2),
        default=0.0,
        help='Total value of inventory'
    )
    
    discrepancy_count = IntegerField(
        string='Discrepancy Count',
        default=0,
        help='Number of products with discrepancies'
    )
    
    discrepancy_value = FloatField(
        string='Discrepancy Value',
        digits=(12, 2),
        default=0.0,
        help='Total value of discrepancies'
    )
    
    # Notes
    note = TextField(
        string='Notes',
        help='Additional notes about this inventory'
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
            vals['name'] = self._generate_inventory_name()
        
        if 'date' not in vals:
            vals['date'] = datetime.now()
        
        if 'company_id' not in vals:
            vals['company_id'] = self.env.user.company_id.id
        
        return super().create(vals)
    
    def write(self, vals):
        """Override write to update state"""
        result = super().write(vals)
        
        # Update state when moves change
        if 'move_ids' in vals:
            self._update_state()
        
        return result
    
    def _generate_inventory_name(self):
        """Generate unique inventory name"""
        return f"INV-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    def _update_state(self):
        """Update inventory state based on moves"""
        for inventory in self:
            if not inventory.move_ids:
                inventory.state = 'draft'
                continue
            
            move_states = [move.state for move in inventory.move_ids]
            
            if all(state == 'done' for state in move_states):
                inventory.state = 'done'
                if not inventory.date_done:
                    inventory.date_done = datetime.now()
            elif any(state in ['assigned', 'confirmed'] for state in move_states):
                inventory.state = 'in_progress'
            else:
                inventory.state = 'draft'
    
    def action_start(self):
        """Start the inventory"""
        if self.state != 'draft':
            raise ValueError("Only draft inventories can be started")
        
        # Generate inventory lines
        self._generate_inventory_lines()
        
        self.state = 'in_progress'
        return True
    
    def action_done(self):
        """Complete the inventory"""
        if self.state != 'in_progress':
            raise ValueError("Inventory must be in progress to be completed")
        
        # Process all moves
        for move in self.move_ids:
            move.action_done()
        
        # Update statistics
        self._update_statistics()
        
        self.state = 'done'
        self.date_done = datetime.now()
        return True
    
    def action_cancel(self):
        """Cancel the inventory"""
        if self.state == 'done':
            raise ValueError("Cannot cancel completed inventories")
        
        # Cancel all moves
        for move in self.move_ids:
            move.action_cancel()
        
        self.state = 'cancel'
        return True
    
    def _generate_inventory_lines(self):
        """Generate inventory lines based on filters"""
        # Get products to inventory
        products = self._get_products_to_inventory()
        
        # Get locations to inventory
        locations = self._get_locations_to_inventory()
        
        # Create inventory moves
        for product in products:
            for location in locations:
                # Get current quantity
                current_qty = self._get_current_quantity(product, location)
                
                # Create inventory move
                move_vals = {
                    'name': f'Inventory: {product.name}',
                    'product_id': product.id,
                    'location_id': location.id,
                    'location_dest_id': location.id,
                    'product_uom_qty': current_qty,
                    'quantity_done': current_qty,
                    'move_type': 'internal',
                    'origin': f'Inventory - {self.name}',
                    'reference': f'INV-{self.id}',
                    'inventory_id': self.id,
                    'company_id': self.company_id.id,
                    'date': self.date,
                    'state': 'draft'
                }
                
                self.env['stock.move'].create(move_vals)
    
    def _get_products_to_inventory(self):
        """Get products to include in inventory"""
        domain = []
        
        if self.product_ids:
            domain.append(('id', 'in', [p.id for p in self.product_ids]))
        
        if self.age_group_filter != 'none':
            domain.append(('age_group', '=', self.age_group_filter))
        
        return self.env['product.template'].search(domain)
    
    def _get_locations_to_inventory(self):
        """Get locations to include in inventory"""
        if self.location_ids:
            return self.location_ids
        else:
            return self.env['stock.location'].search([('usage', '=', 'internal')])
    
    def _get_current_quantity(self, product, location):
        """Get current quantity of product in location"""
        quants = self.env['stock.quant'].search([
            ('product_id', '=', product.id),
            ('location_id', '=', location.id)
        ])
        
        return sum(quant.quantity for quant in quants)
    
    def _update_statistics(self):
        """Update inventory statistics"""
        for inventory in self:
            # Count products and quantities
            products = set()
            total_qty = 0.0
            total_value = 0.0
            discrepancy_count = 0
            discrepancy_value = 0.0
            
            for move in inventory.move_ids:
                products.add(move.product_id.id)
                total_qty += move.quantity_done
                total_value += move.quantity_done * move.price_unit
                
                # Check for discrepancies
                if move.quantity_done != move.product_uom_qty:
                    discrepancy_count += 1
                    discrepancy_value += abs(move.quantity_done - move.product_uom_qty) * move.price_unit
            
            inventory.total_products = len(products)
            inventory.total_quantity = total_qty
            inventory.total_value = total_value
            inventory.discrepancy_count = discrepancy_count
            inventory.discrepancy_value = discrepancy_value
    
    def action_view_moves(self):
        """View moves for this inventory"""
        return {
            'type': 'ir.actions.act_window',
            'name': f'Moves - {self.name}',
            'res_model': 'stock.move',
            'view_mode': 'tree,form',
            'domain': [('inventory_id', '=', self.id)],
            'context': {'default_inventory_id': self.id}
        }
    
    def get_inventory_summary(self):
        """Get inventory summary data"""
        return {
            'inventory_name': self.name,
            'inventory_type': self.inventory_type,
            'state': self.state,
            'location_count': len(self.location_ids),
            'product_count': len(self.product_ids),
            'move_count': len(self.move_ids),
            'date': self.date,
            'date_done': self.date_done,
            'age_group_filter': self.age_group_filter,
            'quality_check_required': self.quality_check_required,
            'total_products': self.total_products,
            'total_quantity': self.total_quantity,
            'total_value': self.total_value,
            'discrepancy_count': self.discrepancy_count,
            'discrepancy_value': self.discrepancy_value,
            'company': self.company_id.name
        }