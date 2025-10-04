# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Purchase Order
==================================

Purchase order management for kids clothing retail.
"""

from core_framework.orm import BaseModel, CharField, TextField, BooleanField, IntegerField, DateTimeField, Many2OneField, SelectionField, FloatField, One2ManyField, Many2ManyField
from core_framework.orm import Field
from typing import Dict, Any, Optional
import logging
from datetime import datetime
from core_framework.exceptions import ValidationError

logger = logging.getLogger(__name__)

class PurchaseOrder(BaseModel):
    """Purchase order for supplier procurement"""
    
    _name = 'purchase.order'
    _description = 'Purchase Order'
    _table = 'purchase_order'
    
    # Basic Information
    name = CharField(
        string='Order Reference',
        size=100,
        required=True,
        help='Purchase order reference number'
    )
    
    partner_id = Many2OneField(
        'res.partner',
        string='Supplier',
        required=True,
        help='Supplier for this purchase order'
    )
    
    date_order = DateTimeField(
        string='Order Date',
        default=datetime.now,
        required=True,
        help='Date when the purchase order was created'
    )
    
    date_planned = DateTimeField(
        string='Scheduled Date',
        help='Expected delivery date'
    )
    
    # Order Details
    order_line_ids = One2ManyField(
        'purchase.order.line',
        'order_id',
        string='Order Lines',
        help='Purchase order lines'
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
    
    currency_id = Many2OneField(
        'res.currency',
        string='Currency',
        required=True,
        help='Currency for this purchase order'
    )
    
    # State Management
    state = SelectionField(
        string='Status',
        selection=[
            ('draft', 'Draft'),
            ('sent', 'RFQ Sent'),
            ('to_approve', 'To Approve'),
            ('purchase', 'Purchase Order'),
            ('done', 'Locked'),
            ('cancel', 'Cancelled'),
        ],
        default='draft',
        required=True,
        help='Current state of the purchase order'
    )
    
    # Approval Workflow
    approval_required = BooleanField(
        string='Approval Required',
        default=False,
        help='Whether this order requires approval'
    )
    
    approved_by = Many2OneField(
        'res.users',
        string='Approved By',
        help='User who approved this order'
    )
    
    approval_date = DateTimeField(
        string='Approval Date',
        help='Date when the order was approved'
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
        help='Target age group for this purchase'
    )
    
    season = SelectionField(
        string='Season',
        selection=[
            ('summer', 'Summer'),
            ('winter', 'Winter'),
            ('monsoon', 'Monsoon'),
            ('all_season', 'All Season'),
        ],
        help='Season for this purchase'
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
        help='Size range for this purchase'
    )
    
    gender = SelectionField(
        string='Gender',
        selection=[
            ('unisex', 'Unisex'),
            ('boys', 'Boys'),
            ('girls', 'Girls'),
        ],
        help='Gender category for this purchase'
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
        help='Special occasion for this purchase'
    )
    
    # Additional Information
    notes = TextField(
        string='Notes',
        help='Additional notes for this purchase order'
    )
    
    user_id = Many2OneField(
        'res.users',
        string='Purchase Representative',
        default=lambda self: self.env.user,
        help='User responsible for this purchase order'
    )
    
    company_id = Many2OneField(
        'res.company',
        string='Company',
        required=True,
        help='Company for this purchase order'
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
            vals['name'] = self._generate_order_reference()
        
        if 'company_id' not in vals:
            vals['company_id'] = self.env.user.company_id.id
        
        if 'currency_id' not in vals:
            vals['currency_id'] = self.env.user.company_id.currency_id.id
        
        return super().create(vals)
    
    def write(self, vals):
        """Override write to update timestamps"""
        vals['write_date'] = datetime.now()
        return super().write(vals)
    
    def _generate_order_reference(self):
        """Generate unique order reference"""
        # Simple implementation - in production, use proper sequence
        return f"PO{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    def action_send_rfq(self):
        """Send RFQ to supplier"""
        for record in self:
            if record.state != 'draft':
                raise ValidationError("Only draft orders can be sent as RFQ")
            record.state = 'sent'
    
    def action_approve(self):
        """Approve purchase order"""
        for record in self:
            if record.state not in ['sent', 'to_approve']:
                raise ValidationError("Only sent or to approve orders can be approved")
            record.state = 'purchase'
            record.approved_by = self.env.user.id
            record.approval_date = datetime.now()
    
    def action_done(self):
        """Mark purchase order as done"""
        for record in self:
            if record.state != 'purchase':
                raise ValidationError("Only purchase orders can be marked as done")
            record.state = 'done'
    
    def action_cancel(self):
        """Cancel purchase order"""
        for record in self:
            if record.state in ['done']:
                raise ValidationError("Done orders cannot be cancelled")
            record.state = 'cancel'
    
    def action_view_order_lines(self):
        """View order lines"""
        return {
            'type': 'ocean.actions.act_window',
            'name': 'Purchase Order Lines',
            'res_model': 'purchase.order.line',
            'view_mode': 'tree,form',
            'domain': [('order_id', '=', self.id)],
        }
    
    def action_view_vendor_bills(self):
        """View vendor bills"""
        return {
            'type': 'ocean.actions.act_window',
            'name': 'Vendor Bills',
            'res_model': 'vendor.bill',
            'view_mode': 'tree,form',
            'domain': [('purchase_order_id', '=', self.id)],
        }
    
    def get_order_summary(self):
        """Get order summary"""
        return {
            'total_lines': len(self.order_line_ids),
            'total_quantity': sum(line.product_qty for line in self.order_line_ids),
            'total_amount': self.amount_total,
            'currency': self.currency_id.name,
        }
    
    def _validate_order(self):
        """Validate purchase order"""
        if not self.order_line_ids:
            raise ValidationError("Purchase order must have at least one line")
        
        for line in self.order_line_ids:
            if line.product_qty <= 0:
                raise ValidationError("Product quantity must be greater than 0")
    
    def _calculate_totals(self):
        """Calculate order totals"""
        self.amount_untaxed = sum(line.price_subtotal for line in self.order_line_ids)
        self.amount_tax = sum(line.price_tax for line in self.order_line_ids)
        self.amount_total = self.amount_untaxed + self.amount_tax