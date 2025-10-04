#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Analytics KPI Model
======================================

Analytics KPI management for performance tracking.
"""

from core_framework.orm import (
    BaseModel, CharField, TextField, SelectionField, Many2OneField,
    BooleanField, IntegerField, FloatField
)
from addons.core_base.models.base_mixins import KidsClothingMixin


class AnalyticsKPI(BaseModel, KidsClothingMixin):
    """Analytics KPI Model"""
    
    _name = 'analytics.kpi'
    _description = 'Analytics KPI'
    _order = 'sequence, name'
    
    # Basic Information
    name = CharField('KPI Name', required=True, size=200)
    description = TextField('Description')
    code = CharField('KPI Code', required=True, size=50)
    
    # KPI Configuration
    metric_id = Many2OneField('analytics.metric', 'Metric', required=True)
    target_value = FloatField('Target Value', required=True)
    unit = CharField('Unit', size=50)
    
    # Model Relationship
    model_id = Many2OneField('analytics.model', 'Analytics Model', required=True)
    
    # KPI Settings
    sequence = IntegerField('Sequence', default=10)
    active = BooleanField('Active', default=True)
    
    # Performance Thresholds
    excellent_threshold = FloatField('Excellent Threshold', 
                                   help='Percentage above target for excellent performance')
    good_threshold = FloatField('Good Threshold', 
                               help='Percentage above target for good performance')
    warning_threshold = FloatField('Warning Threshold', 
                                  help='Percentage below target for warning')
    critical_threshold = FloatField('Critical Threshold', 
                                   help='Percentage below target for critical')
    
    # Alert Configuration
    alert_enabled = BooleanField('Alert Enabled', default=True)
    alert_frequency = SelectionField([
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
    ], 'Alert Frequency', default='daily')
    
    def calculate_performance(self, current_value):
        """Calculate KPI performance"""
        if self.target_value == 0:
            return 0
        
        performance_percent = (current_value / self.target_value) * 100
        return performance_percent
    
    def get_performance_status(self, current_value):
        """Get performance status based on current value"""
        performance = self.calculate_performance(current_value)
        
        if performance >= (100 + (self.excellent_threshold or 0)):
            return 'excellent'
        elif performance >= (100 + (self.good_threshold or 0)):
            return 'good'
        elif performance >= (100 - (self.warning_threshold or 0)):
            return 'warning'
        elif performance >= (100 - (self.critical_threshold or 0)):
            return 'critical'
        else:
            return 'poor'
    
    def get_kpi_summary(self):
        """Get KPI summary"""
        return {
            'id': self.id,
            'name': self.name,
            'code': self.code,
            'target_value': self.target_value,
            'unit': self.unit,
            'alert_enabled': self.alert_enabled,
            'alert_frequency': self.alert_frequency,
        }