#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Dashboard Template Model
===========================================

Dashboard template management for pre-configured dashboards.
"""

from core_framework.orm import (
    BaseModel, CharField, TextField, SelectionField, Many2OneField,
    BooleanField, One2ManyField, IntegerField, ImageField
)
from addons.core_base.models.base_mixins import KidsClothingMixin


class DashboardTemplate(BaseModel, KidsClothingMixin):
    """Dashboard Template Model"""
    
    _name = 'dashboard.template'
    _description = 'Dashboard Template'
    _order = 'sequence, name'
    
    # Basic Information
    name = CharField('Template Name', required=True, size=200)
    description = TextField('Description')
    category = SelectionField([
        ('sales', 'Sales Dashboard'),
        ('inventory', 'Inventory Dashboard'),
        ('financial', 'Financial Dashboard'),
        ('hr', 'HR Dashboard'),
        ('marketing', 'Marketing Dashboard'),
        ('operations', 'Operations Dashboard'),
        ('executive', 'Executive Dashboard'),
        ('custom', 'Custom Dashboard'),
    ], 'Category', required=True)
    
    # Template Configuration
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
    
    grid_size = SelectionField([
        ('12', '12 Columns'),
        ('16', '16 Columns'),
        ('24', '24 Columns'),
    ], 'Grid Size', default='12')
    
    # Template Content
    widget_ids = One2ManyField('dashboard.template.widget', 'template_id', 'Widgets')
    
    # Template Settings
    sequence = IntegerField('Sequence', default=10)
    active = BooleanField('Active', default=True)
    is_public = BooleanField('Public Template', default=True)
    is_default = BooleanField('Default Template', default=False)
    
    # Template Preview
    preview_image = ImageField('Preview Image', max_width=800, max_height=600)
    preview_description = TextField('Preview Description')
    
    # Usage Statistics
    usage_count = IntegerField('Usage Count', default=0)
    rating = FloatField('Rating', digits=(3, 2), default=0.0)
    
    def create_dashboard_from_template(self, user_id, dashboard_name=None):
        """Create dashboard from template"""
        dashboard_name = dashboard_name or f"{self.name} - Dashboard"
        
        dashboard = self.env['dashboard.dashboard'].create({
            'name': dashboard_name,
            'description': self.description,
            'user_id': user_id,
            'layout': self.layout,
            'theme': self.theme,
            'grid_size': self.grid_size,
            'template_id': self.id,
        })
        
        # Add widgets from template
        for template_widget in self.widget_ids:
            dashboard.add_widget(
                template_widget.widget_id.id,
                template_widget.x_position,
                template_widget.y_position,
                template_widget.width,
                template_widget.height
            )
        
        # Update usage count
        self.write({'usage_count': self.usage_count + 1})
        
        return dashboard
    
    def get_template_config(self):
        """Get template configuration"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'category': self.category,
            'layout': self.layout,
            'theme': self.theme,
            'grid_size': int(self.grid_size),
            'widgets': [widget.get_widget_config() for widget in self.widget_ids],
            'preview_image': self.preview_image,
            'preview_description': self.preview_description,
            'usage_count': self.usage_count,
            'rating': self.rating,
            'is_public': self.is_public,
            'is_default': self.is_default,
        }
    
    def duplicate_template(self, new_name=None):
        """Duplicate template"""
        new_name = new_name or f"{self.name} (Copy)"
        
        new_template = self.create({
            'name': new_name,
            'description': self.description,
            'category': self.category,
            'layout': self.layout,
            'theme': self.theme,
            'grid_size': self.grid_size,
            'sequence': self.sequence,
            'active': self.active,
            'is_public': self.is_public,
            'is_default': False,  # Duplicated templates are not default
            'preview_description': self.preview_description,
        })
        
        # Duplicate template widgets
        for template_widget in self.widget_ids:
            template_widget.create({
                'template_id': new_template.id,
                'widget_id': template_widget.widget_id.id,
                'x_position': template_widget.x_position,
                'y_position': template_widget.y_position,
                'width': template_widget.width,
                'height': template_widget.height,
                'sequence': template_widget.sequence,
            })
        
        return new_template


class DashboardTemplateWidget(BaseModel, KidsClothingMixin):
    """Dashboard Template Widget Model"""
    
    _name = 'dashboard.template.widget'
    _description = 'Dashboard Template Widget'
    _order = 'sequence'
    
    template_id = Many2OneField('dashboard.template', 'Template', required=True)
    widget_id = Many2OneField('dashboard.widget', 'Widget', required=True)
    
    # Position Configuration
    x_position = IntegerField('X Position', default=0)
    y_position = IntegerField('Y Position', default=0)
    width = IntegerField('Width', default=4)
    height = IntegerField('Height', default=300)
    sequence = IntegerField('Sequence', default=10)
    
    def get_widget_config(self):
        """Get widget configuration for template"""
        widget_config = self.widget_id.get_widget_config()
        widget_config.update({
            'template_widget_id': self.id,
            'x_position': self.x_position,
            'y_position': self.y_position,
            'width': self.width,
            'height': self.height,
            'sequence': self.sequence,
        })
        
        return widget_config