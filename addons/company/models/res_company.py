# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Company - Company Management
==============================================

Standalone version of the company management model.
"""

from core_framework.orm import BaseModel, CharField, TextField, BooleanField, IntegerField, DateTimeField, Many2OneField, SelectionField, FloatField, One2ManyField, Many2ManyField, DateField
from core_framework.orm import Field
from typing import Dict, Any, Optional, List
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class ResCompany(BaseModel):
    """Extended company model for Kids Clothing ERP"""
    
    _name = 'res.company'
    _description = 'Companies'
    _table = 'res_company'
    
    # Basic company information
    name = CharField(
        string='Company Name',
        size=255,
        required=True,
        help='Name of the company'
    )
    
    # Company Information
    company_type = SelectionField(
        string='Company Type',
        selection=[
            ('retail', 'Retail Store'),
            ('wholesale', 'Wholesale'),
            ('franchise', 'Franchise'),
            ('corporate', 'Corporate'),
            ('distributor', 'Distributor'),
            ('manufacturer', 'Manufacturer'),
        ],
        default='retail',
        help='Type of company'
    )
    
    business_nature = SelectionField(
        string='Business Nature',
        selection=[
            ('kids_clothing', 'Kids Clothing'),
            ('fashion_retail', 'Fashion Retail'),
            ('general_retail', 'General Retail'),
            ('ecommerce', 'E-commerce'),
            ('wholesale_trade', 'Wholesale Trade'),
            ('manufacturing', 'Manufacturing'),
        ],
        default='kids_clothing',
        help='Nature of business'
    )
    
    # Company Hierarchy
    parent_company_id = IntegerField(
        string='Parent Company ID',
        help='Parent company in hierarchy'
    )
    
    child_company_ids = One2ManyField(
        string='Child Companies',
        comodel_name='res.company',
        inverse_name='parent_company_id',
        help='Child companies in hierarchy'
    )
    
    company_level = IntegerField(
        string='Company Level',
        default=1,
        help='Level in company hierarchy'
    )
    
    # GST Information
    gstin = CharField(
        string='GSTIN',
        size=15,
        help='GST Identification Number'
    )
    
    gst_registration_date = DateField(
        string='GST Registration Date',
        help='Date of GST registration'
    )
    
    gst_status = SelectionField(
        string='GST Status',
        selection=[
            ('registered', 'Registered'),
            ('unregistered', 'Unregistered'),
            ('cancelled', 'Cancelled'),
            ('suspended', 'Suspended'),
        ],
        default='registered',
        help='GST registration status'
    )
    
    # Company Address
    registered_address = TextField(
        string='Registered Address',
        help='Registered office address'
    )
    
    business_address = TextField(
        string='Business Address',
        help='Business office address'
    )
    
    warehouse_address = TextField(
        string='Warehouse Address',
        help='Warehouse address'
    )
    
    # Contact Information
    contact_person = CharField(
        string='Contact Person',
        size=100,
        help='Primary contact person'
    )
    
    contact_phone = CharField(
        string='Contact Phone',
        size=20,
        help='Primary contact phone'
    )
    
    contact_email = CharField(
        string='Contact Email',
        size=100,
        help='Primary contact email'
    )
    
    # Financial Information
    financial_year_start = DateField(
        string='Financial Year Start',
        help='Start date of financial year'
    )
    
    financial_year_end = DateField(
        string='Financial Year End',
        help='End date of financial year'
    )
    
    currency_id = IntegerField(
        string='Currency ID',
        default=1,  # Default to INR
        help='Company currency'
    )
    
    # Company Settings
    enable_multi_company = BooleanField(
        string='Enable Multi-Company',
        default=True,
        help='Enable multi-company operations'
    )
    
    enable_gst = BooleanField(
        string='Enable GST',
        default=True,
        help='Enable GST compliance'
    )
    
    enable_e_invoice = BooleanField(
        string='Enable E-invoice',
        default=True,
        help='Enable E-invoice generation'
    )
    
    enable_e_way_bill = BooleanField(
        string='Enable E-way Bill',
        default=True,
        help='Enable E-way bill generation'
    )
    
    # Company Branches
    branch_ids = One2ManyField(
        string='Branches',
        comodel_name='company.branch',
        inverse_name='company_id',
        help='Company branches'
    )
    
    # Company Locations
    location_ids = One2ManyField(
        string='Locations',
        comodel_name='company.location',
        inverse_name='company_id',
        help='Company locations'
    )
    
    # Company Users
    user_ids = Many2ManyField(
        string='Users',
        comodel_name='res.users',
        help='Users assigned to this company'
    )
    
    # Company Analytics
    total_users = IntegerField(
        string='Total Users',
        default=0,
        help='Total number of users in this company'
    )
    
    active_users = IntegerField(
        string='Active Users',
        default=0,
        help='Number of active users in this company'
    )
    
    # Company Status
    is_active = BooleanField(
        string='Active',
        default=True,
        help='Whether the company is active'
    )
    
    is_default = BooleanField(
        string='Default Company',
        default=False,
        help='Whether this is the default company'
    )
    
    # Company Documents
    logo = CharField(
        string='Company Logo',
        size=255,
        help='Company logo path'
    )
    
    # Company Communication
    website = CharField(
        string='Website',
        size=100,
        help='Company website'
    )
    
    def create(self, vals: Dict[str, Any]):
        """Override create to set default values"""
        # Set default financial year if not provided
        if 'financial_year_start' not in vals:
            current_year = datetime.now().year
            vals['financial_year_start'] = f'{current_year}-04-01'
            vals['financial_year_end'] = f'{current_year + 1}-03-31'
        
        # Set company level
        if 'parent_company_id' in vals and vals['parent_company_id']:
            # In standalone version, we'll set level to 2 for child companies
            vals['company_level'] = 2
        else:
            vals['company_level'] = 1
        
        return super().create(vals)
    
    def write(self, vals: Dict[str, Any]):
        """Override write to handle company updates"""
        result = super().write(vals)
        
        # Update child company levels if parent changed
        if 'parent_company_id' in vals:
            for company in self:
                company._update_child_levels()
        
        return result
    
    def _update_child_levels(self):
        """Update child company levels"""
        for child in self.child_company_ids:
            child.company_level = self.company_level + 1
            child._update_child_levels()
    
    def unlink(self):
        """Override unlink to prevent deletion of companies with data"""
        for company in self:
            if company.user_ids:
                raise ValueError('Cannot delete company with users. Please reassign users first.')
            
            if company.branch_ids:
                raise ValueError('Cannot delete company with branches. Please delete branches first.')
            
            if company.location_ids:
                raise ValueError('Cannot delete company with locations. Please delete locations first.')
        
        return super().unlink()
    
    def action_activate(self):
        """Activate company"""
        self.is_active = True
        return True
    
    def action_deactivate(self):
        """Deactivate company"""
        self.is_active = False
        return True
    
    def action_set_default(self):
        """Set as default company"""
        # Remove default from other companies
        other_companies = self.search([('is_default', '=', True)])
        for company in other_companies:
            company.is_default = False
        
        # Set this company as default
        self.is_default = True
        return True
    
    def action_validate_gstin(self):
        """Validate GSTIN"""
        self.ensure_one()
        
        if not self.gstin:
            raise ValueError('GSTIN is required for validation')
        
        # In standalone version, we'll do basic validation
        if len(self.gstin) != 15:
            raise ValueError('Invalid GSTIN format')
        
        return True
    
    def action_generate_gstin(self):
        """Generate GSTIN based on company details"""
        self.ensure_one()
        
        # Generate GSTIN (simplified for standalone)
        state_code = '01'  # Default state code
        pan_number = 'ABCDE1234F'  # Default PAN
        entity_number = '1'
        z_character = 'Z'
        checksum = '1'
        
        gstin = state_code + pan_number + entity_number + z_character + checksum
        
        self.gstin = gstin
        return True
    
    def get_company_hierarchy(self):
        """Get company hierarchy"""
        hierarchy = []
        current_company = self
        
        while current_company:
            hierarchy.insert(0, current_company)
            if current_company.parent_company_id:
                current_company = self.search([('id', '=', current_company.parent_company_id)])
            else:
                current_company = None
        
        return hierarchy
    
    def get_child_companies(self):
        """Get all child companies"""
        child_companies = []
        
        for child in self.child_company_ids:
            child_companies.append(child)
            child_companies.extend(child.get_child_companies())
        
        return child_companies
    
    def get_company_users(self):
        """Get all users in this company"""
        return self.user_ids
    
    def get_company_branches(self):
        """Get all branches in this company"""
        return self.branch_ids
    
    def get_company_locations(self):
        """Get all locations in this company"""
        return self.location_ids
    
    def get_company_analytics(self):
        """Get company analytics"""
        return {
            'total_users': self.total_users,
            'active_users': self.active_users,
            'total_branches': 0,  # Simplified for standalone
            'total_locations': 0,  # Simplified for standalone
            'company_type': self.company_type,
            'business_nature': self.business_nature,
            'gst_status': self.gst_status,
            'is_active': self.is_active,
            'is_default': self.is_default,
        }
    
    @classmethod
    def get_companies_by_type(cls, company_type: str):
        """Get companies by type"""
        return cls.search([
            ('company_type', '=', company_type),
            ('is_active', '=', True),
        ])
    
    @classmethod
    def get_companies_by_business_nature(cls, business_nature: str):
        """Get companies by business nature"""
        return cls.search([
            ('business_nature', '=', business_nature),
            ('is_active', '=', True),
        ])
    
    @classmethod
    def get_companies_with_gst(cls):
        """Get companies with GST registration"""
        return cls.search([
            ('gstin', '!=', None),
            ('gst_status', '=', 'registered'),
            ('is_active', '=', True),
        ])
    
    @classmethod
    def get_default_company(cls):
        """Get default company"""
        return cls.search([('is_default', '=', True)], limit=1)
    
    @classmethod
    def get_company_analytics_summary(cls):
        """Get company analytics summary"""
        # In standalone version, we'll return mock data
        return {
            'total_companies': 0,
            'active_companies': 0,
            'companies_with_gst': 0,
            'default_companies': 0,
            'inactive_companies': 0,
            'active_percentage': 0,
        }
    
    def _check_gstin(self):
        """Validate GSTIN format"""
        if self.gstin and len(self.gstin) != 15:
            raise ValueError('Invalid GSTIN format')
    
    def _check_parent_company(self):
        """Validate parent company"""
        if self.parent_company_id and self.parent_company_id == self.id:
            raise ValueError('Company cannot be its own parent')
        
        if self.parent_company_id:
            # Check for circular reference
            current = self.search([('id', '=', self.parent_company_id)])
            while current:
                if current.id == self.id:
                    raise ValueError('Circular reference in company hierarchy')
                if current.parent_company_id:
                    current = self.search([('id', '=', current.parent_company_id)])
                else:
                    current = None
    
    def _check_financial_year(self):
        """Validate financial year"""
        if self.financial_year_start and self.financial_year_end:
            if self.financial_year_start >= self.financial_year_end:
                raise ValueError('Financial year start must be before end date')
            
            # Check if financial year is 12 months
            start_date = datetime.strptime(self.financial_year_start, '%Y-%m-%d').date()
            end_date = datetime.strptime(self.financial_year_end, '%Y-%m-%d').date()
            diff_days = (end_date - start_date).days
            
            if diff_days < 365 or diff_days > 366:
                raise ValueError('Financial year must be 12 months')
    
    def _check_default_company(self):
        """Validate default company"""
        if self.is_default:
            # Check if there's already a default company
            existing_default = self.search([
                ('is_default', '=', True),
                ('id', '!=', self.id),
            ])
            if existing_default:
                raise ValueError('Only one company can be set as default')
    
    def action_duplicate(self):
        """Duplicate company"""
        self.ensure_one()
        
        new_company = self.copy({
            'name': f'{self.name} (Copy)',
            'is_default': False,
        })
        
        return new_company
    
    def action_export_company(self):
        """Export company data"""
        self.ensure_one()
        
        return {
            'name': self.name,
            'company_type': self.company_type,
            'business_nature': self.business_nature,
            'gstin': self.gstin,
            'gst_status': self.gst_status,
            'currency_id': self.currency_id,
            'financial_year_start': self.financial_year_start,
            'financial_year_end': self.financial_year_end,
            'enable_multi_company': self.enable_multi_company,
            'enable_gst': self.enable_gst,
            'enable_e_invoice': self.enable_e_invoice,
            'enable_e_way_bill': self.enable_e_way_bill,
        }
    
    def action_import_company(self, company_data: Dict[str, Any]):
        """Import company data"""
        self.ensure_one()
        
        self.write(company_data)
        return True