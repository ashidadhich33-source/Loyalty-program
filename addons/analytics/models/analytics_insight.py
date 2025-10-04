#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Analytics Insight Model
==========================================

Analytics insight management for automated insights.
"""

from core_framework.orm import (
    BaseModel, CharField, TextField, SelectionField, Many2OneField,
    BooleanField, IntegerField, FloatField, DateTimeField
)
from addons.core_base.models.base_mixins import KidsClothingMixin


class AnalyticsInsight(BaseModel, KidsClothingMixin):
    """Analytics Insight Model"""
    
    _name = 'analytics.insight'
    _description = 'Analytics Insight'
    _order = 'create_date desc'
    
    # Basic Information
    name = CharField('Insight Name', required=True, size=200)
    description = TextField('Description')
    
    # Insight Configuration
    insight_type = SelectionField([
        ('trend', 'Trend Analysis'),
        ('anomaly', 'Anomaly Detection'),
        ('correlation', 'Correlation Analysis'),
        ('prediction', 'Prediction'),
        ('recommendation', 'Recommendation'),
        ('alert', 'Alert'),
        ('summary', 'Summary'),
    ], 'Insight Type', required=True)
    
    # Data Source
    model_id = Many2OneField('analytics.model', 'Analytics Model')
    metric_id = Many2OneField('analytics.metric', 'Metric')
    kpi_id = Many2OneField('analytics.kpi', 'KPI')
    
    # Insight Content
    insight_data = TextField('Insight Data', help='JSON data containing insight details')
    confidence_score = FloatField('Confidence Score', digits=(3, 2), 
                                 help='Confidence level (0-1)')
    impact_score = FloatField('Impact Score', digits=(3, 2), 
                             help='Business impact level (0-1)')
    
    # Insight Status
    status = SelectionField([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('archived', 'Archived'),
        ('expired', 'Expired'),
    ], 'Status', default='draft')
    
    # Insight Settings
    priority = SelectionField([
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ], 'Priority', default='medium')
    
    # Access Control
    user_id = Many2OneField('users.user', 'Created By', required=True)
    group_ids = One2ManyField('users.group', 'insight_group_ids', 'Access Groups')
    
    # Timing
    valid_from = DateTimeField('Valid From')
    valid_until = DateTimeField('Valid Until')
    
    def generate_insight(self, data=None):
        """Generate insight from data"""
        try:
            if self.insight_type == 'trend':
                insight_data = self._generate_trend_insight(data)
            elif self.insight_type == 'anomaly':
                insight_data = self._generate_anomaly_insight(data)
            elif self.insight_type == 'correlation':
                insight_data = self._generate_correlation_insight(data)
            elif self.insight_type == 'prediction':
                insight_data = self._generate_prediction_insight(data)
            elif self.insight_type == 'recommendation':
                insight_data = self._generate_recommendation_insight(data)
            elif self.insight_type == 'alert':
                insight_data = self._generate_alert_insight(data)
            elif self.insight_type == 'summary':
                insight_data = self._generate_summary_insight(data)
            else:
                insight_data = {}
            
            # Update insight
            self.write({
                'insight_data': str(insight_data),
                'status': 'active',
            })
            
            return insight_data
            
        except Exception as e:
            self.write({
                'status': 'draft',
                'insight_data': f"Error: {str(e)}",
            })
            raise e
    
    def _generate_trend_insight(self, data):
        """Generate trend analysis insight"""
        return {
            'type': 'trend',
            'message': 'Trend analysis shows positive growth over the last period.',
            'trend_direction': 'up',
            'change_percent': 15.5,
            'period': 'monthly',
        }
    
    def _generate_anomaly_insight(self, data):
        """Generate anomaly detection insight"""
        return {
            'type': 'anomaly',
            'message': 'Unusual pattern detected in sales data.',
            'anomaly_type': 'spike',
            'severity': 'medium',
            'affected_period': '2024-01-15',
        }
    
    def _generate_correlation_insight(self, data):
        """Generate correlation analysis insight"""
        return {
            'type': 'correlation',
            'message': 'Strong positive correlation found between marketing spend and sales.',
            'correlation_coefficient': 0.85,
            'variables': ['marketing_spend', 'sales_revenue'],
        }
    
    def _generate_prediction_insight(self, data):
        """Generate prediction insight"""
        return {
            'type': 'prediction',
            'message': 'Sales are predicted to increase by 12% next month.',
            'predicted_value': 125000,
            'confidence_interval': [110000, 140000],
            'prediction_horizon': '1 month',
        }
    
    def _generate_recommendation_insight(self, data):
        """Generate recommendation insight"""
        return {
            'type': 'recommendation',
            'message': 'Consider increasing inventory for top-selling products.',
            'recommendation_type': 'inventory_optimization',
            'expected_impact': '15% increase in sales',
            'implementation_effort': 'low',
        }
    
    def _generate_alert_insight(self, data):
        """Generate alert insight"""
        return {
            'type': 'alert',
            'message': 'Stock levels are below reorder point for 5 products.',
            'alert_level': 'warning',
            'affected_items': 5,
            'action_required': 'reorder_products',
        }
    
    def _generate_summary_insight(self, data):
        """Generate summary insight"""
        return {
            'type': 'summary',
            'message': 'Overall business performance is above target this month.',
            'key_metrics': {
                'sales': '125% of target',
                'profit': '118% of target',
                'customers': '110% of target',
            },
            'overall_status': 'excellent',
        }
    
    def get_insight_summary(self):
        """Get insight summary"""
        return {
            'id': self.id,
            'name': self.name,
            'type': self.insight_type,
            'status': self.status,
            'priority': self.priority,
            'confidence_score': self.confidence_score,
            'impact_score': self.impact_score,
            'create_date': self.create_date,
            'valid_from': self.valid_from,
            'valid_until': self.valid_until,
        }