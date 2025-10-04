# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Contacts - Partner Management
==============================================

Standalone version of the partner management model.
"""

from core_framework.orm import BaseModel, CharField, TextField, BooleanField, IntegerField, DateTimeField, Many2OneField, SelectionField, FloatField, One2ManyField, Many2ManyField, DateField
from core_framework.orm import Field
from typing import Dict, Any, Optional, List
import logging
from datetime import datetime, date

logger = logging.getLogger(__name__)

class ResPartner(BaseModel):
    """Extended partner model for Kids Clothing ERP"""
    
    _name = 'res.partner'
    _description = 'Partners'
    _table = 'res_partner'
    
    # Basic partner information
    name = CharField(
        string='Name',
        size=255,
        required=True,
        help='Name of the partner'
    )
    
    # Contact Type
    contact_type = SelectionField(
        string='Contact Type',
        selection=[
            ('customer', 'Customer'),
            ('supplier', 'Supplier'),
            ('vendor', 'Vendor'),
            ('both', 'Customer & Supplier'),
            ('other', 'Other'),
        ],
        default='customer',
        help='Type of contact'
    )
    
    # Kids Clothing Specific
    preferred_age_group = SelectionField(
        string='Preferred Age Group',
        selection=[
            ('newborn', 'Newborn (0-3 months)'),
            ('infant', 'Infant (3-12 months)'),
            ('toddler', 'Toddler (1-3 years)'),
            ('preschool', 'Preschool (3-5 years)'),
            ('school_age', 'School Age (6-12 years)'),
            ('teen', 'Teen (13-18 years)'),
        ],
        help='Preferred age group for products'
    )
    
    preferred_gender = SelectionField(
        string='Preferred Gender',
        selection=[
            ('boy', 'Boy'),
            ('girl', 'Girl'),
            ('unisex', 'Unisex'),
        ],
        help='Preferred gender for products'
    )
    
    preferred_brands = Many2ManyField(
        string='Preferred Brands',
        comodel_name='product.brand',
        help='Preferred product brands'
    )
    
    preferred_colors = CharField(
        string='Preferred Colors',
        size=255,
        help='Preferred colors'
    )
    
    preferred_styles = CharField(
        string='Preferred Styles',
        size=255,
        help='Preferred styles'
    )
    
    # Contact Details
    alternate_mobile = CharField(
        string='Alternate Mobile',
        size=20,
        help='Alternate mobile number'
    )
    
    whatsapp_number = CharField(
        string='WhatsApp Number',
        size=20,
        help='WhatsApp number'
    )
    
    # Location Information
    street = CharField(
        string='Street',
        size=255,
        help='Street address'
    )
    
    city = CharField(
        string='City',
        size=100,
        help='City'
    )
    
    state = CharField(
        string='State',
        size=100,
        help='State'
    )
    
    pincode = CharField(
        string='Pincode',
        size=10,
        help='Pincode/ZIP code'
    )
    
    country = CharField(
        string='Country',
        size=100,
        default='India',
        help='Country'
    )
    
    # GST Information
    gstin = CharField(
        string='GSTIN',
        size=15,
        help='GST Registration Number'
    )
    
    skype_id = CharField(
        string='Skype ID',
        size=100,
        help='Skype ID'
    )
    
    linkedin_url = CharField(
        string='LinkedIn URL',
        size=255,
        help='LinkedIn profile URL'
    )
    
    facebook_url = CharField(
        string='Facebook URL',
        size=255,
        help='Facebook profile URL'
    )
    
    instagram_url = CharField(
        string='Instagram URL',
        size=255,
        help='Instagram profile URL'
    )
    
    # Indian Localization
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
    
    gst_registered = BooleanField(
        string='GST Registered',
        default=False,
        help='Whether GST registered'
    )
    
    # Contact Categories and Tags
    category_ids = Many2ManyField(
        string='Categories',
        comodel_name='contact.category',
        help='Contact categories'
    )
    
    tag_ids = Many2ManyField(
        string='Tags',
        comodel_name='contact.tag',
        help='Contact tags'
    )
    
    # Contact Status
    status = SelectionField(
        string='Status',
        selection=[
            ('active', 'Active'),
            ('inactive', 'Inactive'),
            ('prospect', 'Prospect'),
            ('blacklisted', 'Blacklisted'),
        ],
        default='active',
        help='Contact status'
    )
    
    # Contact Rating
    rating = SelectionField(
        string='Rating',
        selection=[
            ('1', '1 Star'),
            ('2', '2 Stars'),
            ('3', '3 Stars'),
            ('4', '4 Stars'),
            ('5', '5 Stars'),
        ],
        help='Contact rating'
    )
    
    # Contact Analytics
    total_orders = IntegerField(
        string='Total Orders',
        default=0,
        help='Total number of orders'
    )
    
    total_purchases = FloatField(
        string='Total Purchases',
        default=0.0,
        help='Total purchase amount'
    )
    
    last_order_date = DateField(
        string='Last Order Date',
        help='Date of last order'
    )
    
    average_order_value = FloatField(
        string='Average Order Value',
        default=0.0,
        help='Average order value'
    )
    
    # Relations
    child_profile_ids = One2ManyField(
        string='Child Profiles',
        comodel_name='child.profile',
        inverse_name='parent_id',
        help='Child profiles for this contact'
    )
    
    history_ids = One2ManyField(
        string='History',
        comodel_name='contact.history',
        inverse_name='contact_id',
        help='Contact history'
    )
    
    communication_ids = One2ManyField(
        string='Communications',
        comodel_name='contact.communication',
        inverse_name='contact_id',
        help='Contact communications'
    )
    
    address_ids = One2ManyField(
        string='Addresses',
        comodel_name='contact.address',
        inverse_name='contact_id',
        help='Contact addresses'
    )
    
    # Multi-Company
    company_ids = Many2ManyField(
        string='Companies',
        comodel_name='res.company',
        help='Companies this contact belongs to'
    )
    
    def create(self, vals: Dict[str, Any]):
        """Override create to set default values"""
        return super().create(vals)
    
    def write(self, vals: Dict[str, Any]):
        """Override write to handle partner updates"""
        result = super().write(vals)
        
        # Log partner updates
        for partner in self:
            if vals:
                logger.info(f"Partner {partner.name} updated: {', '.join(vals.keys())}")
        
        return result
    
    def get_partner_analytics(self):
        """Get partner analytics"""
        return {
            'total_orders': self.total_orders,
            'total_purchases': self.total_purchases,
            'last_order_date': self.last_order_date,
            'average_order_value': self.average_order_value,
            'status': self.status,
            'rating': self.rating,
            'contact_type': self.contact_type,
        }
    
    @classmethod
    def get_partners_by_type(cls, contact_type: str):
        """Get partners by type"""
        return cls.search([
            ('contact_type', '=', contact_type),
            ('status', '=', 'active'),
        ])
    
    @classmethod
    def get_customers(cls):
        """Get all customers"""
        return cls.search([
            ('contact_type', 'in', ['customer', 'both']),
            ('status', '=', 'active'),
        ])
    
    @classmethod
    def get_suppliers(cls):
        """Get all suppliers"""
        return cls.search([
            ('contact_type', 'in', ['supplier', 'both']),
            ('status', '=', 'active'),
        ])
    
    @classmethod
    def get_vendors(cls):
        """Get all vendors"""
        return cls.search([
            ('contact_type', '=', 'vendor'),
            ('status', '=', 'active'),
        ])
    
    @classmethod
    def get_partners_by_company(cls, company_id: int):
        """Get partners by company"""
        return cls.search([
            ('company_ids', 'in', [company_id]),
            ('status', '=', 'active'),
        ])
    
    @classmethod
    def get_partner_analytics_summary(cls):
        """Get partner analytics summary"""
        # In standalone version, we'll return mock data
        return {
            'total_partners': 0,
            'active_partners': 0,
            'customers': 0,
            'suppliers': 0,
            'vendors': 0,
            'inactive_partners': 0,
            'active_percentage': 0,
        }
    
    def _check_gstin(self):
        """Validate GSTIN format"""
        if self.gstin and self.gst_registered:
            if len(self.gstin) != 15:
                raise ValueError('GSTIN must be 15 characters long')
    
    def _check_pan(self):
        """Validate PAN format"""
        if self.pan_number:
            if len(self.pan_number) != 10:
                raise ValueError('PAN must be 10 characters long')
    
    def action_activate(self):
        """Activate partner"""
        self.status = 'active'
        return True
    
    def action_deactivate(self):
        """Deactivate partner"""
        self.status = 'inactive'
        return True
    
    def action_blacklist(self):
        """Blacklist partner"""
        self.status = 'blacklisted'
        return True
    
    def action_unblacklist(self):
        """Remove from blacklist"""
        self.status = 'active'
        return True
    
    def get_child_profiles(self):
        """Get child profiles for this partner"""
        return self.child_profile_ids
    
    def get_contact_history(self):
        """Get contact history"""
        return self.history_ids
    
    def get_communications(self):
        """Get communications"""
        return self.communication_ids
    
    def get_addresses(self):
        """Get addresses"""
        return self.address_ids
    
    def action_duplicate(self):
        """Duplicate partner"""
        self.ensure_one()
        
        new_partner = self.copy({
            'name': f'{self.name} (Copy)',
        })
        
        return new_partner
    
    def action_export_partner(self):
        """Export partner data"""
        self.ensure_one()
        
        return {
            'name': self.name,
            'contact_type': self.contact_type,
            'preferred_age_group': self.preferred_age_group,
            'preferred_gender': self.preferred_gender,
            'gstin': self.gstin,
            'pan_number': self.pan_number,
            'gst_registered': self.gst_registered,
            'status': self.status,
            'rating': self.rating,
        }
    
    def action_import_partner(self, partner_data: Dict[str, Any]):
        """Import partner data"""
        self.ensure_one()
        
        self.write(partner_data)
        return True