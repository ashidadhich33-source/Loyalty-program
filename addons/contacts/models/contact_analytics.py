# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Contacts - Contact Analytics Management
========================================================

Standalone version of the contact analytics management model.
"""

from core_framework.orm import BaseModel, CharField, TextField, BooleanField, IntegerField, DateTimeField, Many2OneField, SelectionField, FloatField, DateField
from core_framework.orm import Field
from typing import Dict, Any, Optional
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class ContactAnalytics(BaseModel):
    """Contact analytics model for Kids Clothing ERP"""
    
    _name = 'contact.analytics'
    _description = 'Contact Analytics'
    _table = 'contact_analytics'
    
    # Basic analytics information
    contact_id = IntegerField(
        string='Contact ID',
        required=True,
        help='Contact this analytics belongs to'
    )
    
    analytics_type = SelectionField(
        string='Analytics Type',
        selection=[
            ('sales', 'Sales Analytics'),
            ('communication', 'Communication Analytics'),
            ('engagement', 'Engagement Analytics'),
            ('loyalty', 'Loyalty Analytics'),
            ('preferences', 'Preferences Analytics'),
            ('custom', 'Custom Analytics'),
        ],
        required=True,
        help='Type of analytics'
    )
    
    # Analytics period
    date_from = DateField(
        string='From Date',
        required=True,
        help='Start date of analytics period'
    )
    
    date_to = DateField(
        string='To Date',
        required=True,
        help='End date of analytics period'
    )
    
    # Sales analytics
    total_orders = IntegerField(
        string='Total Orders',
        default=0,
        help='Total number of orders'
    )
    
    total_sales = FloatField(
        string='Total Sales',
        default=0.0,
        help='Total sales amount'
    )
    
    average_order_value = FloatField(
        string='Average Order Value',
        default=0.0,
        help='Average order value'
    )
    
    last_order_date = DateField(
        string='Last Order Date',
        help='Date of last order'
    )
    
    # Communication analytics
    total_communications = IntegerField(
        string='Total Communications',
        default=0,
        help='Total number of communications'
    )
    
    email_count = IntegerField(
        string='Email Count',
        default=0,
        help='Number of emails'
    )
    
    phone_count = IntegerField(
        string='Phone Count',
        default=0,
        help='Number of phone calls'
    )
    
    sms_count = IntegerField(
        string='SMS Count',
        default=0,
        help='Number of SMS'
    )
    
    # Engagement analytics
    engagement_score = FloatField(
        string='Engagement Score',
        default=0.0,
        help='Engagement score (0-100)'
    )
    
    response_rate = FloatField(
        string='Response Rate (%)',
        default=0.0,
        help='Response rate percentage'
    )
    
    satisfaction_score = FloatField(
        string='Satisfaction Score',
        default=0.0,
        help='Customer satisfaction score (0-5)'
    )
    
    # Loyalty analytics
    loyalty_points = IntegerField(
        string='Loyalty Points',
        default=0,
        help='Loyalty points earned'
    )
    
    loyalty_level = SelectionField(
        string='Loyalty Level',
        selection=[
            ('bronze', 'Bronze'),
            ('silver', 'Silver'),
            ('gold', 'Gold'),
            ('platinum', 'Platinum'),
        ],
        help='Loyalty level'
    )
    
    # Preferences analytics
    preferred_categories = TextField(
        string='Preferred Categories',
        help='Preferred product categories'
    )
    
    preferred_brands = TextField(
        string='Preferred Brands',
        help='Preferred brands'
    )
    
    preferred_colors = TextField(
        string='Preferred Colors',
        help='Preferred colors'
    )
    
    # Analytics status
    is_processed = BooleanField(
        string='Processed',
        default=False,
        help='Whether analytics has been processed'
    )
    
    processed_date = DateTimeField(
        string='Processed Date',
        help='Date when analytics was processed'
    )
    
    # Company relationship
    company_id = IntegerField(
        string='Company ID',
        default=1,
        help='Company this analytics belongs to'
    )
    
    def create(self, vals: Dict[str, Any]):
        """Override create to set default values"""
        return super().create(vals)
    
    def write(self, vals: Dict[str, Any]):
        """Override write to handle analytics updates"""
        result = super().write(vals)
        
        # Log analytics updates
        for analytics in self:
            if vals:
                logger.info(f"Analytics for contact {analytics.contact_id} updated: {', '.join(vals.keys())}")
        
        return result
    
    def action_process(self):
        """Process analytics data"""
        self.ensure_one()
        
        # In standalone version, we'll do basic processing
        self.is_processed = True
        self.processed_date = datetime.now()
        
        logger.info(f"Analytics for contact {self.contact_id} processed")
        return True
    
    def get_analytics_summary(self):
        """Get analytics summary"""
        return {
            'analytics_type': self.analytics_type,
            'date_from': self.date_from,
            'date_to': self.date_to,
            'total_orders': self.total_orders,
            'total_sales': self.total_sales,
            'average_order_value': self.average_order_value,
            'last_order_date': self.last_order_date,
            'total_communications': self.total_communications,
            'engagement_score': self.engagement_score,
            'response_rate': self.response_rate,
            'satisfaction_score': self.satisfaction_score,
            'loyalty_points': self.loyalty_points,
            'loyalty_level': self.loyalty_level,
            'is_processed': self.is_processed,
        }
    
    @classmethod
    def get_analytics_by_contact(cls, contact_id: int, analytics_type: str = None):
        """Get analytics by contact"""
        domain = [('contact_id', '=', contact_id)]
        if analytics_type:
            domain.append(('analytics_type', '=', analytics_type))
        
        return cls.search(domain, order='date_to desc')
    
    @classmethod
    def get_analytics_by_type(cls, analytics_type: str):
        """Get analytics by type"""
        return cls.search([
            ('analytics_type', '=', analytics_type),
        ], order='date_to desc')
    
    @classmethod
    def get_analytics_by_period(cls, date_from: str, date_to: str):
        """Get analytics by period"""
        return cls.search([
            ('date_from', '>=', date_from),
            ('date_to', '<=', date_to),
        ], order='date_to desc')
    
    @classmethod
    def get_processed_analytics(cls, contact_id: int):
        """Get processed analytics for contact"""
        return cls.search([
            ('contact_id', '=', contact_id),
            ('is_processed', '=', True),
        ], order='date_to desc')
    
    @classmethod
    def get_analytics_summary_by_contact(cls, contact_id: int):
        """Get analytics summary for contact"""
        analytics = cls.search([('contact_id', '=', contact_id)])
        
        if not analytics:
            return {
                'total_orders': 0,
                'total_sales': 0.0,
                'average_order_value': 0.0,
                'total_communications': 0,
                'engagement_score': 0.0,
                'response_rate': 0.0,
                'satisfaction_score': 0.0,
                'loyalty_points': 0,
                'loyalty_level': 'bronze',
            }
        
        # Calculate totals
        total_orders = sum(a.total_orders for a in analytics)
        total_sales = sum(a.total_sales for a in analytics)
        total_communications = sum(a.total_communications for a in analytics)
        total_loyalty_points = sum(a.loyalty_points for a in analytics)
        
        # Calculate averages
        average_order_value = total_sales / total_orders if total_orders > 0 else 0.0
        engagement_score = sum(a.engagement_score for a in analytics) / len(analytics) if analytics else 0.0
        response_rate = sum(a.response_rate for a in analytics) / len(analytics) if analytics else 0.0
        satisfaction_score = sum(a.satisfaction_score for a in analytics) / len(analytics) if analytics else 0.0
        
        # Determine loyalty level
        if total_loyalty_points >= 10000:
            loyalty_level = 'platinum'
        elif total_loyalty_points >= 5000:
            loyalty_level = 'gold'
        elif total_loyalty_points >= 2000:
            loyalty_level = 'silver'
        else:
            loyalty_level = 'bronze'
        
        return {
            'total_orders': total_orders,
            'total_sales': total_sales,
            'average_order_value': average_order_value,
            'total_communications': total_communications,
            'engagement_score': engagement_score,
            'response_rate': response_rate,
            'satisfaction_score': satisfaction_score,
            'loyalty_points': total_loyalty_points,
            'loyalty_level': loyalty_level,
        }
    
    @classmethod
    def get_analytics_analytics(cls):
        """Get analytics analytics"""
        # In standalone version, we'll return mock data
        return {
            'total_analytics': 0,
            'processed_analytics': 0,
            'by_type': {},
            'unprocessed_analytics': 0,
            'processed_percentage': 0,
        }
    
    def _check_dates(self):
        """Validate analytics dates"""
        if self.date_from and self.date_to:
            if self.date_from >= self.date_to:
                raise ValueError('From date must be before to date')
    
    def _check_scores(self):
        """Validate scores"""
        if self.engagement_score < 0 or self.engagement_score > 100:
            raise ValueError('Engagement score must be between 0 and 100')
        
        if self.response_rate < 0 or self.response_rate > 100:
            raise ValueError('Response rate must be between 0 and 100')
        
        if self.satisfaction_score < 0 or self.satisfaction_score > 5:
            raise ValueError('Satisfaction score must be between 0 and 5')
    
    def action_duplicate(self):
        """Duplicate analytics"""
        self.ensure_one()
        
        new_analytics = self.copy({
            'is_processed': False,
            'processed_date': None,
        })
        
        return new_analytics
    
    def action_export_analytics(self):
        """Export analytics data"""
        self.ensure_one()
        
        return {
            'contact_id': self.contact_id,
            'analytics_type': self.analytics_type,
            'date_from': self.date_from,
            'date_to': self.date_to,
            'total_orders': self.total_orders,
            'total_sales': self.total_sales,
            'average_order_value': self.average_order_value,
            'last_order_date': self.last_order_date,
            'total_communications': self.total_communications,
            'email_count': self.email_count,
            'phone_count': self.phone_count,
            'sms_count': self.sms_count,
            'engagement_score': self.engagement_score,
            'response_rate': self.response_rate,
            'satisfaction_score': self.satisfaction_score,
            'loyalty_points': self.loyalty_points,
            'loyalty_level': self.loyalty_level,
            'preferred_categories': self.preferred_categories,
            'preferred_brands': self.preferred_brands,
            'preferred_colors': self.preferred_colors,
        }
    
    def action_import_analytics(self, analytics_data: Dict[str, Any]):
        """Import analytics data"""
        self.ensure_one()
        
        self.write(analytics_data)
        return True