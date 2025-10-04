#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Analytics Metric Model
==========================================

Analytics metric management for data analysis.
"""

from core_framework.orm import (
    BaseModel, CharField, TextField, SelectionField, Many2OneField,
    BooleanField, One2ManyField, IntegerField, FloatField
)
from addons.core_base.models.base_mixins import KidsClothingMixin


class AnalyticsMetric(BaseModel, KidsClothingMixin):
    """Analytics Metric Model"""
    
    _name = 'analytics.metric'
    _description = 'Analytics Metric'
    _order = 'sequence, name'
    
    # Basic Information
    name = CharField('Metric Name', required=True, size=200)
    description = TextField('Description')
    code = CharField('Metric Code', required=True, size=50)
    
    # Metric Configuration
    metric_type = SelectionField([
        ('sum', 'Sum'),
        ('avg', 'Average'),
        ('count', 'Count'),
        ('min', 'Minimum'),
        ('max', 'Maximum'),
        ('median', 'Median'),
        ('std_dev', 'Standard Deviation'),
        ('variance', 'Variance'),
        ('custom', 'Custom Formula'),
    ], 'Metric Type', required=True)
    
    # Data Configuration
    fact_id = Many2OneField('analytics.fact', 'Fact', required=True)
    formula = TextField('Custom Formula', help='Custom calculation formula')
    unit = CharField('Unit', size=50, help='Unit of measurement')
    
    # Model Relationship
    model_id = Many2OneField('analytics.model', 'Analytics Model', required=True)
    
    # Metric Settings
    sequence = IntegerField('Sequence', default=10)
    active = BooleanField('Active', default=True)
    
    # Display Configuration
    display_format = SelectionField([
        ('number', 'Number'),
        ('currency', 'Currency'),
        ('percentage', 'Percentage'),
        ('decimal', 'Decimal'),
        ('integer', 'Integer'),
    ], 'Display Format', default='number')
    
    decimal_places = IntegerField('Decimal Places', default=2)
    currency_symbol = CharField('Currency Symbol', size=10, default='₹')
    
    # Thresholds and Alerts
    warning_threshold = FloatField('Warning Threshold')
    critical_threshold = FloatField('Critical Threshold')
    alert_enabled = BooleanField('Alert Enabled', default=False)
    
    # Trend Analysis
    trend_period = SelectionField([
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('yearly', 'Yearly'),
    ], 'Trend Period', default='monthly')
    
    def calculate_metric(self, data=None):
        """Calculate metric value"""
        if not data:
            return 0
        
        if self.metric_type == 'sum':
            return sum(item.get('value', 0) for item in data)
        elif self.metric_type == 'avg':
            values = [item.get('value', 0) for item in data]
            return sum(values) / len(values) if values else 0
        elif self.metric_type == 'count':
            return len(data)
        elif self.metric_type == 'min':
            values = [item.get('value', 0) for item in data]
            return min(values) if values else 0
        elif self.metric_type == 'max':
            values = [item.get('value', 0) for item in data]
            return max(values) if values else 0
        elif self.metric_type == 'median':
            values = sorted([item.get('value', 0) for item in data])
            n = len(values)
            if n % 2 == 0:
                return (values[n//2 - 1] + values[n//2]) / 2
            else:
                return values[n//2]
        elif self.metric_type == 'custom':
            return self._evaluate_custom_formula(data)
        else:
            return 0
    
    def _evaluate_custom_formula(self, data):
        """Evaluate custom formula"""
        if not self.formula:
            return 0
        
        # Safe evaluation of custom formula
        local_vars = {
            'data': data,
            'sum': sum,
            'avg': lambda x: sum(x) / len(x) if x else 0,
            'count': len,
            'min': min,
            'max': max,
            'len': len,
        }
        
        try:
            return eval(self.formula, {}, local_vars)
        except:
            return 0
    
    def format_value(self, value):
        """Format metric value for display"""
        if self.display_format == 'currency':
            return f"{self.currency_symbol}{value:,.{self.decimal_places}f}"
        elif self.display_format == 'percentage':
            return f"{value:.{self.decimal_places}f}%"
        elif self.display_format == 'integer':
            return f"{int(value):,}"
        else:
            return f"{value:,.{self.decimal_places}f}"
    
    def get_trend_data(self, period_count=12):
        """Get trend data for the metric"""
        # Implementation for trend data
        return {
            'periods': [f"Period {i+1}" for i in range(period_count)],
            'values': [0] * period_count,  # Placeholder data
            'trend': 'stable',
            'change_percent': 0,
        }
    
    def check_thresholds(self, value):
        """Check if value exceeds thresholds"""
        alerts = []
        
        if self.alert_enabled:
            if self.critical_threshold and value >= self.critical_threshold:
                alerts.append({
                    'level': 'critical',
                    'message': f"{self.name} has reached critical threshold: {self.format_value(value)}",
                    'threshold': self.critical_threshold,
                })
            elif self.warning_threshold and value >= self.warning_threshold:
                alerts.append({
                    'level': 'warning',
                    'message': f"{self.name} has reached warning threshold: {self.format_value(value)}",
                    'threshold': self.warning_threshold,
                })
        
        return alerts
    
    def get_metric_summary(self):
        """Get metric summary"""
        return {
            'id': self.id,
            'name': self.name,
            'code': self.code,
            'type': self.metric_type,
            'unit': self.unit,
            'display_format': self.display_format,
            'alert_enabled': self.alert_enabled,
            'warning_threshold': self.warning_threshold,
            'critical_threshold': self.critical_threshold,
        }