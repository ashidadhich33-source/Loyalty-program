# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Contacts - Contact Category Management
======================================================

Standalone version of the contact category management model.
"""

from core_framework.orm import BaseModel, CharField, TextField, BooleanField, IntegerField, DateTimeField, Many2OneField, SelectionField, One2ManyField
from core_framework.orm import Field
from typing import Dict, Any, Optional
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class ContactCategory(BaseModel):
    """Contact category model for Kids Clothing ERP"""
    
    _name = 'contact.category'
    _description = 'Contact Category'
    _table = 'contact_category'
    
    # Basic category information
    name = CharField(
        string='Category Name',
        size=100,
        required=True,
        help='Name of the category'
    )
    
    description = TextField(
        string='Description',
        help='Description of the category'
    )
    
    code = CharField(
        string='Category Code',
        size=20,
        help='Unique code for the category'
    )
    
    # Category hierarchy
    parent_id = IntegerField(
        string='Parent Category ID',
        help='Parent category in hierarchy'
    )
    
    child_ids = One2ManyField(
        string='Child Categories',
        comodel_name='contact.category',
        inverse_name='parent_id',
        help='Child categories in hierarchy'
    )
    
    category_level = IntegerField(
        string='Category Level',
        default=1,
        help='Level in category hierarchy'
    )
    
    # Category settings
    is_active = BooleanField(
        string='Active',
        default=True,
        help='Whether the category is active'
    )
    
    is_system_category = BooleanField(
        string='System Category',
        default=False,
        help='Whether this is a system category'
    )
    
    # Category analytics
    contact_count = IntegerField(
        string='Contact Count',
        default=0,
        help='Number of contacts in this category'
    )
    
    # Company relationship
    company_id = IntegerField(
        string='Company ID',
        default=1,
        help='Company this category belongs to'
    )
    
    def create(self, vals: Dict[str, Any]):
        """Override create to set default values"""
        # Set category level
        if 'parent_id' in vals and vals['parent_id']:
            # In standalone version, we'll set level to 2 for child categories
            vals['category_level'] = 2
        else:
            vals['category_level'] = 1
        
        return super().create(vals)
    
    def write(self, vals: Dict[str, Any]):
        """Override write to handle category updates"""
        result = super().write(vals)
        
        # Update child category levels if parent changed
        if 'parent_id' in vals:
            for category in self:
                category._update_child_levels()
        
        # Log category updates
        for category in self:
            if vals:
                logger.info(f"Category {category.name} updated: {', '.join(vals.keys())}")
        
        return result
    
    def _update_child_levels(self):
        """Update child category levels"""
        for child in self.child_ids:
            child.category_level = self.category_level + 1
            child._update_child_levels()
    
    def unlink(self):
        """Override unlink to prevent deletion of system categories"""
        for category in self:
            if category.is_system_category:
                raise ValueError('System categories cannot be deleted')
        
        return super().unlink()
    
    def action_activate(self):
        """Activate category"""
        self.is_active = True
        return True
    
    def action_deactivate(self):
        """Deactivate category"""
        self.is_active = False
        return True
    
    def get_category_hierarchy(self):
        """Get category hierarchy"""
        hierarchy = []
        current_category = self
        
        while current_category:
            hierarchy.insert(0, current_category)
            if current_category.parent_id:
                current_category = self.search([('id', '=', current_category.parent_id)])
            else:
                current_category = None
        
        return hierarchy
    
    def get_child_categories(self):
        """Get all child categories"""
        child_categories = []
        
        for child in self.child_ids:
            child_categories.append(child)
            child_categories.extend(child.get_child_categories())
        
        return child_categories
    
    def get_category_analytics(self):
        """Get category analytics"""
        return {
            'contact_count': self.contact_count,
            'category_level': self.category_level,
            'is_active': self.is_active,
            'is_system_category': self.is_system_category,
            'child_count': 0,  # Simplified for standalone
        }
    
    @classmethod
    def get_categories_by_company(cls, company_id: int):
        """Get categories by company"""
        return cls.search([
            ('company_id', '=', company_id),
            ('is_active', '=', True),
        ])
    
    @classmethod
    def get_root_categories(cls, company_id: int):
        """Get root categories (no parent)"""
        return cls.search([
            ('company_id', '=', company_id),
            ('parent_id', '=', None),
            ('is_active', '=', True),
        ])
    
    @classmethod
    def get_system_categories(cls):
        """Get system categories"""
        return cls.search([
            ('is_system_category', '=', True),
            ('is_active', '=', True),
        ])
    
    @classmethod
    def get_custom_categories(cls):
        """Get custom categories"""
        return cls.search([
            ('is_system_category', '=', False),
            ('is_active', '=', True),
        ])
    
    @classmethod
    def get_category_analytics_summary(cls):
        """Get category analytics summary"""
        # In standalone version, we'll return mock data
        return {
            'total_categories': 0,
            'active_categories': 0,
            'system_categories': 0,
            'custom_categories': 0,
            'inactive_categories': 0,
            'active_percentage': 0,
        }
    
    def _check_parent_category(self):
        """Validate parent category"""
        if self.parent_id and self.parent_id == self.id:
            raise ValueError('Category cannot be its own parent')
        
        if self.parent_id:
            # Check for circular reference
            current = self.search([('id', '=', self.parent_id)])
            while current:
                if current.id == self.id:
                    raise ValueError('Circular reference in category hierarchy')
                if current.parent_id:
                    current = self.search([('id', '=', current.parent_id)])
                else:
                    current = None
    
    def action_duplicate(self):
        """Duplicate category"""
        self.ensure_one()
        
        new_category = self.copy({
            'name': f'{self.name} (Copy)',
            'is_system_category': False,
        })
        
        return new_category
    
    def action_export_category(self):
        """Export category data"""
        self.ensure_one()
        
        return {
            'name': self.name,
            'description': self.description,
            'code': self.code,
            'parent_id': self.parent_id,
            'is_active': self.is_active,
            'is_system_category': self.is_system_category,
            'company_id': self.company_id,
        }
    
    def action_import_category(self, category_data: Dict[str, Any]):
        """Import category data"""
        self.ensure_one()
        
        self.write(category_data)
        return True