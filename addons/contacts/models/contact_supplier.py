# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Contacts - Supplier Management
===============================================

Standalone version of the supplier management model.
"""

from core_framework.orm import BaseModel, CharField, TextField, BooleanField, IntegerField, DateTimeField, Many2OneField, SelectionField, FloatField
from core_framework.orm import Field
from typing import Dict, Any, Optional
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class ContactSupplier(BaseModel):
    """Supplier contact model for Kids Clothing ERP"""
    
    _name = 'contact.supplier'
    _description = 'Supplier Contact'
    _table = 'contact_supplier'
    
    # Basic supplier information
    name = CharField(
        string='Supplier Name',
        size=255,
        required=True,
        help='Name of the supplier'
    )
    
    partner_id = IntegerField(
        string='Partner ID',
        required=True,
        help='Related partner'
    )
    
    supplier_code = CharField(
        string='Supplier Code',
        size=50,
        help='Unique supplier code'
    )
    
    supplier_type = SelectionField(
        string='Supplier Type',
        selection=[
            ('manufacturer', 'Manufacturer'),
            ('wholesaler', 'Wholesaler'),
            ('distributor', 'Distributor'),
            ('service_provider', 'Service Provider'),
            ('other', 'Other'),
        ],
        default='manufacturer',
        help='Type of supplier'
    )
    
    # Supplier details
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
    
    # Payment terms
    payment_terms = IntegerField(
        string='Payment Terms ID',
        help='Payment terms for this supplier'
    )
    
    credit_limit = FloatField(
        string='Credit Limit',
        default=0.0,
        help='Credit limit for this supplier'
    )
    
    credit_balance = FloatField(
        string='Credit Balance',
        default=0.0,
        help='Current credit balance'
    )
    
    # Supplier status
    status = SelectionField(
        string='Status',
        selection=[
            ('active', 'Active'),
            ('inactive', 'Inactive'),
            ('blacklisted', 'Blacklisted'),
        ],
        default='active',
        help='Supplier status'
    )
    
    # Supplier rating
    rating = SelectionField(
        string='Rating',
        selection=[
            ('1', '1 Star'),
            ('2', '2 Stars'),
            ('3', '3 Stars'),
            ('4', '4 Stars'),
            ('5', '5 Stars'),
        ],
        help='Supplier rating'
    )
    
    # Company relationship
    company_id = IntegerField(
        string='Company ID',
        default=1,
        help='Company this supplier belongs to'
    )
    
    # Supplier analytics
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
    
    last_order_date = DateTimeField(
        string='Last Order Date',
        help='Date of last order'
    )
    
    average_order_value = FloatField(
        string='Average Order Value',
        default=0.0,
        help='Average order value'
    )
    
    # Supplier notes
    notes = TextField(
        string='Notes',
        help='Additional notes about the supplier'
    )
    
    def create(self, vals: Dict[str, Any]):
        """Override create to set default values"""
        # Generate supplier code if not provided
        if not vals.get('supplier_code'):
            vals['supplier_code'] = f"SUPP{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        return super().create(vals)
    
    def write(self, vals: Dict[str, Any]):
        """Override write to handle supplier updates"""
        result = super().write(vals)
        
        # Log supplier updates
        for supplier in self:
            if vals:
                logger.info(f"Supplier {supplier.name} updated: {', '.join(vals.keys())}")
        
        return result
    
    def get_supplier_analytics(self):
        """Get supplier analytics"""
        return {
            'total_orders': self.total_orders,
            'total_purchases': self.total_purchases,
            'last_order_date': self.last_order_date,
            'average_order_value': self.average_order_value,
            'status': self.status,
            'rating': self.rating,
            'supplier_type': self.supplier_type,
        }
    
    @classmethod
    def get_suppliers_by_type(cls, supplier_type: str):
        """Get suppliers by type"""
        return cls.search([
            ('supplier_type', '=', supplier_type),
            ('status', '=', 'active'),
        ])
    
    @classmethod
    def get_suppliers_by_company(cls, company_id: int):
        """Get suppliers by company"""
        return cls.search([
            ('company_id', '=', company_id),
            ('status', '=', 'active'),
        ])
    
    @classmethod
    def get_suppliers_by_rating(cls, rating: str):
        """Get suppliers by rating"""
        return cls.search([
            ('rating', '=', rating),
            ('status', '=', 'active'),
        ])
    
    @classmethod
    def get_supplier_analytics_summary(cls):
        """Get supplier analytics summary"""
        # In standalone version, we'll return mock data
        return {
            'total_suppliers': 0,
            'active_suppliers': 0,
            'by_type': {},
            'by_rating': {},
            'inactive_suppliers': 0,
            'active_percentage': 0,
        }
    
    def action_activate(self):
        """Activate supplier"""
        self.status = 'active'
        return True
    
    def action_deactivate(self):
        """Deactivate supplier"""
        self.status = 'inactive'
        return True
    
    def action_blacklist(self):
        """Blacklist supplier"""
        self.status = 'blacklisted'
        return True
    
    def action_unblacklist(self):
        """Remove from blacklist"""
        self.status = 'active'
        return True
    
    def get_available_credit(self):
        """Get available credit"""
        return self.credit_limit - self.credit_balance
    
    def action_duplicate(self):
        """Duplicate supplier"""
        self.ensure_one()
        
        new_supplier = self.copy({
            'name': f'{self.name} (Copy)',
            'supplier_code': f"SUPP{datetime.now().strftime('%Y%m%d%H%M%S')}",
        })
        
        return new_supplier
    
    def action_export_supplier(self):
        """Export supplier data"""
        self.ensure_one()
        
        return {
            'name': self.name,
            'supplier_code': self.supplier_code,
            'supplier_type': self.supplier_type,
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
            'payment_terms': self.payment_terms,
            'credit_limit': self.credit_limit,
            'status': self.status,
            'rating': self.rating,
        }
    
    def action_import_supplier(self, supplier_data: Dict[str, Any]):
        """Import supplier data"""
        self.ensure_one()
        
        self.write(supplier_data)
        return True