# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Warehouse Operation
=======================================

Warehouse operation management for kids clothing retail.
"""

from core_framework.orm import BaseModel, CharField, TextField, BooleanField, IntegerField, DateTimeField, Many2OneField, SelectionField, FloatField, One2ManyField, Many2ManyField
from core_framework.orm import Field
from typing import Dict, Any, Optional
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class WarehouseOperation(BaseModel):
    """Warehouse operation for inventory management"""
    
    _name = 'warehouse.operation'
    _description = 'Warehouse Operation'
    _table = 'warehouse_operation'
    
    # Basic Information
    name = CharField(
        string='Operation Name',
        size=100,
        required=True,
        help='Name of the warehouse operation'
    )
    
    code = CharField(
        string='Operation Code',
        size=20,
        help='Short code for the operation'
    )
    
    description = TextField(
        string='Description',
        help='Description of the operation'
    )
    
    # Warehouse Reference
    warehouse_id = Many2OneField(
        'warehouse',
        string='Warehouse',
        required=True,
        help='Warehouse for this operation'
    )
    
    # Operation Type
    operation_type = SelectionField(
        string='Operation Type',
        selection=[
            ('receiving', 'Receiving'),
            ('putaway', 'Putaway'),
            ('picking', 'Picking'),
            ('packing', 'Packing'),
            ('shipping', 'Shipping'),
            ('inventory', 'Inventory Count'),
            ('transfer', 'Transfer'),
            ('adjustment', 'Adjustment'),
            ('quality_check', 'Quality Check'),
            ('maintenance', 'Maintenance')
        ],
        required=True,
        help='Type of warehouse operation'
    )
    
    # Operation State
    state = SelectionField(
        string='State',
        selection=[
            ('draft', 'Draft'),
            ('in_progress', 'In Progress'),
            ('done', 'Done'),
            ('cancel', 'Cancelled')
        ],
        default='draft',
        help='Current state of the operation'
    )
    
    # Priority
    priority = SelectionField(
        string='Priority',
        selection=[
            ('0', 'Normal'),
            ('1', 'High'),
            ('2', 'Very High')
        ],
        default='0',
        help='Priority of the operation'
    )
    
    # User Information
    user_id = Many2OneField(
        'res.users',
        string='Operator',
        required=True,
        help='User performing the operation'
    )
    
    # Date Information
    scheduled_date = DateTimeField(
        string='Scheduled Date',
        help='Scheduled date for the operation'
    )
    
    start_date = DateTimeField(
        string='Start Date',
        help='Actual start date of the operation'
    )
    
    end_date = DateTimeField(
        string='End Date',
        help='Actual end date of the operation'
    )
    
    # Duration
    estimated_duration = FloatField(
        string='Estimated Duration (hours)',
        digits=(8, 2),
        default=0.0,
        help='Estimated duration in hours'
    )
    
    actual_duration = FloatField(
        string='Actual Duration (hours)',
        digits=(8, 2),
        default=0.0,
        help='Actual duration in hours'
    )
    
    # Kids Clothing Specific
    customer_age = IntegerField(
        string='Customer Age',
        help='Age of the customer (for age-specific operations)'
    )
    
    product_age_group = SelectionField(
        string='Product Age Group',
        selection=[
            ('toddler', 'Toddler (0-3 years)'),
            ('child', 'Child (3-12 years)'),
            ('teen', 'Teen (12+ years)'),
            ('mixed', 'Mixed Age Groups')
        ],
        help='Age group of products involved'
    )
    
    # Seasonal Information
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
        help='Seasonal category of products'
    )
    
    # Quality Control
    quality_check_required = BooleanField(
        string='Quality Check Required',
        default=False,
        help='Whether quality check is required'
    )
    
    quality_check_done = BooleanField(
        string='Quality Check Done',
        default=False,
        help='Whether quality check is completed'
    )
    
    quality_notes = TextField(
        string='Quality Notes',
        help='Quality check notes'
    )
    
    # Performance Metrics
    efficiency_score = FloatField(
        string='Efficiency Score',
        digits=(5, 2),
        default=0.0,
        help='Operation efficiency score (0-100)'
    )
    
    accuracy_score = FloatField(
        string='Accuracy Score',
        digits=(5, 2),
        default=100.0,
        help='Operation accuracy score (0-100)'
    )
    
    # Related Records
    move_ids = One2ManyField(
        'stock.move',
        string='Stock Moves',
        help='Stock moves related to this operation'
    )
    
    picking_ids = One2ManyField(
        'stock.picking',
        string='Stock Pickings',
        help='Stock pickings related to this operation'
    )
    
    # Notes
    note = TextField(
        string='Notes',
        help='Additional notes about this operation'
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
        if 'code' not in vals and 'name' in vals:
            vals['code'] = vals['name'].upper().replace(' ', '_')
        
        if 'user_id' not in vals:
            vals['user_id'] = self.env.user.id
        
        if 'scheduled_date' not in vals:
            vals['scheduled_date'] = datetime.now()
        
        return super().create(vals)
    
    def write(self, vals):
        """Override write to update state"""
        result = super().write(vals)
        
        # Update state when dates change
        if any(field in vals for field in ['start_date', 'end_date']):
            self._update_state()
        
        # Calculate duration
        if any(field in vals for field in ['start_date', 'end_date']):
            self._calculate_duration()
        
        return result
    
    def _update_state(self):
        """Update operation state based on dates"""
        for operation in self:
            if operation.end_date:
                operation.state = 'done'
            elif operation.start_date:
                operation.state = 'in_progress'
            else:
                operation.state = 'draft'
    
    def _calculate_duration(self):
        """Calculate actual duration"""
        for operation in self:
            if operation.start_date and operation.end_date:
                duration = operation.end_date - operation.start_date
                operation.actual_duration = duration.total_seconds() / 3600  # Convert to hours
                
                # Calculate efficiency score
                if operation.estimated_duration > 0:
                    operation.efficiency_score = (operation.estimated_duration / operation.actual_duration) * 100
    
    def action_start(self):
        """Start the operation"""
        if self.state != 'draft':
            raise ValueError("Only draft operations can be started")
        
        self.state = 'in_progress'
        self.start_date = datetime.now()
        return True
    
    def action_done(self):
        """Mark operation as done"""
        if self.state != 'in_progress':
            raise ValueError("Operation must be in progress to be marked as done")
        
        # Validate operation
        self._validate_operation()
        
        self.state = 'done'
        self.end_date = datetime.now()
        
        # Calculate final metrics
        self._calculate_duration()
        
        return True
    
    def action_cancel(self):
        """Cancel the operation"""
        if self.state == 'done':
            raise ValueError("Cannot cancel completed operations")
        
        self.state = 'cancel'
        return True
    
    def _validate_operation(self):
        """Validate operation before completion"""
        errors = []
        
        # Check required fields
        if not self.warehouse_id:
            errors.append("Warehouse is required")
        
        if not self.user_id:
            errors.append("Operator is required")
        
        if not self.operation_type:
            errors.append("Operation type is required")
        
        # Check quality requirements
        if self.quality_check_required and not self.quality_check_done:
            errors.append("Quality check is required but not completed")
        
        # Check age group compatibility
        if self.customer_age and self.product_age_group:
            if self.customer_age <= 3 and self.product_age_group != 'toddler':
                errors.append("Customer age and product age group mismatch")
            elif 3 < self.customer_age <= 12 and self.product_age_group != 'child':
                errors.append("Customer age and product age group mismatch")
            elif self.customer_age > 12 and self.product_age_group != 'teen':
                errors.append("Customer age and product age group mismatch")
        
        if errors:
            raise ValueError('\n'.join(errors))
    
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
    
    def action_view_moves(self):
        """View related stock moves"""
        return {
            'type': 'ir.actions.act_window',
            'name': f'Stock Moves - {self.name}',
            'res_model': 'stock.move',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', [move.id for move in self.move_ids])],
            'context': {'default_origin': self.name}
        }
    
    def action_view_pickings(self):
        """View related stock pickings"""
        return {
            'type': 'ir.actions.act_window',
            'name': f'Stock Pickings - {self.name}',
            'res_model': 'stock.picking',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', [picking.id for picking in self.picking_ids])],
            'context': {'default_origin': self.name}
        }
    
    def get_operation_summary(self):
        """Get operation summary data"""
        return {
            'operation_name': self.name,
            'operation_code': self.code,
            'warehouse': self.warehouse_id.name,
            'operation_type': self.operation_type,
            'state': self.state,
            'priority': self.priority,
            'operator': self.user_id.name,
            'scheduled_date': self.scheduled_date,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'estimated_duration': self.estimated_duration,
            'actual_duration': self.actual_duration,
            'customer_age': self.customer_age,
            'product_age_group': self.product_age_group,
            'seasonal_category': self.seasonal_category,
            'quality_check_required': self.quality_check_required,
            'quality_check_done': self.quality_check_done,
            'efficiency_score': self.efficiency_score,
            'accuracy_score': self.accuracy_score,
            'move_count': len(self.move_ids),
            'picking_count': len(self.picking_ids)
        }
    
    def get_performance_metrics(self):
        """Get performance metrics"""
        return {
            'efficiency_score': self.efficiency_score,
            'accuracy_score': self.accuracy_score,
            'duration_variance': self._get_duration_variance(),
            'quality_score': self._get_quality_score()
        }
    
    def _get_duration_variance(self):
        """Get duration variance percentage"""
        if self.estimated_duration <= 0:
            return 0.0
        
        return ((self.actual_duration - self.estimated_duration) / self.estimated_duration) * 100
    
    def _get_quality_score(self):
        """Get quality score"""
        if not self.quality_check_required:
            return 100.0
        
        return 100.0 if self.quality_check_done else 0.0