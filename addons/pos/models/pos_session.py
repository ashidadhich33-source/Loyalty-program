# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - POS Session
===============================

POS session management for kids clothing retail.
"""

from core_framework.orm import BaseModel, CharField, TextField, BooleanField, IntegerField, DateTimeField, Many2OneField, SelectionField, FloatField, One2ManyField, Many2ManyField
from core_framework.orm import Field
from typing import Dict, Any, Optional
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class PosSession(BaseModel):
    """POS session for tracking sales and cash management"""
    
    _name = 'pos.session'
    _description = 'POS Session'
    _table = 'pos_session'
    
    # Basic Information
    name = CharField(
        string='Session Name',
        size=100,
        required=True,
        help='Name of the POS session'
    )
    
    config_id = Many2OneField(
        'pos.config',
        string='POS Configuration',
        required=True,
        help='POS configuration for this session'
    )
    
    user_id = Many2OneField(
        'res.users',
        string='Cashier',
        required=True,
        help='Cashier for this session'
    )
    
    # Session State
    state = SelectionField(
        string='State',
        selection=[
            ('opened', 'Opened'),
            ('closing_control', 'Closing Control'),
            ('closed', 'Closed')
        ],
        default='opened',
        help='Current state of the session'
    )
    
    # Session Timing
    start_at = DateTimeField(
        string='Start At',
        required=True,
        help='Session start time'
    )
    
    stop_at = DateTimeField(
        string='Stop At',
        help='Session end time'
    )
    
    # Cash Management
    start_cash = FloatField(
        string='Start Cash',
        digits=(12, 2),
        default=0.0,
        help='Starting cash amount'
    )
    
    end_cash = FloatField(
        string='End Cash',
        digits=(12, 2),
        help='Ending cash amount'
    )
    
    cash_difference = FloatField(
        string='Cash Difference',
        digits=(12, 2),
        help='Difference between expected and actual cash'
    )
    
    # Sales Summary
    order_count = IntegerField(
        string='Order Count',
        default=0,
        help='Number of orders in this session'
    )
    
    total_sales = FloatField(
        string='Total Sales',
        digits=(12, 2),
        default=0.0,
        help='Total sales amount'
    )
    
    total_discount = FloatField(
        string='Total Discount',
        digits=(12, 2),
        default=0.0,
        help='Total discount given'
    )
    
    total_tax = FloatField(
        string='Total Tax',
        digits=(12, 2),
        default=0.0,
        help='Total tax collected'
    )
    
    # Payment Summary
    payment_ids = One2ManyField(
        string='Payments',
        comodel_name='pos.payment',
        inverse_name='session_id',
        help='All payments in this session'
    )
    
    order_ids = One2ManyField(
        string='Orders',
        comodel_name='pos.order',
        inverse_name='session_id',
        help='All orders in this session'
    )
    
    # Session Notes
    notes = TextField(
        string='Notes',
        help='Session notes and comments'
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
            vals['name'] = f"Session {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        
        return super().create(vals)
    
    def write(self, vals):
        """Override write to update session data"""
        result = super().write(vals)
        
        # Update session statistics
        if 'state' in vals and vals['state'] == 'closed':
            self._update_session_statistics()
        
        return result
    
    def _update_session_statistics(self):
        """Update session statistics when closing"""
        for session in self:
            # Count orders
            session.order_count = len(session.order_ids)
            
            # Calculate totals
            session.total_sales = sum(session.order_ids.mapped('amount_total'))
            session.total_discount = sum(session.order_ids.mapped('amount_discount'))
            session.total_tax = sum(session.order_ids.mapped('amount_tax'))
            
            # Calculate cash difference
            if session.end_cash is not None:
                expected_cash = session.start_cash + sum([
                    payment.amount for payment in session.payment_ids 
                    if payment.payment_method_id.is_cash
                ])
                session.cash_difference = session.end_cash - expected_cash
    
    def action_close(self):
        """Close the POS session"""
        if self.state != 'opened':
            raise ValueError("Only opened sessions can be closed")
        
        # Update session statistics
        self._update_session_statistics()
        
        # Set end time
        self.stop_at = datetime.now()
        self.state = 'closed'
        
        # Update POS config
        if self.config_id.current_session_id == self:
            self.config_id.current_session_id = False
        
        return True
    
    def action_open_cashbox(self):
        """Open cash box for cash management"""
        return {
            'type': 'ir.actions.act_window',
            'name': 'Cash Management',
            'res_model': 'pos.cashbox.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_session_id': self.id}
        }
    
    def action_view_orders(self):
        """View all orders in this session"""
        return {
            'type': 'ir.actions.act_window',
            'name': f'Orders - {self.name}',
            'res_model': 'pos.order',
            'view_mode': 'tree,form',
            'domain': [('session_id', '=', self.id)],
            'context': {'default_session_id': self.id}
        }
    
    def action_view_payments(self):
        """View all payments in this session"""
        return {
            'type': 'ir.actions.act_window',
            'name': f'Payments - {self.name}',
            'res_model': 'pos.payment',
            'view_mode': 'tree,form',
            'domain': [('session_id', '=', self.id)],
            'context': {'default_session_id': self.id}
        }
    
    def get_session_summary(self):
        """Get session summary data"""
        return {
            'session_name': self.name,
            'cashier': self.user_id.name,
            'start_time': self.start_at,
            'end_time': self.stop_at,
            'duration': self._get_session_duration(),
            'order_count': self.order_count,
            'total_sales': self.total_sales,
            'total_discount': self.total_discount,
            'total_tax': self.total_tax,
            'cash_difference': self.cash_difference,
            'payment_summary': self._get_payment_summary()
        }
    
    def _get_session_duration(self):
        """Calculate session duration"""
        if not self.start_at:
            return "N/A"
        
        end_time = self.stop_at or datetime.now()
        duration = end_time - self.start_at
        
        hours = duration.total_seconds() // 3600
        minutes = (duration.total_seconds() % 3600) // 60
        
        return f"{int(hours)}h {int(minutes)}m"
    
    def _get_payment_summary(self):
        """Get payment method summary"""
        payment_summary = {}
        
        for payment in self.payment_ids:
            method_name = payment.payment_method_id.name
            if method_name not in payment_summary:
                payment_summary[method_name] = 0
            payment_summary[method_name] += payment.amount
        
        return payment_summary
    
    def validate_session(self):
        """Validate session data"""
        errors = []
        
        # Check required fields
        if not self.config_id:
            errors.append("POS configuration is required")
        
        if not self.user_id:
            errors.append("Cashier is required")
        
        if not self.start_at:
            errors.append("Start time is required")
        
        # Check cash management
        if self.state == 'closed' and self.end_cash is None:
            errors.append("End cash amount is required when closing session")
        
        if errors:
            raise ValueError('\n'.join(errors))
        
        return True