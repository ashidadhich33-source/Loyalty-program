#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Dashboard Widget Model
==========================================

Dashboard widget management for customizable dashboards.
"""

from core_framework.orm import (
    BaseModel, CharField, TextField, SelectionField, Many2OneField,
    IntegerField, BooleanField, One2ManyField, FloatField
)
from addons.core_base.models.base_mixins import KidsClothingMixin


class DashboardWidget(BaseModel, KidsClothingMixin):
    """Dashboard Widget Model"""
    
    _name = 'dashboard.widget'
    _description = 'Dashboard Widget'
    _order = 'sequence, name'
    
    # Basic Information
    name = CharField('Widget Name', required=True, size=200)
    title = CharField('Widget Title', size=200)
    description = TextField('Description')
    widget_type = SelectionField([
        ('chart', 'Chart'),
        ('table', 'Table'),
        ('metric', 'Metric'),
        ('gauge', 'Gauge'),
        ('progress', 'Progress Bar'),
        ('text', 'Text Block'),
        ('image', 'Image'),
        ('iframe', 'Iframe'),
        ('custom', 'Custom Widget'),
    ], 'Widget Type', required=True)
    
    # Widget Configuration
    chart_type = SelectionField([
        ('line', 'Line Chart'),
        ('bar', 'Bar Chart'),
        ('pie', 'Pie Chart'),
        ('doughnut', 'Doughnut Chart'),
        ('area', 'Area Chart'),
        ('scatter', 'Scatter Plot'),
        ('radar', 'Radar Chart'),
        ('polar', 'Polar Chart'),
    ], 'Chart Type')
    
    # Data Configuration
    data_source = SelectionField([
        ('model', 'Model Data'),
        ('sql', 'SQL Query'),
        ('python', 'Python Code'),
        ('static', 'Static Data'),
    ], 'Data Source', required=True)
    
    model_name = CharField('Model Name', size=100)
    domain = TextField('Domain', help='Search domain for model data')
    sql_query = TextField('SQL Query')
    python_code = TextField('Python Code')
    static_data = TextField('Static Data', help='JSON data')
    
    # Display Configuration
    width = IntegerField('Width', default=4, help='Width in grid units (1-12)')
    height = IntegerField('Height', default=300, help='Height in pixels')
    sequence = IntegerField('Sequence', default=10)
    
    # Styling
    background_color = CharField('Background Color', size=20, default='#ffffff')
    text_color = CharField('Text Color', size=20, default='#000000')
    border_color = CharField('Border Color', size=20, default='#e0e0e0')
    border_width = IntegerField('Border Width', default=1)
    border_radius = IntegerField('Border Radius', default=4)
    
    # Chart Configuration
    show_legend = BooleanField('Show Legend', default=True)
    show_grid = BooleanField('Show Grid', default=True)
    show_labels = BooleanField('Show Labels', default=True)
    chart_colors = TextField('Chart Colors', help='JSON array of colors')
    
    # Refresh Configuration
    auto_refresh = BooleanField('Auto Refresh', default=False)
    refresh_interval = IntegerField('Refresh Interval (seconds)', default=300)
    last_refresh = CharField('Last Refresh', size=50)
    
    # Access Control
    user_id = Many2OneField('users.user', 'Owner')
    group_ids = One2ManyField('users.group', 'widget_group_ids', 'Access Groups')
    is_public = BooleanField('Public Widget', default=False)
    
    # Dashboard Relationships
    dashboard_ids = One2ManyField('dashboard.dashboard', 'widget_ids', 'Dashboards')
    
    def get_widget_data(self):
        """Get widget data based on data source"""
        try:
            if self.data_source == 'model':
                return self._get_model_data()
            elif self.data_source == 'sql':
                return self._get_sql_data()
            elif self.data_source == 'python':
                return self._get_python_data()
            elif self.data_source == 'static':
                return self._get_static_data()
            else:
                return {}
        except Exception as e:
            return {'error': str(e)}
    
    def _get_model_data(self):
        """Get data from model"""
        if not self.model_name:
            return {}
        
        model = self.env[self.model_name]
        domain = []
        
        if self.domain:
            import json
            try:
                domain = json.loads(self.domain)
            except:
                domain = []
        
        records = model.search(domain)
        return {
            'labels': [str(record.id) for record in records],
            'data': [1] * len(records),  # Placeholder data
            'count': len(records),
        }
    
    def _get_sql_data(self):
        """Get data from SQL query"""
        if not self.sql_query:
            return {}
        
        # Execute SQL query
        # This would use the database manager
        return {'message': 'SQL data not implemented yet'}
    
    def _get_python_data(self):
        """Get data from Python code"""
        if not self.python_code:
            return {}
        
        # Execute Python code safely
        local_vars = {
            'env': self.env,
            'self': self,
        }
        exec(self.python_code, {}, local_vars)
        return local_vars.get('result', {})
    
    def _get_static_data(self):
        """Get static data"""
        if not self.static_data:
            return {}
        
        import json
        try:
            return json.loads(self.static_data)
        except:
            return {}
    
    def refresh_widget(self):
        """Refresh widget data"""
        from datetime import datetime
        
        data = self.get_widget_data()
        self.write({
            'last_refresh': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        })
        
        return data
    
    def get_widget_config(self):
        """Get widget configuration for frontend"""
        return {
            'id': self.id,
            'name': self.name,
            'title': self.title or self.name,
            'type': self.widget_type,
            'chart_type': self.chart_type,
            'width': self.width,
            'height': self.height,
            'sequence': self.sequence,
            'styling': {
                'background_color': self.background_color,
                'text_color': self.text_color,
                'border_color': self.border_color,
                'border_width': self.border_width,
                'border_radius': self.border_radius,
            },
            'chart_config': {
                'show_legend': self.show_legend,
                'show_grid': self.show_grid,
                'show_labels': self.show_labels,
                'colors': self.chart_colors,
            },
            'refresh': {
                'auto_refresh': self.auto_refresh,
                'refresh_interval': self.refresh_interval,
                'last_refresh': self.last_refresh,
            },
        }
    
    def duplicate_widget(self, new_name=None):
        """Duplicate widget"""
        new_name = new_name or f"{self.name} (Copy)"
        
        new_widget = self.create({
            'name': new_name,
            'title': self.title,
            'description': self.description,
            'widget_type': self.widget_type,
            'chart_type': self.chart_type,
            'data_source': self.data_source,
            'model_name': self.model_name,
            'domain': self.domain,
            'sql_query': self.sql_query,
            'python_code': self.python_code,
            'static_data': self.static_data,
            'width': self.width,
            'height': self.height,
            'sequence': self.sequence,
            'background_color': self.background_color,
            'text_color': self.text_color,
            'border_color': self.border_color,
            'border_width': self.border_width,
            'border_radius': self.border_radius,
            'show_legend': self.show_legend,
            'show_grid': self.show_grid,
            'show_labels': self.show_labels,
            'chart_colors': self.chart_colors,
            'auto_refresh': self.auto_refresh,
            'refresh_interval': self.refresh_interval,
            'user_id': self.user_id.id,
            'is_public': self.is_public,
        })
        
        return new_widget