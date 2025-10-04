#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Analytics Dimension Model
============================================

Analytics dimension management for data analysis.
"""

from core_framework.orm import (
    BaseModel, CharField, TextField, SelectionField, Many2OneField,
    BooleanField, IntegerField
)
from addons.core_base.models.base_mixins import KidsClothingMixin


class AnalyticsDimension(BaseModel, KidsClothingMixin):
    """Analytics Dimension Model"""
    
    _name = 'analytics.dimension'
    _description = 'Analytics Dimension'
    _order = 'sequence, name'
    
    # Basic Information
    name = CharField('Dimension Name', required=True, size=200)
    description = TextField('Description')
    code = CharField('Dimension Code', required=True, size=50)
    
    # Dimension Configuration
    field_name = CharField('Field Name', required=True, size=100, 
                          help='Field name in source model')
    data_type = SelectionField([
        ('char', 'Text'),
        ('integer', 'Integer'),
        ('float', 'Float'),
        ('date', 'Date'),
        ('datetime', 'DateTime'),
        ('boolean', 'Boolean'),
        ('selection', 'Selection'),
    ], 'Data Type', required=True)
    
    # Model Relationship
    model_id = Many2OneField('analytics.model', 'Analytics Model', required=True)
    
    # Dimension Settings
    sequence = IntegerField('Sequence', default=10)
    active = BooleanField('Active', default=True)
    
    # Grouping Configuration
    group_by = BooleanField('Group By', default=True, 
                           help='Use this dimension for grouping')
    sort_order = SelectionField([
        ('asc', 'Ascending'),
        ('desc', 'Descending'),
        ('none', 'No Sorting'),
    ], 'Sort Order', default='asc')
    
    # Filter Configuration
    filter_enabled = BooleanField('Filter Enabled', default=True)
    filter_type = SelectionField([
        ('exact', 'Exact Match'),
        ('contains', 'Contains'),
        ('starts_with', 'Starts With'),
        ('ends_with', 'Ends With'),
        ('range', 'Range'),
        ('list', 'List'),
    ], 'Filter Type', default='exact')
    
    def get_dimension_values(self, source_data):
        """Get unique values for this dimension"""
        values = set()
        
        for record in source_data:
            value = getattr(record, self.field_name, '')
            if value:
                values.add(value)
        
        # Convert to list and sort
        values_list = list(values)
        
        if self.sort_order == 'asc':
            values_list.sort()
        elif self.sort_order == 'desc':
            values_list.sort(reverse=True)
        
        return values_list
    
    def get_dimension_summary(self):
        """Get dimension summary"""
        return {
            'id': self.id,
            'name': self.name,
            'code': self.code,
            'field_name': self.field_name,
            'data_type': self.data_type,
            'group_by': self.group_by,
            'sort_order': self.sort_order,
            'filter_enabled': self.filter_enabled,
            'filter_type': self.filter_type,
        }