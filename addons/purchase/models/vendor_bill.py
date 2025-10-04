# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Vendor Bill
================================

Vendor bill management for kids clothing retail.
"""

from core_framework.orm import BaseModel, CharField, TextField, BooleanField, IntegerField, DateTimeField, Many2OneField, SelectionField, FloatField, One2ManyField, Many2ManyField
from core_framework.orm import Field
from typing import Dict, Any, Optional
import logging
from datetime import datetime
from core_framework.exceptions import ValidationError

logger = logging.getLogger(__name__)

class VendorBill(BaseModel):
    """Vendor bill for supplier invoices"""
    
    _name = 'vendor.bill'
    _description = 'Vendor Bill'
    _table = 'vendor_bill'
    
    # Basic Information
    name = CharField(
        string='Bill Reference',
        size=100,
        required=True,
        help='Vendor bill reference number'
    )
    
    partner_id = Many2OneField(
        'res.partner',
        string='Supplier',
        required=True,
        help='Supplier for this bill'
    )
    
    purchase_order_id = Many2OneField(
        'purchase.order',
        string='Purchase Order',
        help='Related purchase order'
    )
    
    bill_date = DateTimeField(
        string='Bill Date',
        default=datetime.now,
        required=True,
        help='Date of the vendor bill'
    )
    
    due_date = DateTimeField(
        string='Due Date',
        help='Due date for payment'
    )
    
    # Bill Details
    bill_line_ids = One2ManyField(
        'vendor.bill.line',
        'bill_id',
        string='Bill Lines',
        help='Vendor bill lines'
    )
    
    # Financial Information
    amount_untaxed = FloatField(
        string='Untaxed Amount',
        digits=(16, 2),
        help='Total amount without taxes'
    )
    
    amount_tax = FloatField(
        string='Tax Amount',
        digits=(16, 2),
        help='Total tax amount'
    )
    
    amount_total = FloatField(
        string='Total Amount',
        digits=(16, 2),
        help='Total amount including taxes'
    )
    
    amount_paid = FloatField(
        string='Amount Paid',
        digits=(16, 2),
        default=0.0,
        help='Amount already paid'
    )
    
    amount_residual = FloatField(
        string='Amount Due',
        digits=(16, 2),
        help='Amount remaining to be paid'
    )
    
    currency_id = Many2OneField(
        'res.currency',
        string='Currency',
        required=True,
        help='Currency for this bill'
    )
    
    # State Management
    state = SelectionField(
        string='Status',
        selection=[
            ('draft', 'Draft'),
            ('posted', 'Posted'),
            ('paid', 'Paid'),
            ('cancelled', 'Cancelled'),
        ],
        default='draft',
        required=True,
        help='Current state of the vendor bill'
    )
    
    # Payment Information
    payment_state = SelectionField(
        string='Payment Status',
        selection=[
            ('not_paid', 'Not Paid'),
            ('in_payment', 'In Payment'),
            ('paid', 'Paid'),
            ('partial', 'Partially Paid'),
            ('reversed', 'Reversed'),
        ],
        default='not_paid',
        help='Payment status of the bill'
    )
    
    # Kids Clothing Specific Fields
    age_group = SelectionField(
        string='Age Group',
        selection=[
            ('infant', 'Infant (0-2 years)'),
            ('toddler', 'Toddler (2-4 years)'),
            ('child', 'Child (4-8 years)'),
            ('teen', 'Teen (8-16 years)'),
        ],
        help='Target age group for this bill'
    )
    
    season = SelectionField(
        string='Season',
        selection=[
            ('summer', 'Summer'),
            ('winter', 'Winter'),
            ('monsoon', 'Monsoon'),
            ('all_season', 'All Season'),
        ],
        help='Season for this bill'
    )
    
    size_range = SelectionField(
        string='Size Range',
        selection=[
            ('xs', 'XS'),
            ('s', 'S'),
            ('m', 'M'),
            ('l', 'L'),
            ('xl', 'XL'),
            ('xxl', 'XXL'),
        ],
        help='Size range for this bill'
    )
    
    gender = SelectionField(
        string='Gender',
        selection=[
            ('unisex', 'Unisex'),
            ('boys', 'Boys'),
            ('girls', 'Girls'),
        ],
        help='Gender category for this bill'
    )
    
    special_occasion = SelectionField(
        string='Special Occasion',
        selection=[
            ('daily_wear', 'Daily Wear'),
            ('party_wear', 'Party Wear'),
            ('festival', 'Festival'),
            ('school', 'School'),
            ('sports', 'Sports'),
            ('formal', 'Formal'),
        ],
        help='Special occasion for this bill'
    )
    
    # Additional Information
    notes = TextField(
        string='Notes',
        help='Additional notes for this bill'
    )
    
    user_id = Many2OneField(
        'res.users',
        string='Responsible',
        default=lambda self: self.env.user,
        help='User responsible for this bill'
    )
    
    company_id = Many2OneField(
        'res.company',
        string='Company',
        required=True,
        help='Company for this bill'
    )
    
    # Timestamps
    create_date = DateTimeField(
        string='Created On',
        default=datetime.now,
        help='Date when the record was created'
    )
    
    write_date = DateTimeField(
        string='Last Updated On',
        default=datetime.now,
        help='Date when the record was last updated'
    )
    
    def create(self, vals):
        """Override create to set default values"""
        if 'name' not in vals:
            vals['name'] = self._generate_bill_reference()
        
        if 'company_id' not in vals:
            vals['company_id'] = self.env.user.company_id.id
        
        if 'currency_id' not in vals:
            vals['currency_id'] = self.env.user.company_id.currency_id.id
        
        return super().create(vals)
    
    def write(self, vals):
        """Override write to update timestamps"""
        vals['write_date'] = datetime.now()
        return super().write(vals)
    
    def _generate_bill_reference(self):
        """Generate unique bill reference"""
        # Simple implementation - in production, use proper sequence
        return f"VB{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    def action_post(self):
        """Post vendor bill"""
        for record in self:
            if record.state != 'draft':
                raise ValidationError("Only draft bills can be posted")
            record.state = 'posted'
            record._calculate_totals()
    
    def action_pay(self):
        """Mark bill as paid"""
        for record in self:
            if record.state != 'posted':
                raise ValidationError("Only posted bills can be paid")
            record.state = 'paid'
            record.payment_state = 'paid'
            record.amount_paid = record.amount_total
            record.amount_residual = 0.0
    
    def action_cancel(self):
        """Cancel vendor bill"""
        for record in self:
            if record.state in ['paid']:
                raise ValidationError("Paid bills cannot be cancelled")
            record.state = 'cancelled'
    
    def action_view_bill_lines(self):
        """View bill lines"""
        return {
            'type': 'ocean.actions.act_window',
            'name': 'Vendor Bill Lines',
            'res_model': 'vendor.bill.line',
            'view_mode': 'tree,form',
            'domain': [('bill_id', '=', self.id)],
        }
    
    def action_view_purchase_order(self):
        """View purchase order"""
        if self.purchase_order_id:
            return {
                'type': 'ocean.actions.act_window',
                'name': 'Purchase Order',
                'res_model': 'purchase.order',
                'view_mode': 'form',
                'res_id': self.purchase_order_id.id,
            }
        return False
    
    def get_bill_summary(self):
        """Get bill summary"""
        return {
            'total_lines': len(self.bill_line_ids),
            'total_amount': self.amount_total,
            'amount_paid': self.amount_paid,
            'amount_due': self.amount_residual,
            'currency': self.currency_id.name,
            'payment_status': self.payment_state,
        }
    
    def _validate_bill(self):
        """Validate vendor bill"""
        if not self.bill_line_ids:
            raise ValidationError("Vendor bill must have at least one line")
        
        for line in self.bill_line_ids:
            if line.quantity <= 0:
                raise ValidationError("Product quantity must be greater than 0")
    
    def _calculate_totals(self):
        """Calculate bill totals"""
        self.amount_untaxed = sum(line.price_subtotal for line in self.bill_line_ids)
        self.amount_tax = sum(line.price_tax for line in self.bill_line_ids)
        self.amount_total = self.amount_untaxed + self.amount_tax
        self.amount_residual = self.amount_total - self.amount_paid