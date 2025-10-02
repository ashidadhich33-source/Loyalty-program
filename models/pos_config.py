# -*- coding: utf-8 -*-

from odoo import models, fields, api


class PosConfig(models.Model):
    _inherit = 'pos.config'

    # Kids Clothing specific POS configuration
    enable_loyalty_program = fields.Boolean(
        string='Enable Loyalty Program',
        default=True,
        help='Enable loyalty points system for customers'
    )
    
    loyalty_points_per_currency = fields.Float(
        string='Loyalty Points per Currency Unit',
        default=1.0,
        help='Number of loyalty points earned per currency unit spent'
    )
    
    enable_gift_wrapping = fields.Boolean(
        string='Enable Gift Wrapping',
        default=True,
        help='Enable gift wrapping service'
    )
    
    gift_wrap_price = fields.Float(
        string='Gift Wrap Price',
        default=5.0,
        help='Price for gift wrapping service'
    )
    
    enable_exchange_return = fields.Boolean(
        string='Enable Exchange/Return',
        default=True,
        help='Enable exchange and return functionality'
    )
    
    exchange_return_days = fields.Integer(
        string='Exchange/Return Days',
        default=30,
        help='Number of days allowed for exchange/return'
    )
    
    # Age verification
    require_age_verification = fields.Boolean(
        string='Require Age Verification',
        default=False,
        help='Require age verification for certain products'
    )
    
    # Size recommendation
    enable_size_recommendation = fields.Boolean(
        string='Enable Size Recommendation',
        default=True,
        help='Enable size recommendation based on child age'
    )
    
    # Seasonal promotions
    enable_seasonal_promotions = fields.Boolean(
        string='Enable Seasonal Promotions',
        default=True,
        help='Enable seasonal promotion system'
    )
    
    # Multi-payment methods
    enable_multi_payment = fields.Boolean(
        string='Enable Multi-Payment',
        default=True,
        help='Allow multiple payment methods in single transaction'
    )
    
    # Customer information
    collect_child_info = fields.Boolean(
        string='Collect Child Information',
        default=True,
        help='Collect child information during checkout'
    )
    
    # Receipt customization
    receipt_template = fields.Selection([
        ('standard', 'Standard Receipt'),
        ('kids_friendly', 'Kids Friendly Receipt'),
        ('gift_receipt', 'Gift Receipt'),
    ], string='Receipt Template', default='kids_friendly')
    
    # Barcode scanning
    enable_barcode_scanning = fields.Boolean(
        string='Enable Barcode Scanning',
        default=True,
        help='Enable barcode scanning for products'
    )
    
    # Product recommendations
    enable_product_recommendations = fields.Boolean(
        string='Enable Product Recommendations',
        default=True,
        help='Show product recommendations based on purchase history'
    )
    
    @api.model
    def get_kids_clothing_config(self):
        """Get kids clothing specific configuration"""
        return {
            'loyalty_program': self.enable_loyalty_program,
            'loyalty_points_rate': self.loyalty_points_per_currency,
            'gift_wrapping': self.enable_gift_wrapping,
            'gift_wrap_price': self.gift_wrap_price,
            'exchange_return': self.enable_exchange_return,
            'exchange_return_days': self.exchange_return_days,
            'age_verification': self.require_age_verification,
            'size_recommendation': self.enable_size_recommendation,
            'seasonal_promotions': self.enable_seasonal_promotions,
            'multi_payment': self.enable_multi_payment,
            'child_info': self.collect_child_info,
            'receipt_template': self.receipt_template,
            'barcode_scanning': self.enable_barcode_scanning,
            'product_recommendations': self.enable_product_recommendations,
        }