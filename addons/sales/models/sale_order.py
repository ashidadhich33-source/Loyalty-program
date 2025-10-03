#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Sale Order Model
===================================

Sales order management for kids clothing retail.
"""

import logging
from datetime import datetime, timedelta
from core_framework.orm import BaseModel, CharField, TextField, BooleanField, IntegerField, DateTimeField, Many2OneField, SelectionField, FloatField, One2ManyField, Many2ManyField
from core_framework.exceptions import ValidationError

logger = logging.getLogger(__name__)

class SaleOrder(BaseModel):
    """Sales orders for kids clothing retail"""
    
    _name = 'sale.order'
    _description = 'Sales Order'
    _table = 'sale_order'
    _order = 'date_order desc, id desc'
    
    # Basic Information
    name = CharField(
        string='Order Reference',
        size=64,
        required=True,
        help='Unique order reference'
    )
    
    partner_id = Many2OneField(
        'contact.customer',
        string='Customer',
        required=True,
        help='Customer for this order'
    )
    
    # Order Details
    date_order = DateTimeField(
        string='Order Date',
        default=datetime.now,
        required=True,
        help='Date when the order was placed'
    )
    
    date_required = DateTimeField(
        string='Required Date',
        help='Date when the order is required'
    )
    
    date_shipped = DateTimeField(
        string='Shipped Date',
        help='Date when the order was shipped'
    )
    
    date_delivered = DateTimeField(
        string='Delivered Date',
        help='Date when the order was delivered'
    )
    
    # Order Status
    state = SelectionField(
        string='Status',
        selection=[
            ('draft', 'Quotation'),
            ('sent', 'Quotation Sent'),
            ('sale', 'Sales Order'),
            ('done', 'Locked'),
            ('cancel', 'Cancelled')
        ],
        default='draft',
        help='Current status of the order'
    )
    
    # Pricing Information
    amount_untaxed = FloatField(
        string='Untaxed Amount',
        digits=(12, 2),
        default=0.0,
        help='Amount without taxes'
    )
    
    amount_tax = FloatField(
        string='Tax Amount',
        digits=(12, 2),
        default=0.0,
        help='Total tax amount'
    )
    
    amount_total = FloatField(
        string='Total Amount',
        digits=(12, 2),
        default=0.0,
        help='Total amount including taxes'
    )
    
    # Discount Information
    discount_type = SelectionField(
        string='Discount Type',
        selection=[
            ('percentage', 'Percentage'),
            ('fixed', 'Fixed Amount'),
            ('none', 'No Discount')
        ],
        default='none',
        help='Type of discount applied'
    )
    
    discount_amount = FloatField(
        string='Discount Amount',
        digits=(12, 2),
        default=0.0,
        help='Discount amount'
    )
    
    discount_percentage = FloatField(
        string='Discount %',
        digits=(5, 2),
        default=0.0,
        help='Discount percentage'
    )
    
    # Kids Clothing Specific Fields
    child_profile_id = Many2OneField(
        'child.profile',
        string='Child Profile',
        help='Child profile for age-based recommendations'
    )
    
    age_group = SelectionField(
        string='Age Group',
        selection=[
            ('newborn', 'Newborn (0-6 months)'),
            ('infant', 'Infant (6-12 months)'),
            ('toddler', 'Toddler (1-3 years)'),
            ('preschool', 'Preschool (3-5 years)'),
            ('school', 'School (5-12 years)'),
            ('teen', 'Teen (12+ years)'),
            ('all', 'All Ages')
        ],
        help='Target age group for this order'
    )
    
    gender_preference = SelectionField(
        string='Gender Preference',
        selection=[
            ('boys', 'Boys'),
            ('girls', 'Girls'),
            ('unisex', 'Unisex'),
            ('all', 'All Genders')
        ],
        help='Gender preference for this order'
    )
    
    season = SelectionField(
        string='Season',
        selection=[
            ('summer', 'Summer'),
            ('winter', 'Winter'),
            ('monsoon', 'Monsoon'),
            ('all_season', 'All Season'),
            ('festive', 'Festive'),
            ('party', 'Party Wear')
        ],
        help='Seasonal preference for this order'
    )
    
    # Order Lines
    order_line_ids = One2ManyField(
        string='Order Lines',
        comodel_name='sale.order.line',
        inverse_name='order_id',
        help='Order lines for this order'
    )
    
    # Delivery Information
    delivery_address_id = Many2OneField(
        'contact.address',
        string='Delivery Address',
        help='Delivery address for this order'
    )
    
    delivery_method = SelectionField(
        string='Delivery Method',
        selection=[
            ('home_delivery', 'Home Delivery'),
            ('store_pickup', 'Store Pickup'),
            ('express', 'Express Delivery'),
            ('standard', 'Standard Delivery')
        ],
        help='Delivery method for this order'
    )
    
    delivery_notes = TextField(
        string='Delivery Notes',
        help='Special delivery instructions'
    )
    
    # Payment Information
    payment_method = SelectionField(
        string='Payment Method',
        selection=[
            ('cash', 'Cash'),
            ('card', 'Credit/Debit Card'),
            ('upi', 'UPI'),
            ('netbanking', 'Net Banking'),
            ('wallet', 'Digital Wallet'),
            ('emi', 'EMI'),
            ('cod', 'Cash on Delivery')
        ],
        help='Payment method for this order'
    )
    
    payment_status = SelectionField(
        string='Payment Status',
        selection=[
            ('pending', 'Pending'),
            ('partial', 'Partially Paid'),
            ('paid', 'Paid'),
            ('refunded', 'Refunded')
        ],
        default='pending',
        help='Payment status of this order'
    )
    
    # Company Information
    company_id = Many2OneField(
        'res.company',
        string='Company',
        required=True,
        help='Company for this order'
    )
    
    user_id = Many2OneField(
        'res.users',
        string='Salesperson',
        help='Salesperson responsible for this order'
    )
    
    team_id = Many2OneField(
        'sales.team',
        string='Sales Team',
        help='Sales team responsible for this order'
    )
    
    # Notes and Terms
    note = TextField(
        string='Notes',
        help='Internal notes for this order'
    )
    
    terms_conditions = TextField(
        string='Terms & Conditions',
        help='Terms and conditions for this order'
    )
    
    # Analytics
    customer_rating = IntegerField(
        string='Customer Rating',
        help='Customer rating for this order (1-5)'
    )
    
    customer_feedback = TextField(
        string='Customer Feedback',
        help='Customer feedback for this order'
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
            vals['name'] = self._get_next_order_number()
        
        if 'company_id' not in vals:
            vals['company_id'] = self.env.user.company_id.id
        
        if 'user_id' not in vals:
            vals['user_id'] = self.env.user.id
        
        return super().create(vals)
    
    def write(self, vals):
        """Override write to update amounts"""
        result = super().write(vals)
        
        # Update amounts if order lines changed
        if any(field in vals for field in ['order_line_ids', 'discount_type', 'discount_amount', 'discount_percentage']):
            self._update_amounts()
        
        return result
    
    def _get_next_order_number(self):
        """Get next order number"""
        # This would integrate with sequence management
        return f"SO{datetime.now().strftime('%Y%m%d')}{self.env['ir.sequence'].next_by_code('sale.order')}"
    
    def _update_amounts(self):
        """Update order amounts"""
        for order in self:
            # Calculate amounts from order lines
            untaxed_amount = sum(line.price_subtotal for line in order.order_line_ids)
            
            # Apply discount
            if order.discount_type == 'percentage':
                discount_amount = untaxed_amount * (order.discount_percentage / 100)
            elif order.discount_type == 'fixed':
                discount_amount = order.discount_amount
            else:
                discount_amount = 0.0
            
            # Calculate tax (simplified)
            tax_amount = (untaxed_amount - discount_amount) * 0.18  # 18% GST
            
            # Update amounts
            order.amount_untaxed = untaxed_amount - discount_amount
            order.amount_tax = tax_amount
            order.amount_total = order.amount_untaxed + order.amount_tax
    
    def action_quotation_send(self):
        """Send quotation to customer"""
        for order in self:
            if order.state != 'draft':
                raise ValidationError("Only draft quotations can be sent")
            
            order.state = 'sent'
            # Here you would send email to customer
    
    def action_confirm(self):
        """Confirm quotation to sales order"""
        for order in self:
            if order.state not in ['draft', 'sent']:
                raise ValidationError("Only quotations can be confirmed")
            
            order.state = 'sale'
            order.date_order = datetime.now()
    
    def action_done(self):
        """Mark order as done"""
        for order in self:
            if order.state != 'sale':
                raise ValidationError("Only sales orders can be marked as done")
            
            order.state = 'done'
            order.date_delivered = datetime.now()
    
    def action_cancel(self):
        """Cancel order"""
        for order in self:
            if order.state == 'done':
                raise ValidationError("Cannot cancel delivered orders")
            
            order.state = 'cancel'
    
    def action_draft(self):
        """Reset to draft"""
        for order in self:
            if order.state == 'done':
                raise ValidationError("Cannot reset delivered orders")
            
            order.state = 'draft'
    
    def action_view_delivery(self):
        """View delivery orders"""
        return {
            'type': 'ocean.actions.act_window',
            'name': f'Delivery Orders - {self.name}',
            'res_model': 'sale.delivery',
            'view_mode': 'tree,form',
            'domain': [('sale_order_id', '=', self.id)],
            'context': {'default_sale_order_id': self.id}
        }
    
    def action_view_returns(self):
        """View return orders"""
        return {
            'type': 'ocean.actions.act_window',
            'name': f'Return Orders - {self.name}',
            'res_model': 'sale.return',
            'view_mode': 'tree,form',
            'domain': [('sale_order_id', '=', self.id)],
            'context': {'default_sale_order_id': self.id}
        }
    
    def action_analyze_order(self):
        """Analyze order performance"""
        return {
            'type': 'ocean.actions.act_window',
            'name': f'Order Analytics - {self.name}',
            'res_model': 'sale.analytics',
            'view_mode': 'form',
            'domain': [('order_id', '=', self.id)],
            'context': {'default_order_id': self.id}
        }