# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Warehouse
=============================

Warehouse management for kids clothing retail.
"""

from core_framework.orm import BaseModel, CharField, TextField, BooleanField, IntegerField, DateTimeField, Many2OneField, SelectionField, FloatField, One2ManyField, Many2ManyField
from core_framework.orm import Field
from typing import Dict, Any, Optional
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class Warehouse(BaseModel):
    """Warehouse for inventory management"""
    
    _name = 'warehouse'
    _description = 'Warehouse'
    _table = 'warehouse'
    
    # Basic Information
    name = CharField(
        string='Warehouse Name',
        size=100,
        required=True,
        help='Name of the warehouse'
    )
    
    code = CharField(
        string='Warehouse Code',
        size=20,
        help='Short code for the warehouse'
    )
    
    description = TextField(
        string='Description',
        help='Description of the warehouse'
    )
    
    # Company
    company_id = Many2OneField(
        'res.company',
        string='Company',
        required=True,
        help='Company this warehouse belongs to'
    )
    
    # Warehouse Type
    warehouse_type = SelectionField(
        string='Warehouse Type',
        selection=[
            ('main', 'Main Warehouse'),
            ('branch', 'Branch Warehouse'),
            ('distribution', 'Distribution Center'),
            ('retail', 'Retail Store'),
            ('online', 'Online Fulfillment'),
            ('return', 'Return Center'),
            ('seasonal', 'Seasonal Storage')
        ],
        default='main',
        help='Type of warehouse'
    )
    
    # Configuration
    is_active = BooleanField(
        string='Active',
        default=True,
        help='Whether this warehouse is active'
    )
    
    is_default = BooleanField(
        string='Default',
        default=False,
        help='Whether this is the default warehouse'
    )
    
    # Location Information
    location_id = Many2OneField(
        'stock.location',
        string='Location',
        required=True,
        help='Main location for this warehouse'
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
    total_area = FloatField(
        string='Total Area (sq ft)',
        digits=(12, 2),
        default=0.0,
        help='Total warehouse area in square feet'
    )
    
    storage_area = FloatField(
        string='Storage Area (sq ft)',
        digits=(12, 2),
        default=0.0,
        help='Storage area in square feet'
    )
    
    office_area = FloatField(
        string='Office Area (sq ft)',
        digits=(12, 2),
        default=0.0,
        help='Office area in square feet'
    )
    
    # Capacity
    max_capacity = FloatField(
        string='Max Capacity',
        digits=(12, 2),
        default=0.0,
        help='Maximum storage capacity'
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
        help='Whether warehouse has temperature control'
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
    
    # Humidity Control
    humidity_controlled = BooleanField(
        string='Humidity Controlled',
        default=False,
        help='Whether warehouse has humidity control'
    )
    
    min_humidity = FloatField(
        string='Min Humidity',
        digits=(5, 2),
        help='Minimum humidity percentage'
    )
    
    max_humidity = FloatField(
        string='Max Humidity',
        digits=(5, 2),
        help='Maximum humidity percentage'
    )
    
    # Security
    security_level = SelectionField(
        string='Security Level',
        selection=[
            ('basic', 'Basic'),
            ('standard', 'Standard'),
            ('high', 'High'),
            ('maximum', 'Maximum')
        ],
        default='standard',
        help='Security level of the warehouse'
    )
    
    requires_access_control = BooleanField(
        string='Requires Access Control',
        default=True,
        help='Whether warehouse requires access control'
    )
    
    # Kids Clothing Specific
    age_group_specialization = SelectionField(
        string='Age Group Specialization',
        selection=[
            ('none', 'No Specialization'),
            ('toddler', 'Toddler Specialized'),
            ('child', 'Child Specialized'),
            ('teen', 'Teen Specialized'),
            ('mixed', 'Mixed Age Groups')
        ],
        default='mixed',
        help='Age group specialization of the warehouse'
    )
    
    seasonal_storage = BooleanField(
        string='Seasonal Storage',
        default=False,
        help='Whether warehouse handles seasonal storage'
    )
    
    # Operations
    operation_hours = CharField(
        string='Operation Hours',
        size=100,
        help='Operating hours of the warehouse'
    )
    
    timezone = CharField(
        string='Timezone',
        size=50,
        default='UTC',
        help='Timezone of the warehouse'
    )
    
    # Statistics
    total_products = IntegerField(
        string='Total Products',
        default=0,
        help='Total number of different products'
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
        help='Total value of inventory'
    )
    
    # Performance Metrics
    turnover_rate = FloatField(
        string='Turnover Rate',
        digits=(5, 2),
        default=0.0,
        help='Inventory turnover rate per year'
    )
    
    accuracy_rate = FloatField(
        string='Accuracy Rate',
        digits=(5, 2),
        default=100.0,
        help='Inventory accuracy rate percentage'
    )
    
    # Notes
    note = TextField(
        string='Notes',
        help='Additional notes about this warehouse'
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
        
        # Update statistics when warehouse changes
        if any(field in vals for field in ['is_active', 'warehouse_type']):
            self._update_statistics()
        
        return result
    
    def _update_statistics(self):
        """Update warehouse statistics"""
        for warehouse in self:
            # Count products and quantities in warehouse location
            quants = self.env['stock.quant'].search([('location_id', '=', warehouse.location_id.id)])
            
            warehouse.total_products = len(set(quant.product_id.id for quant in quants))
            warehouse.total_quantity = sum(quant.quantity for quant in quants)
            warehouse.total_value = sum(quant.value for quant in quants)
    
    def action_view_locations(self):
        """View locations in this warehouse"""
        return {
            'type': 'ir.actions.act_window',
            'name': f'Locations - {self.name}',
            'res_model': 'stock.location',
            'view_mode': 'tree,form',
            'domain': [('id', 'child_of', self.location_id.id)],
            'context': {'default_parent_id': self.location_id.id}
        }
    
    def action_view_quants(self):
        """View stock quants in this warehouse"""
        return {
            'type': 'ir.actions.act_window',
            'name': f'Stock Quants - {self.name}',
            'res_model': 'stock.quant',
            'view_mode': 'tree,form',
            'domain': [('location_id', 'child_of', self.location_id.id)],
            'context': {'default_location_id': self.location_id.id}
        }
    
    def action_view_moves(self):
        """View stock moves for this warehouse"""
        return {
            'type': 'ir.actions.act_window',
            'name': f'Stock Moves - {self.name}',
            'res_model': 'stock.move',
            'view_mode': 'tree,form',
            'domain': ['|', ('location_id', 'child_of', self.location_id.id), ('location_dest_id', 'child_of', self.location_id.id)],
            'context': {'default_location_id': self.location_id.id}
        }
    
    def action_view_aging_report(self):
        """View aging report for this warehouse"""
        return {
            'type': 'ir.actions.act_window',
            'name': f'Aging Report - {self.name}',
            'res_model': 'stock.aging',
            'view_mode': 'tree,form',
            'domain': [('warehouse_id', '=', self.id)],
            'context': {'default_warehouse_id': self.id}
        }
    
    def action_view_expiry_report(self):
        """View expiry report for this warehouse"""
        return {
            'type': 'ir.actions.act_window',
            'name': f'Expiry Report - {self.name}',
            'res_model': 'stock.expiry',
            'view_mode': 'tree,form',
            'domain': [('warehouse_id', '=', self.id)],
            'context': {'default_warehouse_id': self.id}
        }
    
    def get_warehouse_summary(self):
        """Get warehouse summary data"""
        return {
            'warehouse_name': self.name,
            'warehouse_code': self.code,
            'warehouse_type': self.warehouse_type,
            'is_active': self.is_active,
            'is_default': self.is_default,
            'company': self.company_id.name,
            'location': self.location_id.name,
            'address': self._get_full_address(),
            'total_area': self.total_area,
            'storage_area': self.storage_area,
            'office_area': self.office_area,
            'max_capacity': self.max_capacity,
            'current_capacity': self.current_capacity,
            'capacity_usage': self._get_capacity_usage(),
            'temperature_controlled': self.temperature_controlled,
            'min_temperature': self.min_temperature,
            'max_temperature': self.max_temperature,
            'humidity_controlled': self.humidity_controlled,
            'min_humidity': self.min_humidity,
            'max_humidity': self.max_humidity,
            'security_level': self.security_level,
            'requires_access_control': self.requires_access_control,
            'age_group_specialization': self.age_group_specialization,
            'seasonal_storage': self.seasonal_storage,
            'operation_hours': self.operation_hours,
            'timezone': self.timezone,
            'total_products': self.total_products,
            'total_quantity': self.total_quantity,
            'total_value': self.total_value,
            'turnover_rate': self.turnover_rate,
            'accuracy_rate': self.accuracy_rate
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
        """Validate if product age group is allowed in this warehouse"""
        if self.age_group_specialization == 'none' or self.age_group_specialization == 'mixed':
            return True
        
        if self.age_group_specialization == 'toddler' and product_age_group == 'toddler':
            return True
        elif self.age_group_specialization == 'child' and product_age_group == 'child':
            return True
        elif self.age_group_specialization == 'teen' and product_age_group == 'teen':
            return True
        
        return False
    
    def check_capacity(self, additional_quantity=0):
        """Check if warehouse has enough capacity"""
        if self.max_capacity <= 0:
            return True, "No capacity limit"
        
        total_quantity = self.current_capacity + additional_quantity
        if total_quantity > self.max_capacity:
            return False, f"Capacity exceeded. Max: {self.max_capacity}, Current: {self.current_capacity}, Additional: {additional_quantity}"
        
        return True, "Capacity available"
    
    def get_warehouse_hierarchy(self):
        """Get complete warehouse hierarchy"""
        hierarchy = []
        current = self.location_id
        
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