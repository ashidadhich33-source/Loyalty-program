# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime, timedelta


class PosSession(models.Model):
    _inherit = 'pos.session'

    # Kids Clothing specific session fields
    total_loyalty_points_earned = fields.Integer(
        string='Total Loyalty Points Earned',
        compute='_compute_loyalty_points',
        store=True,
        help='Total loyalty points earned in this session'
    )
    
    total_loyalty_points_used = fields.Integer(
        string='Total Loyalty Points Used',
        compute='_compute_loyalty_points',
        store=True,
        help='Total loyalty points used in this session'
    )
    
    gift_wraps_sold = fields.Integer(
        string='Gift Wraps Sold',
        compute='_compute_gift_wraps',
        store=True,
        help='Number of gift wraps sold in this session'
    )
    
    exchanges_processed = fields.Integer(
        string='Exchanges Processed',
        compute='_compute_exchanges',
        store=True,
        help='Number of exchanges processed in this session'
    )
    
    returns_processed = fields.Integer(
        string='Returns Processed',
        compute='_compute_returns',
        store=True,
        help='Number of returns processed in this session'
    )
    
    # Age group sales
    newborn_sales = fields.Float(
        string='Newborn Sales',
        compute='_compute_age_group_sales',
        store=True,
        help='Sales for newborn products (0-3 months)'
    )
    
    infant_sales = fields.Float(
        string='Infant Sales',
        compute='_compute_age_group_sales',
        store=True,
        help='Sales for infant products (3-12 months)'
    )
    
    toddler_sales = fields.Float(
        string='Toddler Sales',
        compute='_compute_age_group_sales',
        store=True,
        help='Sales for toddler products (1-3 years)'
    )
    
    preschool_sales = fields.Float(
        string='Preschool Sales',
        compute='_compute_age_group_sales',
        store=True,
        help='Sales for preschool products (3-5 years)'
    )
    
    child_sales = fields.Float(
        string='Child Sales',
        compute='_compute_age_group_sales',
        store=True,
        help='Sales for child products (5-12 years)'
    )
    
    teen_sales = fields.Float(
        string='Teen Sales',
        compute='_compute_age_group_sales',
        store=True,
        help='Sales for teen products (12+ years)'
    )
    
    # Gender sales
    boys_sales = fields.Float(
        string='Boys Sales',
        compute='_compute_gender_sales',
        store=True,
        help='Sales for boys products'
    )
    
    girls_sales = fields.Float(
        string='Girls Sales',
        compute='_compute_gender_sales',
        store=True,
        help='Sales for girls products'
    )
    
    unisex_sales = fields.Float(
        string='Unisex Sales',
        compute='_compute_gender_sales',
        store=True,
        help='Sales for unisex products'
    )
    
    # Seasonal sales
    spring_sales = fields.Float(
        string='Spring Sales',
        compute='_compute_seasonal_sales',
        store=True,
        help='Sales for spring products'
    )
    
    summer_sales = fields.Float(
        string='Summer Sales',
        compute='_compute_seasonal_sales',
        store=True,
        help='Sales for summer products'
    )
    
    fall_sales = fields.Float(
        string='Fall Sales',
        compute='_compute_seasonal_sales',
        store=True,
        help='Sales for fall products'
    )
    
    winter_sales = fields.Float(
        string='Winter Sales',
        compute='_compute_seasonal_sales',
        store=True,
        help='Sales for winter products'
    )
    
    @api.depends('order_ids.loyalty_points_earned', 'order_ids.loyalty_points_used')
    def _compute_loyalty_points(self):
        """Compute total loyalty points earned and used"""
        for session in self:
            session.total_loyalty_points_earned = sum(
                order.loyalty_points_earned for order in session.order_ids
            )
            session.total_loyalty_points_used = sum(
                order.loyalty_points_used for order in session.order_ids
            )
    
    @api.depends('order_ids.gift_wrap_applied')
    def _compute_gift_wraps(self):
        """Compute total gift wraps sold"""
        for session in self:
            session.gift_wraps_sold = len(
                session.order_ids.filtered('gift_wrap_applied')
            )
    
    @api.depends('order_ids.is_exchange')
    def _compute_exchanges(self):
        """Compute total exchanges processed"""
        for session in self:
            session.exchanges_processed = len(
                session.order_ids.filtered('is_exchange')
            )
    
    @api.depends('order_ids.is_return')
    def _compute_returns(self):
        """Compute total returns processed"""
        for session in self:
            session.returns_processed = len(
                session.order_ids.filtered('is_return')
            )
    
    @api.depends('order_ids.amount_total', 'order_ids.order_line.product_id')
    def _compute_age_group_sales(self):
        """Compute sales by age group"""
        for session in self:
            session.newborn_sales = 0.0
            session.infant_sales = 0.0
            session.toddler_sales = 0.0
            session.preschool_sales = 0.0
            session.child_sales = 0.0
            session.teen_sales = 0.0
            
            for order in session.order_ids:
                for line in order.order_line:
                    if line.product_id.is_kids_clothing:
                        age_range = line.product_id.age_range
                        if age_range:
                            if '0-3' in age_range or 'newborn' in age_range.lower():
                                session.newborn_sales += line.price_subtotal
                            elif '3-12' in age_range or 'infant' in age_range.lower():
                                session.infant_sales += line.price_subtotal
                            elif '1-3' in age_range or 'toddler' in age_range.lower():
                                session.toddler_sales += line.price_subtotal
                            elif '3-5' in age_range or 'preschool' in age_range.lower():
                                session.preschool_sales += line.price_subtotal
                            elif '5-12' in age_range or 'child' in age_range.lower():
                                session.child_sales += line.price_subtotal
                            elif '12+' in age_range or 'teen' in age_range.lower():
                                session.teen_sales += line.price_subtotal
    
    @api.depends('order_ids.amount_total', 'order_ids.order_line.product_id')
    def _compute_gender_sales(self):
        """Compute sales by gender"""
        for session in self:
            session.boys_sales = 0.0
            session.girls_sales = 0.0
            session.unisex_sales = 0.0
            
            for order in session.order_ids:
                for line in order.order_line:
                    if line.product_id.is_kids_clothing:
                        gender = line.product_id.gender
                        if gender == 'boys':
                            session.boys_sales += line.price_subtotal
                        elif gender == 'girls':
                            session.girls_sales += line.price_subtotal
                        else:
                            session.unisex_sales += line.price_subtotal
    
    @api.depends('order_ids.amount_total', 'order_ids.order_line.product_id')
    def _compute_seasonal_sales(self):
        """Compute sales by season"""
        for session in self:
            session.spring_sales = 0.0
            session.summer_sales = 0.0
            session.fall_sales = 0.0
            session.winter_sales = 0.0
            
            for order in session.order_ids:
                for line in order.order_line:
                    if line.product_id.is_kids_clothing:
                        season = line.product_id.season
                        if season == 'spring':
                            session.spring_sales += line.price_subtotal
                        elif season == 'summer':
                            session.summer_sales += line.price_subtotal
                        elif season == 'fall':
                            session.fall_sales += line.price_subtotal
                        elif season == 'winter':
                            session.winter_sales += line.price_subtotal
    
    def get_session_analytics(self):
        """Get comprehensive session analytics"""
        return {
            'loyalty_points': {
                'earned': self.total_loyalty_points_earned,
                'used': self.total_loyalty_points_used,
                'net': self.total_loyalty_points_earned - self.total_loyalty_points_used,
            },
            'gift_services': {
                'wraps_sold': self.gift_wraps_sold,
                'exchanges': self.exchanges_processed,
                'returns': self.returns_processed,
            },
            'age_group_sales': {
                'newborn': self.newborn_sales,
                'infant': self.infant_sales,
                'toddler': self.toddler_sales,
                'preschool': self.preschool_sales,
                'child': self.child_sales,
                'teen': self.teen_sales,
            },
            'gender_sales': {
                'boys': self.boys_sales,
                'girls': self.girls_sales,
                'unisex': self.unisex_sales,
            },
            'seasonal_sales': {
                'spring': self.spring_sales,
                'summer': self.summer_sales,
                'fall': self.fall_sales,
                'winter': self.winter_sales,
            },
        }