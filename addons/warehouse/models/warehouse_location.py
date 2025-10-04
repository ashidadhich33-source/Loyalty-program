# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Warehouse Location
=====================================

Warehouse location management for kids clothing retail.
"""

from core_framework.orm import BaseModel, CharField, TextField, BooleanField, IntegerField, DateTimeField, Many2OneField, SelectionField, FloatField, One2ManyField, Many2ManyField
from core_framework.orm import Field
from typing import Dict, Any, Optional
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class WarehouseLocation(BaseModel):
    """Warehouse location for detailed inventory management"""
    
    _name = 'warehouse.location'
    _description = 'Warehouse Location'
    _table = 'warehouse_location'
    
    # Basic Information
    name = CharField(
        string='Location Name',
        size=100,
        required=True,
        help='Name of the warehouse location'
    )
    
    code = CharField(
        string='Location Code',
        size=20,
        help='Short code for the location'
    )
    
    description = TextField(
        string='Description',
        help='Description of the location'
    )
    
    # Warehouse Reference
    warehouse_id = Many2OneField(
        'warehouse',
        string='Warehouse',
        required=True,
        help='Warehouse this location belongs to'
    )
    
    # Stock Location Reference
    stock_location_id = Many2OneField(
        'stock.location',
        string='Stock Location',
        required=True,
        help='Related stock location'
    )
    
    # Location Hierarchy
    parent_id = Many2OneField(
        'warehouse.location',
        string='Parent Location',
        help='Parent location in the hierarchy'
    )
    
    child_ids = One2ManyField(
        'warehouse.location',
        string='Child Locations',
        inverse_name='parent_id',
        help='Child locations'
    )
    
    # Location Type
    location_type = SelectionField(
        string='Location Type',
        selection=[
            ('zone', 'Zone'),
            ('aisle', 'Aisle'),
            ('rack', 'Rack'),
            ('shelf', 'Shelf'),
            ('bin', 'Bin'),
            ('floor', 'Floor'),
            ('mezzanine', 'Mezzanine'),
            ('cold_storage', 'Cold Storage'),
            ('hazardous', 'Hazardous Storage'),
            ('quarantine', 'Quarantine')
        ],
        default='zone',
        help='Type of warehouse location'
    )
    
    # Configuration
    is_active = BooleanField(
        string='Active',
        default=True,
        help='Whether this location is active'
    )
    
    is_pickable = BooleanField(
        string='Pickable',
        default=True,
        help='Whether this location is pickable'
    )
    
    is_putaway_location = BooleanField(
        string='Putaway Location',
        default=True,
        help='Whether this location is used for putaway'
    )
    
    # Physical Properties
    posx = FloatField(
        string='X Position',
        digits=(8, 2),
        default=0.0,
        help='X coordinate in warehouse'
    )
    
    posy = FloatField(
        string='Y Position',
        digits=(8, 2),
        default=0.0,
        help='Y coordinate in warehouse'
    )
    
    posz = FloatField(
        string='Z Position',
        digits=(8, 2),
        default=0.0,
        help='Z coordinate in warehouse'
    )
    
    # Dimensions
    length = FloatField(
        string='Length (ft)',
        digits=(8, 2),
        default=0.0,
        help='Length of the location in feet'
    )
    
    width = FloatField(
        string='Width (ft)',
        digits=(8, 2),
        default=0.0,
        help='Width of the location in feet'
    )
    
    height = FloatField(
        string='Height (ft)',
        digits=(8, 2),
        default=0.0,
        help='Height of the location in feet'
    )
    
    # Capacity
    max_capacity = FloatField(
        string='Max Capacity',
        digits=(12, 2),
        default=0.0,
        help='Maximum capacity of the location'
    )
    
    current_capacity = FloatField(
        string='Current Capacity',
        digits=(12, 2),
        default=0.0,
        help='Current capacity usage'
    )
    
    max_weight = FloatField(
        string='Max Weight (kg)',
        digits=(12, 2),
        default=0.0,
        help='Maximum weight capacity in kg'
    )
    
    current_weight = FloatField(
        string='Current Weight (kg)',
        digits=(12, 2),
        default=0.0,
        help='Current weight usage in kg'
    )
    
    # Temperature Control
    temperature_controlled = BooleanField(
        string='Temperature Controlled',
        default=False,
        help='Whether location has temperature control'
    )
    
    min_temperature = FloatField(
        string='Min Temperature',
        digits=(5, 2),
        help='Minimum temperature in Celsius'
    )
    
    max_temperature = FloatField(
        string='Max Temperature',
        digits=(5, 2),
        help='Maximum temperature in Celsius'
    )
    
    # Kids Clothing Specific
    age_group_restriction = SelectionField(
        string='Age Group Restriction',
        selection=[
            ('none', 'No Restriction'),
            ('toddler', 'Toddler Only (0-3 years)'),
            ('child', 'Child Only (3-12 years)'),
            ('teen', 'Teen Only (12+ years)'),
            ('toddler_child', 'Toddler & Child (0-12 years)'),
            ('child_teen', 'Child & Teen (3+ years)')
        ],
        default='none',
        help='Age group restriction for this location'
    )
    
    seasonal_storage = BooleanField(
        string='Seasonal Storage',
        default=False,
        help='Whether this location is used for seasonal storage'
    )
    
    # Security
    requires_access_control = BooleanField(
        string='Requires Access Control',
        default=False,
        help='Whether location requires access control'
    )
    
    access_level = SelectionField(
        string='Access Level',
        selection=[
            ('public', 'Public'),
            ('restricted', 'Restricted'),
            ('confidential', 'Confidential'),
            ('top_secret', 'Top Secret')
        ],
        default='public',
        help='Access level required'
    )
    
    # Statistics
    product_count = IntegerField(
        string='Product Count',
        default=0,
        help='Number of different products in this location'
    )
    
    total_quantity = FloatField(
        string='Total Quantity',
        digits=(12, 3),
        default=0.0,
        help='Total quantity of all products'
    )
    
    total_value = FloatField(
        string='Total Value',
        digits=(12, 2),
        default=0.0,
        help='Total value of inventory in this location'
    )
    
    # Performance Metrics
    pick_frequency = IntegerField(
        string='Pick Frequency',
        default=0,
        help='Number of picks from this location'
    )
    
    last_pick_date = DateTimeField(
        string='Last Pick Date',
        help='Date of last pick from this location'
    )
    
    # Notes
    note = TextField(
        string='Notes',
        help='Additional notes about this location'
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
        if 'code' not in vals and 'name' in vals:
            vals['code'] = vals['name'].upper().replace(' ', '_')
        
        return super().create(vals)
    
    def write(self, vals):
        """Override write to update statistics"""
        result = super().write(vals)
        
        # Update statistics when location changes
        if any(field in vals for field in ['is_active', 'location_type']):
            self._update_statistics()
        
        return result
    
    def _update_statistics(self):
        """Update location statistics"""
        for location in self:
            # Count products and quantities in stock location
            quants = self.env['stock.quant'].search([('location_id', '=', location.stock_location_id.id)])
            
            location.product_count = len(set(quant.product_id.id for quant in quants))
            location.total_quantity = sum(quant.quantity for quant in quants)
            location.total_value = sum(quant.value for quant in quants)
    
    def action_view_quants(self):
        """View stock quants for this location"""
        return {
            'type': 'ir.actions.act_window',
            'name': f'Stock Quants - {self.name}',
            'res_model': 'stock.quant',
            'view_mode': 'tree,form',
            'domain': [('location_id', '=', self.stock_location_id.id)],
            'context': {'default_location_id': self.stock_location_id.id}
        }
    
    def action_view_moves(self):
        """View stock moves for this location"""
        return {
            'type': 'ir.actions.act_window',
            'name': f'Stock Moves - {self.name}',
            'res_model': 'stock.move',
            'view_mode': 'tree,form',
            'domain': ['|', ('location_id', '=', self.stock_location_id.id), ('location_dest_id', '=', self.stock_location_id.id)],
            'context': {'default_location_id': self.stock_location_id.id}
        }
    
    def action_view_pickings(self):
        """View stock pickings for this location"""
        return {
            'type': 'ir.actions.act_window',
            'name': f'Stock Pickings - {self.name}',
            'res_model': 'stock.picking',
            'view_mode': 'tree,form',
            'domain': ['|', ('location_id', '=', self.stock_location_id.id), ('location_dest_id', '=', self.stock_location_id.id)],
            'context': {'default_location_id': self.stock_location_id.id}
        }
    
    def get_location_summary(self):
        """Get location summary data"""
        return {
            'location_name': self.name,
            'location_code': self.code,
            'warehouse': self.warehouse_id.name,
            'stock_location': self.stock_location_id.name,
            'location_type': self.location_type,
            'is_active': self.is_active,
            'is_pickable': self.is_pickable,
            'is_putaway_location': self.is_putaway_location,
            'parent_location': self.parent_id.name if self.parent_id else 'None',
            'child_count': len(self.child_ids),
            'coordinates': f"({self.posx}, {self.posy}, {self.posz})",
            'dimensions': f"{self.length}x{self.width}x{self.height} ft",
            'max_capacity': self.max_capacity,
            'current_capacity': self.current_capacity,
            'capacity_usage': self._get_capacity_usage(),
            'max_weight': self.max_weight,
            'current_weight': self.current_weight,
            'weight_usage': self._get_weight_usage(),
            'temperature_controlled': self.temperature_controlled,
            'min_temperature': self.min_temperature,
            'max_temperature': self.max_temperature,
            'age_group_restriction': self.age_group_restriction,
            'seasonal_storage': self.seasonal_storage,
            'requires_access_control': self.requires_access_control,
            'access_level': self.access_level,
            'product_count': self.product_count,
            'total_quantity': self.total_quantity,
            'total_value': self.total_value,
            'pick_frequency': self.pick_frequency,
            'last_pick_date': self.last_pick_date
        }
    
    def _get_capacity_usage(self):
        """Get capacity usage percentage"""
        if self.max_capacity <= 0:
            return 0.0
        
        return (self.current_capacity / self.max_capacity) * 100
    
    def _get_weight_usage(self):
        """Get weight usage percentage"""
        if self.max_weight <= 0:
            return 0.0
        
        return (self.current_weight / self.max_weight) * 100
    
    def validate_age_group(self, product_age_group):
        """Validate if product age group is allowed in this location"""
        if self.age_group_restriction == 'none':
            return True
        
        if self.age_group_restriction == 'toddler' and product_age_group == 'toddler':
            return True
        elif self.age_group_restriction == 'child' and product_age_group == 'child':
            return True
        elif self.age_group_restriction == 'teen' and product_age_group == 'teen':
            return True
        elif self.age_group_restriction == 'toddler_child' and product_age_group in ['toddler', 'child']:
            return True
        elif self.age_group_restriction == 'child_teen' and product_age_group in ['child', 'teen']:
            return True
        
        return False
    
    def check_capacity(self, additional_quantity=0, additional_weight=0):
        """Check if location has enough capacity"""
        capacity_ok = True
        weight_ok = True
        messages = []
        
        if self.max_capacity > 0:
            total_quantity = self.current_capacity + additional_quantity
            if total_quantity > self.max_capacity:
                capacity_ok = False
                messages.append(f"Capacity exceeded. Max: {self.max_capacity}, Current: {self.current_capacity}, Additional: {additional_quantity}")
        
        if self.max_weight > 0:
            total_weight = self.current_weight + additional_weight
            if total_weight > self.max_weight:
                weight_ok = False
                messages.append(f"Weight exceeded. Max: {self.max_weight}, Current: {self.current_weight}, Additional: {additional_weight}")
        
        return capacity_ok and weight_ok, '; '.join(messages) if messages else "Capacity available"
    
    def get_location_hierarchy(self):
        """Get complete location hierarchy"""
        hierarchy = []
        current = self
        
        while current:
            hierarchy.insert(0, {
                'id': current.id,
                'name': current.name,
                'code': current.code,
                'type': current.location_type,
                'warehouse': current.warehouse_id.name
            })
            current = current.parent_id
        
        return hierarchy