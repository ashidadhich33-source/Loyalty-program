#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - POS Configuration Model
===========================================

POS configuration management for kids clothing retail.
"""

import logging
from core_framework.orm import BaseModel, CharField, TextField, BooleanField, IntegerField, DateTimeField, Many2OneField, SelectionField, FloatField, One2ManyField, Many2ManyField
from core_framework.exceptions import ValidationError

logger = logging.getLogger(__name__)

class PosConfig(BaseModel):
    """POS configuration for different locations"""
    
    _name = 'pos.config'
    _description = 'POS Configuration'
    _table = 'pos_config'
    _order = 'name'
    
    # Basic Information
    name = CharField(
        string='Configuration Name',
        size=100,
        required=True,
        help='Name of the POS configuration'
    )
    
    code = CharField(
        string='Configuration Code',
        size=20,
        required=True,
        help='Unique code for the POS configuration'
    )
    
    description = TextField(
        string='Description',
        help='Description of the POS configuration'
    )
    
    # Location Information
    company_id = Many2OneField(
        'res.company',
        string='Company',
        required=True,
        help='Company for this POS configuration'
    )
    
    warehouse_id = Many2OneField(
        'stock.warehouse',
        string='Warehouse',
        help='Default warehouse for this POS'
    )
    
    # POS Settings
    is_active = BooleanField(
        string='Active',
        default=True,
        help='Whether this POS configuration is active'
    )
    
    auto_close_session = BooleanField(
        string='Auto Close Session',
        default=True,
        help='Automatically close session after inactivity'
    )
    
    session_timeout = IntegerField(
        string='Session Timeout (minutes)',
        default=30,
        help='Session timeout in minutes'
    )
    
    # Product Settings
    allow_price_change = BooleanField(
        string='Allow Price Change',
        default=False,
        help='Allow cashier to change product prices'
    )
    
    allow_discount = BooleanField(
        string='Allow Discount',
        default=True,
        help='Allow cashier to apply discounts'
    )
    
    max_discount_percentage = FloatField(
        string='Max Discount %',
        digits=(5, 2),
        default=20.0,
        help='Maximum discount percentage allowed'
    )
    
    # Payment Settings
    payment_method_ids = Many2ManyField(
        'pos.payment.method',
        string='Payment Methods',
        help='Available payment methods for this POS'
    )
    
    default_payment_method_id = Many2OneField(
        'pos.payment.method',
        string='Default Payment Method',
        help='Default payment method'
    )
    
    # Receipt Settings
    receipt_header = TextField(
        string='Receipt Header',
        help='Header text for receipts'
    )
    
    receipt_footer = TextField(
        string='Receipt Footer',
        help='Footer text for receipts'
    )
    
    print_receipt = BooleanField(
        string='Print Receipt',
        default=True,
        help='Automatically print receipt after sale'
    )
    
    # Loyalty Settings
    enable_loyalty = BooleanField(
        string='Enable Loyalty',
        default=True,
        help='Enable loyalty points for this POS'
    )
    
    loyalty_points_per_rupee = FloatField(
        string='Points per Rupee',
        digits=(5, 2),
        default=1.0,
        help='Loyalty points earned per rupee spent'
    )
    
    # Age-based Settings
    enable_age_discount = BooleanField(
        string='Enable Age Discount',
        default=True,
        help='Enable age-based discounts'
    )
    
    age_discount_percentage = FloatField(
        string='Age Discount %',
        digits=(5, 2),
        default=10.0,
        help='Default age-based discount percentage'
    )
    
    # Session Management
    current_session_id = Many2OneField(
        'pos.session',
        string='Current Session',
        help='Currently active session'
    )
    
    session_ids = One2ManyField(
        string='Sessions',
        comodel_name='pos.session',
        inverse_name='config_id',
        help='All sessions for this POS'
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
        
        return super().create(vals)
    
    def write(self, vals):
        """Override write to validate settings"""
        result = super().write(vals)
        
        # Validate discount settings
        if 'max_discount_percentage' in vals:
            if vals['max_discount_percentage'] < 0 or vals['max_discount_percentage'] > 100:
                raise ValidationError("Discount percentage must be between 0 and 100")
        
        return result
    
    def action_start_session(self):
        """Start a new POS session"""
        # Check if there's already an active session
        if self.current_session_id and self.current_session_id.state == 'opened':
            raise ValidationError("There is already an active session for this POS")
        
        # Create new session
        session_vals = {
            'config_id': self.id,
            'user_id': self.env.user.id,
            'state': 'opened',
            'start_at': self.env['datetime'].now()
        }
        
        session = self.env['pos.session'].create(session_vals)
        self.current_session_id = session.id
        
        return {
            'type': 'ocean.actions.act_window',
            'name': f'POS Session - {self.name}',
            'res_model': 'pos.session',
            'res_id': session.id,
            'view_mode': 'form',
            'target': 'current'
        }
    
    def action_close_session(self):
        """Close the current POS session"""
        if not self.current_session_id:
            raise ValidationError("No active session to close")
        
        if self.current_session_id.state != 'opened':
            raise ValidationError("Session is not in opened state")
        
        self.current_session_id.action_close()
        self.current_session_id = False
        
        return True
    
    def get_pos_dashboard_data(self):
        """Get dashboard data for this POS"""
        today = self.env['datetime'].today()
        
        # Get today's sales
        today_sales = self.env['pos.order'].search_count([
            ('session_id.config_id', '=', self.id),
            ('date_order', '>=', today),
            ('state', '=', 'done')
        ])
        
        # Get today's revenue
        today_revenue = sum(self.env['pos.order'].search([
            ('session_id.config_id', '=', self.id),
            ('date_order', '>=', today),
            ('state', '=', 'done')
        ]).mapped('amount_total'))
        
        # Get active session info
        active_session = self.current_session_id
        session_info = {
            'has_active_session': bool(active_session),
            'session_id': active_session.id if active_session else False,
            'session_user': active_session.user_id.name if active_session else False,
            'session_start': active_session.start_at if active_session else False
        }
        
        return {
            'today_sales': today_sales,
            'today_revenue': today_revenue,
            'session_info': session_info
        }
    
    def validate_pos_config(self):
        """Validate POS configuration"""
        errors = []
        
        # Check required fields
        if not self.payment_method_ids:
            errors.append("At least one payment method must be configured")
        
        if self.enable_loyalty and self.loyalty_points_per_rupee <= 0:
            errors.append("Loyalty points per rupee must be greater than 0")
        
        if self.max_discount_percentage < 0 or self.max_discount_percentage > 100:
            errors.append("Maximum discount percentage must be between 0 and 100")
        
        if errors:
            raise ValidationError('\n'.join(errors))
        
        return True