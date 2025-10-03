#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Sale Return Model
=====================================

Return order management for kids clothing retail.
"""

import logging
from datetime import datetime, timedelta
from core_framework.orm import BaseModel, CharField, TextField, BooleanField, IntegerField, DateTimeField, Many2OneField, SelectionField, FloatField, One2ManyField, Many2ManyField
from core_framework.exceptions import ValidationError

logger = logging.getLogger(__name__)

class SaleReturn(BaseModel):
    """Return orders for kids clothing retail"""
    
    _name = 'sale.return'
    _description = 'Sale Return'
    _table = 'sale_return'
    _order = 'date_return desc, id desc'
    
    # Basic Information
    name = CharField(
        string='Return Reference',
        size=64,
        required=True,
        help='Unique return reference'
    )
    
    sale_order_id = Many2OneField(
        'sale.order',
        string='Sales Order',
        required=True,
        help='Related sales order'
    )
    
    partner_id = Many2OneField(
        'contact.customer',
        string='Customer',
        related='sale_order_id.partner_id',
        help='Customer for this return'
    )
    
    # Return Details
    date_return = DateTimeField(
        string='Return Date',
        default=datetime.now,
        required=True,
        help='Date when return was initiated'
    )
    
    date_received = DateTimeField(
        string='Received Date',
        help='Date when returned items were received'
    )
    
    date_processed = DateTimeField(
        string='Processed Date',
        help='Date when return was processed'
    )
    
    # Return Status
    state = SelectionField(
        string='Status',
        selection=[
            ('draft', 'Draft'),
            ('confirmed', 'Confirmed'),
            ('received', 'Received'),
            ('processed', 'Processed'),
            ('refunded', 'Refunded'),
            ('exchanged', 'Exchanged'),
            ('rejected', 'Rejected'),
            ('cancelled', 'Cancelled')
        ],
        default='draft',
        help='Current status of the return'
    )
    
    # Return Type
    return_type = SelectionField(
        string='Return Type',
        selection=[
            ('refund', 'Refund'),
            ('exchange', 'Exchange'),
            ('store_credit', 'Store Credit'),
            ('repair', 'Repair'),
            ('replacement', 'Replacement')
        ],
        required=True,
        help='Type of return requested'
    )
    
    # Return Reason
    return_reason = SelectionField(
        string='Return Reason',
        selection=[
            ('defective', 'Defective Product'),
            ('wrong_size', 'Wrong Size'),
            ('wrong_color', 'Wrong Color'),
            ('not_as_described', 'Not as Described'),
            ('damaged_shipping', 'Damaged in Shipping'),
            ('changed_mind', 'Changed Mind'),
            ('gift_return', 'Gift Return'),
            ('other', 'Other')
        ],
        required=True,
        help='Reason for return'
    )
    
    return_reason_notes = TextField(
        string='Return Reason Notes',
        help='Additional notes about return reason'
    )
    
    # Return Items
    return_line_ids = One2ManyField(
        string='Return Lines',
        comodel_name='sale.return.line',
        inverse_name='return_id',
        help='Return lines for this return'
    )
    
    # Return Amounts
    amount_untaxed = FloatField(
        string='Untaxed Amount',
        digits=(12, 2),
        default=0.0,
        help='Return amount without taxes'
    )
    
    amount_tax = FloatField(
        string='Tax Amount',
        digits=(12, 2),
        default=0.0,
        help='Return tax amount'
    )
    
    amount_total = FloatField(
        string='Total Amount',
        digits=(12, 2),
        default=0.0,
        help='Total return amount'
    )
    
    # Refund Information
    refund_method = SelectionField(
        string='Refund Method',
        selection=[
            ('original_payment', 'Original Payment Method'),
            ('store_credit', 'Store Credit'),
            ('bank_transfer', 'Bank Transfer'),
            ('cash', 'Cash'),
            ('check', 'Check')
        ],
        help='Method of refund'
    )
    
    refund_amount = FloatField(
        string='Refund Amount',
        digits=(12, 2),
        default=0.0,
        help='Amount to be refunded'
    )
    
    refund_status = SelectionField(
        string='Refund Status',
        selection=[
            ('pending', 'Pending'),
            ('processed', 'Processed'),
            ('completed', 'Completed'),
            ('failed', 'Failed')
        ],
        default='pending',
        help='Status of refund'
    )
    
    # Exchange Information
    exchange_order_id = Many2OneField(
        'sale.order',
        string='Exchange Order',
        help='New order for exchange'
    )
    
    exchange_products = TextField(
        string='Exchange Products',
        help='Products requested for exchange'
    )
    
    # Return Conditions
    return_within_days = IntegerField(
        string='Return Within Days',
        default=30,
        help='Number of days within which return is allowed'
    )
    
    is_within_return_period = BooleanField(
        string='Within Return Period',
        compute='_compute_return_period',
        help='Whether return is within allowed period'
    )
    
    # Return Conditions
    return_conditions = TextField(
        string='Return Conditions',
        help='Conditions for return acceptance'
    )
    
    # Return Notes
    return_notes = TextField(
        string='Return Notes',
        help='Internal notes for this return'
    )
    
    customer_notes = TextField(
        string='Customer Notes',
        help='Customer notes for this return'
    )
    
    # Return Approval
    requires_approval = BooleanField(
        string='Requires Approval',
        default=False,
        help='Whether this return requires approval'
    )
    
    approved_by = Many2OneField(
        'res.users',
        string='Approved By',
        help='User who approved this return'
    )
    
    approval_date = DateTimeField(
        string='Approval Date',
        help='Date when return was approved'
    )
    
    # Company Information
    company_id = Many2OneField(
        'res.company',
        string='Company',
        related='sale_order_id.company_id',
        help='Company for this return'
    )
    
    user_id = Many2OneField(
        'res.users',
        string='Return Handler',
        help='Person handling this return'
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
            vals['name'] = self._get_next_return_number()
        
        return super().create(vals)
    
    def write(self, vals):
        """Override write to update amounts"""
        result = super().write(vals)
        
        # Update amounts if return lines changed
        if 'return_line_ids' in vals:
            self._update_amounts()
        
        return result
    
    def _get_next_return_number(self):
        """Get next return number"""
        return f"RET{datetime.now().strftime('%Y%m%d')}{self.env['ir.sequence'].next_by_code('sale.return')}"
    
    def _compute_return_period(self):
        """Compute if return is within allowed period"""
        for return_order in self:
            if return_order.sale_order_id.date_order:
                days_since_order = (datetime.now() - return_order.sale_order_id.date_order).days
                return_order.is_within_return_period = days_since_order <= return_order.return_within_days
            else:
                return_order.is_within_return_period = False
    
    def _update_amounts(self):
        """Update return amounts"""
        for return_order in self:
            # Calculate amounts from return lines
            untaxed_amount = sum(line.price_subtotal for line in return_order.return_line_ids)
            
            # Calculate tax (simplified 18% GST)
            tax_amount = untaxed_amount * 0.18
            
            # Update amounts
            return_order.amount_untaxed = untaxed_amount
            return_order.amount_tax = tax_amount
            return_order.amount_total = untaxed_amount + tax_amount
            return_order.refund_amount = return_order.amount_total
    
    def action_confirm(self):
        """Confirm return order"""
        for return_order in self:
            if return_order.state != 'draft':
                raise ValidationError("Only draft returns can be confirmed")
            
            if not return_order.is_within_return_period:
                raise ValidationError("Return is outside the allowed period")
            
            return_order.state = 'confirmed'
    
    def action_receive(self):
        """Mark return as received"""
        for return_order in self:
            if return_order.state != 'confirmed':
                raise ValidationError("Only confirmed returns can be received")
            
            return_order.state = 'received'
            return_order.date_received = datetime.now()
    
    def action_process(self):
        """Process return order"""
        for return_order in self:
            if return_order.state != 'received':
                raise ValidationError("Only received returns can be processed")
            
            return_order.state = 'processed'
            return_order.date_processed = datetime.now()
    
    def action_refund(self):
        """Process refund for return"""
        for return_order in self:
            if return_order.state != 'processed':
                raise ValidationError("Only processed returns can be refunded")
            
            if return_order.return_type != 'refund':
                raise ValidationError("Only refund returns can be refunded")
            
            return_order.state = 'refunded'
            return_order.refund_status = 'completed'
    
    def action_exchange(self):
        """Process exchange for return"""
        for return_order in self:
            if return_order.state != 'processed':
                raise ValidationError("Only processed returns can be exchanged")
            
            if return_order.return_type != 'exchange':
                raise ValidationError("Only exchange returns can be exchanged")
            
            return_order.state = 'exchanged'
    
    def action_reject(self):
        """Reject return order"""
        for return_order in self:
            if return_order.state in ['refunded', 'exchanged']:
                raise ValidationError("Cannot reject completed returns")
            
            return_order.state = 'rejected'
    
    def action_cancel(self):
        """Cancel return order"""
        for return_order in self:
            if return_order.state in ['refunded', 'exchanged']:
                raise ValidationError("Cannot cancel completed returns")
            
            return_order.state = 'cancelled'
    
    def action_view_sale_order(self):
        """View related sales order"""
        return {
            'type': 'ocean.actions.act_window',
            'name': f'Sales Order - {self.sale_order_id.name}',
            'res_model': 'sale.order',
            'res_id': self.sale_order_id.id,
            'view_mode': 'form',
            'target': 'current'
        }
    
    def action_create_exchange_order(self):
        """Create exchange order"""
        return {
            'type': 'ocean.actions.act_window',
            'name': f'Create Exchange Order - {self.name}',
            'res_model': 'sale.order',
            'view_mode': 'form',
            'context': {
                'default_partner_id': self.partner_id.id,
                'default_is_exchange': True,
                'default_original_return_id': self.id
            },
            'target': 'current'
        }
    
    def action_approve(self):
        """Approve return order"""
        for return_order in self:
            if not return_order.requires_approval:
                raise ValidationError("This return does not require approval")
            
            if return_order.state != 'draft':
                raise ValidationError("Only draft returns can be approved")
            
            return_order.approved_by = self.env.user.id
            return_order.approval_date = datetime.now()
            return_order.requires_approval = False