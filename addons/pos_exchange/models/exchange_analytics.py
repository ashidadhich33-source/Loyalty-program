#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Exchange Analytics Model
===========================================

Exchange analytics and reporting for exchange performance.
"""

import logging
from datetime import datetime, timedelta
from core_framework.orm import BaseModel, CharField, TextField, BooleanField, IntegerField, DateTimeField, Many2OneField, SelectionField, FloatField, One2ManyField, Many2ManyField
from core_framework.exceptions import ValidationError

logger = logging.getLogger(__name__)

class ExchangeAnalytics(BaseModel):
    """Exchange analytics and performance metrics"""
    
    _name = 'exchange.analytics'
    _description = 'Exchange Analytics'
    _table = 'exchange_analytics'
    _order = 'date desc'
    
    # Basic Information
    name = CharField(
        string='Analytics Name',
        size=100,
        required=True,
        help='Name of the analytics record'
    )
    
    date = DateTimeField(
        string='Date',
        default=datetime.now,
        help='Date of analysis'
    )
    
    # Exchange Metrics
    total_exchanges = IntegerField(
        string='Total Exchanges',
        default=0,
        help='Total number of exchanges'
    )
    
    approved_exchanges = IntegerField(
        string='Approved Exchanges',
        default=0,
        help='Number of approved exchanges'
    )
    
    rejected_exchanges = IntegerField(
        string='Rejected Exchanges',
        default=0,
        help='Number of rejected exchanges'
    )
    
    pending_exchanges = IntegerField(
        string='Pending Exchanges',
        default=0,
        help='Number of pending exchanges'
    )
    
    # Exchange Types
    size_exchanges = IntegerField(
        string='Size Exchanges',
        default=0,
        help='Number of size exchanges'
    )
    
    color_exchanges = IntegerField(
        string='Color Exchanges',
        default=0,
        help='Number of color exchanges'
    )
    
    style_exchanges = IntegerField(
        string='Style Exchanges',
        default=0,
        help='Number of style exchanges'
    )
    
    age_group_exchanges = IntegerField(
        string='Age Group Exchanges',
        default=0,
        help='Number of age group exchanges'
    )
    
    product_exchanges = IntegerField(
        string='Product Exchanges',
        default=0,
        help='Number of product exchanges'
    )
    
    # Financial Metrics
    total_exchange_value = FloatField(
        string='Total Exchange Value',
        digits=(12, 2),
        default=0.0,
        help='Total value of exchanges'
    )
    
    average_exchange_value = FloatField(
        string='Average Exchange Value',
        digits=(10, 2),
        default=0.0,
        help='Average exchange value'
    )
    
    refund_amount = FloatField(
        string='Refund Amount',
        digits=(12, 2),
        default=0.0,
        help='Total refund amount'
    )
    
    additional_payment = FloatField(
        string='Additional Payment',
        digits=(12, 2),
        default=0.0,
        help='Total additional payment amount'
    )
    
    # Customer Metrics
    total_customers = IntegerField(
        string='Total Customers',
        default=0,
        help='Total number of customers with exchanges'
    )
    
    repeat_exchange_customers = IntegerField(
        string='Repeat Exchange Customers',
        default=0,
        help='Number of customers with multiple exchanges'
    )
    
    # Age Group Analysis
    newborn_exchanges = IntegerField(
        string='Newborn Exchanges',
        default=0,
        help='Exchanges for newborn age group'
    )
    
    infant_exchanges = IntegerField(
        string='Infant Exchanges',
        default=0,
        help='Exchanges for infant age group'
    )
    
    toddler_exchanges = IntegerField(
        string='Toddler Exchanges',
        default=0,
        help='Exchanges for toddler age group'
    )
    
    preschool_exchanges = IntegerField(
        string='Preschool Exchanges',
        default=0,
        help='Exchanges for preschool age group'
    )
    
    school_exchanges = IntegerField(
        string='School Exchanges',
        default=0,
        help='Exchanges for school age group'
    )
    
    teen_exchanges = IntegerField(
        string='Teen Exchanges',
        default=0,
        help='Exchanges for teen age group'
    )
    
    # Gender Analysis
    boys_exchanges = IntegerField(
        string='Boys Exchanges',
        default=0,
        help='Exchanges for boys'
    )
    
    girls_exchanges = IntegerField(
        string='Girls Exchanges',
        default=0,
        help='Exchanges for girls'
    )
    
    unisex_exchanges = IntegerField(
        string='Unisex Exchanges',
        default=0,
        help='Exchanges for unisex items'
    )
    
    # Approval Metrics
    approval_rate = FloatField(
        string='Approval Rate %',
        digits=(5, 2),
        default=0.0,
        help='Exchange approval rate percentage'
    )
    
    average_approval_time = FloatField(
        string='Average Approval Time (hours)',
        digits=(5, 2),
        default=0.0,
        help='Average time for approval in hours'
    )
    
    # Time Analysis
    exchanges_within_7_days = IntegerField(
        string='Exchanges within 7 days',
        default=0,
        help='Exchanges within 7 days of purchase'
    )
    
    exchanges_within_15_days = IntegerField(
        string='Exchanges within 15 days',
        default=0,
        help='Exchanges within 15 days of purchase'
    )
    
    exchanges_within_30_days = IntegerField(
        string='Exchanges within 30 days',
        default=0,
        help='Exchanges within 30 days of purchase'
    )
    
    # Top Exchange Products
    top_exchanged_products = TextField(
        string='Top Exchanged Products',
        help='Top exchanged products data'
    )
    
    top_exchange_reasons = TextField(
        string='Top Exchange Reasons',
        help='Top exchange reasons data'
    )
    
    # Status
    is_processed = BooleanField(
        string='Processed',
        default=False,
        help='Whether analytics has been processed'
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
        """Override create to calculate metrics"""
        result = super().create(vals)
        result._calculate_analytics()
        return result
    
    def write(self, vals):
        """Override write to recalculate metrics"""
        result = super().write(vals)
        if 'date' in vals:
            self._calculate_analytics()
        return result
    
    def _calculate_analytics(self):
        """Calculate analytics metrics"""
        for record in self:
            # Get exchanges for analysis
            exchanges = self.env['exchange.request'].search([])
            
            # Calculate basic metrics
            record.total_exchanges = len(exchanges)
            record.approved_exchanges = len([ex for ex in exchanges if ex.state == 'approved'])
            record.rejected_exchanges = len([ex for ex in exchanges if ex.state == 'rejected'])
            record.pending_exchanges = len([ex for ex in exchanges if ex.state in ['submitted', 'under_review']])
            
            # Calculate exchange types
            record.size_exchanges = len([ex for ex in exchanges if ex.exchange_type == 'size'])
            record.color_exchanges = len([ex for ex in exchanges if ex.exchange_type == 'color'])
            record.style_exchanges = len([ex for ex in exchanges if ex.exchange_type == 'style'])
            record.age_group_exchanges = len([ex for ex in exchanges if ex.exchange_type == 'age_group'])
            record.product_exchanges = len([ex for ex in exchanges if ex.exchange_type == 'product'])
            
            # Calculate financial metrics
            record.total_exchange_value = sum(ex.exchange_amount for ex in exchanges)
            record.average_exchange_value = record.total_exchange_value / max(record.total_exchanges, 1)
            record.refund_amount = sum(ex.difference_amount for ex in exchanges if ex.difference_amount > 0)
            record.additional_payment = sum(abs(ex.difference_amount) for ex in exchanges if ex.difference_amount < 0)
            
            # Calculate customer metrics
            customers = set(ex.partner_id.id for ex in exchanges if ex.partner_id)
            record.total_customers = len(customers)
            
            # Calculate age group exchanges
            record._calculate_age_group_exchanges(exchanges)
            
            # Calculate gender exchanges
            record._calculate_gender_exchanges(exchanges)
            
            # Calculate approval metrics
            if record.total_exchanges > 0:
                record.approval_rate = (record.approved_exchanges / record.total_exchanges) * 100
            
            # Calculate time analysis
            record._calculate_time_analysis(exchanges)
            
            record.is_processed = True
    
    def _calculate_age_group_exchanges(self, exchanges):
        """Calculate age group exchanges"""
        for record in self:
            age_group_counts = {
                'newborn': 0,
                'infant': 0,
                'toddler': 0,
                'preschool': 0,
                'school': 0,
                'teen': 0
            }
            
            for exchange in exchanges:
                for line in exchange.exchange_line_ids:
                    if line.original_product_id and hasattr(line.original_product_id, 'age_group'):
                        age_group = line.original_product_id.age_group
                        if age_group in age_group_counts:
                            age_group_counts[age_group] += 1
            
            record.newborn_exchanges = age_group_counts['newborn']
            record.infant_exchanges = age_group_counts['infant']
            record.toddler_exchanges = age_group_counts['toddler']
            record.preschool_exchanges = age_group_counts['preschool']
            record.school_exchanges = age_group_counts['school']
            record.teen_exchanges = age_group_counts['teen']
    
    def _calculate_gender_exchanges(self, exchanges):
        """Calculate gender exchanges"""
        for record in self:
            gender_counts = {
                'boys': 0,
                'girls': 0,
                'unisex': 0
            }
            
            for exchange in exchanges:
                for line in exchange.exchange_line_ids:
                    if line.original_product_id and hasattr(line.original_product_id, 'gender'):
                        gender = line.original_product_id.gender
                        if gender in gender_counts:
                            gender_counts[gender] += 1
            
            record.boys_exchanges = gender_counts['boys']
            record.girls_exchanges = gender_counts['girls']
            record.unisex_exchanges = gender_counts['unisex']
    
    def _calculate_time_analysis(self, exchanges):
        """Calculate time analysis"""
        for record in self:
            now = datetime.now()
            
            for exchange in exchanges:
                if exchange.original_order_id:
                    days_diff = (now - exchange.original_order_id.create_date).days
                    
                    if days_diff <= 7:
                        record.exchanges_within_7_days += 1
                    if days_diff <= 15:
                        record.exchanges_within_15_days += 1
                    if days_diff <= 30:
                        record.exchanges_within_30_days += 1
    
    def get_analytics_summary(self):
        """Get analytics summary"""
        return {
            'exchange_summary': {
                'total_exchanges': self.total_exchanges,
                'approved_exchanges': self.approved_exchanges,
                'rejected_exchanges': self.rejected_exchanges,
                'pending_exchanges': self.pending_exchanges
            },
            'exchange_types': {
                'size': self.size_exchanges,
                'color': self.color_exchanges,
                'style': self.style_exchanges,
                'age_group': self.age_group_exchanges,
                'product': self.product_exchanges
            },
            'financial_summary': {
                'total_value': self.total_exchange_value,
                'average_value': self.average_exchange_value,
                'refund_amount': self.refund_amount,
                'additional_payment': self.additional_payment
            },
            'customer_summary': {
                'total_customers': self.total_customers,
                'repeat_customers': self.repeat_exchange_customers
            },
            'age_group_summary': {
                'newborn': self.newborn_exchanges,
                'infant': self.infant_exchanges,
                'toddler': self.toddler_exchanges,
                'preschool': self.preschool_exchanges,
                'school': self.school_exchanges,
                'teen': self.teen_exchanges
            },
            'gender_summary': {
                'boys': self.boys_exchanges,
                'girls': self.girls_exchanges,
                'unisex': self.unisex_exchanges
            },
            'approval_summary': {
                'approval_rate': self.approval_rate,
                'average_approval_time': self.average_approval_time
            },
            'time_summary': {
                'within_7_days': self.exchanges_within_7_days,
                'within_15_days': self.exchanges_within_15_days,
                'within_30_days': self.exchanges_within_30_days
            }
        }
    
    def action_generate_report(self):
        """Generate detailed analytics report"""
        return {
            'type': 'ocean.actions.act_window',
            'name': f'Exchange Analytics Report - {self.name}',
            'res_model': 'exchange.analytics',
            'view_mode': 'form',
            'res_id': self.id,
            'context': {'report_mode': True}
        }