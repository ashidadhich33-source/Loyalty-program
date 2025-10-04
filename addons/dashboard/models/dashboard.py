#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Dashboard Model
==================================

Dashboard management for customizable dashboards.
"""

from core_framework.orm import (
    BaseModel, CharField, TextField, SelectionField, Many2OneField,
    BooleanField, One2ManyField, IntegerField, DateTimeField, FloatField
)
from addons.core_base.models.base_mixins import KidsClothingMixin


class Dashboard(BaseModel, KidsClothingMixin):
    """Dashboard Model"""
    
    _name = 'dashboard.dashboard'
    _description = 'Dashboard'
    _order = 'create_date desc'
    
    # Basic Information
    name = CharField('Dashboard Name', required=True, size=200)
    description = TextField('Description')
    user_id = Many2OneField('users.user', 'Owner', required=True)
    
    # Dashboard Configuration
    layout = SelectionField([
        ('grid', 'Grid Layout'),
        ('freeform', 'Freeform Layout'),
        ('tabbed', 'Tabbed Layout'),
        ('carousel', 'Carousel Layout'),
    ], 'Layout', default='grid')
    
    theme = SelectionField([
        ('light', 'Light Theme'),
        ('dark', 'Dark Theme'),
        ('colorful', 'Colorful Theme'),
        ('minimal', 'Minimal Theme'),
        ('kids', 'Kids Theme'),
    ], 'Theme', default='light')
    
    # Grid Configuration
    grid_size = SelectionField([
        ('12', '12 Columns'),
        ('16', '16 Columns'),
        ('24', '24 Columns'),
    ], 'Grid Size', default='12')
    
    # Widgets Configuration
    widget_ids = One2ManyField('dashboard.widget.position', 'dashboard_id', 'Widgets')
    
    # Dashboard Settings
    auto_refresh = BooleanField('Auto Refresh', default=False)
    refresh_interval = IntegerField('Refresh Interval (seconds)', default=300)
    show_grid_lines = BooleanField('Show Grid Lines', default=True)
    allow_resize = BooleanField('Allow Resize', default=True)
    allow_drag = BooleanField('Allow Drag', default=True)
    
    # Access Control
    is_public = BooleanField('Public Dashboard', default=False)
    group_ids = One2ManyField('users.group', 'dashboard_group_ids', 'Access Groups')
    shared_with_ids = One2ManyField('users.user', 'shared_dashboard_ids', 'Shared With')
    
    # Status
    active = BooleanField('Active', default=True)
    
    # Template
    template_id = Many2OneField('dashboard.template', 'Template')
    
    # Statistics
    view_count = IntegerField('View Count', default=0)
    last_viewed = DateTimeField('Last Viewed')
    
    def get_dashboard_config(self):
        """Get dashboard configuration for frontend"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'layout': self.layout,
            'theme': self.theme,
            'grid_size': int(self.grid_size),
            'widgets': [widget.get_widget_config() for widget in self.widget_ids],
            'settings': {
                'auto_refresh': self.auto_refresh,
                'refresh_interval': self.refresh_interval,
                'show_grid_lines': self.show_grid_lines,
                'allow_resize': self.allow_resize,
                'allow_drag': self.allow_drag,
            },
            'is_public': self.is_public,
            'view_count': self.view_count,
            'last_viewed': self.last_viewed,
        }
    
    def add_widget(self, widget_id, x_position=0, y_position=0, width=4, height=300):
        """Add widget to dashboard"""
        widget_position = self.env['dashboard.widget.position'].create({
            'dashboard_id': self.id,
            'widget_id': widget_id,
            'x_position': x_position,
            'y_position': y_position,
            'width': width,
            'height': height,
        })
        
        return widget_position
    
    def remove_widget(self, widget_position_id):
        """Remove widget from dashboard"""
        widget_position = self.env['dashboard.widget.position'].browse([widget_position_id])
        if widget_position:
            widget_position.unlink()
    
    def update_widget_position(self, widget_position_id, x_position, y_position, width, height):
        """Update widget position and size"""
        widget_position = self.env['dashboard.widget.position'].browse([widget_position_id])
        if widget_position:
            widget_position.write({
                'x_position': x_position,
                'y_position': y_position,
                'width': width,
                'height': height,
            })
    
    def duplicate_dashboard(self, new_name=None):
        """Duplicate dashboard"""
        new_name = new_name or f"{self.name} (Copy)"
        
        new_dashboard = self.create({
            'name': new_name,
            'description': self.description,
            'user_id': self.user_id.id,
            'layout': self.layout,
            'theme': self.theme,
            'grid_size': self.grid_size,
            'auto_refresh': self.auto_refresh,
            'refresh_interval': self.refresh_interval,
            'show_grid_lines': self.show_grid_lines,
            'allow_resize': self.allow_resize,
            'allow_drag': self.allow_drag,
            'is_public': self.is_public,
        })
        
        # Duplicate widget positions
        for widget_pos in self.widget_ids:
            widget_pos.create({
                'dashboard_id': new_dashboard.id,
                'widget_id': widget_pos.widget_id.id,
                'x_position': widget_pos.x_position,
                'y_position': widget_pos.y_position,
                'width': widget_pos.width,
                'height': widget_pos.height,
                'sequence': widget_pos.sequence,
            })
        
        return new_dashboard
    
    def share_dashboard(self, user_ids):
        """Share dashboard with users"""
        self.write({
            'shared_with_ids': [(6, 0, user_ids)],
        })
    
    def record_view(self):
        """Record dashboard view"""
        from datetime import datetime
        
        self.write({
            'view_count': self.view_count + 1,
            'last_viewed': datetime.now(),
        })
    
    def export_dashboard(self, format='pdf'):
        """Export dashboard to specified format"""
        if format == 'pdf':
            return self._export_to_pdf()
        elif format == 'image':
            return self._export_to_image()
        elif format == 'json':
            return self._export_to_json()
        else:
            raise ValueError(f"Unsupported export format: {format}")
    
    def _export_to_pdf(self):
        """Export dashboard to PDF"""
        # Implementation for PDF export
        return {
            'file_path': f'/tmp/dashboard_{self.id}.pdf',
            'file_name': f"{self.name}.pdf",
            'format': 'pdf',
        }
    
    def _export_to_image(self):
        """Export dashboard to image"""
        # Implementation for image export
        return {
            'file_path': f'/tmp/dashboard_{self.id}.png',
            'file_name': f"{self.name}.png",
            'format': 'image',
        }
    
    def _export_to_json(self):
        """Export dashboard to JSON"""
        import json
        
        config = self.get_dashboard_config()
        file_path = f'/tmp/dashboard_{self.id}.json'
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, default=str)
        
        return {
            'file_path': file_path,
            'file_name': f"{self.name}.json",
            'format': 'json',
        }
    
    def get_accessible_dashboards(self, user_id):
        """Get dashboards accessible to user"""
        domain = [
            '|',  # OR condition
            ('user_id', '=', user_id),  # Own dashboards
            '|',  # OR condition
            ('is_public', '=', True),  # Public dashboards
            ('shared_with_ids', 'in', [user_id]),  # Shared dashboards
        ]
        
        return self.search(domain)
    
    def create_from_template(self, template_id, name=None):
        """Create dashboard from template"""
        template = self.env['dashboard.template'].browse([template_id])
        if not template:
            raise ValueError("Template not found")
        
        dashboard_name = name or f"{template.name} - {self.name}"
        
        new_dashboard = self.create({
            'name': dashboard_name,
            'description': template.description,
            'user_id': self.user_id.id,
            'layout': template.layout,
            'theme': template.theme,
            'grid_size': template.grid_size,
            'template_id': template_id,
        })
        
        # Add widgets from template
        for template_widget in template.widget_ids:
            new_dashboard.add_widget(
                template_widget.widget_id.id,
                template_widget.x_position,
                template_widget.y_position,
                template_widget.width,
                template_widget.height
            )
        
        return new_dashboard


