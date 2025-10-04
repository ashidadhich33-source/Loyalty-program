# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Purchase Order Wizard
=========================================

Purchase order creation wizard for kids clothing retail.
"""

from core_framework.orm import BaseModel, CharField, TextField, BooleanField, IntegerField, DateTimeField, Many2OneField, SelectionField, FloatField, One2ManyField, Many2ManyField
from core_framework.orm import Field
from typing import Dict, Any, Optional
import logging
from datetime import datetime
from core_framework.exceptions import ValidationError

logger = logging.getLogger(__name__)

class PurchaseOrderWizard(BaseModel):
    """Wizard for creating purchase orders"""
    
    _name = 'purchase.order.wizard'
    _description = 'Purchase Order Wizard'
    _table = 'purchase_order_wizard'
    
    # Basic Information
    name = CharField(
        string='Order Reference',
        size=100,
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
    
    def action_create_order(self):
        """Create purchase order from wizard"""
        for record in self:
            if not record.partner_id:
                raise ValidationError("Please select a supplier")
            
            # Create purchase order
            order_vals = {
                'name': record.name or self._generate_order_reference(),
                'partner_id': record.partner_id.id,
                'date_order': record.date_order,
                'date_planned': record.date_planned,
                'age_group': record.age_group,
                'season': record.season,
                'size_range': record.size_range,
                'gender': record.gender,
                'special_occasion': record.special_occasion,
                'notes': record.notes,
            }
            
            order = self.env['purchase.order'].create(order_vals)
            
            return {
                'type': 'ocean.actions.act_window',
                'name': 'Purchase Order',
                'res_model': 'purchase.order',
                'view_mode': 'form',
                'res_id': order.id,
            }
    
    def _generate_order_reference(self):
        """Generate unique order reference"""
        return f"PO{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
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
    
    def get_wizard_summary(self):
        """Get wizard summary"""
        return {
            'supplier': self.partner_id.name if self.partner_id else 'Not Selected',
            'order_date': self.date_order.strftime('%Y-%m-%d') if self.date_order else 'Not Set',
            'planned_date': self.date_planned.strftime('%Y-%m-%d') if self.date_planned else 'Not Set',
            'age_group': self.age_group or 'Not Selected',
            'season': self.season or 'Not Selected',
            'gender': self.gender or 'Not Selected',
        }