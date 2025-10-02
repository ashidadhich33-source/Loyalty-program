# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    # Kids Clothing specific fields
    is_kids_clothing_order = fields.Boolean(
        string='Kids Clothing Order',
        help='Check if this is a kids clothing order'
    )
    
    child_name = fields.Char(
        string='Child Name',
        help='Name of the child for whom the order is placed'
    )
    
    child_age = fields.Integer(
        string='Child Age',
        help='Age of the child'
    )
    
    special_instructions = fields.Text(
        string='Special Instructions',
        help='Special instructions for the order'
    )
    
    gift_wrapping = fields.Boolean(
        string='Gift Wrapping',
        help='Request gift wrapping'
    )
    
    gift_message = fields.Text(
        string='Gift Message',
        help='Gift message for the recipient'
    )
    
    # Order status
    order_status = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('in_production', 'In Production'),
        ('ready_for_pickup', 'Ready for Pickup'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ], string='Order Status', default='draft', track_visibility='onchange')
    
    # Delivery information
    delivery_date = fields.Date(
        string='Delivery Date',
        help='Expected delivery date'
    )
    
    delivery_method = fields.Selection([
        ('pickup', 'Store Pickup'),
        ('home_delivery', 'Home Delivery'),
        ('express', 'Express Delivery'),
    ], string='Delivery Method', default='pickup')
    
    # Customer preferences
    customer_preferences = fields.Text(
        string='Customer Preferences',
        help='Customer preferences and notes'
    )
    
    # Loyalty points
    loyalty_points_earned = fields.Integer(
        string='Loyalty Points Earned',
        compute='_compute_loyalty_points_earned',
        store=True
    )
    
    loyalty_points_used = fields.Integer(
        string='Loyalty Points Used',
        default=0
    )
    
    @api.depends('amount_total')
    def _compute_loyalty_points_earned(self):
        """Calculate loyalty points earned based on order total"""
        for order in self:
            if order.is_kids_clothing_order:
                # 1 point per dollar spent
                order.loyalty_points_earned = int(order.amount_total)
            else:
                order.loyalty_points_earned = 0
    
    @api.model
    def create(self, vals):
        """Override create to set default values for kids clothing orders"""
        if vals.get('is_kids_clothing_order'):
            vals.setdefault('order_status', 'draft')
        return super().create(vals)
    
    def action_confirm(self):
        """Override confirm to update order status"""
        result = super().action_confirm()
        for order in self:
            if order.is_kids_clothing_order:
                order.order_status = 'confirmed'
        return result
    
    def action_cancel(self):
        """Override cancel to update order status"""
        result = super().action_cancel()
        for order in self:
            if order.is_kids_clothing_order:
                order.order_status = 'cancelled'
        return result
    
    def action_mark_ready(self):
        """Mark order as ready for pickup"""
        for order in self:
            if order.is_kids_clothing_order:
                order.order_status = 'ready_for_pickup'
    
    def action_mark_shipped(self):
        """Mark order as shipped"""
        for order in self:
            if order.is_kids_clothing_order:
                order.order_status = 'shipped'
    
    def action_mark_delivered(self):
        """Mark order as delivered"""
        for order in self:
            if order.is_kids_clothing_order:
                order.order_status = 'delivered'
                # Update customer loyalty points
                if order.partner_id:
                    order.partner_id.loyalty_points += order.loyalty_points_earned


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    # Kids Clothing specific fields
    child_size = fields.Char(
        string='Child Size',
        help='Size for the child clothing item'
    )
    
    color_preference = fields.Char(
        string='Color Preference',
        help='Preferred color for the item'
    )
    
    special_requirements = fields.Text(
        string='Special Requirements',
        help='Special requirements for this line item'
    )
    
    @api.onchange('product_id')
    def _onchange_product_id(self):
        """Override to set kids clothing specific fields"""
        result = super()._onchange_product_id()
        if self.product_id and self.product_id.is_kids_clothing:
            # Set default values for kids clothing products
            self.child_size = self.product_id.size_variants[0].size if self.product_id.size_variants else ''
        return result