class DashboardWidgetPosition(BaseModel, KidsClothingMixin):
    """Dashboard Widget Position Model"""
    
    _name = 'dashboard.widget.position'
    _description = 'Dashboard Widget Position'
    _order = 'sequence'
    
    dashboard_id = Many2OneField('dashboard.dashboard', 'Dashboard', required=True)
    widget_id = Many2OneField('dashboard.widget', 'Widget', required=True)
    
    # Position Configuration
    x_position = IntegerField('X Position', default=0)
    y_position = IntegerField('Y Position', default=0)
    width = IntegerField('Width', default=4)
    height = IntegerField('Height', default=300)
    sequence = IntegerField('Sequence', default=10)
    
    # Widget Settings
    title = CharField('Widget Title', size=200)
    show_title = BooleanField('Show Title', default=True)
    show_border = BooleanField('Show Border', default=True)
    background_color = CharField('Background Color', size=20, default='#ffffff')
    
    def get_widget_config(self):
        """Get widget position configuration"""
        widget_config = self.widget_id.get_widget_config()
        widget_config.update({
            'position_id': self.id,
            'title': self.title or self.widget_id.name,
            'x_position': self.x_position,
            'y_position': self.y_position,
            'width': self.width,
            'height': self.height,
            'sequence': self.sequence,
            'show_title': self.show_title,
            'show_border': self.show_border,
            'background_color': self.background_color,
        })
        
        return widget_config