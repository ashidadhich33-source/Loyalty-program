# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - POS Exchange
================================

POS exchange management for kids clothing retail.
"""

from core_framework.orm import BaseModel, CharField, TextField, BooleanField, IntegerField, DateTimeField, Many2OneField, SelectionField, FloatField, One2ManyField, Many2ManyField
from core_framework.orm import Field
from typing import Dict, Any, Optional
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class PosExchange(BaseModel):
    """POS exchange for product exchanges"""
    
    _name = 'pos.exchange'
    _description = 'POS Exchange'
    _table = 'pos_exchange'
    
    # Basic Information
    name = CharField(
        string='Exchange Reference',
        size=100,
        required=True,
        help='Exchange reference number'
    )
    
    session_id = Many2OneField(
        'pos.session',
        string='Session',
        required=True,
        help='POS session for this exchange'
    )
    
    config_id = Many2OneField(
        'pos.config',
        string='POS Configuration',
        related='session_id.config_id',
        store=True,
        help='POS configuration'
    )
    
    user_id = Many2OneField(
        'res.users',
        string='Cashier',
        required=True,
        help='Cashier who processed this exchange'
    )
    
    # Customer Information
    partner_id = Many2OneField(
        'res.partner',
        string='Customer',
        required=True,
        help='Customer for this exchange'
    )
    
    # Original Order Information
    original_order_id = Many2OneField(
        'pos.order',
        string='Original Order',
        required=True,
        help='Original order being exchanged'
    )
    
    # Exchange State
    state = SelectionField(
        string='State',
        selection=[
            ('draft', 'Draft'),
            ('confirmed', 'Confirmed'),
            ('done', 'Done'),
            ('cancel', 'Cancelled')
        ],
        default='draft',
        help='Current state of the exchange'
    )
    
    # Exchange Timing
    exchange_date = DateTimeField(
        string='Exchange Date',
        required=True,
        help='Date and time of the exchange'
    )
    
    # Exchange Lines
    exchange_lines = One2ManyField(
        string='Exchange Lines',
        comodel_name='pos.exchange.line',
        inverse_name='exchange_id',
        help='Exchange line items'
    )
    
    # Exchange Reason
    exchange_reason_id = Many2OneField(
        'pos.exchange.reason',
        string='Exchange Reason',
        help='Reason for the exchange'
    )
    
    reason_note = TextField(
        string='Reason Note',
        help='Additional notes about the exchange reason'
    )
    
    # Amounts
    amount_returned = FloatField(
        string='Amount Returned',
        digits=(12, 2),
        default=0.0,
        help='Amount returned to customer'
    )
    
    amount_charged = FloatField(
        string='Amount Charged',
        digits=(12, 2),
        default=0.0,
        help='Additional amount charged to customer'
    )
    
    amount_difference = FloatField(
        string='Amount Difference',
        digits=(12, 2),
        default=0.0,
        help='Net difference amount'
    )
    
    # Exchange Type
    exchange_type = SelectionField(
        string='Exchange Type',
        selection=[
            ('size_change', 'Size Change'),
            ('color_change', 'Color Change'),
            ('style_change', 'Style Change'),
            ('defective', 'Defective Product'),
            ('wrong_item', 'Wrong Item'),
            ('customer_preference', 'Customer Preference'),
            ('other', 'Other')
        ],
        default='size_change',
        help='Type of exchange'
    )
    
    # Age-based Information
    customer_age = IntegerField(
        string='Customer Age',
        help='Age of the customer (for age-based policies)'
    )
    
    # Exchange Policy
    within_exchange_period = BooleanField(
        string='Within Exchange Period',
        default=True,
        help='Whether exchange is within allowed period'
    )
    
    exchange_period_days = IntegerField(
        string='Exchange Period (Days)',
        default=7,
        help='Number of days allowed for exchange'
    )
    
    # Receipt Information
    exchange_receipt_number = CharField(
        string='Exchange Receipt Number',
        size=50,
        help='Exchange receipt number'
    )
    
    print_exchange_receipt = BooleanField(
        string='Print Exchange Receipt',
        default=True,
        help='Whether to print exchange receipt'
    )
    
    # Notes
    note = TextField(
        string='Notes',
        help='Exchange notes and comments'
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
            vals['name'] = self._generate_exchange_name()
        
        if 'exchange_date' not in vals:
            vals['exchange_date'] = datetime.now()
        
        if 'user_id' not in vals:
            vals['user_id'] = self.env.user.id
        
        return super().create(vals)
    
    def write(self, vals):
        """Override write to update amounts"""
        result = super().write(vals)
        
        # Update amounts when lines change
        if 'exchange_lines' in vals:
            self._update_amounts()
        
        return result
    
    def _generate_exchange_name(self):
        """Generate unique exchange name"""
        return f"EXC-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    def _update_amounts(self):
        """Update exchange amounts based on lines"""
        for exchange in self:
            # Calculate amounts from lines
            amount_returned = sum(line.return_amount for line in exchange.exchange_lines)
            amount_charged = sum(line.charge_amount for line in exchange.exchange_lines)
            
            # Update amounts
            exchange.amount_returned = amount_returned
            exchange.amount_charged = amount_charged
            exchange.amount_difference = amount_charged - amount_returned
    
    def action_confirm(self):
        """Confirm the exchange"""
        if self.state != 'draft':
            raise ValueError("Only draft exchanges can be confirmed")
        
        # Validate exchange
        self._validate_exchange()
        
        # Update state
        self.state = 'confirmed'
        
        # Generate exchange receipt number
        if not self.exchange_receipt_number:
            self.exchange_receipt_number = self._generate_exchange_receipt_number()
        
        return True
    
    def action_done(self):
        """Mark exchange as done"""
        if self.state not in ['confirmed', 'draft']:
            raise ValueError("Exchange must be confirmed or draft to mark as done")
        
        self.state = 'done'
        
        # Update inventory
        self._update_inventory()
        
        return True
    
    def action_cancel(self):
        """Cancel the exchange"""
        if self.state == 'done':
            raise ValueError("Cannot cancel completed exchanges")
        
        self.state = 'cancel'
        return True
    
    def _validate_exchange(self):
        """Validate exchange before confirmation"""
        errors = []
        
        # Check if exchange has lines
        if not self.exchange_lines:
            errors.append("Exchange must have at least one line")
        
        # Check exchange period
        if not self.within_exchange_period:
            errors.append("Exchange is outside the allowed period")
        
        # Check customer age for age-based policies
        if self.customer_age and self.customer_age < 3:
            # Special policy for toddlers
            if self.exchange_period_days > 14:
                errors.append("Exchange period exceeds limit for toddler items")
        
        if errors:
            raise ValueError('\n'.join(errors))
    
    def _generate_exchange_receipt_number(self):
        """Generate exchange receipt number"""
        return f"EXC-RCP-{self.id:06d}"
    
    def _update_inventory(self):
        """Update inventory for exchanged products"""
        # This would integrate with inventory addon
        for line in self.exchange_lines:
            # Return original product to stock
            # Remove new product from stock
            pass
    
    def action_view_lines(self):
        """View exchange lines"""
        return {
            'type': 'ir.actions.act_window',
            'name': f'Exchange Lines - {self.name}',
            'res_model': 'pos.exchange.line',
            'view_mode': 'tree,form',
            'domain': [('exchange_id', '=', self.id)],
            'context': {'default_exchange_id': self.id}
        }
    
    def action_view_original_order(self):
        """View original order"""
        return {
            'type': 'ir.actions.act_window',
            'name': f'Original Order - {self.original_order_id.name}',
            'res_model': 'pos.order',
            'res_id': self.original_order_id.id,
            'view_mode': 'form',
            'target': 'new'
        }
    
    def action_print_exchange_receipt(self):
        """Print exchange receipt"""
        return {
            'type': 'ir.actions.report',
            'report_name': 'pos_exchange.report_exchange_receipt',
            'report_type': 'qweb-pdf',
            'data': {'ids': [self.id]},
            'target': 'new'
        }
    
    def get_exchange_summary(self):
        """Get exchange summary data"""
        return {
            'exchange_name': self.name,
            'customer': self.partner_id.name,
            'cashier': self.user_id.name,
            'exchange_date': self.exchange_date,
            'state': self.state,
            'exchange_type': self.exchange_type,
            'line_count': len(self.exchange_lines),
            'amount_returned': self.amount_returned,
            'amount_charged': self.amount_charged,
            'amount_difference': self.amount_difference,
            'original_order': self.original_order_id.name,
            'exchange_reason': self.exchange_reason_id.name if self.exchange_reason_id else 'Not specified'
        }