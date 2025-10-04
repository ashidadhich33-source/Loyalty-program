# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Stock Inventory Wizard
==========================================

Stock inventory adjustment wizard for kids clothing retail.
"""

from core_framework.orm import BaseModel, CharField, TextField, BooleanField, IntegerField, DateTimeField, Many2OneField, SelectionField, FloatField, One2ManyField, Many2ManyField
from core_framework.orm import Field
from typing import Dict, Any, Optional
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class StockInventoryWizard(BaseModel):
    """Stock inventory adjustment wizard"""
    
    _name = 'stock.inventory.wizard'
    _description = 'Stock Inventory Wizard'
    _table = 'stock_inventory_wizard'
    
    # Basic Information
    name = CharField(
        string='Inventory Reference',
        size=100,
        required=True,
        help='Reference of the inventory adjustment'
    )
    
    # Inventory Type
    inventory_type = SelectionField(
        string='Inventory Type',
        selection=[
            ('full', 'Full Inventory'),
            ('partial', 'Partial Inventory'),
            ('cycle', 'Cycle Count'),
            ('spot', 'Spot Check'),
            ('damage', 'Damage Check'),
            ('expiry', 'Expiry Check')
        ],
        default='full',
        required=True,
        help='Type of inventory adjustment'
    )
    
    # Location Selection
    location_ids = Many2ManyField(
        'stock.location',
        string='Locations',
        help='Locations to include in inventory'
    )
    
    # Product Selection
    product_ids = Many2ManyField(
        'product.template',
        string='Products',
        help='Products to include in inventory'
    )
    
    # Company
    company_id = Many2OneField(
        'res.company',
        string='Company',
        required=True,
        help='Company this inventory belongs to'
    )
    
    # Date Information
    date = DateTimeField(
        string='Inventory Date',
        required=True,
        help='Date of the inventory'
    )
    
    # Kids Clothing Specific
    age_group_filter = SelectionField(
        string='Age Group Filter',
        selection=[
            ('none', 'No Filter'),
            ('toddler', 'Toddler Only (0-3 years)'),
            ('child', 'Child Only (3-12 years)'),
            ('teen', 'Teen Only (12+ years)'),
            ('toddler_child', 'Toddler & Child (0-12 years)'),
            ('child_teen', 'Child & Teen (3+ years)')
        ],
        default='none',
        help='Age group filter for inventory'
    )
    
    # Quality Check
    quality_check_required = BooleanField(
        string='Quality Check Required',
        default=False,
        help='Whether quality check is required'
    )
    
    # Notes
    note = TextField(
        string='Notes',
        help='Additional notes about this inventory'
    )
    
    # Timestamps
    create_date = DateTimeField(
        string='Created On',
        auto_now_add=True
    )
    
    def action_create_inventory(self):
        """Create inventory from wizard data"""
        for wizard in self:
            # Validate wizard data
            wizard._validate_wizard()
            
            # Create inventory
            inventory = wizard._create_inventory()
        
        return {
            'type': 'ir.actions.act_window',
            'name': 'Inventory Created',
            'res_model': 'stock.inventory',
            'res_id': inventory.id,
            'view_mode': 'form',
            'target': 'new'
        }
    
    def _validate_wizard(self):
        """Validate wizard data"""
        errors = []
        
        # Check required fields
        if not self.name:
            errors.append("Inventory reference is required")
        
        if not self.inventory_type:
            errors.append("Inventory type is required")
        
        if not self.date:
            errors.append("Inventory date is required")
        
        # Check if locations or products are selected
        if not self.location_ids and not self.product_ids:
            errors.append("At least one location or product must be selected")
        
        if errors:
            raise ValueError('\n'.join(errors))
    
    def _create_inventory(self):
        """Create inventory from wizard data"""
        # Create inventory
        inventory_vals = {
            'name': self.name,
            'inventory_type': self.inventory_type,
            'location_ids': [(6, 0, [loc.id for loc in self.location_ids])],
            'product_ids': [(6, 0, [prod.id for prod in self.product_ids])],
            'company_id': self.company_id.id,
            'date': self.date,
            'age_group_filter': self.age_group_filter,
            'quality_check_required': self.quality_check_required,
            'note': self.note,
            'state': 'draft'
        }
        
        inventory = self.env['stock.inventory'].create(inventory_vals)
        
        return inventory
    
    def action_view_locations(self):
        """View selected locations"""
        if not self.location_ids:
            return None
        
        return {
            'type': 'ir.actions.act_window',
            'name': 'Selected Locations',
            'res_model': 'stock.location',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', [loc.id for loc in self.location_ids])],
            'target': 'new'
        }
    
    def action_view_products(self):
        """View selected products"""
        if not self.product_ids:
            return None
        
        return {
            'type': 'ir.actions.act_window',
            'name': 'Selected Products',
            'res_model': 'product.template',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', [prod.id for prod in self.product_ids])],
            'target': 'new'
        }
    
    def get_wizard_summary(self):
        """Get wizard summary data"""
        return {
            'inventory_name': self.name,
            'inventory_type': self.inventory_type,
            'location_count': len(self.location_ids),
            'product_count': len(self.product_ids),
            'date': self.date,
            'age_group_filter': self.age_group_filter,
            'quality_check_required': self.quality_check_required,
            'company': self.company_id.name
        }