# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Vendor Bill Wizard
=======================================

Vendor bill creation wizard for kids clothing retail.
"""

from core_framework.orm import BaseModel, CharField, TextField, BooleanField, IntegerField, DateTimeField, Many2OneField, SelectionField, FloatField, One2ManyField, Many2ManyField
from core_framework.orm import Field
from typing import Dict, Any, Optional
import logging
from datetime import datetime
from core_framework.exceptions import ValidationError

logger = logging.getLogger(__name__)

class VendorBillWizard(BaseModel):
    """Wizard for creating vendor bills"""
    
    _name = 'vendor.bill.wizard'
    _description = 'Vendor Bill Wizard'
    _table = 'vendor_bill_wizard'
    
    # Basic Information
    name = CharField(
        string='Bill Reference',
        size=100,
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
    
    def action_create_bill(self):
        """Create vendor bill from wizard"""
        for record in self:
            if not record.partner_id:
                raise ValidationError("Please select a supplier")
            
            # Create vendor bill
            bill_vals = {
                'name': record.name or self._generate_bill_reference(),
                'partner_id': record.partner_id.id,
                'purchase_order_id': record.purchase_order_id.id if record.purchase_order_id else False,
                'bill_date': record.bill_date,
                'due_date': record.due_date,
                'age_group': record.age_group,
                'season': record.season,
                'size_range': record.size_range,
                'gender': record.gender,
                'special_occasion': record.special_occasion,
                'notes': record.notes,
            }
            
            bill = self.env['vendor.bill'].create(bill_vals)
            
            return {
                'type': 'ocean.actions.act_window',
                'name': 'Vendor Bill',
                'res_model': 'vendor.bill',
                'view_mode': 'form',
                'res_id': bill.id,
            }
    
    def _generate_bill_reference(self):
        """Generate unique bill reference"""
        return f"VB{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    def action_view_supplier(self):
        """View supplier details"""
        if self.partner_id:
            return {
                'type': 'ocean.actions.act_window',
                'name': 'Supplier Details',
                'res_model': 'res.partner',
                'view_mode': 'form',
                'res_id': self.partner_id.id,
            }
        return False
    
    def action_view_purchase_order(self):
        """View purchase order details"""
        if self.purchase_order_id:
            return {
                'type': 'ocean.actions.act_window',
                'name': 'Purchase Order',
                'res_model': 'purchase.order',
                'view_mode': 'form',
                'res_id': self.purchase_order_id.id,
            }
        return False
    
    def get_wizard_summary(self):
        """Get wizard summary"""
        return {
            'supplier': self.partner_id.name if self.partner_id else 'Not Selected',
            'purchase_order': self.purchase_order_id.name if self.purchase_order_id else 'Not Selected',
            'bill_date': self.bill_date.strftime('%Y-%m-%d') if self.bill_date else 'Not Set',
            'due_date': self.due_date.strftime('%Y-%m-%d') if self.due_date else 'Not Set',
            'age_group': self.age_group or 'Not Selected',
            'season': self.season or 'Not Selected',
            'gender': self.gender or 'Not Selected',
        }