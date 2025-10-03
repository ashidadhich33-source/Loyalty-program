#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - POS Configuration Model
==========================================

POS configuration management for different locations.
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
        help='Short code for the configuration'
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
    
    location_id = Many2OneField(
        'res.partner',
        string='Location',
        help='Physical location of the POS'
    )
    
    warehouse_id = Many2OneField(
        'stock.warehouse',
        string='Warehouse',
        help='Warehouse for inventory management'
    )
    
    # POS Settings
    is_active = BooleanField(
        string='Active',
        default=True,
        help='Whether this configuration is active'
    )
    
    is_default = BooleanField(
        string='Default Configuration',
        default=False,
        help='Whether this is the default POS configuration'
    )
    
    # UI Settings
    theme = SelectionField(
        string='Theme',
        selection=[
            ('light', 'Light Theme'),
            ('dark', 'Dark Theme'),
            ('kids', 'Kids Theme'),
            ('colorful', 'Colorful Theme')
        ],
        default='kids',
        help='POS interface theme'
    )
    
    touchscreen_mode = BooleanField(
        string='Touchscreen Mode',
        default=True,
        help='Enable touchscreen interface'
    )
    
    show_product_images = BooleanField(
        string='Show Product Images',
        default=True,
        help='Show product images in POS interface'
    )
    
    show_product_prices = BooleanField(
        string='Show Product Prices',
        default=True,
        help='Show product prices in POS interface'
    )
    
    # Payment Settings
    allow_cash_payment = BooleanField(
        string='Allow Cash Payment',
        default=True,
        help='Allow cash payments'
    )
    
    allow_card_payment = BooleanField(
        string='Allow Card Payment',
        default=True,
        help='Allow card payments'
    )
    
    allow_upi_payment = BooleanField(
        string='Allow UPI Payment',
        default=True,
        help='Allow UPI payments'
    )
    
    allow_wallet_payment = BooleanField(
        string='Allow Wallet Payment',
        default=True,
        help='Allow wallet payments (Paytm, PhonePe)'
    )
    
    # Receipt Settings
    print_receipt = BooleanField(
        string='Print Receipt',
        default=True,
        help='Automatically print receipts'
    )
    
    receipt_template = CharField(
        string='Receipt Template',
        size=100,
        default='standard',
        help='Receipt template to use'
    )
    
    receipt_footer = TextField(
        string='Receipt Footer',
        help='Footer text for receipts'
    )
    
    # Inventory Settings
    auto_validate_orders = BooleanField(
        string='Auto Validate Orders',
        default=True,
        help='Automatically validate orders'
    )
    
    auto_create_picking = BooleanField(
        string='Auto Create Picking',
        default=True,
        help='Automatically create stock pickings'
    )
    
    # Customer Settings
    require_customer = BooleanField(
        string='Require Customer',
        default=False,
        help='Require customer selection for orders'
    )
    
    allow_anonymous_orders = BooleanField(
        string='Allow Anonymous Orders',
        default=True,
        help='Allow orders without customer'
    )
    
    # Loyalty Settings
    enable_loyalty = BooleanField(
        string='Enable Loyalty Program',
        default=True,
        help='Enable loyalty points in POS'
    )
    
    loyalty_points_per_rupee = FloatField(
        string='Loyalty Points per Rupee',
        digits=(5, 2),
        default=1.0,
        help='Loyalty points earned per rupee spent'
    )
    
    # Discount Settings
    enable_discounts = BooleanField(
        string='Enable Discounts',
        default=True,
        help='Enable discount functionality'
    )
    
    max_discount_percentage = FloatField(
        string='Max Discount %',
        digits=(5, 2),
        default=50.0,
        help='Maximum discount percentage allowed'
    )
    
    # Tax Settings
    tax_calculation = SelectionField(
        string='Tax Calculation',
        selection=[
            ('inclusive', 'Tax Inclusive'),
            ('exclusive', 'Tax Exclusive')
        ],
        default='inclusive',
        help='Tax calculation method'
    )
    
    # Session Settings
    session_timeout = IntegerField(
        string='Session Timeout (minutes)',
        default=480,
        help='Session timeout in minutes'
    )
    
    auto_close_session = BooleanField(
        string='Auto Close Session',
        default=True,
        help='Automatically close sessions at end of day'
    )
    
    # Analytics Settings
    track_analytics = BooleanField(
        string='Track Analytics',
        default=True,
        help='Track POS analytics and metrics'
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
        
        # Validate configuration
        for record in self:
            record._validate_configuration()
        
        return result
    
    def _validate_configuration(self):
        """Validate POS configuration settings"""
        errors = []
        
        # Validate payment methods
        if not any([
            self.allow_cash_payment,
            self.allow_card_payment,
            self.allow_upi_payment,
            self.allow_wallet_payment
        ]):
            errors.append("At least one payment method must be enabled")
        
        # Validate discount settings
        if self.max_discount_percentage < 0 or self.max_discount_percentage > 100:
            errors.append("Maximum discount percentage must be between 0 and 100")
        
        # Validate loyalty settings
        if self.enable_loyalty and self.loyalty_points_per_rupee < 0:
            errors.append("Loyalty points per rupee must be positive")
        
        if errors:
            raise ValidationError('\n'.join(errors))
    
    def get_pos_settings(self):
        """Get POS settings for frontend"""
        return {
            'theme': self.theme,
            'touchscreen_mode': self.touchscreen_mode,
            'show_product_images': self.show_product_images,
            'show_product_prices': self.show_product_prices,
            'payment_methods': {
                'cash': self.allow_cash_payment,
                'card': self.allow_card_payment,
                'upi': self.allow_upi_payment,
                'wallet': self.allow_wallet_payment
            },
            'receipt_settings': {
                'print_receipt': self.print_receipt,
                'template': self.receipt_template,
                'footer': self.receipt_footer
            },
            'customer_settings': {
                'require_customer': self.require_customer,
                'allow_anonymous': self.allow_anonymous_orders
            },
            'loyalty_settings': {
                'enabled': self.enable_loyalty,
                'points_per_rupee': self.loyalty_points_per_rupee
            },
            'discount_settings': {
                'enabled': self.enable_discounts,
                'max_percentage': self.max_discount_percentage
            },
            'tax_settings': {
                'calculation': self.tax_calculation
            },
            'session_settings': {
                'timeout': self.session_timeout,
                'auto_close': self.auto_close_session
            }
        }
    
    def action_open_pos_interface(self):
        """Action to open POS interface"""
        return {
            'type': 'ocean.actions.act_url',
            'url': f'/pos/interface/{self.id}',
            'target': 'new'
        }
    
    def action_view_sessions(self):
        """Action to view POS sessions"""
        return {
            'type': 'ocean.actions.act_window',
            'name': f'POS Sessions - {self.name}',
            'res_model': 'pos.session',
            'view_mode': 'tree,form',
            'domain': [('config_id', '=', self.id)],
            'context': {'default_config_id': self.id}
        }
    
    def action_view_orders(self):
        """Action to view POS orders"""
        return {
            'type': 'ocean.actions.act_window',
            'name': f'POS Orders - {self.name}',
            'res_model': 'pos.order',
            'view_mode': 'tree,form',
            'domain': [('config_id', '=', self.id)],
            'context': {'default_config_id': self.id}
        }