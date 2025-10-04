# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - POS Exchange Wizard
======================================

Exchange processing wizard for POS sessions.
"""

from core_framework.orm import BaseModel, CharField, TextField, BooleanField, IntegerField, DateTimeField, Many2OneField, SelectionField, FloatField, One2ManyField, Many2ManyField
from core_framework.orm import Field
from typing import Dict, Any, Optional
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class PosExchangeWizard(BaseModel):
    """Exchange processing wizard"""
    
    _name = 'pos.exchange.wizard'
    _description = 'POS Exchange Wizard'
    _table = 'pos_exchange_wizard'
    
    # Basic Information
    session_id = Many2OneField(
        'pos.session',
        string='Session',
        required=True,
        help='POS session for this exchange'
    )
    
    partner_id = Many2OneField(
        'res.partner',
        string='Customer',
        required=True,
        help='Customer for this exchange'
    )
    
    original_order_id = Many2OneField(
        'pos.order',
        string='Original Order',
        required=True,
        help='Original order being exchanged'
    )
    
    # Exchange Information
    exchange_reason_id = Many2OneField(
        'pos.exchange.reason',
        string='Exchange Reason',
        required=True,
        help='Reason for the exchange'
    )
    
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
        required=True,
        help='Type of exchange'
    )
    
    # Customer Information
    customer_age = IntegerField(
        string='Customer Age',
        help='Age of the customer'
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
    
    # Notes
    reason_note = TextField(
        string='Reason Note',
        help='Additional notes about the exchange reason'
    )
    
    note = TextField(
        string='Notes',
        help='Exchange notes and comments'
    )
    
    # Timestamps
    create_date = DateTimeField(
        string='Created On',
        auto_now_add=True
    )
    
    def action_process_exchange(self):
        """Process the exchange"""
        for wizard in self:
            # Validate wizard data
            wizard._validate_wizard()
            
            # Create exchange
            exchange = wizard._create_exchange()
            
            # Confirm exchange
            exchange.action_confirm()
            exchange.action_done()
        
        return {
            'type': 'ir.actions.act_window',
            'name': 'Exchange Processed',
            'res_model': 'pos.exchange',
            'res_id': exchange.id,
            'view_mode': 'form',
            'target': 'new'
        }
    
    def _validate_wizard(self):
        """Validate wizard data"""
        errors = []
        
        # Check required fields
        if not self.partner_id:
            errors.append("Customer is required")
        
        if not self.original_order_id:
            errors.append("Original order is required")
        
        if not self.exchange_reason_id:
            errors.append("Exchange reason is required")
        
        if not self.exchange_type:
            errors.append("Exchange type is required")
        
        # Check exchange period
        if not self.within_exchange_period:
            errors.append("Exchange is outside the allowed period")
        
        # Check age-based policies
        if self.customer_age and self.exchange_reason_id:
            if not self.exchange_reason_id.validate_age_group(self.customer_age):
                errors.append(f"Exchange reason '{self.exchange_reason_id.name}' does not apply to customer age {self.customer_age}")
        
        # Check exchange type validation
        if self.exchange_reason_id and self.exchange_type:
            if not self.exchange_reason_id.validate_exchange_type(self.exchange_type):
                errors.append(f"Exchange reason '{self.exchange_reason_id.name}' does not allow '{self.exchange_type}' exchanges")
        
        if errors:
            raise ValueError('\n'.join(errors))
    
    def _create_exchange(self):
        """Create exchange from wizard data"""
        # Create exchange
        exchange_vals = {
            'session_id': self.session_id.id,
            'partner_id': self.partner_id.id,
            'original_order_id': self.original_order_id.id,
            'exchange_reason_id': self.exchange_reason_id.id,
            'exchange_type': self.exchange_type,
            'customer_age': self.customer_age,
            'within_exchange_period': self.within_exchange_period,
            'exchange_period_days': self.exchange_period_days,
            'reason_note': self.reason_note,
            'note': self.note,
            'state': 'draft',
            'exchange_date': datetime.now()
        }
        
        exchange = self.env['pos.exchange'].create(exchange_vals)
        
        return exchange
    
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
    
    def action_view_customer(self):
        """View customer details"""
        return {
            'type': 'ir.actions.act_window',
            'name': f'Customer - {self.partner_id.name}',
            'res_model': 'res.partner',
            'res_id': self.partner_id.id,
            'view_mode': 'form',
            'target': 'new'
        }
    
    def get_wizard_summary(self):
        """Get wizard summary data"""
        return {
            'customer': self.partner_id.name,
            'original_order': self.original_order_id.name,
            'exchange_reason': self.exchange_reason_id.name if self.exchange_reason_id else 'Not specified',
            'exchange_type': self.exchange_type,
            'customer_age': self.customer_age,
            'within_exchange_period': self.within_exchange_period,
            'exchange_period_days': self.exchange_period_days,
            'session': self.session_id.name
        }