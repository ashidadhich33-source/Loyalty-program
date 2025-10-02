# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Contacts - Contact Tag Management
==================================================

Standalone version of the contact tag management model.
"""

from core_framework.orm import BaseModel, CharField, TextField, BooleanField, IntegerField, DateTimeField, Many2OneField, SelectionField
from core_framework.orm import Field
from typing import Dict, Any, Optional
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class ContactTag(BaseModel):
    """Contact tag model for Kids Clothing ERP"""
    
    _name = 'contact.tag'
    _description = 'Contact Tag'
    _table = 'contact_tag'
    
    # Basic tag information
    name = CharField(
        string='Tag Name',
        size=100,
        required=True,
        help='Name of the tag'
    )
    
    description = TextField(
        string='Description',
        help='Description of the tag'
    )
    
    color = CharField(
        string='Color',
        size=7,
        default='#000000',
        help='Color code for the tag (hex)'
    )
    
    # Tag settings
    is_active = BooleanField(
        string='Active',
        default=True,
        help='Whether the tag is active'
    )
    
    is_system_tag = BooleanField(
        string='System Tag',
        default=False,
        help='Whether this is a system tag'
    )
    
    # Tag analytics
    contact_count = IntegerField(
        string='Contact Count',
        default=0,
        help='Number of contacts with this tag'
    )
    
    # Company relationship
    company_id = IntegerField(
        string='Company ID',
        default=1,
        help='Company this tag belongs to'
    )
    
    def create(self, vals: Dict[str, Any]):
        """Override create to set default values"""
        return super().create(vals)
    
    def write(self, vals: Dict[str, Any]):
        """Override write to handle tag updates"""
        result = super().write(vals)
        
        # Log tag updates
        for tag in self:
            if vals:
                logger.info(f"Tag {tag.name} updated: {', '.join(vals.keys())}")
        
        return result
    
    def unlink(self):
        """Override unlink to prevent deletion of system tags"""
        for tag in self:
            if tag.is_system_tag:
                raise ValueError('System tags cannot be deleted')
        
        return super().unlink()
    
    def action_activate(self):
        """Activate tag"""
        self.is_active = True
        return True
    
    def action_deactivate(self):
        """Deactivate tag"""
        self.is_active = False
        return True
    
    def get_tag_analytics(self):
        """Get tag analytics"""
        return {
            'contact_count': self.contact_count,
            'is_active': self.is_active,
            'is_system_tag': self.is_system_tag,
            'color': self.color,
        }
    
    @classmethod
    def get_tags_by_company(cls, company_id: int):
        """Get tags by company"""
        return cls.search([
            ('company_id', '=', company_id),
            ('is_active', '=', True),
        ])
    
    @classmethod
    def get_system_tags(cls):
        """Get system tags"""
        return cls.search([
            ('is_system_tag', '=', True),
            ('is_active', '=', True),
        ])
    
    @classmethod
    def get_custom_tags(cls):
        """Get custom tags"""
        return cls.search([
            ('is_system_tag', '=', False),
            ('is_active', '=', True),
        ])
    
    @classmethod
    def get_tags_by_color(cls, color: str):
        """Get tags by color"""
        return cls.search([
            ('color', '=', color),
            ('is_active', '=', True),
        ])
    
    @classmethod
    def get_tag_analytics_summary(cls):
        """Get tag analytics summary"""
        # In standalone version, we'll return mock data
        return {
            'total_tags': 0,
            'active_tags': 0,
            'system_tags': 0,
            'custom_tags': 0,
            'inactive_tags': 0,
            'active_percentage': 0,
        }
    
    def _check_color(self):
        """Validate color format"""
        if self.color:
            # Check if color is valid hex format
            if not self.color.startswith('#') or len(self.color) != 7:
                raise ValueError('Color must be in hex format (#RRGGBB)')
            
            # Check if hex characters are valid
            hex_chars = self.color[1:]
            if not all(c in '0123456789ABCDEFabcdef' for c in hex_chars):
                raise ValueError('Color must contain valid hex characters')
    
    def action_duplicate(self):
        """Duplicate tag"""
        self.ensure_one()
        
        new_tag = self.copy({
            'name': f'{self.name} (Copy)',
            'is_system_tag': False,
        })
        
        return new_tag
    
    def action_export_tag(self):
        """Export tag data"""
        self.ensure_one()
        
        return {
            'name': self.name,
            'description': self.description,
            'color': self.color,
            'is_active': self.is_active,
            'is_system_tag': self.is_system_tag,
            'company_id': self.company_id,
        }
    
    def action_import_tag(self, tag_data: Dict[str, Any]):
        """Import tag data"""
        self.ensure_one()
        
        self.write(tag_data)
        return True