# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    # Kids Clothing specific fields
    is_kids_clothing_customer = fields.Boolean(
        string='Kids Clothing Customer',
        help='Check if this partner is a kids clothing customer'
    )
    
    child_age = fields.Integer(
        string='Child Age',
        help='Age of the child for size recommendations'
    )
    
    preferred_brand = fields.Char(
        string='Preferred Brand',
        help='Customer preferred clothing brand'
    )
    
    size_preference = fields.Selection([
        ('xs', 'XS (2-4 years)'),
        ('s', 'S (4-6 years)'),
        ('m', 'M (6-8 years)'),
        ('l', 'L (8-10 years)'),
        ('xl', 'XL (10-12 years)'),
    ], string='Size Preference', help='Preferred clothing size')
    
    clothing_style = fields.Selection([
        ('casual', 'Casual'),
        ('formal', 'Formal'),
        ('sport', 'Sport'),
        ('party', 'Party'),
        ('school', 'School'),
    ], string='Clothing Style', help='Preferred clothing style')
    
    # Customer loyalty program
    loyalty_points = fields.Integer(
        string='Loyalty Points',
        default=0,
        help='Customer loyalty points'
    )
    
    loyalty_tier = fields.Selection([
        ('bronze', 'Bronze'),
        ('silver', 'Silver'),
        ('gold', 'Gold'),
        ('platinum', 'Platinum'),
    ], string='Loyalty Tier', default='bronze')
    
    # Purchase history
    total_purchases = fields.Float(
        string='Total Purchases',
        compute='_compute_total_purchases',
        store=True
    )
    
    last_purchase_date = fields.Date(
        string='Last Purchase Date',
        compute='_compute_last_purchase_date',
        store=True
    )
    
    @api.depends('sale_order_ids.amount_total')
    def _compute_total_purchases(self):
        for partner in self:
            partner.total_purchases = sum(
                order.amount_total for order in partner.sale_order_ids
                if order.state in ['sale', 'done']
            )
    
    @api.depends('sale_order_ids.date_order')
    def _compute_last_purchase_date(self):
        for partner in self:
            orders = partner.sale_order_ids.filtered(
                lambda o: o.state in ['sale', 'done']
            ).sorted('date_order', reverse=True)
            partner.last_purchase_date = orders[0].date_order if orders else False
    
    @api.model
    def create(self, vals):
        """Override create to set default values for kids clothing customers"""
        if vals.get('is_kids_clothing_customer'):
            vals.setdefault('loyalty_tier', 'bronze')
        return super().create(vals)
    
    def action_view_sales(self):
        """Action to view customer sales orders"""
        action = self.env.ref('sale.action_orders').read()[0]
        action['domain'] = [('partner_id', '=', self.id)]
        action['context'] = {'default_partner_id': self.id}
        return action