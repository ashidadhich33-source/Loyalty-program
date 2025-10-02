# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Contacts - Contact Address Management
=====================================================

Standalone version of the contact address management model.
"""

from core_framework.orm import BaseModel, CharField, TextField, BooleanField, IntegerField, DateTimeField, Many2OneField, SelectionField
from core_framework.orm import Field
from typing import Dict, Any, Optional
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class ContactAddress(BaseModel):
    """Contact address model for Kids Clothing ERP"""
    
    _name = 'contact.address'
    _description = 'Contact Address'
    _table = 'contact_address'
    
    # Basic address information
    contact_id = IntegerField(
        string='Contact ID',
        required=True,
        help='Contact this address belongs to'
    )
    
    address_type = SelectionField(
        string='Address Type',
        selection=[
            ('home', 'Home'),
            ('office', 'Office'),
            ('billing', 'Billing'),
            ('shipping', 'Shipping'),
            ('other', 'Other'),
        ],
        required=True,
        help='Type of address'
    )
    
    name = CharField(
        string='Address Name',
        size=255,
        help='Name for this address'
    )
    
    # Address details
    street = CharField(
        string='Street',
        size=255,
        help='Street address'
    )
    
    street2 = CharField(
        string='Street2',
        size=255,
        help='Street address line 2'
    )
    
    city = CharField(
        string='City',
        size=100,
        help='City'
    )
    
    state_id = IntegerField(
        string='State ID',
        help='State'
    )
    
    zip = CharField(
        string='ZIP',
        size=20,
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
        help='Phone number for this address'
    )
    
    mobile = CharField(
        string='Mobile',
        size=20,
        help='Mobile number for this address'
    )
    
    email = CharField(
        string='Email',
        size=255,
        help='Email address for this address'
    )
    
    # Address settings
    is_default = BooleanField(
        string='Default Address',
        default=False,
        help='Whether this is the default address'
    )
    
    is_active = BooleanField(
        string='Active',
        default=True,
        help='Whether this address is active'
    )
    
    # Additional information
    notes = TextField(
        string='Notes',
        help='Additional notes about this address'
    )
    
    # Company relationship
    company_id = IntegerField(
        string='Company ID',
        default=1,
        help='Company this address belongs to'
    )
    
    def create(self, vals: Dict[str, Any]):
        """Override create to set default values"""
        return super().create(vals)
    
    def write(self, vals: Dict[str, Any]):
        """Override write to handle address updates"""
        result = super().write(vals)
        
        # Log address updates
        for address in self:
            if vals:
                logger.info(f"Address for contact {address.contact_id} updated: {', '.join(vals.keys())}")
        
        return result
    
    def get_address_info(self):
        """Get address information"""
        return {
            'contact_id': self.contact_id,
            'address_type': self.address_type,
            'name': self.name,
            'street': self.street,
            'street2': self.street2,
            'city': self.city,
            'state_id': self.state_id,
            'zip': self.zip,
            'country_id': self.country_id,
            'phone': self.phone,
            'mobile': self.mobile,
            'email': self.email,
            'is_default': self.is_default,
            'is_active': self.is_active,
            'notes': self.notes,
        }
    
    @classmethod
    def get_addresses_by_contact(cls, contact_id: int):
        """Get addresses by contact"""
        return cls.search([
            ('contact_id', '=', contact_id),
            ('is_active', '=', True),
        ])
    
    @classmethod
    def get_addresses_by_type(cls, address_type: str):
        """Get addresses by type"""
        return cls.search([
            ('address_type', '=', address_type),
            ('is_active', '=', True),
        ])
    
    @classmethod
    def get_default_address(cls, contact_id: int, address_type: str = None):
        """Get default address for contact"""
        domain = [
            ('contact_id', '=', contact_id),
            ('is_default', '=', True),
            ('is_active', '=', True),
        ]
        
        if address_type:
            domain.append(('address_type', '=', address_type))
        
        return cls.search(domain, limit=1)
    
    @classmethod
    def get_addresses_by_city(cls, city: str):
        """Get addresses by city"""
        return cls.search([
            ('city', '=', city),
            ('is_active', '=', True),
        ])
    
    @classmethod
    def get_addresses_by_state(cls, state_id: int):
        """Get addresses by state"""
        return cls.search([
            ('state_id', '=', state_id),
            ('is_active', '=', True),
        ])
    
    @classmethod
    def get_addresses_by_country(cls, country_id: int):
        """Get addresses by country"""
        return cls.search([
            ('country_id', '=', country_id),
            ('is_active', '=', True),
        ])
    
    @classmethod
    def get_address_analytics(cls, contact_id: int):
        """Get address analytics for contact"""
        addresses = cls.search([('contact_id', '=', contact_id)])
        
        if not addresses:
            return {
                'total_addresses': 0,
                'by_type': {},
                'default_addresses': 0,
                'active_addresses': 0,
            }
        
        # Count by type
        by_type = {}
        for address in addresses:
            addr_type = address.address_type
            by_type[addr_type] = by_type.get(addr_type, 0) + 1
        
        return {
            'total_addresses': len(addresses),
            'by_type': by_type,
            'default_addresses': len([a for a in addresses if a.is_default]),
            'active_addresses': len([a for a in addresses if a.is_active]),
        }
    
    @classmethod
    def get_address_analytics_summary(cls):
        """Get address analytics summary"""
        # In standalone version, we'll return mock data
        return {
            'total_addresses': 0,
            'by_type': {},
            'default_addresses': 0,
            'active_addresses': 0,
            'inactive_addresses': 0,
            'active_percentage': 0,
        }
    
    def action_set_default(self):
        """Set as default address"""
        # Remove default from other addresses of same type for same contact
        other_addresses = self.search([
            ('contact_id', '=', self.contact_id),
            ('address_type', '=', self.address_type),
            ('is_default', '=', True),
            ('id', '!=', self.id),
        ])
        for address in other_addresses:
            address.is_default = False
        
        # Set this address as default
        self.is_default = True
        return True
    
    def action_activate(self):
        """Activate address"""
        self.is_active = True
        return True
    
    def action_deactivate(self):
        """Deactivate address"""
        self.is_active = False
        return True
    
    def get_full_address(self):
        """Get full address as string"""
        address_parts = []
        
        if self.street:
            address_parts.append(self.street)
        if self.street2:
            address_parts.append(self.street2)
        if self.city:
            address_parts.append(self.city)
        if self.zip:
            address_parts.append(self.zip)
        
        return ', '.join(address_parts)
    
    def action_duplicate(self):
        """Duplicate address"""
        self.ensure_one()
        
        new_address = self.copy({
            'name': f'{self.name} (Copy)',
            'is_default': False,
        })
        
        return new_address
    
    def action_export_address(self):
        """Export address data"""
        self.ensure_one()
        
        return {
            'contact_id': self.contact_id,
            'address_type': self.address_type,
            'name': self.name,
            'street': self.street,
            'street2': self.street2,
            'city': self.city,
            'state_id': self.state_id,
            'zip': self.zip,
            'country_id': self.country_id,
            'phone': self.phone,
            'mobile': self.mobile,
            'email': self.email,
            'is_default': self.is_default,
            'is_active': self.is_active,
            'notes': self.notes,
        }
    
    def action_import_address(self, address_data: Dict[str, Any]):
        """Import address data"""
        self.ensure_one()
        
        self.write(address_data)
        return True