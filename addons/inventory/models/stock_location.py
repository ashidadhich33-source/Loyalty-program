# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Stock Location
==================================

Stock location management for kids clothing retail.
"""

from core_framework.orm import BaseModel, CharField, TextField, BooleanField, IntegerField, DateTimeField, Many2OneField, SelectionField, FloatField, One2ManyField, Many2ManyField
from core_framework.orm import Field
from typing import Dict, Any, Optional
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class StockLocation(BaseModel):
    """Stock location for inventory management"""
    
    _name = 'stock.location'
    _description = 'Stock Location'
    _table = 'stock_location'
    
    # Basic Information
    name = CharField(
        string='Location Name',
        size=100,
        required=True,
        help='Name of the stock location'
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
    
    # Location Hierarchy
    parent_id = Many2OneField(
        'stock.location',
        string='Parent Location',
        help='Parent location in the hierarchy'
    )
    
    child_ids = One2ManyField(
        'stock.location',
        string='Child Locations',
        inverse_name='parent_id',
        help='Child locations'
    )
    
    # Location Type
    location_type = SelectionField(
        string='Location Type',
        selection=[
            ('internal', 'Internal Location'),
            ('customer', 'Customer Location'),
            ('vendor', 'Vendor Location'),
            ('inventory', 'Inventory Location'),
            ('production', 'Production Location'),
            ('transit', 'Transit Location'),
            ('view', 'View')
        ],
        default='internal',
        help='Type of location'
    )
    
    # Usage
    usage = SelectionField(
        string='Usage',
        selection=[
            ('supplier', 'Vendor Location'),
            ('view', 'View'),
            ('internal', 'Internal Location'),
            ('customer', 'Customer Location'),
            ('inventory', 'Inventory'),
            ('production', 'Production'),
            ('transit', 'Transit Location')
        ],
        default='internal',
        help='Usage of the location'
    )
    
    # Configuration
    is_active = BooleanField(
        string='Active',
        default=True,
        help='Whether this location is active'
    )
    
    is_scrap_location = BooleanField(
        string='Scrap Location',
        default=False,
        help='Whether this is a scrap location'
    )
    
    is_return_location = BooleanField(
        string='Return Location',
        default=False,
        help='Whether this is a return location'
    )
    
    # Company
    company_id = Many2OneField(
        'res.company',
        string='Company',
        required=True,
        help='Company this location belongs to'
    )
    
    # Address Information
    street = CharField(
        string='Street',
        size=200,
        help='Street address'
    )
    
    street2 = CharField(
        string='Street 2',
        size=200,
        help='Additional street information'
    )
    
    city = CharField(
        string='City',
        size=100,
        help='City'
    )
    
    state_id = Many2OneField(
        'res.country.state',
        string='State',
        help='State/Province'
    )
    
    zip = CharField(
        string='ZIP',
        size=20,
        help='ZIP/Postal code'
    )
    
    country_id = Many2OneField(
        'res.country',
        string='Country',
        help='Country'
    )
    
    # Contact Information
    phone = CharField(
        string='Phone',
        size=20,
        help='Phone number'
    )
    
    email = CharField(
        string='Email',
        size=100,
        help='Email address'
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
        if any(field in vals for field in ['is_active', 'usage', 'location_type']):
            self._update_statistics()
        
        return result
    
    def _update_statistics(self):
        """Update location statistics"""
        for location in self:
            # Count products and quantities
            quants = self.env['stock.quant'].search([('location_id', '=', location.id)])
            
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
            'domain': [('location_id', '=', self.id)],
            'context': {'default_location_id': self.id}
        }
    
    def action_view_moves(self):
        """View stock moves for this location"""
        return {
            'type': 'ir.actions.act_window',
            'name': f'Stock Moves - {self.name}',
            'res_model': 'stock.move',
            'view_mode': 'tree,form',
            'domain': ['|', ('location_id', '=', self.id), ('location_dest_id', '=', self.id)],
            'context': {'default_location_id': self.id}
        }
    
    def action_view_pickings(self):
        """View stock pickings for this location"""
        return {
            'type': 'ir.actions.act_window',
            'name': f'Stock Pickings - {self.name}',
            'res_model': 'stock.picking',
            'view_mode': 'tree,form',
            'domain': ['|', ('location_id', '=', self.id), ('location_dest_id', '=', self.id)],
            'context': {'default_location_id': self.id}
        }
    
    def get_location_summary(self):
        """Get location summary data"""
        return {
            'location_name': self.name,
            'location_code': self.code,
            'location_type': self.location_type,
            'usage': self.usage,
            'is_active': self.is_active,
            'parent_location': self.parent_id.name if self.parent_id else 'None',
            'child_count': len(self.child_ids),
            'company': self.company_id.name,
            'address': self._get_full_address(),
            'product_count': self.product_count,
            'total_quantity': self.total_quantity,
            'total_value': self.total_value,
            'capacity_usage': self._get_capacity_usage(),
            'temperature_controlled': self.temperature_controlled,
            'age_group_restriction': self.age_group_restriction,
            'requires_access_control': self.requires_access_control,
            'access_level': self.access_level
        }
    
    def _get_full_address(self):
        """Get full address string"""
        address_parts = []
        if self.street:
            address_parts.append(self.street)
        if self.street2:
            address_parts.append(self.street2)
        if self.city:
            address_parts.append(self.city)
        if self.state_id:
            address_parts.append(self.state_id.name)
        if self.zip:
            address_parts.append(self.zip)
        if self.country_id:
            address_parts.append(self.country_id.name)
        
        return ', '.join(address_parts)
    
    def _get_capacity_usage(self):
        """Get capacity usage percentage"""
        if self.max_capacity <= 0:
            return 0.0
        
        return (self.current_capacity / self.max_capacity) * 100
    
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
    
    def check_capacity(self, additional_quantity=0):
        """Check if location has enough capacity"""
        if self.max_capacity <= 0:
            return True, "No capacity limit"
        
        total_quantity = self.current_capacity + additional_quantity
        if total_quantity > self.max_capacity:
            return False, f"Capacity exceeded. Max: {self.max_capacity}, Current: {self.current_capacity}, Additional: {additional_quantity}"
        
        return True, "Capacity available"
    
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
                'usage': current.usage
            })
            current = current.parent_id
        
        return hierarchy