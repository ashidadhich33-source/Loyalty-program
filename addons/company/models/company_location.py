# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Company - Company Location
============================================

Standalone version of the company location model.
"""

from core_framework.orm import BaseModel, CharField, TextField, BooleanField, IntegerField, DateTimeField, Many2OneField, SelectionField, FloatField
from core_framework.orm import Field
from typing import Dict, Any, Optional
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class CompanyLocation(BaseModel):
    """Company location model for Kids Clothing ERP"""
    
    _name = 'company.location'
    _description = 'Company Location'
    _table = 'company_location'
    
    # Basic fields
    name = CharField(
        string='Location Name',
        size=100,
        required=True,
        help='Name of the location'
    )
    
    code = CharField(
        string='Location Code',
        size=20,
        required=True,
        help='Unique code for the location'
    )
    
    description = TextField(
        string='Description',
        help='Description of the location'
    )
    
    # Company relationship
    company_id = IntegerField(
        string='Company ID',
        required=True,
        help='Company this location belongs to'
    )
    
    branch_id = IntegerField(
        string='Branch ID',
        help='Branch this location belongs to'
    )
    
    # Location information
    location_type = SelectionField(
        string='Location Type',
        selection=[
            ('warehouse', 'Warehouse'),
            ('showroom', 'Showroom'),
            ('office', 'Office'),
            ('store', 'Store'),
            ('factory', 'Factory'),
            ('distribution_center', 'Distribution Center'),
            ('retail_outlet', 'Retail Outlet'),
        ],
        default='warehouse',
        help='Type of location'
    )
    
    # Location address
    street = CharField(
        string='Street',
        size=100,
        help='Street address'
    )
    
    street2 = CharField(
        string='Street2',
        size=100,
        help='Street address line 2'
    )
    
    city = CharField(
        string='City',
        size=50,
        help='City'
    )
    
    state_id = IntegerField(
        string='State ID',
        help='State'
    )
    
    zip = CharField(
        string='ZIP',
        size=10,
        help='ZIP code'
    )
    
    country_id = IntegerField(
        string='Country ID',
        help='Country'
    )
    
    # Contact information
    phone = CharField(
        string='Phone',
        size=20,
        help='Location phone number'
    )
    
    mobile = CharField(
        string='Mobile',
        size=20,
        help='Location mobile number'
    )
    
    email = CharField(
        string='Email',
        size=100,
        help='Location email address'
    )
    
    # Location settings
    is_active = BooleanField(
        string='Active',
        default=True,
        help='Whether the location is active'
    )
    
    is_default = BooleanField(
        string='Default Location',
        default=False,
        help='Whether this is the default location'
    )
    
    # Location capacity
    max_capacity = IntegerField(
        string='Max Capacity',
        default=1000,
        help='Maximum capacity for this location'
    )
    
    current_capacity = IntegerField(
        string='Current Capacity',
        default=0,
        help='Current capacity for this location'
    )
    
    # Location features
    enable_inventory = BooleanField(
        string='Enable Inventory',
        default=True,
        help='Enable inventory for this location'
    )
    
    enable_sales = BooleanField(
        string='Enable Sales',
        default=True,
        help='Enable sales for this location'
    )
    
    enable_purchase = BooleanField(
        string='Enable Purchase',
        default=True,
        help='Enable purchase for this location'
    )
    
    enable_pos = BooleanField(
        string='Enable POS',
        default=True,
        help='Enable POS for this location'
    )
    
    # Location analytics
    total_sales = FloatField(
        string='Total Sales',
        default=0.0,
        help='Total sales for this location'
    )
    
    total_orders = IntegerField(
        string='Total Orders',
        default=0,
        help='Total orders for this location'
    )
    
    # Location manager
    manager_id = IntegerField(
        string='Location Manager ID',
        help='Location manager'
    )
    
    def create(self, vals: Dict[str, Any]):
        """Override create to set default values"""
        return super().create(vals)
    
    def write(self, vals: Dict[str, Any]):
        """Override write to handle location updates"""
        result = super().write(vals)
        
        # Log location updates
        for location in self:
            if vals:
                logger.info(f"Location {location.name} updated: {', '.join(vals.keys())}")
        
        return result
    
    def unlink(self):
        """Override unlink to prevent deletion of locations with data"""
        for location in self:
            # In standalone version, we'll do basic validation
            if location.current_capacity > 0:
                raise ValueError('Cannot delete location with capacity. Please clear capacity first.')
        
        return super().unlink()
    
    def action_activate(self):
        """Activate location"""
        self.is_active = True
        return True
    
    def action_deactivate(self):
        """Deactivate location"""
        self.is_active = False
        return True
    
    def action_set_default(self):
        """Set as default location"""
        # Remove default from other locations in same company
        other_locations = self.search([
            ('company_id', '=', self.company_id),
            ('is_default', '=', True),
        ])
        for location in other_locations:
            location.is_default = False
        
        # Set this location as default
        self.is_default = True
        return True
    
    def get_location_analytics(self):
        """Get location analytics"""
        return {
            'total_capacity': self.max_capacity,
            'current_capacity': self.current_capacity,
            'total_sales': self.total_sales,
            'total_orders': self.total_orders,
            'location_type': self.location_type,
            'is_active': self.is_active,
            'is_default': self.is_default,
            'enable_inventory': self.enable_inventory,
            'enable_sales': self.enable_sales,
            'enable_purchase': self.enable_purchase,
            'enable_pos': self.enable_pos,
        }
    
    @classmethod
    def get_locations_by_company(cls, company_id: int):
        """Get locations by company"""
        return cls.search([
            ('company_id', '=', company_id),
            ('is_active', '=', True),
        ])
    
    @classmethod
    def get_locations_by_branch(cls, branch_id: int):
        """Get locations by branch"""
        return cls.search([
            ('branch_id', '=', branch_id),
            ('is_active', '=', True),
        ])
    
    @classmethod
    def get_locations_by_type(cls, location_type: str):
        """Get locations by type"""
        return cls.search([
            ('location_type', '=', location_type),
            ('is_active', '=', True),
        ])
    
    @classmethod
    def get_default_location(cls, company_id: int):
        """Get default location for company"""
        return cls.search([
            ('company_id', '=', company_id),
            ('is_default', '=', True),
        ], limit=1)
    
    @classmethod
    def get_location_analytics_summary(cls):
        """Get location analytics summary"""
        # In standalone version, we'll return mock data
        return {
            'total_locations': 0,
            'active_locations': 0,
            'default_locations': 0,
            'inactive_locations': 0,
            'active_percentage': 0,
        }
    
    def _check_code(self):
        """Validate location code"""
        if self.code:
            # Check for duplicate codes in same company
            existing = self.search([
                ('code', '=', self.code),
                ('company_id', '=', self.company_id),
                ('id', '!=', self.id),
            ])
            if existing:
                raise ValueError('Location code must be unique within company')
    
    def _check_default_location(self):
        """Validate default location"""
        if self.is_default:
            # Check if there's already a default location in same company
            existing_default = self.search([
                ('is_default', '=', True),
                ('company_id', '=', self.company_id),
                ('id', '!=', self.id),
            ])
            if existing_default:
                raise ValueError('Only one location can be set as default per company')
    
    def _check_capacity(self):
        """Validate capacity"""
        if self.current_capacity > self.max_capacity:
            raise ValueError('Current capacity cannot exceed maximum capacity')
    
    def action_duplicate(self):
        """Duplicate location"""
        self.ensure_one()
        
        new_location = self.copy({
            'name': f'{self.name} (Copy)',
            'code': f'{self.code}_copy',
            'is_default': False,
        })
        
        return new_location
    
    def action_export_location(self):
        """Export location data"""
        self.ensure_one()
        
        return {
            'name': self.name,
            'code': self.code,
            'location_type': self.location_type,
            'company_id': self.company_id,
            'branch_id': self.branch_id,
            'street': self.street,
            'city': self.city,
            'state_id': self.state_id,
            'zip': self.zip,
            'country_id': self.country_id,
            'phone': self.phone,
            'mobile': self.mobile,
            'email': self.email,
            'max_capacity': self.max_capacity,
            'enable_inventory': self.enable_inventory,
            'enable_sales': self.enable_sales,
            'enable_purchase': self.enable_purchase,
            'enable_pos': self.enable_pos,
        }
    
    def action_import_location(self, location_data: Dict[str, Any]):
        """Import location data"""
        self.ensure_one()
        
        self.write(location_data)
        return True