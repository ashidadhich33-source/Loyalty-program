#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Sale Delivery Model
=======================================

Delivery order management for kids clothing retail.
"""

import logging
from datetime import datetime, timedelta
from core_framework.orm import BaseModel, CharField, TextField, BooleanField, IntegerField, DateTimeField, Many2OneField, SelectionField, FloatField, One2ManyField, Many2ManyField
from core_framework.exceptions import ValidationError

logger = logging.getLogger(__name__)

class SaleDelivery(BaseModel):
    """Delivery orders for kids clothing retail"""
    
    _name = 'sale.delivery'
    _description = 'Sale Delivery'
    _table = 'sale_delivery'
    _order = 'date_delivery desc, id desc'
    
    # Basic Information
    name = CharField(
        string='Delivery Reference',
        size=64,
        required=True,
        help='Unique delivery reference'
    )
    
    sale_order_id = Many2OneField(
        'sale.order',
        string='Sales Order',
        required=True,
        help='Related sales order'
    )
    
    partner_id = Many2OneField(
        'contact.customer',
        string='Customer',
        related='sale_order_id.partner_id',
        help='Customer for this delivery'
    )
    
    # Delivery Details
    date_delivery = DateTimeField(
        string='Delivery Date',
        default=datetime.now,
        required=True,
        help='Date when delivery is scheduled'
    )
    
    date_actual = DateTimeField(
        string='Actual Delivery Date',
        help='Actual date when delivery was completed'
    )
    
    # Delivery Status
    state = SelectionField(
        string='Status',
        selection=[
            ('draft', 'Draft'),
            ('confirmed', 'Confirmed'),
            ('in_transit', 'In Transit'),
            ('delivered', 'Delivered'),
            ('failed', 'Failed'),
            ('cancelled', 'Cancelled')
        ],
        default='draft',
        help='Current status of the delivery'
    )
    
    # Delivery Address
    delivery_address_id = Many2OneField(
        'contact.address',
        string='Delivery Address',
        help='Delivery address for this order'
    )
    
    delivery_address = TextField(
        string='Delivery Address',
        help='Full delivery address'
    )
    
    delivery_city = CharField(
        string='City',
        size=50,
        help='Delivery city'
    )
    
    delivery_state = CharField(
        string='State',
        size=50,
        help='Delivery state'
    )
    
    delivery_zip = CharField(
        string='ZIP Code',
        size=20,
        help='Delivery ZIP code'
    )
    
    delivery_country = CharField(
        string='Country',
        size=50,
        help='Delivery country'
    )
    
    # Delivery Method
    delivery_method = SelectionField(
        string='Delivery Method',
        selection=[
            ('home_delivery', 'Home Delivery'),
            ('store_pickup', 'Store Pickup'),
            ('express', 'Express Delivery'),
            ('standard', 'Standard Delivery'),
            ('same_day', 'Same Day Delivery')
        ],
        help='Delivery method for this order'
    )
    
    delivery_carrier_id = Many2OneField(
        'delivery.carrier',
        string='Delivery Carrier',
        help='Delivery carrier for this order'
    )
    
    tracking_number = CharField(
        string='Tracking Number',
        size=100,
        help='Tracking number for this delivery'
    )
    
    # Delivery Items
    delivery_line_ids = One2ManyField(
        string='Delivery Lines',
        comodel_name='sale.delivery.line',
        inverse_name='delivery_id',
        help='Delivery lines for this delivery'
    )
    
    # Delivery Information
    delivery_notes = TextField(
        string='Delivery Notes',
        help='Special delivery instructions'
    )
    
    delivery_contact = CharField(
        string='Delivery Contact',
        size=100,
        help='Contact person for delivery'
    )
    
    delivery_phone = CharField(
        string='Delivery Phone',
        size=20,
        help='Phone number for delivery contact'
    )
    
    # Delivery Charges
    delivery_charges = FloatField(
        string='Delivery Charges',
        digits=(12, 2),
        default=0.0,
        help='Delivery charges for this order'
    )
    
    delivery_charges_paid = BooleanField(
        string='Delivery Charges Paid',
        default=False,
        help='Whether delivery charges are paid'
    )
    
    # Delivery Performance
    delivery_rating = IntegerField(
        string='Delivery Rating',
        help='Customer rating for delivery (1-5)'
    )
    
    delivery_feedback = TextField(
        string='Delivery Feedback',
        help='Customer feedback for delivery'
    )
    
    # Delivery Issues
    delivery_issues = TextField(
        string='Delivery Issues',
        help='Issues encountered during delivery'
    )
    
    delivery_attempts = IntegerField(
        string='Delivery Attempts',
        default=0,
        help='Number of delivery attempts'
    )
    
    # Company Information
    company_id = Many2OneField(
        'res.company',
        string='Company',
        related='sale_order_id.company_id',
        help='Company for this delivery'
    )
    
    user_id = Many2OneField(
        'res.users',
        string='Delivery Person',
        help='Person responsible for delivery'
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
            vals['name'] = self._get_next_delivery_number()
        
        return super().create(vals)
    
    def write(self, vals):
        """Override write to update status"""
        result = super().write(vals)
        
        # Update delivery status
        if 'state' in vals:
            self._update_delivery_status()
        
        return result
    
    def _get_next_delivery_number(self):
        """Get next delivery number"""
        return f"DEL{datetime.now().strftime('%Y%m%d')}{self.env['ir.sequence'].next_by_code('sale.delivery')}"
    
    def _update_delivery_status(self):
        """Update delivery status"""
        for delivery in self:
            if delivery.state == 'delivered':
                delivery.date_actual = datetime.now()
                # Update sales order status
                if delivery.sale_order_id.state == 'sale':
                    delivery.sale_order_id.action_done()
    
    def action_confirm(self):
        """Confirm delivery order"""
        for delivery in self:
            if delivery.state != 'draft':
                raise ValidationError("Only draft deliveries can be confirmed")
            
            delivery.state = 'confirmed'
    
    def action_ship(self):
        """Mark delivery as shipped"""
        for delivery in self:
            if delivery.state != 'confirmed':
                raise ValidationError("Only confirmed deliveries can be shipped")
            
            delivery.state = 'in_transit'
    
    def action_deliver(self):
        """Mark delivery as delivered"""
        for delivery in self:
            if delivery.state != 'in_transit':
                raise ValidationError("Only in-transit deliveries can be delivered")
            
            delivery.state = 'delivered'
            delivery.date_actual = datetime.now()
    
    def action_fail(self):
        """Mark delivery as failed"""
        for delivery in self:
            if delivery.state not in ['confirmed', 'in_transit']:
                raise ValidationError("Only confirmed or in-transit deliveries can be failed")
            
            delivery.state = 'failed'
            delivery.delivery_attempts += 1
    
    def action_retry(self):
        """Retry failed delivery"""
        for delivery in self:
            if delivery.state != 'failed':
                raise ValidationError("Only failed deliveries can be retried")
            
            delivery.state = 'confirmed'
    
    def action_cancel(self):
        """Cancel delivery"""
        for delivery in self:
            if delivery.state == 'delivered':
                raise ValidationError("Cannot cancel delivered orders")
            
            delivery.state = 'cancelled'
    
    def action_view_sale_order(self):
        """View related sales order"""
        return {
            'type': 'ocean.actions.act_window',
            'name': f'Sales Order - {self.sale_order_id.name}',
            'res_model': 'sale.order',
            'res_id': self.sale_order_id.id,
            'view_mode': 'form',
            'target': 'current'
        }
    
    def action_track_delivery(self):
        """Track delivery status"""
        if not self.tracking_number:
            raise ValidationError("No tracking number available")
        
        # This would integrate with delivery carrier APIs
        return {
            'type': 'ocean.actions.act_url',
            'url': f'/delivery/track/{self.tracking_number}',
            'target': 'new'
        }
    
    def action_schedule_delivery(self):
        """Schedule delivery"""
        return {
            'type': 'ocean.actions.act_window',
            'name': f'Schedule Delivery - {self.name}',
            'res_model': 'delivery.schedule',
            'view_mode': 'form',
            'context': {'default_delivery_id': self.id},
            'target': 'new'
        }