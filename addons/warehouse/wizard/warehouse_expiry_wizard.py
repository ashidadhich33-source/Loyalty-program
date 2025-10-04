# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Warehouse Expiry Wizard
==========================================

Warehouse expiry analysis wizard for kids clothing retail.
"""

from core_framework.orm import BaseModel, CharField, TextField, BooleanField, IntegerField, DateTimeField, Many2OneField, SelectionField, FloatField, One2ManyField, Many2ManyField
from core_framework.orm import Field
from typing import Dict, Any, Optional
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class WarehouseExpiryWizard(BaseModel):
    """Warehouse expiry analysis wizard"""
    
    _name = 'warehouse.expiry.wizard'
    _description = 'Warehouse Expiry Wizard'
    _table = 'warehouse_expiry_wizard'
    
    # Basic Information
    name = CharField(
        string='Expiry Report Name',
        size=100,
        required=True,
        help='Name of the expiry report'
    )
    
    # Warehouse Reference
    warehouse_id = Many2OneField(
        'warehouse',
        string='Warehouse',
        required=True,
        help='Warehouse for expiry analysis'
    )
    
    # Location Reference
    location_id = Many2OneField(
        'stock.location',
        string='Location',
        help='Specific location for expiry analysis'
    )
    
    # Product Reference
    product_id = Many2OneField(
        'product.template',
        string='Product',
        help='Specific product for expiry analysis'
    )
    
    # Analysis Date
    expiry_date = DateTimeField(
        string='Expiry Date',
        required=True,
        help='Date of the expiry analysis'
    )
    
    # Kids Clothing Specific
    age_group_filter = SelectionField(
        string='Age Group Filter',
        selection=[
            ('none', 'No Filter'),
            ('toddler', 'Toddler Only (0-3 years)'),
            ('child', 'Child Only (3-12 years)'),
            ('teen', 'Teen Only (12+ years)'),
            ('mixed', 'Mixed Age Groups')
        ],
        default='none',
        help='Age group filter for expiry analysis'
    )
    
    # Seasonal Filter
    seasonal_filter = SelectionField(
        string='Seasonal Filter',
        selection=[
            ('none', 'No Filter'),
            ('summer', 'Summer'),
            ('winter', 'Winter'),
            ('spring', 'Spring'),
            ('autumn', 'Autumn'),
            ('all_season', 'All Season'),
            ('holiday', 'Holiday')
        ],
        default='none',
        help='Seasonal filter for expiry analysis'
    )
    
    # Notes
    note = TextField(
        string='Notes',
        help='Additional notes about the expiry analysis'
    )
    
    # Timestamps
    create_date = DateTimeField(
        string='Created On',
        auto_now_add=True
    )
    
    def action_create_expiry_report(self):
        """Create expiry report from wizard data"""
        for wizard in self:
            # Validate wizard data
            wizard._validate_wizard()
            
            # Create expiry report
            expiry_report = wizard._create_expiry_report()
        
        return {
            'type': 'ir.actions.act_window',
            'name': 'Expiry Report Created',
            'res_model': 'stock.expiry',
            'res_id': expiry_report.id,
            'view_mode': 'form',
            'target': 'new'
        }
    
    def _validate_wizard(self):
        """Validate wizard data"""
        errors = []
        
        # Check required fields
        if not self.name:
            errors.append("Expiry report name is required")
        
        if not self.warehouse_id:
            errors.append("Warehouse is required")
        
        if not self.expiry_date:
            errors.append("Expiry date is required")
        
        if errors:
            raise ValueError('\n'.join(errors))
    
    def _create_expiry_report(self):
        """Create expiry report from wizard data"""
        # Create expiry report
        expiry_vals = {
            'name': self.name,
            'warehouse_id': self.warehouse_id.id,
            'location_id': self.location_id.id if self.location_id else None,
            'product_id': self.product_id.id if self.product_id else None,
            'expiry_date': self.expiry_date,
            'product_age_group': self.age_group_filter if self.age_group_filter != 'none' else None,
            'seasonal_category': self.seasonal_filter if self.seasonal_filter != 'none' else None,
            'note': self.note
        }
        
        expiry_report = self.env['stock.expiry'].create(expiry_vals)
        
        # Generate expiry data
        expiry_report._generate_expiry_data()
        
        return expiry_report
    
    def action_view_warehouse(self):
        """View warehouse details"""
        return {
            'type': 'ir.actions.act_window',
            'name': f'Warehouse - {self.warehouse_id.name}',
            'res_model': 'warehouse',
            'res_id': self.warehouse_id.id,
            'view_mode': 'form',
            'target': 'new'
        }
    
    def action_view_location(self):
        """View location details"""
        if not self.location_id:
            return None
        
        return {
            'type': 'ir.actions.act_window',
            'name': f'Location - {self.location_id.name}',
            'res_model': 'stock.location',
            'res_id': self.location_id.id,
            'view_mode': 'form',
            'target': 'new'
        }
    
    def action_view_product(self):
        """View product details"""
        if not self.product_id:
            return None
        
        return {
            'type': 'ir.actions.act_window',
            'name': f'Product - {self.product_id.name}',
            'res_model': 'product.template',
            'res_id': self.product_id.id,
            'view_mode': 'form',
            'target': 'new'
        }
    
    def get_wizard_summary(self):
        """Get wizard summary data"""
        return {
            'expiry_name': self.name,
            'warehouse': self.warehouse_id.name,
            'location': self.location_id.name if self.location_id else 'All Locations',
            'product': self.product_id.name if self.product_id else 'All Products',
            'expiry_date': self.expiry_date,
            'age_group_filter': self.age_group_filter,
            'seasonal_filter': self.seasonal_filter
        }