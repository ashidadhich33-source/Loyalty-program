# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - POS Cash Box Wizard
=======================================

Cash management wizard for POS sessions.
"""

from core_framework.orm import BaseModel, CharField, TextField, BooleanField, IntegerField, DateTimeField, Many2OneField, SelectionField, FloatField, One2ManyField, Many2ManyField
from core_framework.orm import Field
from typing import Dict, Any, Optional
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class PosCashboxWizard(BaseModel):
    """Cash box management wizard"""
    
    _name = 'pos.cashbox.wizard'
    _description = 'POS Cash Box Wizard'
    _table = 'pos_cashbox_wizard'
    
    # Basic Information
    session_id = Many2OneField(
        'pos.session',
        string='Session',
        required=True,
        help='POS session for cash management'
    )
    
    operation_type = SelectionField(
        string='Operation Type',
        selection=[
            ('open', 'Open Cash Box'),
            ('close', 'Close Cash Box'),
            ('add', 'Add Cash'),
            ('remove', 'Remove Cash'),
            ('count', 'Count Cash')
        ],
        required=True,
        help='Type of cash operation'
    )
    
    amount = FloatField(
        string='Amount',
        digits=(12, 2),
        help='Cash amount for the operation'
    )
    
    reason = CharField(
        string='Reason',
        size=200,
        help='Reason for the cash operation'
    )
    
    notes = TextField(
        string='Notes',
        help='Additional notes for the operation'
    )
    
    # Timestamps
    create_date = DateTimeField(
        string='Created On',
        auto_now_add=True
    )
    
    def action_confirm(self):
        """Confirm the cash operation"""
        for wizard in self:
            if wizard.operation_type == 'open':
                wizard._open_cash_box()
            elif wizard.operation_type == 'close':
                wizard._close_cash_box()
            elif wizard.operation_type == 'add':
                wizard._add_cash()
            elif wizard.operation_type == 'remove':
                wizard._remove_cash()
            elif wizard.operation_type == 'count':
                wizard._count_cash()
        
        return {'type': 'ir.actions.act_window_close'}
    
    def _open_cash_box(self):
        """Open cash box for the session"""
        session = self.session_id
        if session.state != 'opened':
            raise ValueError("Session must be opened to perform cash operations")
        
        # Set starting cash amount
        if self.amount:
            session.start_cash = self.amount
        
        # Log the operation
        self._log_cash_operation('Cash box opened', self.amount)
    
    def _close_cash_box(self):
        """Close cash box for the session"""
        session = self.session_id
        if session.state != 'opened':
            raise ValueError("Session must be opened to perform cash operations")
        
        # Set ending cash amount
        if self.amount:
            session.end_cash = self.amount
        
        # Log the operation
        self._log_cash_operation('Cash box closed', self.amount)
    
    def _add_cash(self):
        """Add cash to the session"""
        session = self.session_id
        if session.state != 'opened':
            raise ValueError("Session must be opened to perform cash operations")
        
        if not self.amount or self.amount <= 0:
            raise ValueError("Amount must be greater than 0")
        
        # Log the operation
        self._log_cash_operation(f'Cash added: {self.reason}', self.amount)
    
    def _remove_cash(self):
        """Remove cash from the session"""
        session = self.session_id
        if session.state != 'opened':
            raise ValueError("Session must be opened to perform cash operations")
        
        if not self.amount or self.amount <= 0:
            raise ValueError("Amount must be greater than 0")
        
        # Log the operation
        self._log_cash_operation(f'Cash removed: {self.reason}', -self.amount)
    
    def _count_cash(self):
        """Count cash in the session"""
        session = self.session_id
        if session.state != 'opened':
            raise ValueError("Session must be opened to perform cash operations")
        
        # Log the operation
        self._log_cash_operation('Cash counted', self.amount)
    
    def _log_cash_operation(self, operation, amount):
        """Log cash operation"""
        # This would create a log entry for the cash operation
        # For now, just update the session notes
        session = self.session_id
        if session.notes:
            session.notes += f"\n{operation}: {amount}"
        else:
            session.notes = f"{operation}: {amount}"