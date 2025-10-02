# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Contacts - Vendor Management
==============================================

Standalone version of the vendor management model.
"""

from core_framework.orm import BaseModel, CharField, TextField, BooleanField, IntegerField, DateTimeField, Many2OneField, SelectionField, FloatField
from core_framework.orm import Field
from typing import Dict, Any, Optional
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class ContactVendor(BaseModel):
    """Vendor contact model for Kids Clothing ERP"""
    
    _name = 'contact.vendor'
    _description = 'Vendor Contact'
    _table = 'contact_vendor'
    
    # Basic vendor information
    name = CharField(
        string='Vendor Name',
        size=255,
        required=True,
        help='Name of the vendor'
    )
    
    partner_id = IntegerField(
        string='Partner ID',
        required=True,
        help='Related partner'
    )
    
    vendor_code = CharField(
        string='Vendor Code',
        size=50,
        help='Unique vendor code'
    )
    
    vendor_type = SelectionField(
        string='Vendor Type',
        selection=[
            ('service', 'Service Provider'),
            ('consultant', 'Consultant'),
            ('contractor', 'Contractor'),
            ('freelancer', 'Freelancer'),
            ('other', 'Other'),
        ],
        default='service',
        help='Type of vendor'
    )
    
    # Vendor details
    contact_person = CharField(
        string='Contact Person',
        size=255,
        help='Primary contact person'
    )
    
    designation = CharField(
        string='Designation',
        size=100,
        help='Designation of contact person'
    )
    
    phone = CharField(
        string='Phone',
        size=20,
        help='Phone number'
    )
    
    mobile = CharField(
        string='Mobile',
        size=20,
        help='Mobile number'
    )
    
    email = CharField(
        string='Email',
        size=255,
        help='Email address'
    )
    
    website = CharField(
        string='Website',
        size=255,
        help='Website URL'
    )
    
    # Business information
    business_license = CharField(
        string='Business License',
        size=100,
        help='Business license number'
    )
    
    tax_id = CharField(
        string='Tax ID',
        size=50,
        help='Tax identification number'
    )
    
    gstin = CharField(
        string='GSTIN',
        size=15,
        help='GST Identification Number'
    )
    
    pan_number = CharField(
        string='PAN Number',
        size=10,
        help='PAN Number'
    )
    
    # Service information
    service_category = CharField(
        string='Service Category',
        size=100,
        help='Category of services provided'
    )
    
    service_description = TextField(
        string='Service Description',
        help='Description of services provided'
    )
    
    # Payment terms
    payment_terms = IntegerField(
        string='Payment Terms ID',
        help='Payment terms for this vendor'
    )
    
    hourly_rate = FloatField(
        string='Hourly Rate',
        default=0.0,
        help='Hourly rate for services'
    )
    
    daily_rate = FloatField(
        string='Daily Rate',
        default=0.0,
        help='Daily rate for services'
    )
    
    # Vendor status
    status = SelectionField(
        string='Status',
        selection=[
            ('active', 'Active'),
            ('inactive', 'Inactive'),
            ('blacklisted', 'Blacklisted'),
        ],
        default='active',
        help='Vendor status'
    )
    
    # Vendor rating
    rating = SelectionField(
        string='Rating',
        selection=[
            ('1', '1 Star'),
            ('2', '2 Stars'),
            ('3', '3 Stars'),
            ('4', '4 Stars'),
            ('5', '5 Stars'),
        ],
        help='Vendor rating'
    )
    
    # Company relationship
    company_id = IntegerField(
        string='Company ID',
        default=1,
        help='Company this vendor belongs to'
    )
    
    # Vendor analytics
    total_services = IntegerField(
        string='Total Services',
        default=0,
        help='Total number of services provided'
    )
    
    total_amount = FloatField(
        string='Total Amount',
        default=0.0,
        help='Total amount paid to vendor'
    )
    
    last_service_date = DateTimeField(
        string='Last Service Date',
        help='Date of last service'
    )
    
    average_service_value = FloatField(
        string='Average Service Value',
        default=0.0,
        help='Average service value'
    )
    
    # Vendor notes
    notes = TextField(
        string='Notes',
        help='Additional notes about the vendor'
    )
    
    def create(self, vals: Dict[str, Any]):
        """Override create to set default values"""
        # Generate vendor code if not provided
        if not vals.get('vendor_code'):
            vals['vendor_code'] = f"VEND{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        return super().create(vals)
    
    def write(self, vals: Dict[str, Any]):
        """Override write to handle vendor updates"""
        result = super().write(vals)
        
        # Log vendor updates
        for vendor in self:
            if vals:
                logger.info(f"Vendor {vendor.name} updated: {', '.join(vals.keys())}")
        
        return result
    
    def get_vendor_analytics(self):
        """Get vendor analytics"""
        return {
            'total_services': self.total_services,
            'total_amount': self.total_amount,
            'last_service_date': self.last_service_date,
            'average_service_value': self.average_service_value,
            'status': self.status,
            'rating': self.rating,
            'vendor_type': self.vendor_type,
        }
    
    @classmethod
    def get_vendors_by_type(cls, vendor_type: str):
        """Get vendors by type"""
        return cls.search([
            ('vendor_type', '=', vendor_type),
            ('status', '=', 'active'),
        ])
    
    @classmethod
    def get_vendors_by_company(cls, company_id: int):
        """Get vendors by company"""
        return cls.search([
            ('company_id', '=', company_id),
            ('status', '=', 'active'),
        ])
    
    @classmethod
    def get_vendors_by_rating(cls, rating: str):
        """Get vendors by rating"""
        return cls.search([
            ('rating', '=', rating),
            ('status', '=', 'active'),
        ])
    
    @classmethod
    def get_vendors_by_service_category(cls, service_category: str):
        """Get vendors by service category"""
        return cls.search([
            ('service_category', '=', service_category),
            ('status', '=', 'active'),
        ])
    
    @classmethod
    def get_vendor_analytics_summary(cls):
        """Get vendor analytics summary"""
        # In standalone version, we'll return mock data
        return {
            'total_vendors': 0,
            'active_vendors': 0,
            'by_type': {},
            'by_rating': {},
            'by_service_category': {},
            'inactive_vendors': 0,
            'active_percentage': 0,
        }
    
    def action_activate(self):
        """Activate vendor"""
        self.status = 'active'
        return True
    
    def action_deactivate(self):
        """Deactivate vendor"""
        self.status = 'inactive'
        return True
    
    def action_blacklist(self):
        """Blacklist vendor"""
        self.status = 'blacklisted'
        return True
    
    def action_unblacklist(self):
        """Remove from blacklist"""
        self.status = 'active'
        return True
    
    def get_service_rates(self):
        """Get service rates"""
        return {
            'hourly_rate': self.hourly_rate,
            'daily_rate': self.daily_rate,
        }
    
    def action_duplicate(self):
        """Duplicate vendor"""
        self.ensure_one()
        
        new_vendor = self.copy({
            'name': f'{self.name} (Copy)',
            'vendor_code': f"VEND{datetime.now().strftime('%Y%m%d%H%M%S')}",
        })
        
        return new_vendor
    
    def action_export_vendor(self):
        """Export vendor data"""
        self.ensure_one()
        
        return {
            'name': self.name,
            'vendor_code': self.vendor_code,
            'vendor_type': self.vendor_type,
            'contact_person': self.contact_person,
            'designation': self.designation,
            'phone': self.phone,
            'mobile': self.mobile,
            'email': self.email,
            'website': self.website,
            'business_license': self.business_license,
            'tax_id': self.tax_id,
            'gstin': self.gstin,
            'pan_number': self.pan_number,
            'service_category': self.service_category,
            'service_description': self.service_description,
            'payment_terms': self.payment_terms,
            'hourly_rate': self.hourly_rate,
            'daily_rate': self.daily_rate,
            'status': self.status,
            'rating': self.rating,
        }
    
    def action_import_vendor(self, vendor_data: Dict[str, Any]):
        """Import vendor data"""
        self.ensure_one()
        
        self.write(vendor_data)
        return True