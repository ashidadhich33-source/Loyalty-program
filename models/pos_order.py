# -*- coding: utf-8 -*-

from odoo import models, fields, api


class PosOrder(models.Model):
    _inherit = 'pos.order'

    # Kids Clothing specific fields
    is_kids_clothing_pos = fields.Boolean(
        string='Kids Clothing POS',
        help='Check if this is a kids clothing POS order'
    )
    
    child_name = fields.Char(
        string='Child Name',
        help='Name of the child for whom the order is placed'
    )
    
    child_age = fields.Integer(
        string='Child Age',
        help='Age of the child'
    )
    
    # Customer preferences
    customer_preferences = fields.Text(
        string='Customer Preferences',
        help='Customer preferences and notes'
    )
    
    # Gift information
    is_gift = fields.Boolean(
        string='Is Gift',
        help='Check if this is a gift purchase'
    )
    
    gift_recipient = fields.Char(
        string='Gift Recipient',
        help='Name of the gift recipient'
    )
    
    gift_message = fields.Text(
        string='Gift Message',
        help='Gift message for the recipient'
    )
    
    # Loyalty program
    loyalty_points_earned = fields.Integer(
        string='Loyalty Points Earned',
        compute='_compute_loyalty_points_earned',
        store=True
    )
    
    loyalty_points_used = fields.Integer(
        string='Loyalty Points Used',
        default=0
    )
    
    # Exchange/Return information
    is_exchange = fields.Boolean(
        string='Is Exchange',
        help='Check if this is an exchange order'
    )
    
    original_order_id = fields.Many2one(
        'pos.order',
        string='Original Order',
        help='Original order for exchange'
    )
    
    exchange_reason = fields.Selection([
        ('size', 'Wrong Size'),
        ('color', 'Wrong Color'),
        ('style', 'Style Change'),
        ('defect', 'Product Defect'),
        ('other', 'Other'),
    ], string='Exchange Reason')
    
    @api.depends('amount_total')
    def _compute_loyalty_points_earned(self):
        """Calculate loyalty points earned based on order total"""
        for order in self:
            if order.is_kids_clothing_pos:
                # 1 point per dollar spent
                order.loyalty_points_earned = int(order.amount_total)
            else:
                order.loyalty_points_earned = 0
    
    @api.model
    def create(self, vals):
        """Override create to set default values for kids clothing POS orders"""
        if vals.get('is_kids_clothing_pos'):
            vals.setdefault('state', 'draft')
        return super().create(vals)
    
    def action_pos_order_paid(self):
        """Override to update customer loyalty points"""
        result = super().action_pos_order_paid()
        for order in self:
            if order.is_kids_clothing_pos and order.partner_id:
                # Update customer loyalty points
                order.partner_id.loyalty_points += order.loyalty_points_earned
        return result


class PosOrderLine(models.Model):
    _inherit = 'pos.order.line'

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
    
    # Exchange/Return information
    is_exchange = fields.Boolean(
        string='Is Exchange',
        help='Check if this is an exchange item'
    )
    
    original_line_id = fields.Many2one(
        'pos.order.line',
        string='Original Line',
        help='Original line item for exchange'
    )
    
    exchange_reason = fields.Selection([
        ('size', 'Wrong Size'),
        ('color', 'Wrong Color'),
        ('style', 'Style Change'),
        ('defect', 'Product Defect'),
        ('other', 'Other'),
    ], string='Exchange Reason')
    
    @api.onchange('product_id')
    def _onchange_product_id(self):
        """Override to set kids clothing specific fields"""
        result = super()._onchange_product_id()
        if self.product_id and self.product_id.is_kids_clothing:
            # Set default values for kids clothing products
            self.child_size = self.product_id.size_variants[0].size if self.product_id.size_variants else ''
        return result