#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Dashboard Widget Model
=========================================

Dashboard widget management for customizable dashboards.
"""

from core_framework.orm import (
    BaseModel, CharField, TextField, SelectionField, Many2OneField,
    IntegerField, BooleanField, One2ManyField, FloatField, DateTimeField
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
        ('kpi', 'KPI Card'),
        ('trend', 'Trend Chart'),
        ('pie', 'Pie Chart'),
        ('bar', 'Bar Chart'),
        ('line', 'Line Chart'),
        ('area', 'Area Chart'),
        ('scatter', 'Scatter Plot'),
        ('heatmap', 'Heatmap'),
        ('funnel', 'Funnel Chart'),
        ('radar', 'Radar Chart'),
        ('polar', 'Polar Chart'),
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
        ('bubble', 'Bubble Chart'),
        ('candlestick', 'Candlestick Chart'),
    ], 'Chart Type')
    
    # Data Configuration
    data_source = SelectionField([
        ('model', 'Model Data'),
        ('sql', 'SQL Query'),
        ('python', 'Python Code'),
        ('static', 'Static Data'),
        ('api', 'API Endpoint'),
        ('file', 'File Upload'),
    ], 'Data Source', required=True)
    
    model_name = CharField('Model Name', size=100)
    domain = TextField('Domain', help='Search domain for model data')
    sql_query = TextField('SQL Query')
    python_code = TextField('Python Code')
    static_data = TextField('Static Data', help='JSON data')
    api_endpoint = CharField('API Endpoint', size=500)
    file_path = CharField('File Path', size=500)
    
    # Display Configuration
    width = IntegerField('Default Width', default=4, help='Default width in grid units (1-12)')
    height = IntegerField('Default Height', default=300, help='Default height in pixels')
    sequence = IntegerField('Sequence', default=10)
    
    # Styling
    background_color = CharField('Background Color', size=20, default='#ffffff')
    text_color = CharField('Text Color', size=20, default='#000000')
    border_color = CharField('Border Color', size=20, default='#e0e0e0')
    border_width = IntegerField('Border Width', default=1)
    border_radius = IntegerField('Border Radius', default=4)
    font_size = IntegerField('Font Size', default=14)
    font_family = CharField('Font Family', size=100, default='Arial, sans-serif')
    
    # Chart Configuration
    show_legend = BooleanField('Show Legend', default=True)
    show_grid = BooleanField('Show Grid', default=True)
    show_labels = BooleanField('Show Labels', default=True)
    show_tooltips = BooleanField('Show Tooltips', default=True)
    chart_colors = TextField('Chart Colors', help='JSON array of colors')
    chart_animation = BooleanField('Chart Animation', default=True)
    chart_interactive = BooleanField('Interactive Chart', default=True)
    
    # Refresh Configuration
    auto_refresh = BooleanField('Auto Refresh', default=False)
    refresh_interval = IntegerField('Refresh Interval (seconds)', default=300)
    last_refresh = DateTimeField('Last Refresh')
    cache_duration = IntegerField('Cache Duration (seconds)', default=60)
    
    # Access Control
    user_id = Many2OneField('users.user', 'Owner')
    group_ids = One2ManyField('users.group', 'widget_group_ids', 'Access Groups')
    is_public = BooleanField('Public Widget', default=False)
    is_template = BooleanField('Template Widget', default=False)
    
    # Dashboard Relationships
    dashboard_ids = One2ManyField('dashboard.dashboard', 'widget_ids', 'Dashboards')
    position_ids = One2ManyField('dashboard.widget.position', 'widget_id', 'Positions')
    
    # Widget Library
    library_id = Many2OneField('widget.library', 'Library Category')
    
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
            elif self.data_source == 'api':
                return self._get_api_data()
            elif self.data_source == 'file':
                return self._get_file_data()
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
        
        # Format data based on widget type
        if self.widget_type in ['chart', 'pie', 'bar', 'line', 'area']:
            return self._format_chart_data(records)
        elif self.widget_type == 'table':
            return self._format_table_data(records)
        elif self.widget_type == 'metric':
            return self._format_metric_data(records)
        else:
            return {'count': len(records)}
    
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
    
    def _get_api_data(self):
        """Get data from API endpoint"""
        if not self.api_endpoint:
            return {}
        
        # Implementation for API data fetching
        return {'message': 'API data not implemented yet'}
    
    def _get_file_data(self):
        """Get data from file"""
        if not self.file_path:
            return {}
        
        # Implementation for file data reading
        return {'message': 'File data not implemented yet'}
    
    def _format_chart_data(self, records):
        """Format data for chart widgets"""
        if not records:
            return {'labels': [], 'data': []}
        
        # Basic chart data formatting
        labels = [str(record.id) for record in records[:10]]  # Limit to 10 items
        data = [1] * len(labels)  # Placeholder data
        
        return {
            'labels': labels,
            'data': data,
            'count': len(records),
        }
    
    def _format_table_data(self, records):
        """Format data for table widgets"""
        if not records:
            return {'headers': [], 'rows': []}
        
        # Get first few records for table display
        table_records = records[:20]  # Limit to 20 rows
        
        # Extract field names from first record
        if table_records:
            headers = list(table_records[0].read()[0].keys())[:5]  # Limit to 5 columns
            rows = []
            for record in table_records:
                row_data = record.read()[0]
                rows.append([row_data.get(header, '') for header in headers])
            
            return {
                'headers': headers,
                'rows': rows,
                'count': len(records),
            }
        
        return {'headers': [], 'rows': []}
    
    def _format_metric_data(self, records):
        """Format data for metric widgets"""
        count = len(records)
        
        return {
            'value': count,
            'label': 'Total Records',
            'change': 0,  # Placeholder for change calculation
            'change_percent': 0,
        }
    
    def refresh_widget(self):
        """Refresh widget data"""
        from datetime import datetime
        
        data = self.get_widget_data()
        self.write({
            'last_refresh': datetime.now(),
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
            'data_source': self.data_source,
            'width': self.width,
            'height': self.height,
            'sequence': self.sequence,
            'styling': {
                'background_color': self.background_color,
                'text_color': self.text_color,
                'border_color': self.border_color,
                'border_width': self.border_width,
                'border_radius': self.border_radius,
                'font_size': self.font_size,
                'font_family': self.font_family,
            },
            'chart_config': {
                'show_legend': self.show_legend,
                'show_grid': self.show_grid,
                'show_labels': self.show_labels,
                'show_tooltips': self.show_tooltips,
                'colors': self.chart_colors,
                'animation': self.chart_animation,
                'interactive': self.chart_interactive,
            },
            'refresh': {
                'auto_refresh': self.auto_refresh,
                'refresh_interval': self.refresh_interval,
                'last_refresh': self.last_refresh,
                'cache_duration': self.cache_duration,
            },
            'access': {
                'is_public': self.is_public,
                'is_template': self.is_template,
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
            'api_endpoint': self.api_endpoint,
            'file_path': self.file_path,
            'width': self.width,
            'height': self.height,
            'sequence': self.sequence,
            'background_color': self.background_color,
            'text_color': self.text_color,
            'border_color': self.border_color,
            'border_width': self.border_width,
            'border_radius': self.border_radius,
            'font_size': self.font_size,
            'font_family': self.font_family,
            'show_legend': self.show_legend,
            'show_grid': self.show_grid,
            'show_labels': self.show_labels,
            'show_tooltips': self.show_tooltips,
            'chart_colors': self.chart_colors,
            'chart_animation': self.chart_animation,
            'chart_interactive': self.chart_interactive,
            'auto_refresh': self.auto_refresh,
            'refresh_interval': self.refresh_interval,
            'cache_duration': self.cache_duration,
            'user_id': self.user_id.id,
            'is_public': self.is_public,
            'is_template': False,  # Duplicated widgets are not templates
        })
        
        return new_widget
    
    def create_template(self, template_name=None):
        """Create template from widget"""
        template_name = template_name or f"{self.name} Template"
        
        template_widget = self.create({
            'name': template_name,
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
            'api_endpoint': self.api_endpoint,
            'file_path': self.file_path,
            'width': self.width,
            'height': self.height,
            'sequence': self.sequence,
            'background_color': self.background_color,
            'text_color': self.text_color,
            'border_color': self.border_color,
            'border_width': self.border_width,
            'border_radius': self.border_radius,
            'font_size': self.font_size,
            'font_family': self.font_family,
            'show_legend': self.show_legend,
            'show_grid': self.show_grid,
            'show_labels': self.show_labels,
            'show_tooltips': self.show_tooltips,
            'chart_colors': self.chart_colors,
            'chart_animation': self.chart_animation,
            'chart_interactive': self.chart_interactive,
            'auto_refresh': self.auto_refresh,
            'refresh_interval': self.refresh_interval,
            'cache_duration': self.cache_duration,
            'user_id': self.user_id.id,
            'is_public': True,  # Templates are public
            'is_template': True,
        })
        
        return template_widget