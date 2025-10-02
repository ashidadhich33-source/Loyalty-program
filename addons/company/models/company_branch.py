# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Company - Company Branch
==========================================

Standalone version of the company branch model.
"""

from core_framework.orm import BaseModel, CharField, TextField, BooleanField, IntegerField, DateTimeField, Many2OneField, SelectionField, FloatField, One2ManyField, Many2ManyField
from core_framework.orm import Field
from typing import Dict, Any, Optional, List
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class CompanyBranch(BaseModel):
    """Company branch model for Kids Clothing ERP"""
    
    _name = 'company.branch'
    _description = 'Company Branch'
    _table = 'company_branch'
    
    # Basic fields
    name = CharField(
        string='Branch Name',
        size=100,
        required=True,
        help='Name of the branch'
    )
    
    code = CharField(
        string='Branch Code',
        size=20,
        required=True,
        help='Unique code for the branch'
    )
    
    description = TextField(
        string='Description',
        help='Description of the branch'
    )
    
    # Company relationship
    company_id = IntegerField(
        string='Company ID',
        required=True,
        help='Company this branch belongs to'
    )
    
    # Branch hierarchy
    parent_branch_id = IntegerField(
        string='Parent Branch ID',
        help='Parent branch in hierarchy'
    )
    
    child_branch_ids = One2ManyField(
        string='Child Branches',
        comodel_name='company.branch',
        inverse_name='parent_branch_id',
        help='Child branches in hierarchy'
    )
    
    branch_level = IntegerField(
        string='Branch Level',
        default=1,
        help='Level in branch hierarchy'
    )
    
    # Branch information
    branch_type = SelectionField(
        string='Branch Type',
        selection=[
            ('head_office', 'Head Office'),
            ('regional_office', 'Regional Office'),
            ('branch_office', 'Branch Office'),
            ('warehouse', 'Warehouse'),
            ('showroom', 'Showroom'),
            ('franchise', 'Franchise'),
            ('distributor', 'Distributor'),
        ],
        default='branch_office',
        help='Type of branch'
    )
    
    # Branch address
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
        help='Branch phone number'
    )
    
    mobile = CharField(
        string='Mobile',
        size=20,
        help='Branch mobile number'
    )
    
    email = CharField(
        string='Email',
        size=100,
        help='Branch email address'
    )
    
    website = CharField(
        string='Website',
        size=100,
        help='Branch website'
    )
    
    # Branch manager
    manager_id = IntegerField(
        string='Branch Manager ID',
        help='Branch manager'
    )
    
    # Branch settings
    is_active = BooleanField(
        string='Active',
        default=True,
        help='Whether the branch is active'
    )
    
    is_default = BooleanField(
        string='Default Branch',
        default=False,
        help='Whether this is the default branch'
    )
    
    # Branch capacity
    max_users = IntegerField(
        string='Max Users',
        default=50,
        help='Maximum number of users for this branch'
    )
    
    current_users = IntegerField(
        string='Current Users',
        default=0,
        help='Current number of users in this branch'
    )
    
    # Branch features
    enable_pos = BooleanField(
        string='Enable POS',
        default=True,
        help='Enable POS for this branch'
    )
    
    enable_inventory = BooleanField(
        string='Enable Inventory',
        default=True,
        help='Enable inventory for this branch'
    )
    
    enable_sales = BooleanField(
        string='Enable Sales',
        default=True,
        help='Enable sales for this branch'
    )
    
    enable_purchase = BooleanField(
        string='Enable Purchase',
        default=True,
        help='Enable purchase for this branch'
    )
    
    # Branch analytics
    total_sales = FloatField(
        string='Total Sales',
        default=0.0,
        help='Total sales for this branch'
    )
    
    total_orders = IntegerField(
        string='Total Orders',
        default=0,
        help='Total orders for this branch'
    )
    
    # Branch users
    user_ids = Many2ManyField(
        string='Users',
        comodel_name='res.users',
        help='Users assigned to this branch'
    )
    
    # Branch locations
    location_ids = One2ManyField(
        string='Locations',
        comodel_name='company.location',
        inverse_name='branch_id',
        help='Locations in this branch'
    )
    
    def create(self, vals: Dict[str, Any]):
        """Override create to set default values"""
        # Set branch level
        if 'parent_branch_id' in vals and vals['parent_branch_id']:
            # In standalone version, we'll set level to 2 for child branches
            vals['branch_level'] = 2
        else:
            vals['branch_level'] = 1
        
        return super().create(vals)
    
    def write(self, vals: Dict[str, Any]):
        """Override write to handle branch updates"""
        result = super().write(vals)
        
        # Update child branch levels if parent changed
        if 'parent_branch_id' in vals:
            for branch in self:
                branch._update_child_levels()
        
        return result
    
    def _update_child_levels(self):
        """Update child branch levels"""
        for child in self.child_branch_ids:
            child.branch_level = self.branch_level + 1
            child._update_child_levels()
    
    def unlink(self):
        """Override unlink to prevent deletion of branches with data"""
        for branch in self:
            if branch.user_ids:
                raise ValueError('Cannot delete branch with users. Please reassign users first.')
            
            if branch.location_ids:
                raise ValueError('Cannot delete branch with locations. Please delete locations first.')
        
        return super().unlink()
    
    def action_activate(self):
        """Activate branch"""
        self.is_active = True
        return True
    
    def action_deactivate(self):
        """Deactivate branch"""
        self.is_active = False
        return True
    
    def action_set_default(self):
        """Set as default branch"""
        # Remove default from other branches in same company
        other_branches = self.search([
            ('company_id', '=', self.company_id),
            ('is_default', '=', True),
        ])
        for branch in other_branches:
            branch.is_default = False
        
        # Set this branch as default
        self.is_default = True
        return True
    
    def get_branch_hierarchy(self):
        """Get branch hierarchy"""
        hierarchy = []
        current_branch = self
        
        while current_branch:
            hierarchy.insert(0, current_branch)
            if current_branch.parent_branch_id:
                current_branch = self.search([('id', '=', current_branch.parent_branch_id)])
            else:
                current_branch = None
        
        return hierarchy
    
    def get_child_branches(self):
        """Get all child branches"""
        child_branches = []
        
        for child in self.child_branch_ids:
            child_branches.append(child)
            child_branches.extend(child.get_child_branches())
        
        return child_branches
    
    def get_branch_users(self):
        """Get all users in this branch"""
        return self.user_ids
    
    def get_branch_locations(self):
        """Get all locations in this branch"""
        return self.location_ids
    
    def get_branch_analytics(self):
        """Get branch analytics"""
        return {
            'total_users': self.current_users,
            'max_users': self.max_users,
            'total_sales': self.total_sales,
            'total_orders': self.total_orders,
            'branch_type': self.branch_type,
            'is_active': self.is_active,
            'is_default': self.is_default,
            'enable_pos': self.enable_pos,
            'enable_inventory': self.enable_inventory,
            'enable_sales': self.enable_sales,
            'enable_purchase': self.enable_purchase,
        }
    
    @classmethod
    def get_branches_by_company(cls, company_id: int):
        """Get branches by company"""
        return cls.search([
            ('company_id', '=', company_id),
            ('is_active', '=', True),
        ])
    
    @classmethod
    def get_branches_by_type(cls, branch_type: str):
        """Get branches by type"""
        return cls.search([
            ('branch_type', '=', branch_type),
            ('is_active', '=', True),
        ])
    
    @classmethod
    def get_default_branch(cls, company_id: int):
        """Get default branch for company"""
        return cls.search([
            ('company_id', '=', company_id),
            ('is_default', '=', True),
        ], limit=1)
    
    @classmethod
    def get_branch_analytics_summary(cls):
        """Get branch analytics summary"""
        # In standalone version, we'll return mock data
        return {
            'total_branches': 0,
            'active_branches': 0,
            'default_branches': 0,
            'inactive_branches': 0,
            'active_percentage': 0,
        }
    
    def _check_code(self):
        """Validate branch code"""
        if self.code:
            # Check for duplicate codes in same company
            existing = self.search([
                ('code', '=', self.code),
                ('company_id', '=', self.company_id),
                ('id', '!=', self.id),
            ])
            if existing:
                raise ValueError('Branch code must be unique within company')
    
    def _check_parent_branch(self):
        """Validate parent branch"""
        if self.parent_branch_id and self.parent_branch_id == self.id:
            raise ValueError('Branch cannot be its own parent')
        
        if self.parent_branch_id:
            # Check for circular reference
            current = self.search([('id', '=', self.parent_branch_id)])
            while current:
                if current.id == self.id:
                    raise ValueError('Circular reference in branch hierarchy')
                if current.parent_branch_id:
                    current = self.search([('id', '=', current.parent_branch_id)])
                else:
                    current = None
            
            # Check if parent branch belongs to same company
            if current and current.company_id != self.company_id:
                raise ValueError('Parent branch must belong to same company')
    
    def _check_default_branch(self):
        """Validate default branch"""
        if self.is_default:
            # Check if there's already a default branch in same company
            existing_default = self.search([
                ('is_default', '=', True),
                ('company_id', '=', self.company_id),
                ('id', '!=', self.id),
            ])
            if existing_default:
                raise ValueError('Only one branch can be set as default per company')
    
    def _check_user_capacity(self):
        """Validate user capacity"""
        if self.current_users > self.max_users:
            raise ValueError('Current users exceed maximum capacity')
    
    def action_duplicate(self):
        """Duplicate branch"""
        self.ensure_one()
        
        new_branch = self.copy({
            'name': f'{self.name} (Copy)',
            'code': f'{self.code}_copy',
            'is_default': False,
        })
        
        return new_branch
    
    def action_export_branch(self):
        """Export branch data"""
        self.ensure_one()
        
        return {
            'name': self.name,
            'code': self.code,
            'branch_type': self.branch_type,
            'company_id': self.company_id,
            'parent_branch_id': self.parent_branch_id,
            'street': self.street,
            'city': self.city,
            'state_id': self.state_id,
            'zip': self.zip,
            'country_id': self.country_id,
            'phone': self.phone,
            'mobile': self.mobile,
            'email': self.email,
            'website': self.website,
            'manager_id': self.manager_id,
            'max_users': self.max_users,
            'enable_pos': self.enable_pos,
            'enable_inventory': self.enable_inventory,
            'enable_sales': self.enable_sales,
            'enable_purchase': self.enable_purchase,
        }
    
    def action_import_branch(self, branch_data: Dict[str, Any]):
        """Import branch data"""
        self.ensure_one()
        
        self.write(branch_data)
        return True