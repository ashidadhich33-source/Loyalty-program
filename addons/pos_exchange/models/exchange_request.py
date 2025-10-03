#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Exchange Request Models
==========================================

Exchange request and line management for product exchanges.
"""

import logging
from datetime import datetime, timedelta
from core_framework.orm import BaseModel, CharField, TextField, BooleanField, IntegerField, DateTimeField, Many2OneField, SelectionField, FloatField, One2ManyField, Many2ManyField
from core_framework.exceptions import ValidationError

logger = logging.getLogger(__name__)

class ExchangeRequest(BaseModel):
    """Exchange request for product exchanges"""
    
    _name = 'exchange.request'
    _description = 'Exchange Request'
    _table = 'exchange_request'
    _order = 'create_date desc'
    
    # Basic Information
    name = CharField(
        string='Exchange Reference',
        size=100,
        required=True,
        help='Exchange request reference'
    )
    
    partner_id = Many2OneField(
        'res.partner',
        string='Customer',
        required=True,
        help='Customer requesting exchange'
    )
    
    original_order_id = Many2OneField(
        'pos.order',
        string='Original Order',
        help='Original POS order'
    )
    
    # Exchange Details
    exchange_type = SelectionField(
        string='Exchange Type',
        selection=[
            ('size', 'Size Exchange'),
            ('color', 'Color Exchange'),
            ('style', 'Style Exchange'),
            ('age_group', 'Age Group Exchange'),
            ('product', 'Product Exchange'),
            ('mixed', 'Mixed Exchange')
        ],
        required=True,
        help='Type of exchange'
    )
    
    exchange_reason = SelectionField(
        string='Exchange Reason',
        selection=[
            ('size_issue', 'Size Issue'),
            ('color_preference', 'Color Preference'),
            ('style_preference', 'Style Preference'),
            ('age_group_change', 'Age Group Change'),
            ('product_defect', 'Product Defect'),
            ('customer_preference', 'Customer Preference'),
            ('other', 'Other')
        ],
        required=True,
        help='Reason for exchange'
    )
    
    reason_description = TextField(
        string='Reason Description',
        help='Detailed description of exchange reason'
    )
    
    # Exchange Status
    state = SelectionField(
        string='Status',
        selection=[
            ('draft', 'Draft'),
            ('submitted', 'Submitted'),
            ('under_review', 'Under Review'),
            ('approved', 'Approved'),
            ('rejected', 'Rejected'),
            ('completed', 'Completed'),
            ('cancelled', 'Cancelled')
        ],
        default='draft',
        help='Exchange request status'
    )
    
    # Exchange Lines
    exchange_line_ids = One2ManyField(
        string='Exchange Lines',
        comodel_name='exchange.request.line',
        inverse_name='exchange_id',
        help='Exchange request lines'
    )
    
    # Pricing Information
    original_amount = FloatField(
        string='Original Amount',
        digits=(12, 2),
        default=0.0,
        help='Original purchase amount'
    )
    
    exchange_amount = FloatField(
        string='Exchange Amount',
        digits=(12, 2),
        default=0.0,
        help='Exchange amount'
    )
    
    difference_amount = FloatField(
        string='Difference Amount',
        digits=(12, 2),
        default=0.0,
        help='Amount difference (positive = refund, negative = additional payment)'
    )
    
    # Exchange Policy
    exchange_policy = SelectionField(
        string='Exchange Policy',
        selection=[
            ('free', 'Free Exchange'),
            ('paid', 'Paid Exchange'),
            ('partial', 'Partial Exchange'),
            ('no_exchange', 'No Exchange')
        ],
        default='free',
        help='Exchange policy applied'
    )
    
    # Time Limits
    exchange_within_days = IntegerField(
        string='Exchange Within Days',
        default=30,
        help='Number of days within which exchange is allowed'
    )
    
    is_within_time_limit = BooleanField(
        string='Within Time Limit',
        default=True,
        help='Whether exchange is within time limit'
    )
    
    # Approval Information
    approval_required = BooleanField(
        string='Approval Required',
        default=False,
        help='Whether approval is required'
    )
    
    approver_id = Many2OneField(
        'res.users',
        string='Approver',
        help='User who approved the exchange'
    )
    
    approval_date = DateTimeField(
        string='Approval Date',
        help='Date when exchange was approved'
    )
    
    approval_notes = TextField(
        string='Approval Notes',
        help='Notes from approver'
    )
    
    # Processing Information
    processed_by = Many2OneField(
        'res.users',
        string='Processed By',
        help='User who processed the exchange'
    )
    
    processed_date = DateTimeField(
        string='Processed Date',
        help='Date when exchange was processed'
    )
    
    # Customer Information
    customer_phone = CharField(
        string='Customer Phone',
        size=20,
        help='Customer phone number'
    )
    
    customer_email = CharField(
        string='Customer Email',
        size=100,
        help='Customer email address'
    )
    
    # Notes
    notes = TextField(
        string='Notes',
        help='Additional notes'
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
        if 'name' not in vals:
            vals['name'] = self._generate_exchange_reference()
        
        return super().create(vals)
    
    def write(self, vals):
        """Override write to update calculations"""
        result = super().write(vals)
        
        # Update calculations if lines changed
        if 'exchange_line_ids' in vals:
            for record in self:
                record._update_exchange_calculations()
        
        return result
    
    def _generate_exchange_reference(self):
        """Generate exchange reference"""
        return f"EXC{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    def _update_exchange_calculations(self):
        """Update exchange calculations"""
        for record in self:
            # Calculate amounts from lines
            original_amount = 0.0
            exchange_amount = 0.0
            
            for line in record.exchange_line_ids:
                original_amount += line.original_price_total
                exchange_amount += line.exchange_price_total
            
            # Update fields
            record.original_amount = original_amount
            record.exchange_amount = exchange_amount
            record.difference_amount = exchange_amount - original_amount
            
            # Check time limit
            if record.original_order_id:
                days_diff = (datetime.now() - record.original_order_id.create_date).days
                record.is_within_time_limit = days_diff <= record.exchange_within_days
    
    def action_submit_exchange(self):
        """Submit exchange request"""
        for record in self:
            if record.state == 'draft':
                record.state = 'submitted'
                record._check_approval_requirements()
    
    def action_approve_exchange(self):
        """Approve exchange request"""
        for record in self:
            if record.state in ['submitted', 'under_review']:
                record.state = 'approved'
                record.approver_id = self.env.user
                record.approval_date = datetime.now()
    
    def action_reject_exchange(self):
        """Reject exchange request"""
        for record in self:
            if record.state in ['submitted', 'under_review']:
                record.state = 'rejected'
    
    def action_complete_exchange(self):
        """Complete exchange request"""
        for record in self:
            if record.state == 'approved':
                record.state = 'completed'
                record.processed_by = self.env.user
                record.processed_date = datetime.now()
                record._process_exchange()
    
    def action_cancel_exchange(self):
        """Cancel exchange request"""
        for record in self:
            if record.state in ['draft', 'submitted', 'under_review']:
                record.state = 'cancelled'
    
    def _check_approval_requirements(self):
        """Check if approval is required"""
        for record in self:
            # Check if amount exceeds approval limit
            if record.difference_amount > 1000:  # Example limit
                record.approval_required = True
                record.state = 'under_review'
    
    def _process_exchange(self):
        """Process the exchange"""
        for record in self:
            # Create new order for exchange
            # Update inventory
            # Process payment difference
            # Update customer loyalty points
            pass
    
    def get_exchange_summary(self):
        """Get exchange summary"""
        return {
            'exchange_info': {
                'name': self.name,
                'customer': self.partner_id.name,
                'type': self.exchange_type,
                'reason': self.exchange_reason,
                'status': self.state,
                'date': self.create_date
            },
            'pricing': {
                'original_amount': self.original_amount,
                'exchange_amount': self.exchange_amount,
                'difference_amount': self.difference_amount,
                'policy': self.exchange_policy
            },
            'approval': {
                'required': self.approval_required,
                'approver': self.approver_id.name if self.approver_id else None,
                'approval_date': self.approval_date,
                'notes': self.approval_notes
            },
            'processing': {
                'processed_by': self.processed_by.name if self.processed_by else None,
                'processed_date': self.processed_date
            },
            'time_limit': {
                'within_limit': self.is_within_time_limit,
                'days_allowed': self.exchange_within_days
            }
        }
    
    def action_view_exchange_lines(self):
        """View exchange lines"""
        return {
            'type': 'ocean.actions.act_window',
            'name': f'Exchange Lines - {self.name}',
            'res_model': 'exchange.request.line',
            'view_mode': 'tree,form',
            'domain': [('exchange_id', '=', self.id)],
            'context': {'default_exchange_id': self.id}
        }


class ExchangeRequestLine(BaseModel):
    """Exchange request line for individual items"""
    
    _name = 'exchange.request.line'
    _description = 'Exchange Request Line'
    _table = 'exchange_request_line'
    _order = 'sequence, id'
    
    # Basic Information
    exchange_id = Many2OneField(
        'exchange.request',
        string='Exchange Request',
        required=True,
        help='Parent exchange request'
    )
    
    # Original Product
    original_product_id = Many2OneField(
        'product.product',
        string='Original Product',
        required=True,
        help='Product being exchanged'
    )
    
    original_product_name = CharField(
        string='Original Product Name',
        size=200,
        help='Name of original product'
    )
    
    original_size = CharField(
        string='Original Size',
        size=20,
        help='Original product size'
    )
    
    original_color = CharField(
        string='Original Color',
        size=50,
        help='Original product color'
    )
    
    original_quantity = FloatField(
        string='Original Quantity',
        digits=(10, 3),
        default=1.0,
        help='Original quantity'
    )
    
    original_price_unit = FloatField(
        string='Original Unit Price',
        digits=(12, 2),
        help='Original unit price'
    )
    
    original_price_total = FloatField(
        string='Original Total',
        digits=(12, 2),
        help='Original total price'
    )
    
    # Exchange Product
    exchange_product_id = Many2OneField(
        'product.product',
        string='Exchange Product',
        help='Product to exchange for'
    )
    
    exchange_product_name = CharField(
        string='Exchange Product Name',
        size=200,
        help='Name of exchange product'
    )
    
    exchange_size = CharField(
        string='Exchange Size',
        size=20,
        help='Exchange product size'
    )
    
    exchange_color = CharField(
        string='Exchange Color',
        size=50,
        help='Exchange product color'
    )
    
    exchange_quantity = FloatField(
        string='Exchange Quantity',
        digits=(10, 3),
        default=1.0,
        help='Exchange quantity'
    )
    
    exchange_price_unit = FloatField(
        string='Exchange Unit Price',
        digits=(12, 2),
        help='Exchange unit price'
    )
    
    exchange_price_total = FloatField(
        string='Exchange Total',
        digits=(12, 2),
        help='Exchange total price'
    )
    
    # Exchange Details
    exchange_reason = TextField(
        string='Exchange Reason',
        help='Reason for this specific exchange'
    )
    
    condition_original = SelectionField(
        string='Original Condition',
        selection=[
            ('new', 'New'),
            ('like_new', 'Like New'),
            ('good', 'Good'),
            ('fair', 'Fair'),
            ('poor', 'Poor')
        ],
        default='new',
        help='Condition of original product'
    )
    
    condition_exchange = SelectionField(
        string='Exchange Condition',
        selection=[
            ('new', 'New'),
            ('like_new', 'Like New'),
            ('good', 'Good'),
            ('fair', 'Fair'),
            ('poor', 'Poor')
        ],
        default='new',
        help='Condition of exchange product'
    )
    
    # Display Order
    sequence = IntegerField(
        string='Sequence',
        default=10,
        help='Display order'
    )
    
    # Notes
    notes = TextField(
        string='Notes',
        help='Line notes'
    )
    
    def create(self, vals):
        """Override create to set defaults"""
        result = super().create(vals)
        
        # Update calculations
        for record in result:
            record._update_line_calculations()
        
        return result
    
    def write(self, vals):
        """Override write to update calculations"""
        result = super().write(vals)
        
        # Update calculations if pricing changed
        if any(field in vals for field in ['original_quantity', 'original_price_unit', 'exchange_quantity', 'exchange_price_unit']):
            for record in self:
                record._update_line_calculations()
        
        return result
    
    def _update_line_calculations(self):
        """Update line calculations"""
        for record in self:
            # Calculate original total
            record.original_price_total = record.original_quantity * record.original_price_unit
            
            # Calculate exchange total
            record.exchange_price_total = record.exchange_quantity * record.exchange_price_unit
    
    def get_line_summary(self):
        """Get line summary"""
        return {
            'original_product': {
                'name': self.original_product_name,
                'size': self.original_size,
                'color': self.original_color,
                'quantity': self.original_quantity,
                'unit_price': self.original_price_unit,
                'total': self.original_price_total,
                'condition': self.condition_original
            },
            'exchange_product': {
                'name': self.exchange_product_name,
                'size': self.exchange_size,
                'color': self.exchange_color,
                'quantity': self.exchange_quantity,
                'unit_price': self.exchange_price_unit,
                'total': self.exchange_price_total,
                'condition': self.condition_exchange
            },
            'difference': {
                'amount': self.exchange_price_total - self.original_price_total,
                'reason': self.exchange_reason
            }
        }