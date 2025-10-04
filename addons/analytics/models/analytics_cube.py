#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Analytics Cube Model
======================================

Analytics cube management for OLAP operations.
"""

from core_framework.orm import (
    BaseModel, CharField, TextField, SelectionField, Many2OneField,
    BooleanField, One2ManyField, IntegerField
)
from addons.core_base.models.base_mixins import KidsClothingMixin


class AnalyticsCube(BaseModel, KidsClothingMixin):
    """Analytics Cube Model"""
    
    _name = 'analytics.cube'
    _description = 'Analytics Cube'
    _order = 'sequence, name'
    
    # Basic Information
    name = CharField('Cube Name', required=True, size=200)
    description = TextField('Description')
    code = CharField('Cube Code', required=True, size=50)
    
    # Cube Configuration
    model_id = Many2OneField('analytics.model', 'Analytics Model', required=True)
    
    # Cube Dimensions
    dimension_ids = One2ManyField('analytics.dimension', 'cube_id', 'Dimensions')
    
    # Cube Facts
    fact_ids = One2ManyField('analytics.fact', 'cube_id', 'Facts')
    
    # Cube Settings
    sequence = IntegerField('Sequence', default=10)
    active = BooleanField('Active', default=True)
    
    # Access Control
    user_id = Many2OneField('users.user', 'Created By', required=True)
    group_ids = One2ManyField('users.group', 'cube_group_ids', 'Access Groups')
    
    def execute_olap_query(self, dimensions=None, facts=None, filters=None):
        """Execute OLAP query on the cube"""
        try:
            # Get source data
            source_data = self.model_id._get_source_data(filters)
            
            # Process dimensions
            if dimensions:
                dimension_data = self._process_dimensions(source_data, dimensions)
            else:
                dimension_data = self._process_all_dimensions(source_data)
            
            # Process facts
            if facts:
                fact_data = self._process_facts(source_data, facts)
            else:
                fact_data = self._process_all_facts(source_data)
            
            # Generate cube data
            cube_data = self._generate_cube_data(dimension_data, fact_data)
            
            return cube_data
            
        except Exception as e:
            raise e
    
    def _process_dimensions(self, source_data, dimension_codes):
        """Process specific dimensions"""
        dimensions = {}
        
        for dimension in self.dimension_ids.filtered(lambda d: d.code in dimension_codes):
            dimension_data = []
            for record in source_data:
                value = getattr(record, dimension.field_name, '')
                dimension_data.append({
                    'dimension': dimension.name,
                    'value': value,
                    'label': str(value),
                })
            
            dimensions[dimension.code] = {
                'name': dimension.name,
                'data': dimension_data,
            }
        
        return dimensions
    
    def _process_all_dimensions(self, source_data):
        """Process all dimensions"""
        dimensions = {}
        
        for dimension in self.dimension_ids:
            dimension_data = []
            for record in source_data:
                value = getattr(record, dimension.field_name, '')
                dimension_data.append({
                    'dimension': dimension.name,
                    'value': value,
                    'label': str(value),
                })
            
            dimensions[dimension.code] = {
                'name': dimension.name,
                'data': dimension_data,
            }
        
        return dimensions
    
    def _process_facts(self, source_data, fact_codes):
        """Process specific facts"""
        facts = {}
        
        for fact in self.fact_ids.filtered(lambda f: f.code in fact_codes):
            fact_data = []
            for record in source_data:
                value = getattr(record, fact.field_name, 0)
                fact_data.append({
                    'fact': fact.name,
                    'value': value,
                    'record_id': record.id,
                })
            
            facts[fact.code] = {
                'name': fact.name,
                'data': fact_data,
            }
        
        return facts
    
    def _process_all_facts(self, source_data):
        """Process all facts"""
        facts = {}
        
        for fact in self.fact_ids:
            fact_data = []
            for record in source_data:
                value = getattr(record, fact.field_name, 0)
                fact_data.append({
                    'fact': fact.name,
                    'value': value,
                    'record_id': record.id,
                })
            
            facts[fact.code] = {
                'name': fact.name,
                'data': fact_data,
            }
        
        return facts
    
    def _generate_cube_data(self, dimensions, facts):
        """Generate cube data from dimensions and facts"""
        cube_data = {
            'dimensions': dimensions,
            'facts': facts,
            'summary': {
                'dimensions_count': len(dimensions),
                'facts_count': len(facts),
                'total_records': sum(len(fact['data']) for fact in facts.values()),
            }
        }
        
        return cube_data
    
    def get_cube_summary(self):
        """Get cube summary"""
        return {
            'id': self.id,
            'name': self.name,
            'code': self.code,
            'model': self.model_id.name,
            'dimensions_count': len(self.dimension_ids),
            'facts_count': len(self.fact_ids),
            'active': self.active,
        }