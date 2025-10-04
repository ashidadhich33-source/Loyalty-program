#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Analytics Fact Model
=======================================

Analytics fact management for data analysis.
"""

from core_framework.orm import (
    BaseModel, CharField, TextField, SelectionField, Many2OneField,
    BooleanField, IntegerField
)
from addons.core_base.models.base_mixins import KidsClothingMixin


class AnalyticsFact(BaseModel, KidsClothingMixin):
    """Analytics Fact Model"""
    
    _name = 'analytics.fact'
    _description = 'Analytics Fact'
    _order = 'sequence, name'
    
    # Basic Information
    name = CharField('Fact Name', required=True, size=200)
    description = TextField('Description')
    code = CharField('Fact Code', required=True, size=50)
    
    # Fact Configuration
    field_name = CharField('Field Name', required=True, size=100, 
                          help='Field name in source model')
    data_type = SelectionField([
        ('integer', 'Integer'),
        ('float', 'Float'),
        ('currency', 'Currency'),
        ('percentage', 'Percentage'),
        ('count', 'Count'),
    ], 'Data Type', required=True)
    
    # Aggregation Configuration
    aggregation_type = SelectionField([
        ('sum', 'Sum'),
        ('avg', 'Average'),
        ('count', 'Count'),
        ('min', 'Minimum'),
        ('max', 'Maximum'),
        ('median', 'Median'),
        ('std_dev', 'Standard Deviation'),
    ], 'Aggregation Type', default='sum')
    
    # Model Relationship
    model_id = Many2OneField('analytics.model', 'Analytics Model', required=True)
    
    # Fact Settings
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
    
    def get_fact_values(self, source_data):
        """Get fact values from source data"""
        values = []
        
        for record in source_data:
            value = getattr(record, self.field_name, 0)
            if value is not None:
                values.append({
                    'value': float(value) if value else 0,
                    'record_id': record.id,
                })
        
        return values
    
    def aggregate_values(self, values):
        """Aggregate fact values"""
        if not values:
            return 0
        
        numeric_values = [item['value'] for item in values]
        
        if self.aggregation_type == 'sum':
            return sum(numeric_values)
        elif self.aggregation_type == 'avg':
            return sum(numeric_values) / len(numeric_values)
        elif self.aggregation_type == 'count':
            return len(numeric_values)
        elif self.aggregation_type == 'min':
            return min(numeric_values)
        elif self.aggregation_type == 'max':
            return max(numeric_values)
        elif self.aggregation_type == 'median':
            sorted_values = sorted(numeric_values)
            n = len(sorted_values)
            if n % 2 == 0:
                return (sorted_values[n//2 - 1] + sorted_values[n//2]) / 2
            else:
                return sorted_values[n//2]
        elif self.aggregation_type == 'std_dev':
            if len(numeric_values) < 2:
                return 0
            mean = sum(numeric_values) / len(numeric_values)
            variance = sum((x - mean) ** 2 for x in numeric_values) / len(numeric_values)
            return variance ** 0.5
        else:
            return 0
    
    def format_value(self, value):
        """Format fact value for display"""
        if self.display_format == 'currency':
            return f"{self.currency_symbol}{value:,.{self.decimal_places}f}"
        elif self.display_format == 'percentage':
            return f"{value:.{self.decimal_places}f}%"
        elif self.display_format == 'integer':
            return f"{int(value):,}"
        else:
            return f"{value:,.{self.decimal_places}f}"
    
    def get_fact_summary(self):
        """Get fact summary"""
        return {
            'id': self.id,
            'name': self.name,
            'code': self.code,
            'field_name': self.field_name,
            'data_type': self.data_type,
            'aggregation_type': self.aggregation_type,
            'display_format': self.display_format,
            'decimal_places': self.decimal_places,
        }