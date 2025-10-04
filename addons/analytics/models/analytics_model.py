#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Analytics Model
===================================

Analytics model management for data analysis.
"""

from core_framework.orm import (
    BaseModel, CharField, TextField, SelectionField, Many2OneField,
    BooleanField, One2ManyField, IntegerField, FloatField, DateTimeField
)
from addons.core_base.models.base_mixins import KidsClothingMixin


class AnalyticsModel(BaseModel, KidsClothingMixin):
    """Analytics Model"""
    
    _name = 'analytics.model'
    _description = 'Analytics Model'
    _order = 'sequence, name'
    
    # Basic Information
    name = CharField('Model Name', required=True, size=200)
    description = TextField('Description')
    code = CharField('Model Code', required=True, size=50)
    
    # Model Configuration
    model_type = SelectionField([
        ('descriptive', 'Descriptive Analytics'),
        ('diagnostic', 'Diagnostic Analytics'),
        ('predictive', 'Predictive Analytics'),
        ('prescriptive', 'Prescriptive Analytics'),
        ('real_time', 'Real-time Analytics'),
        ('batch', 'Batch Analytics'),
    ], 'Model Type', required=True)
    
    category = SelectionField([
        ('sales', 'Sales Analytics'),
        ('inventory', 'Inventory Analytics'),
        ('financial', 'Financial Analytics'),
        ('customer', 'Customer Analytics'),
        ('marketing', 'Marketing Analytics'),
        ('hr', 'HR Analytics'),
        ('operations', 'Operations Analytics'),
        ('custom', 'Custom Analytics'),
    ], 'Category', required=True)
    
    # Data Source Configuration
    source_model = CharField('Source Model', size=100, required=True)
    source_domain = TextField('Source Domain', help='Filter domain for source data')
    
    # Model Settings
    sequence = IntegerField('Sequence', default=10)
    active = BooleanField('Active', default=True)
    is_public = BooleanField('Public Model', default=False)
    
    # Analytics Components
    dimension_ids = One2ManyField('analytics.dimension', 'model_id', 'Dimensions')
    fact_ids = One2ManyField('analytics.fact', 'model_id', 'Facts')
    metric_ids = One2ManyField('analytics.metric', 'model_id', 'Metrics')
    kpi_ids = One2ManyField('analytics.kpi', 'model_id', 'KPIs')
    
    # Model Configuration
    refresh_interval = IntegerField('Refresh Interval (minutes)', default=60)
    last_refresh = DateTimeField('Last Refresh')
    cache_duration = IntegerField('Cache Duration (minutes)', default=30)
    
    # Access Control
    user_id = Many2OneField('users.user', 'Created By', required=True)
    group_ids = One2ManyField('users.group', 'model_group_ids', 'Access Groups')
    
    def execute_analytics(self, filters=None):
        """Execute analytics model"""
        try:
            # Get source data
            source_data = self._get_source_data(filters)
            
            # Process dimensions
            dimensions = self._process_dimensions(source_data)
            
            # Process facts
            facts = self._process_facts(source_data)
            
            # Calculate metrics
            metrics = self._calculate_metrics(dimensions, facts)
            
            # Generate insights
            insights = self._generate_insights(metrics)
            
            # Update last refresh
            from datetime import datetime
            self.write({'last_refresh': datetime.now()})
            
            return {
                'dimensions': dimensions,
                'facts': facts,
                'metrics': metrics,
                'insights': insights,
                'refresh_time': self.last_refresh,
            }
            
        except Exception as e:
            raise e
    
    def _get_source_data(self, filters=None):
        """Get source data from model"""
        model = self.env[self.source_model]
        domain = []
        
        # Apply model domain
        if self.source_domain:
            import json
            try:
                domain = json.loads(self.source_domain)
            except:
                domain = []
        
        # Apply additional filters
        if filters:
            domain.extend(filters)
        
        return model.search(domain)
    
    def _process_dimensions(self, source_data):
        """Process dimensions from source data"""
        dimensions = {}
        
        for dimension in self.dimension_ids:
            dimension_data = []
            for record in source_data:
                value = getattr(record, dimension.field_name, '')
                if value not in [item.get('value') for item in dimension_data]:
                    dimension_data.append({
                        'dimension': dimension.name,
                        'value': value,
                        'label': str(value),
                    })
            
            dimensions[dimension.code] = {
                'name': dimension.name,
                'data': dimension_data,
                'type': dimension.data_type,
            }
        
        return dimensions
    
    def _process_facts(self, source_data):
        """Process facts from source data"""
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
                'type': fact.data_type,
                'aggregation': fact.aggregation_type,
            }
        
        return facts
    
    def _calculate_metrics(self, dimensions, facts):
        """Calculate metrics from dimensions and facts"""
        metrics = {}
        
        for metric in self.metric_ids:
            metric_value = self._calculate_metric_value(metric, dimensions, facts)
            
            metrics[metric.code] = {
                'name': metric.name,
                'value': metric_value,
                'formula': metric.formula,
                'unit': metric.unit,
                'type': metric.metric_type,
            }
        
        return metrics
    
    def _calculate_metric_value(self, metric, dimensions, facts):
        """Calculate individual metric value"""
        if metric.formula:
            # Use custom formula
            return self._evaluate_formula(metric.formula, dimensions, facts)
        else:
            # Use default calculation based on metric type
            return self._default_metric_calculation(metric, facts)
    
    def _evaluate_formula(self, formula, dimensions, facts):
        """Evaluate custom formula"""
        # Safe evaluation of formula
        local_vars = {
            'dimensions': dimensions,
            'facts': facts,
            'sum': sum,
            'avg': lambda x: sum(x) / len(x) if x else 0,
            'count': len,
            'min': min,
            'max': max,
        }
        
        try:
            return eval(formula, {}, local_vars)
        except:
            return 0
    
    def _default_metric_calculation(self, metric, facts):
        """Default metric calculation"""
        if metric.metric_type == 'sum':
            return sum(fact['value'] for fact in facts.get(metric.fact_id.code, {}).get('data', []))
        elif metric.metric_type == 'avg':
            data = facts.get(metric.fact_id.code, {}).get('data', [])
            return sum(item['value'] for item in data) / len(data) if data else 0
        elif metric.metric_type == 'count':
            return len(facts.get(metric.fact_id.code, {}).get('data', []))
        elif metric.metric_type == 'min':
            data = facts.get(metric.fact_id.code, {}).get('data', [])
            return min(item['value'] for item in data) if data else 0
        elif metric.metric_type == 'max':
            data = facts.get(metric.fact_id.code, {}).get('data', [])
            return max(item['value'] for item in data) if data else 0
        else:
            return 0
    
    def _generate_insights(self, metrics):
        """Generate insights from metrics"""
        insights = []
        
        for kpi in self.kpi_ids:
            metric_value = metrics.get(kpi.metric_id.code, {}).get('value', 0)
            target_value = kpi.target_value
            
            # Calculate performance
            if target_value > 0:
                performance = (metric_value / target_value) * 100
            else:
                performance = 0
            
            # Generate insight
            insight = {
                'kpi': kpi.name,
                'current_value': metric_value,
                'target_value': target_value,
                'performance': performance,
                'status': 'good' if performance >= 100 else 'needs_improvement',
                'recommendation': self._get_recommendation(kpi, performance),
            }
            
            insights.append(insight)
        
        return insights
    
    def _get_recommendation(self, kpi, performance):
        """Get recommendation based on KPI performance"""
        if performance >= 100:
            return f"{kpi.name} is performing well above target."
        elif performance >= 80:
            return f"{kpi.name} is close to target. Consider optimization."
        else:
            return f"{kpi.name} needs significant improvement to reach target."
    
    def get_analytics_summary(self):
        """Get analytics model summary"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'type': self.model_type,
            'category': self.category,
            'dimensions_count': len(self.dimension_ids),
            'facts_count': len(self.fact_ids),
            'metrics_count': len(self.metric_ids),
            'kpis_count': len(self.kpi_ids),
            'last_refresh': self.last_refresh,
            'active': self.active,
        }
    
    def duplicate_model(self, new_name=None):
        """Duplicate analytics model"""
        new_name = new_name or f"{self.name} (Copy)"
        
        new_model = self.create({
            'name': new_name,
            'description': self.description,
            'code': f"{self.code}_copy",
            'model_type': self.model_type,
            'category': self.category,
            'source_model': self.source_model,
            'source_domain': self.source_domain,
            'sequence': self.sequence,
            'active': self.active,
            'is_public': False,  # Duplicated models are private
            'refresh_interval': self.refresh_interval,
            'cache_duration': self.cache_duration,
            'user_id': self.user_id.id,
        })
        
        # Duplicate dimensions
        for dimension in self.dimension_ids:
            dimension.create({
                'model_id': new_model.id,
                'name': dimension.name,
                'code': dimension.code,
                'field_name': dimension.field_name,
                'data_type': dimension.data_type,
                'sequence': dimension.sequence,
            })
        
        # Duplicate facts
        for fact in self.fact_ids:
            fact.create({
                'model_id': new_model.id,
                'name': fact.name,
                'code': fact.code,
                'field_name': fact.field_name,
                'data_type': fact.data_type,
                'aggregation_type': fact.aggregation_type,
                'sequence': fact.sequence,
            })
        
        # Duplicate metrics
        for metric in self.metric_ids:
            metric.create({
                'model_id': new_model.id,
                'name': metric.name,
                'code': metric.code,
                'metric_type': metric.metric_type,
                'formula': metric.formula,
                'unit': metric.unit,
                'fact_id': metric.fact_id.id,
                'sequence': metric.sequence,
            })
        
        # Duplicate KPIs
        for kpi in self.kpi_ids:
            kpi.create({
                'model_id': new_model.id,
                'name': kpi.name,
                'code': kpi.code,
                'metric_id': kpi.metric_id.id,
                'target_value': kpi.target_value,
                'sequence': kpi.sequence,
            })
        
        return new_model