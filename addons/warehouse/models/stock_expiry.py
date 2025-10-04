# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Stock Expiry
================================

Stock expiry management for kids clothing retail.
"""

from core_framework.orm import BaseModel, CharField, TextField, BooleanField, IntegerField, DateTimeField, Many2OneField, SelectionField, FloatField, One2ManyField, Many2ManyField
from core_framework.orm import Field
from typing import Dict, Any, Optional
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class StockExpiry(BaseModel):
    """Stock expiry tracking for inventory management"""
    
    _name = 'stock.expiry'
    _description = 'Stock Expiry'
    _table = 'stock_expiry'
    
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
        help='Warehouse for this expiry report'
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
    
    # Expiry Analysis
    expiry_date = DateTimeField(
        string='Expiry Date',
        required=True,
        help='Date of the expiry analysis'
    )
    
    # Expiry Categories
    expired_quantity = FloatField(
        string='Expired',
        digits=(12, 3),
        default=0.0,
        help='Quantity that has expired'
    )
    
    expiring_7_days = FloatField(
        string='Expiring in 7 Days',
        digits=(12, 3),
        default=0.0,
        help='Quantity expiring within 7 days'
    )
    
    expiring_15_days = FloatField(
        string='Expiring in 15 Days',
        digits=(12, 3),
        default=0.0,
        help='Quantity expiring within 15 days'
    )
    
    expiring_30_days = FloatField(
        string='Expiring in 30 Days',
        digits=(12, 3),
        default=0.0,
        help='Quantity expiring within 30 days'
    )
    
    expiring_60_days = FloatField(
        string='Expiring in 60 Days',
        digits=(12, 3),
        default=0.0,
        help='Quantity expiring within 60 days'
    )
    
    expiring_90_days = FloatField(
        string='Expiring in 90 Days',
        digits=(12, 3),
        default=0.0,
        help='Quantity expiring within 90 days'
    )
    
    no_expiry = FloatField(
        string='No Expiry',
        digits=(12, 3),
        default=0.0,
        help='Quantity with no expiry date'
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
        help='Total value of inventory'
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
    
    # Expiry Status
    expiry_status = SelectionField(
        string='Expiry Status',
        selection=[
            ('critical', 'Critical (Expired)'),
            ('urgent', 'Urgent (7 days)'),
            ('warning', 'Warning (15 days)'),
            ('caution', 'Caution (30 days)'),
            ('normal', 'Normal (60+ days)'),
            ('no_expiry', 'No Expiry')
        ],
        help='Overall expiry status'
    )
    
    # Action Required
    action_required = SelectionField(
        string='Action Required',
        selection=[
            ('none', 'No Action'),
            ('immediate_sale', 'Immediate Sale'),
            ('clearance', 'Clearance Sale'),
            ('discount', 'Discount Sale'),
            ('return', 'Return to Vendor'),
            ('donate', 'Donate'),
            ('dispose', 'Dispose')
        ],
        default='none',
        help='Action required for expiring inventory'
    )
    
    # Priority
    priority = SelectionField(
        string='Priority',
        selection=[
            ('low', 'Low'),
            ('medium', 'Medium'),
            ('high', 'High'),
            ('urgent', 'Urgent'),
            ('critical', 'Critical')
        ],
        default='low',
        help='Priority level for action'
    )
    
    # Analysis Results
    expiry_risk_score = FloatField(
        string='Expiry Risk Score',
        digits=(5, 2),
        default=0.0,
        help='Expiry risk score (0-100)'
    )
    
    average_days_to_expiry = FloatField(
        string='Average Days to Expiry',
        digits=(8, 2),
        default=0.0,
        help='Average days to expiry'
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
    
    write_date = DateTimeField(
        string='Updated On',
        auto_now=True
    )
    
    def create(self, vals):
        """Override create to set defaults"""
        if 'expiry_date' not in vals:
            vals['expiry_date'] = datetime.now()
        
        return super().create(vals)
    
    def write(self, vals):
        """Override write to update calculations"""
        result = super().write(vals)
        
        # Update calculations when quantities change
        if any(field in vals for field in ['expired_quantity', 'expiring_7_days', 'expiring_15_days', 'expiring_30_days', 'expiring_60_days', 'expiring_90_days', 'no_expiry']):
            self._update_calculations()
        
        return result
    
    def _update_calculations(self):
        """Update calculated fields"""
        for expiry in self:
            # Calculate total quantity
            expiry.total_quantity = (
                expiry.expired_quantity +
                expiry.expiring_7_days +
                expiry.expiring_15_days +
                expiry.expiring_30_days +
                expiry.expiring_60_days +
                expiry.expiring_90_days +
                expiry.no_expiry
            )
            
            # Calculate average days to expiry
            if expiry.total_quantity > 0:
                total_days = (
                    expiry.expired_quantity * -7 +  # Expired (negative days)
                    expiry.expiring_7_days * 3.5 +  # Average of 0-7 days
                    expiry.expiring_15_days * 11 +  # Average of 8-15 days
                    expiry.expiring_30_days * 22.5 +  # Average of 16-30 days
                    expiry.expiring_60_days * 45 +  # Average of 31-60 days
                    expiry.expiring_90_days * 75 +  # Average of 61-90 days
                    expiry.no_expiry * 999  # No expiry (very high number)
                )
                expiry.average_days_to_expiry = total_days / expiry.total_quantity
            
            # Calculate expiry risk score
            expiry._calculate_expiry_risk_score()
            
            # Determine expiry status
            expiry._determine_expiry_status()
            
            # Determine action required
            expiry._determine_action_required()
    
    def _calculate_expiry_risk_score(self):
        """Calculate expiry risk score"""
        for expiry in self:
            if expiry.total_quantity <= 0:
                expiry.expiry_risk_score = 0.0
                continue
            
            # Calculate risk based on expiring quantities
            risk_score = (
                expiry.expired_quantity * 100 +  # Expired = 100% risk
                expiry.expiring_7_days * 90 +  # 7 days = 90% risk
                expiry.expiring_15_days * 70 +  # 15 days = 70% risk
                expiry.expiring_30_days * 50 +  # 30 days = 50% risk
                expiry.expiring_60_days * 30 +  # 60 days = 30% risk
                expiry.expiring_90_days * 10 +  # 90 days = 10% risk
                expiry.no_expiry * 0  # No expiry = 0% risk
            )
            
            expiry.expiry_risk_score = risk_score / expiry.total_quantity
    
    def _determine_expiry_status(self):
        """Determine overall expiry status"""
        for expiry in self:
            if expiry.expired_quantity > 0:
                expiry.expiry_status = 'critical'
            elif expiry.expiring_7_days > expiry.total_quantity * 0.1:
                expiry.expiry_status = 'urgent'
            elif expiry.expiring_15_days > expiry.total_quantity * 0.2:
                expiry.expiry_status = 'warning'
            elif expiry.expiring_30_days > expiry.total_quantity * 0.3:
                expiry.expiry_status = 'caution'
            elif expiry.no_expiry > expiry.total_quantity * 0.8:
                expiry.expiry_status = 'no_expiry'
            else:
                expiry.expiry_status = 'normal'
    
    def _determine_action_required(self):
        """Determine action required based on expiry"""
        for expiry in self:
            if expiry.expired_quantity > 0:
                expiry.action_required = 'immediate_sale'
                expiry.priority = 'critical'
            elif expiry.expiring_7_days > expiry.total_quantity * 0.2:
                expiry.action_required = 'clearance'
                expiry.priority = 'urgent'
            elif expiry.expiring_15_days > expiry.total_quantity * 0.3:
                expiry.action_required = 'discount'
                expiry.priority = 'high'
            elif expiry.expiring_30_days > expiry.total_quantity * 0.4:
                expiry.action_required = 'discount'
                expiry.priority = 'medium'
            else:
                expiry.action_required = 'none'
                expiry.priority = 'low'
    
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
    
    def get_expiry_summary(self):
        """Get expiry summary data"""
        return {
            'expiry_name': self.name,
            'warehouse': self.warehouse_id.name,
            'location': self.location_id.name if self.location_id else 'All Locations',
            'product': self.product_id.name if self.product_id else 'All Products',
            'expiry_date': self.expiry_date,
            'expired_quantity': self.expired_quantity,
            'expiring_7_days': self.expiring_7_days,
            'expiring_15_days': self.expiring_15_days,
            'expiring_30_days': self.expiring_30_days,
            'expiring_60_days': self.expiring_60_days,
            'expiring_90_days': self.expiring_90_days,
            'no_expiry': self.no_expiry,
            'total_quantity': self.total_quantity,
            'total_value': self.total_value,
            'product_age_group': self.product_age_group,
            'seasonal_category': self.seasonal_category,
            'expiry_status': self.expiry_status,
            'action_required': self.action_required,
            'priority': self.priority,
            'expiry_risk_score': self.expiry_risk_score,
            'average_days_to_expiry': self.average_days_to_expiry
        }
    
    def get_expiry_percentage(self):
        """Get expiry percentage breakdown"""
        if self.total_quantity <= 0:
            return {}
        
        return {
            'expired': (self.expired_quantity / self.total_quantity) * 100,
            'expiring_7_days': (self.expiring_7_days / self.total_quantity) * 100,
            'expiring_15_days': (self.expiring_15_days / self.total_quantity) * 100,
            'expiring_30_days': (self.expiring_30_days / self.total_quantity) * 100,
            'expiring_60_days': (self.expiring_60_days / self.total_quantity) * 100,
            'expiring_90_days': (self.expiring_90_days / self.total_quantity) * 100,
            'no_expiry': (self.no_expiry / self.total_quantity) * 100
        }
    
    def check_expiry_alerts(self):
        """Check for expiry alerts"""
        alerts = []
        
        if self.expired_quantity > 0:
            alerts.append({
                'type': 'critical',
                'message': f'Expired inventory: {self.expired_quantity} units have expired'
            })
        
        if self.expiring_7_days > self.total_quantity * 0.1:
            alerts.append({
                'type': 'urgent',
                'message': f'Urgent expiry: {self.expiring_7_days} units expiring within 7 days'
            })
        
        if self.expiring_15_days > self.total_quantity * 0.2:
            alerts.append({
                'type': 'warning',
                'message': f'Expiry warning: {self.expiring_15_days} units expiring within 15 days'
            })
        
        if self.expiry_risk_score > 50:
            alerts.append({
                'type': 'info',
                'message': f'High expiry risk: {self.expiry_risk_score:.1f}% risk score'
            })
        
        return alerts