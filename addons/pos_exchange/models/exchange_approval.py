#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Exchange Approval Model
==========================================

Exchange approval workflow management.
"""

import logging
from datetime import datetime
from core_framework.orm import BaseModel, CharField, TextField, BooleanField, IntegerField, DateTimeField, Many2OneField, SelectionField, FloatField, One2ManyField, Many2ManyField
from core_framework.exceptions import ValidationError

logger = logging.getLogger(__name__)

class ExchangeApproval(BaseModel):
    """Exchange approval workflow"""
    
    _name = 'exchange.approval'
    _description = 'Exchange Approval'
    _table = 'exchange_approval'
    _order = 'create_date desc'
    
    # Basic Information
    name = CharField(
        string='Approval Reference',
        size=100,
        required=True,
        help='Approval reference'
    )
    
    exchange_id = Many2OneField(
        'exchange.request',
        string='Exchange Request',
        required=True,
        help='Related exchange request'
    )
    
    # Approval Details
    approval_type = SelectionField(
        string='Approval Type',
        selection=[
            ('automatic', 'Automatic'),
            ('manager', 'Manager Approval'),
            ('senior_manager', 'Senior Manager Approval'),
            ('admin', 'Admin Approval')
        ],
        required=True,
        help='Type of approval required'
    )
    
    approval_level = IntegerField(
        string='Approval Level',
        default=1,
        help='Approval level (1, 2, 3, etc.)'
    )
    
    # Approval Status
    state = SelectionField(
        string='Status',
        selection=[
            ('pending', 'Pending'),
            ('approved', 'Approved'),
            ('rejected', 'Rejected'),
            ('cancelled', 'Cancelled')
        ],
        default='pending',
        help='Approval status'
    )
    
    # Approver Information
    approver_id = Many2OneField(
        'res.users',
        string='Approver',
        help='User who approved/rejected'
    )
    
    approval_date = DateTimeField(
        string='Approval Date',
        help='Date of approval/rejection'
    )
    
    approval_notes = TextField(
        string='Approval Notes',
        help='Notes from approver'
    )
    
    # Approval Criteria
    amount_threshold = FloatField(
        string='Amount Threshold',
        digits=(12, 2),
        help='Amount threshold for this approval'
    )
    
    exchange_amount = FloatField(
        string='Exchange Amount',
        digits=(12, 2),
        help='Amount of exchange request'
    )
    
    # Approval Rules
    requires_receipt = BooleanField(
        string='Requires Receipt',
        default=True,
        help='Whether receipt is required'
    )
    
    requires_original_packaging = BooleanField(
        string='Requires Original Packaging',
        default=True,
        help='Whether original packaging is required'
    )
    
    within_time_limit = BooleanField(
        string='Within Time Limit',
        default=True,
        help='Whether exchange is within time limit'
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
            vals['name'] = self._generate_approval_reference()
        
        return super().create(vals)
    
    def _generate_approval_reference(self):
        """Generate approval reference"""
        return f"APR{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    def action_approve(self):
        """Approve the exchange"""
        for record in self:
            if record.state == 'pending':
                record.state = 'approved'
                record.approver_id = self.env.user
                record.approval_date = datetime.now()
                
                # Update exchange request
                record.exchange_id.action_approve_exchange()
    
    def action_reject(self):
        """Reject the exchange"""
        for record in self:
            if record.state == 'pending':
                record.state = 'rejected'
                record.approver_id = self.env.user
                record.approval_date = datetime.now()
                
                # Update exchange request
                record.exchange_id.action_reject_exchange()
    
    def action_cancel(self):
        """Cancel the approval"""
        for record in self:
            if record.state == 'pending':
                record.state = 'cancelled'
    
    def get_approval_summary(self):
        """Get approval summary"""
        return {
            'approval_info': {
                'name': self.name,
                'type': self.approval_type,
                'level': self.approval_level,
                'status': self.state,
                'date': self.create_date
            },
            'approver_info': {
                'approver': self.approver_id.name if self.approver_id else None,
                'approval_date': self.approval_date,
                'notes': self.approval_notes
            },
            'criteria': {
                'amount_threshold': self.amount_threshold,
                'exchange_amount': self.exchange_amount,
                'requires_receipt': self.requires_receipt,
                'requires_packaging': self.requires_original_packaging,
                'within_time_limit': self.within_time_limit
            }
        }