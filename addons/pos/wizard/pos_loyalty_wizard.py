# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - POS Loyalty Points Redemption Wizard
=======================================================

Loyalty points redemption wizard for POS transactions.
"""

from ocean import models, fields, api, _
from ocean.exceptions import ValidationError, UserError
import logging

_logger = logging.getLogger(__name__)


class PosLoyaltyWizard(models.TransientModel):
    """POS Loyalty Points Redemption Wizard"""
    
    _name = 'pos.loyalty.wizard'
    _description = 'POS Loyalty Points Redemption Wizard'
    
    # Order Information
    order_id = fields.Many2one(
        'pos.order',
        string='POS Order',
        required=True
    )
    
    # Customer Information
    customer_id = fields.Many2one(
        'contact.customer',
        string='Customer',
        related='order_id.partner_id',
        readonly=True
    )
    
    customer_name = fields.Char(
        string='Customer Name',
        related='customer_id.name',
        readonly=True
    )
    
    # Loyalty Information
    available_points = fields.Integer(
        string='Available Points',
        compute='_compute_loyalty_info',
        readonly=True
    )
    
    loyalty_level = fields.Selection([
        ('bronze', 'Bronze'),
        ('silver', 'Silver'),
        ('gold', 'Gold'),
        ('platinum', 'Platinum'),
    ], string='Loyalty Level', compute='_compute_loyalty_info', readonly=True)
    
    points_rate = fields.Float(
        string='Points Rate',
        default=100.0,
        help='Points required per rupee discount (e.g., 100 points = 1 rupee)'
    )
    
    max_discount = fields.Float(
        string='Maximum Discount',
        compute='_compute_loyalty_info',
        readonly=True
    )
    
    # Redemption Details
    points_to_redeem = fields.Integer(
        string='Points to Redeem',
        default=0,
        help='Number of points to redeem'
    )
    
    discount_amount = fields.Float(
        string='Discount Amount',
        compute='_compute_discount_amount',
        readonly=True,
        help='Discount amount from points redemption'
    )
    
    order_total = fields.Float(
        string='Order Total',
        related='order_id.amount_total',
        readonly=True
    )
    
    final_amount = fields.Float(
        string='Final Amount',
        compute='_compute_final_amount',
        readonly=True
    )
    
    # Quick Redemption Options
    quick_redeem_100 = fields.Boolean(
        string='Redeem 100 Points',
        default=False
    )
    
    quick_redeem_500 = fields.Boolean(
        string='Redeem 500 Points',
        default=False
    )
    
    quick_redeem_1000 = fields.Boolean(
        string='Redeem 1000 Points',
        default=False
    )
    
    quick_redeem_max = fields.Boolean(
        string='Redeem Maximum Points',
        default=False
    )
    
    @api.depends('customer_id')
    def _compute_loyalty_info(self):
        """Compute customer loyalty information"""
        for wizard in self:
            if wizard.customer_id:
                wizard.available_points = wizard.customer_id.loyalty_points
                wizard.loyalty_level = wizard.customer_id.loyalty_level
                wizard.max_discount = wizard.available_points / wizard.points_rate
            else:
                wizard.available_points = 0
                wizard.loyalty_level = False
                wizard.max_discount = 0.0
    
    @api.depends('points_to_redeem', 'points_rate')
    def _compute_discount_amount(self):
        """Compute discount amount from points"""
        for wizard in self:
            if wizard.points_to_redeem > 0:
                wizard.discount_amount = wizard.points_to_redeem / wizard.points_rate
            else:
                wizard.discount_amount = 0.0
    
    @api.depends('order_total', 'discount_amount')
    def _compute_final_amount(self):
        """Compute final order amount after discount"""
        for wizard in self:
            wizard.final_amount = wizard.order_total - wizard.discount_amount
    
    @api.onchange('quick_redeem_100')
    def _onchange_quick_redeem_100(self):
        """Quick redeem 100 points"""
        if self.quick_redeem_100:
            self.points_to_redeem = 100
            self.quick_redeem_500 = False
            self.quick_redeem_1000 = False
            self.quick_redeem_max = False
    
    @api.onchange('quick_redeem_500')
    def _onchange_quick_redeem_500(self):
        """Quick redeem 500 points"""
        if self.quick_redeem_500:
            self.points_to_redeem = 500
            self.quick_redeem_100 = False
            self.quick_redeem_1000 = False
            self.quick_redeem_max = False
    
    @api.onchange('quick_redeem_1000')
    def _onchange_quick_redeem_1000(self):
        """Quick redeem 1000 points"""
        if self.quick_redeem_1000:
            self.points_to_redeem = 1000
            self.quick_redeem_100 = False
            self.quick_redeem_500 = False
            self.quick_redeem_max = False
    
    @api.onchange('quick_redeem_max')
    def _onchange_quick_redeem_max(self):
        """Quick redeem maximum points"""
        if self.quick_redeem_max:
            self.points_to_redeem = self.available_points
            self.quick_redeem_100 = False
            self.quick_redeem_500 = False
            self.quick_redeem_1000 = False
    
    @api.constrains('points_to_redeem')
    def _check_points_to_redeem(self):
        """Validate points to redeem"""
        for wizard in self:
            if wizard.points_to_redeem < 0:
                raise ValidationError(_('Points to redeem cannot be negative.'))
            
            if wizard.points_to_redeem > wizard.available_points:
                raise ValidationError(_('Points to redeem cannot exceed available points.'))
            
            if wizard.points_to_redeem > 0 and wizard.discount_amount > wizard.order_total:
                raise ValidationError(_('Discount amount cannot exceed order total.'))
    
    def action_redeem_points(self):
        """Redeem loyalty points"""
        self.ensure_one()
        
        if not self.customer_id:
            raise UserError(_('Please select a customer to redeem loyalty points.'))
        
        if self.points_to_redeem <= 0:
            raise UserError(_('Please enter points to redeem.'))
        
        # Redeem points through order
        result = self.order_id.action_redeem_loyalty_points(self.points_to_redeem)
        
        # Close wizard
        return {
            'type': 'ir.actions.act_window_close',
            'context': {
                'loyalty_points_redeemed': True,
                'points_redeemed': self.points_to_redeem,
                'discount_amount': self.discount_amount
            }
        }
    
    def action_remove_points(self):
        """Remove loyalty points redemption"""
        self.ensure_one()
        
        result = self.order_id.action_remove_loyalty_points()
        
        # Close wizard
        return {
            'type': 'ir.actions.act_window_close',
            'context': {
                'loyalty_points_removed': True
            }
        }
    
    def action_cancel(self):
        """Cancel loyalty points redemption"""
        return {'type': 'ir.actions.act_window_close'}