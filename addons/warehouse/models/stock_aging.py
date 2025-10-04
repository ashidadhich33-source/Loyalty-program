# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Stock Aging
===============================

Stock aging management for kids clothing retail.
"""

from core_framework.orm import BaseModel, CharField, TextField, BooleanField, IntegerField, DateTimeField, Many2OneField, SelectionField, FloatField, One2ManyField, Many2ManyField
from core_framework.orm import Field
from typing import Dict, Any, Optional
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class StockAging(BaseModel):
    """Stock aging analysis for inventory management"""
    
    _name = 'stock.aging'
    _description = 'Stock Aging'
    _table = 'stock_aging'
    
    # Basic Information
    name = CharField(
        string='Aging Report Name',
        size=100,
        required=True,
        help='Name of the aging report'
    )
    
    # Warehouse Reference
    warehouse_id = Many2OneField(
        'warehouse',
        string='Warehouse',
        required=True,
        help='Warehouse for this aging report'
    )
    
    # Location Reference
    location_id = Many2OneField(
        'stock.location',
        string='Location',
        help='Specific location for aging analysis'
    )
    
    # Product Reference
    product_id = Many2OneField(
        'product.template',
        string='Product',
        help='Specific product for aging analysis'
    )
    
    # Aging Analysis
    aging_date = DateTimeField(
        string='Aging Date',
        required=True,
        help='Date of the aging analysis'
    )
    
    # Age Categories
    age_0_30_days = FloatField(
        string='0-30 Days',
        digits=(12, 3),
        default=0.0,
        help='Quantity aged 0-30 days'
    )
    
    age_31_60_days = FloatField(
        string='31-60 Days',
        digits=(12, 3),
        default=0.0,
        help='Quantity aged 31-60 days'
    )
    
    age_61_90_days = FloatField(
        string='61-90 Days',
        digits=(12, 3),
        default=0.0,
        help='Quantity aged 61-90 days'
    )
    
    age_91_180_days = FloatField(
        string='91-180 Days',
        digits=(12, 3),
        default=0.0,
        help='Quantity aged 91-180 days'
    )
    
    age_181_365_days = FloatField(
        string='181-365 Days',
        digits=(12, 3),
        default=0.0,
        help='Quantity aged 181-365 days'
    )
    
    age_over_365_days = FloatField(
        string='Over 365 Days',
        digits=(12, 3),
        default=0.0,
        help='Quantity aged over 365 days'
    )
    
    # Total Quantities
    total_quantity = FloatField(
        string='Total Quantity',
        digits=(12, 3),
        default=0.0,
        help='Total quantity analyzed'
    )
    
    total_value = FloatField(
        string='Total Value',
        digits=(12, 2),
        default=0.0,
        help='Total value of aged inventory'
    )
    
    # Kids Clothing Specific
    product_age_group = SelectionField(
        string='Product Age Group',
        selection=[
            ('toddler', 'Toddler (0-3 years)'),
            ('child', 'Child (3-12 years)'),
            ('teen', 'Teen (12+ years)'),
            ('mixed', 'Mixed Age Groups')
        ],
        help='Age group of the products analyzed'
    )
    
    # Seasonal Analysis
    seasonal_category = SelectionField(
        string='Seasonal Category',
        selection=[
            ('summer', 'Summer'),
            ('winter', 'Winter'),
            ('spring', 'Spring'),
            ('autumn', 'Autumn'),
            ('all_season', 'All Season'),
            ('holiday', 'Holiday')
        ],
        help='Seasonal category of the products'
    )
    
    # Aging Status
    aging_status = SelectionField(
        string='Aging Status',
        selection=[
            ('fresh', 'Fresh (0-30 days)'),
            ('current', 'Current (31-90 days)'),
            ('aging', 'Aging (91-180 days)'),
            ('stale', 'Stale (181-365 days)'),
            ('obsolete', 'Obsolete (365+ days)')
        ],
        help='Overall aging status'
    )
    
    # Action Required
    action_required = SelectionField(
        string='Action Required',
        selection=[
            ('none', 'No Action'),
            ('promotion', 'Promotion Required'),
            ('discount', 'Discount Required'),
            ('clearance', 'Clearance Sale'),
            ('return', 'Return to Vendor'),
            ('donate', 'Donate'),
            ('dispose', 'Dispose')
        ],
        default='none',
        help='Action required for aged inventory'
    )
    
    # Priority
    priority = SelectionField(
        string='Priority',
        selection=[
            ('low', 'Low'),
            ('medium', 'Medium'),
            ('high', 'High'),
            ('urgent', 'Urgent')
        ],
        default='low',
        help='Priority level for action'
    )
    
    # Analysis Results
    turnover_rate = FloatField(
        string='Turnover Rate',
        digits=(5, 2),
        default=0.0,
        help='Inventory turnover rate'
    )
    
    average_age = FloatField(
        string='Average Age (Days)',
        digits=(8, 2),
        default=0.0,
        help='Average age of inventory in days'
    )
    
    # Notes
    note = TextField(
        string='Notes',
        help='Additional notes about the aging analysis'
    )
    
    # Timestamps
    create_date = DateTimeField(
        string='Created On',
        auto_now_add=True
    )
    
    write_date = DateTimeField(
        string='Updated On',
        auto_now=True
    )
    
    def create(self, vals):
        """Override create to set defaults"""
        if 'aging_date' not in vals:
            vals['aging_date'] = datetime.now()
        
        return super().create(vals)
    
    def write(self, vals):
        """Override write to update calculations"""
        result = super().write(vals)
        
        # Update calculations when quantities change
        if any(field in vals for field in ['age_0_30_days', 'age_31_60_days', 'age_61_90_days', 'age_91_180_days', 'age_181_365_days', 'age_over_365_days']):
            self._update_calculations()
        
        return result
    
    def _update_calculations(self):
        """Update calculated fields"""
        for aging in self:
            # Calculate total quantity
            aging.total_quantity = (
                aging.age_0_30_days +
                aging.age_31_60_days +
                aging.age_61_90_days +
                aging.age_91_180_days +
                aging.age_181_365_days +
                aging.age_over_365_days
            )
            
            # Calculate average age
            if aging.total_quantity > 0:
                total_days = (
                    aging.age_0_30_days * 15 +  # Average of 0-30 days
                    aging.age_31_60_days * 45 +  # Average of 31-60 days
                    aging.age_61_90_days * 75 +  # Average of 61-90 days
                    aging.age_91_180_days * 135 +  # Average of 91-180 days
                    aging.age_181_365_days * 273 +  # Average of 181-365 days
                    aging.age_over_365_days * 500  # Average of over 365 days
                )
                aging.average_age = total_days / aging.total_quantity
            
            # Determine aging status
            aging._determine_aging_status()
            
            # Determine action required
            aging._determine_action_required()
    
    def _determine_aging_status(self):
        """Determine overall aging status"""
        for aging in self:
            if aging.age_over_365_days > aging.total_quantity * 0.5:
                aging.aging_status = 'obsolete'
            elif aging.age_181_365_days > aging.total_quantity * 0.3:
                aging.aging_status = 'stale'
            elif aging.age_91_180_days > aging.total_quantity * 0.3:
                aging.aging_status = 'aging'
            elif aging.age_31_90_days > aging.total_quantity * 0.5:
                aging.aging_status = 'current'
            else:
                aging.aging_status = 'fresh'
    
    def _determine_action_required(self):
        """Determine action required based on aging"""
        for aging in self:
            if aging.age_over_365_days > aging.total_quantity * 0.3:
                aging.action_required = 'dispose'
                aging.priority = 'urgent'
            elif aging.age_181_365_days > aging.total_quantity * 0.4:
                aging.action_required = 'clearance'
                aging.priority = 'high'
            elif aging.age_91_180_days > aging.total_quantity * 0.5:
                aging.action_required = 'discount'
                aging.priority = 'medium'
            elif aging.age_31_90_days > aging.total_quantity * 0.6:
                aging.action_required = 'promotion'
                aging.priority = 'low'
            else:
                aging.action_required = 'none'
                aging.priority = 'low'
    
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
    
    def get_aging_summary(self):
        """Get aging summary data"""
        return {
            'aging_name': self.name,
            'warehouse': self.warehouse_id.name,
            'location': self.location_id.name if self.location_id else 'All Locations',
            'product': self.product_id.name if self.product_id else 'All Products',
            'aging_date': self.aging_date,
            'age_0_30_days': self.age_0_30_days,
            'age_31_60_days': self.age_31_60_days,
            'age_61_90_days': self.age_61_90_days,
            'age_91_180_days': self.age_91_180_days,
            'age_181_365_days': self.age_181_365_days,
            'age_over_365_days': self.age_over_365_days,
            'total_quantity': self.total_quantity,
            'total_value': self.total_value,
            'product_age_group': self.product_age_group,
            'seasonal_category': self.seasonal_category,
            'aging_status': self.aging_status,
            'action_required': self.action_required,
            'priority': self.priority,
            'turnover_rate': self.turnover_rate,
            'average_age': self.average_age
        }
    
    def get_aging_percentage(self):
        """Get aging percentage breakdown"""
        if self.total_quantity <= 0:
            return {}
        
        return {
            'fresh': (self.age_0_30_days / self.total_quantity) * 100,
            'current': (self.age_31_90_days / self.total_quantity) * 100,
            'aging': (self.age_91_180_days / self.total_quantity) * 100,
            'stale': (self.age_181_365_days / self.total_quantity) * 100,
            'obsolete': (self.age_over_365_days / self.total_quantity) * 100
        }
    
    def check_aging_alerts(self):
        """Check for aging alerts"""
        alerts = []
        
        if self.age_over_365_days > self.total_quantity * 0.2:
            alerts.append({
                'type': 'critical',
                'message': f'High obsolete inventory: {self.age_over_365_days} units over 365 days old'
            })
        
        if self.age_181_365_days > self.total_quantity * 0.3:
            alerts.append({
                'type': 'warning',
                'message': f'High stale inventory: {self.age_181_365_days} units 181-365 days old'
            })
        
        if self.average_age > 180:
            alerts.append({
                'type': 'info',
                'message': f'High average age: {self.average_age:.1f} days'
            })
        
        return alerts