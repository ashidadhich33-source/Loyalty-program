#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - POS Session Model
====================================

POS session management for tracking sales sessions.
"""

import logging
from datetime import datetime, timedelta
from core_framework.orm import BaseModel, CharField, TextField, BooleanField, IntegerField, DateTimeField, Many2OneField, SelectionField, FloatField, One2ManyField, Many2ManyField
from core_framework.exceptions import ValidationError

logger = logging.getLogger(__name__)

class PosSession(BaseModel):
    """POS session for tracking sales sessions"""
    
    _name = 'pos.session'
    _description = 'POS Session'
    _table = 'pos_session'
    _order = 'create_date desc'
    
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
    
    # Session Status
    state = SelectionField(
        string='Status',
        selection=[
            ('opening_control', 'Opening Control'),
            ('opened', 'Opened'),
            ('closing_control', 'Closing Control'),
            ('closed', 'Closed')
        ],
        default='opening_control',
        help='Current status of the session'
    )
    
    # Session Timing
    start_at = DateTimeField(
        string='Start Time',
        help='Session start time'
    )
    
    stop_at = DateTimeField(
        string='Stop Time',
        help='Session stop time'
    )
    
    duration = IntegerField(
        string='Duration (minutes)',
        help='Session duration in minutes'
    )
    
    # Cash Management
    opening_cash = FloatField(
        string='Opening Cash',
        digits=(12, 2),
        default=0.0,
        help='Cash at session start'
    )
    
    closing_cash = FloatField(
        string='Closing Cash',
        digits=(12, 2),
        help='Cash at session end'
    )
    
    expected_cash = FloatField(
        string='Expected Cash',
        digits=(12, 2),
        help='Expected cash based on sales'
    )
    
    cash_difference = FloatField(
        string='Cash Difference',
        digits=(12, 2),
        help='Difference between expected and actual cash'
    )
    
    # Sales Summary
    total_sales = FloatField(
        string='Total Sales',
        digits=(12, 2),
        default=0.0,
        help='Total sales amount'
    )
    
    total_orders = IntegerField(
        string='Total Orders',
        default=0,
        help='Total number of orders'
    )
    
    total_items = IntegerField(
        string='Total Items',
        default=0,
        help='Total number of items sold'
    )
    
    # Payment Summary
    cash_payments = FloatField(
        string='Cash Payments',
        digits=(12, 2),
        default=0.0,
        help='Total cash payments'
    )
    
    card_payments = FloatField(
        string='Card Payments',
        digits=(12, 2),
        default=0.0,
        help='Total card payments'
    )
    
    upi_payments = FloatField(
        string='UPI Payments',
        digits=(12, 2),
        default=0.0,
        help='Total UPI payments'
    )
    
    wallet_payments = FloatField(
        string='Wallet Payments',
        digits=(12, 2),
        default=0.0,
        help='Total wallet payments'
    )
    
    # Customer Summary
    total_customers = IntegerField(
        string='Total Customers',
        default=0,
        help='Total number of customers served'
    )
    
    new_customers = IntegerField(
        string='New Customers',
        default=0,
        help='Number of new customers'
    )
    
    returning_customers = IntegerField(
        string='Returning Customers',
        default=0,
        help='Number of returning customers'
    )
    
    # Loyalty Summary
    loyalty_points_earned = IntegerField(
        string='Loyalty Points Earned',
        default=0,
        help='Total loyalty points earned'
    )
    
    loyalty_points_redeemed = IntegerField(
        string='Loyalty Points Redeemed',
        default=0,
        help='Total loyalty points redeemed'
    )
    
    # Discount Summary
    total_discounts = FloatField(
        string='Total Discounts',
        digits=(12, 2),
        default=0.0,
        help='Total discount amount given'
    )
    
    discount_percentage = FloatField(
        string='Discount %',
        digits=(5, 2),
        default=0.0,
        help='Average discount percentage'
    )
    
    # Returns and Exchanges
    total_returns = FloatField(
        string='Total Returns',
        digits=(12, 2),
        default=0.0,
        help='Total return amount'
    )
    
    total_exchanges = FloatField(
        string='Total Exchanges',
        digits=(12, 2),
        default=0.0,
        help='Total exchange amount'
    )
    
    # Session Notes
    opening_notes = TextField(
        string='Opening Notes',
        help='Notes at session opening'
    )
    
    closing_notes = TextField(
        string='Closing Notes',
        help='Notes at session closing'
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
        """Override write to update calculations"""
        result = super().write(vals)
        
        # Update calculations if state changed
        if 'state' in vals:
            for record in self:
                record._update_session_calculations()
        
        return result
    
    def _update_session_calculations(self):
        """Update session calculations"""
        for record in self:
            if record.state == 'opened':
                record.start_at = datetime.now()
            elif record.state == 'closed':
                record.stop_at = datetime.now()
                if record.start_at:
                    duration = record.stop_at - record.start_at
                    record.duration = int(duration.total_seconds() / 60)
                
                # Calculate cash difference
                if record.expected_cash and record.closing_cash:
                    record.cash_difference = record.closing_cash - record.expected_cash
    
    def action_open_session(self):
        """Open POS session"""
        for record in self:
            if record.state == 'opening_control':
                record.state = 'opened'
                record.start_at = datetime.now()
    
    def action_close_session(self):
        """Close POS session"""
        for record in self:
            if record.state == 'opened':
                record.state = 'closing_control'
                record._calculate_session_summary()
    
    def action_validate_session(self):
        """Validate and close session"""
        for record in self:
            if record.state == 'closing_control':
                record.state = 'closed'
                record.stop_at = datetime.now()
                record._update_session_calculations()
    
    def _calculate_session_summary(self):
        """Calculate session summary"""
        for record in self:
            # Get orders for this session
            orders = self.env['pos.order'].search([
                ('session_id', '=', record.id)
            ])
            
            # Calculate totals
            record.total_orders = len(orders)
            record.total_sales = sum(order.amount_total for order in orders)
            record.total_items = sum(order.total_items for order in orders)
            
            # Calculate payment totals
            record.cash_payments = sum(order.cash_amount for order in orders)
            record.card_payments = sum(order.card_amount for order in orders)
            record.upi_payments = sum(order.upi_amount for order in orders)
            record.wallet_payments = sum(order.wallet_amount for order in orders)
            
            # Calculate customer totals
            customers = set(order.partner_id.id for order in orders if order.partner_id)
            record.total_customers = len(customers)
            
            # Calculate loyalty points
            record.loyalty_points_earned = sum(order.loyalty_points_earned for order in orders)
            record.loyalty_points_redeemed = sum(order.loyalty_points_redeemed for order in orders)
            
            # Calculate discounts
            record.total_discounts = sum(order.discount_amount for order in orders)
            if record.total_sales > 0:
                record.discount_percentage = (record.total_discounts / record.total_sales) * 100
            
            # Calculate expected cash
            record.expected_cash = record.opening_cash + record.cash_payments
    
    def get_session_summary(self):
        """Get session summary for reporting"""
        return {
            'session_info': {
                'name': self.name,
                'cashier': self.user_id.name,
                'start_time': self.start_at,
                'stop_time': self.stop_at,
                'duration': self.duration,
                'status': self.state
            },
            'sales_summary': {
                'total_sales': self.total_sales,
                'total_orders': self.total_orders,
                'total_items': self.total_items,
                'average_order_value': self.total_sales / max(self.total_orders, 1)
            },
            'payment_summary': {
                'cash': self.cash_payments,
                'card': self.card_payments,
                'upi': self.upi_payments,
                'wallet': self.wallet_payments,
                'total': self.total_sales
            },
            'customer_summary': {
                'total_customers': self.total_customers,
                'new_customers': self.new_customers,
                'returning_customers': self.returning_customers
            },
            'loyalty_summary': {
                'points_earned': self.loyalty_points_earned,
                'points_redeemed': self.loyalty_points_redeemed,
                'net_points': self.loyalty_points_earned - self.loyalty_points_redeemed
            },
            'discount_summary': {
                'total_discounts': self.total_discounts,
                'discount_percentage': self.discount_percentage
            },
            'cash_summary': {
                'opening_cash': self.opening_cash,
                'closing_cash': self.closing_cash,
                'expected_cash': self.expected_cash,
                'cash_difference': self.cash_difference
            }
        }
    
    def action_view_orders(self):
        """Action to view session orders"""
        return {
            'type': 'ocean.actions.act_window',
            'name': f'Session Orders - {self.name}',
            'res_model': 'pos.order',
            'view_mode': 'tree,form',
            'domain': [('session_id', '=', self.id)],
            'context': {'default_session_id': self.id}
        }
    
    def action_generate_report(self):
        """Action to generate session report"""
        return {
            'type': 'ocean.actions.act_window',
            'name': f'Session Report - {self.name}',
            'res_model': 'pos.analytics',
            'view_mode': 'form',
            'domain': [('session_id', '=', self.id)],
            'context': {'default_session_id': self.id}
        }