# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - POS Payment Terminal
========================================

POS payment terminal management for kids clothing retail.
"""

from core_framework.orm import BaseModel, CharField, TextField, BooleanField, IntegerField, DateTimeField, Many2OneField, SelectionField, FloatField, One2ManyField, Many2ManyField
from core_framework.orm import Field
from typing import Dict, Any, Optional
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class PosPaymentTerminal(BaseModel):
    """POS payment terminal configuration"""
    
    _name = 'pos.payment.terminal'
    _description = 'POS Payment Terminal'
    _table = 'pos_payment_terminal'
    
    # Basic Information
    name = CharField(
        string='Terminal Name',
        size=100,
        required=True,
        help='Name of the payment terminal'
    )
    
    terminal_id = CharField(
        string='Terminal ID',
        size=50,
        required=True,
        help='Unique terminal identifier'
    )
    
    description = TextField(
        string='Description',
        help='Description of the payment terminal'
    )
    
    # Terminal Type
    terminal_type = SelectionField(
        string='Terminal Type',
        selection=[
            ('card_reader', 'Card Reader'),
            ('pos_machine', 'POS Machine'),
            ('mobile_pos', 'Mobile POS'),
            ('tablet_pos', 'Tablet POS'),
            ('desktop_pos', 'Desktop POS'),
            ('kiosk', 'Self-Service Kiosk'),
            ('other', 'Other')
        ],
        required=True,
        help='Type of payment terminal'
    )
    
    # Configuration
    is_active = BooleanField(
        string='Active',
        default=True,
        help='Whether this terminal is active'
    )
    
    is_online = BooleanField(
        string='Online',
        default=True,
        help='Whether this terminal is online'
    )
    
    # POS Configuration
    config_id = Many2OneField(
        'pos.config',
        string='POS Configuration',
        required=True,
        help='POS configuration for this terminal'
    )
    
    # Location Information
    location = CharField(
        string='Location',
        size=100,
        help='Physical location of the terminal'
    )
    
    store_id = Many2OneField(
        'res.company',
        string='Store',
        help='Store where this terminal is located'
    )
    
    # Hardware Information
    manufacturer = CharField(
        string='Manufacturer',
        size=100,
        help='Terminal manufacturer'
    )
    
    model = CharField(
        string='Model',
        size=100,
        help='Terminal model'
    )
    
    serial_number = CharField(
        string='Serial Number',
        size=100,
        help='Terminal serial number'
    )
    
    firmware_version = CharField(
        string='Firmware Version',
        size=50,
        help='Terminal firmware version'
    )
    
    # Network Configuration
    ip_address = CharField(
        string='IP Address',
        size=50,
        help='Terminal IP address'
    )
    
    mac_address = CharField(
        string='MAC Address',
        size=50,
        help='Terminal MAC address'
    )
    
    port = IntegerField(
        string='Port',
        default=8080,
        help='Terminal communication port'
    )
    
    # Payment Methods
    payment_method_ids = Many2ManyField(
        'pos.payment.method',
        string='Supported Payment Methods',
        help='Payment methods supported by this terminal'
    )
    
    # Terminal Status
    status = SelectionField(
        string='Status',
        selection=[
            ('active', 'Active'),
            ('inactive', 'Inactive'),
            ('maintenance', 'Maintenance'),
            ('error', 'Error'),
            ('offline', 'Offline')
        ],
        default='active',
        help='Current terminal status'
    )
    
    last_heartbeat = DateTimeField(
        string='Last Heartbeat',
        help='Last heartbeat received from terminal'
    )
    
    # Transaction Limits
    daily_transaction_limit = IntegerField(
        string='Daily Transaction Limit',
        default=0,
        help='Maximum number of transactions per day'
    )
    
    daily_amount_limit = FloatField(
        string='Daily Amount Limit',
        digits=(12, 2),
        default=0.0,
        help='Maximum transaction amount per day'
    )
    
    # Security Settings
    requires_pin = BooleanField(
        string='Requires PIN',
        default=True,
        help='Whether terminal requires PIN verification'
    )
    
    requires_signature = BooleanField(
        string='Requires Signature',
        default=False,
        help='Whether terminal requires signature'
    )
    
    encryption_enabled = BooleanField(
        string='Encryption Enabled',
        default=True,
        help='Whether terminal encryption is enabled'
    )
    
    # Maintenance
    last_maintenance = DateTimeField(
        string='Last Maintenance',
        help='Last maintenance date'
    )
    
    next_maintenance = DateTimeField(
        string='Next Maintenance',
        help='Next scheduled maintenance date'
    )
    
    maintenance_notes = TextField(
        string='Maintenance Notes',
        help='Maintenance notes and history'
    )
    
    # Usage Statistics
    total_transactions = IntegerField(
        string='Total Transactions',
        default=0,
        help='Total number of transactions processed'
    )
    
    total_amount = FloatField(
        string='Total Amount',
        digits=(12, 2),
        default=0.0,
        help='Total amount processed'
    )
    
    success_rate = FloatField(
        string='Success Rate',
        digits=(5, 2),
        default=100.0,
        help='Transaction success rate percentage'
    )
    
    average_transaction_time = FloatField(
        string='Average Transaction Time',
        digits=(8, 2),
        default=0.0,
        help='Average transaction processing time in seconds'
    )
    
    # Error Tracking
    error_count = IntegerField(
        string='Error Count',
        default=0,
        help='Number of errors encountered'
    )
    
    last_error = DateTimeField(
        string='Last Error',
        help='Last error occurrence'
    )
    
    error_message = TextField(
        string='Error Message',
        help='Last error message'
    )
    
    # Notes
    note = TextField(
        string='Notes',
        help='Additional notes about this terminal'
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
        if 'terminal_id' not in vals and 'name' in vals:
            vals['terminal_id'] = vals['name'].upper().replace(' ', '_')
        
        return super().create(vals)
    
    def write(self, vals):
        """Override write to update statistics"""
        result = super().write(vals)
        
        # Update last heartbeat if status changes
        if 'status' in vals:
            self.last_heartbeat = datetime.now()
        
        return result
    
    def action_test_connection(self):
        """Test terminal connection"""
        # This would test the terminal connection
        self.is_online = True
        self.last_heartbeat = datetime.now()
        return True
    
    def action_reset_terminal(self):
        """Reset terminal"""
        # This would reset the terminal
        self.status = 'active'
        self.is_online = True
        self.last_heartbeat = datetime.now()
        return True
    
    def action_view_transactions(self):
        """View transactions for this terminal"""
        return {
            'type': 'ir.actions.act_window',
            'name': f'Transactions - {self.name}',
            'res_model': 'pos.payment.transaction',
            'view_mode': 'tree,form',
            'domain': [('terminal_id', '=', self.id)],
            'context': {'default_terminal_id': self.id}
        }
    
    def action_schedule_maintenance(self):
        """Schedule maintenance for terminal"""
        # This would schedule maintenance
        return True
    
    def get_terminal_summary(self):
        """Get terminal summary data"""
        return {
            'terminal_name': self.name,
            'terminal_id': self.terminal_id,
            'terminal_type': self.terminal_type,
            'is_active': self.is_active,
            'is_online': self.is_online,
            'status': self.status,
            'location': self.location,
            'store': self.store_id.name if self.store_id else 'Not specified',
            'manufacturer': self.manufacturer,
            'model': self.model,
            'ip_address': self.ip_address,
            'total_transactions': self.total_transactions,
            'total_amount': self.total_amount,
            'success_rate': self.success_rate,
            'average_transaction_time': self.average_transaction_time,
            'error_count': self.error_count,
            'last_heartbeat': self.last_heartbeat,
            'last_maintenance': self.last_maintenance,
            'next_maintenance': self.next_maintenance
        }
    
    def validate_transaction(self, amount, payment_method):
        """Validate transaction for this terminal"""
        errors = []
        
        # Check if terminal is active
        if not self.is_active:
            errors.append("Terminal is not active")
        
        # Check if terminal is online
        if not self.is_online:
            errors.append("Terminal is offline")
        
        # Check daily transaction limit
        if self.daily_transaction_limit > 0:
            today_transactions = self._get_today_transaction_count()
            if today_transactions >= self.daily_transaction_limit:
                errors.append("Daily transaction limit reached")
        
        # Check daily amount limit
        if self.daily_amount_limit > 0:
            today_amount = self._get_today_transaction_amount()
            if today_amount + amount > self.daily_amount_limit:
                errors.append("Daily amount limit would be exceeded")
        
        # Check if payment method is supported
        if payment_method not in self.payment_method_ids:
            errors.append(f"Payment method {payment_method.name} not supported by this terminal")
        
        if errors:
            raise ValueError('\n'.join(errors))
        
        return True
    
    def _get_today_transaction_count(self):
        """Get today's transaction count"""
        # This would query transactions for today
        return 0
    
    def _get_today_transaction_amount(self):
        """Get today's transaction amount"""
        # This would query transaction amounts for today
        return 0.0
    
    def process_transaction(self, amount, payment_method, transaction_data=None):
        """Process transaction through this terminal"""
        # Validate transaction
        self.validate_transaction(amount, payment_method)
        
        # Process payment through payment method
        result = payment_method.process_payment(amount, transaction_data)
        
        # Update terminal statistics
        self._update_statistics(result)
        
        return result
    
    def _update_statistics(self, transaction_result):
        """Update terminal statistics"""
        if transaction_result['status'] == 'success':
            self.total_transactions += 1
            self.total_amount += transaction_result['amount']
            self.success_rate = self._calculate_success_rate()
        else:
            self.error_count += 1
            self.last_error = datetime.now()
            self.error_message = transaction_result.get('error_message', 'Unknown error')
    
    def _calculate_success_rate(self):
        """Calculate success rate"""
        if self.total_transactions == 0:
            return 100.0
        
        successful_transactions = self.total_transactions - self.error_count
        return (successful_transactions / self.total_transactions) * 100