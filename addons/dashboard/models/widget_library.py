#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Widget Library Model
========================================

Widget library management for organizing and categorizing widgets.
"""

from core_framework.orm import (
    BaseModel, CharField, TextField, SelectionField, Many2OneField,
    BooleanField, One2ManyField, IntegerField, ImageField
)
from addons.core_base.models.base_mixins import KidsClothingMixin


class WidgetLibrary(BaseModel, KidsClothingMixin):
    """Widget Library Model"""
    
    _name = 'widget.library'
    _description = 'Widget Library'
    _order = 'sequence, name'
    
    # Basic Information
    name = CharField('Library Name', required=True, size=200)
    description = TextField('Description')
    code = CharField('Library Code', required=True, size=50)
    
    # Library Configuration
    category = SelectionField([
        ('charts', 'Charts & Graphs'),
        ('tables', 'Tables & Lists'),
        ('metrics', 'Metrics & KPIs'),
        ('text', 'Text & Content'),
        ('media', 'Media & Images'),
        ('custom', 'Custom Widgets'),
        ('system', 'System Widgets'),
    ], 'Category', required=True)
    
    # Library Settings
    sequence = IntegerField('Sequence', default=10)
    active = BooleanField('Active', default=True)
    is_public = BooleanField('Public Library', default=True)
    
    # Library Content
    widget_ids = One2ManyField('dashboard.widget', 'library_id', 'Widgets')
    
    # Library Preview
    icon = CharField('Icon', size=100, help='Font Awesome icon class')
    color = CharField('Color', size=20, help='Hex color code')
    preview_image = ImageField('Preview Image', max_width=400, max_height=300)
    
    # Usage Statistics
    widget_count = IntegerField('Widget Count', default=0)
    usage_count = IntegerField('Usage Count', default=0)
    
    def get_library_config(self):
        """Get library configuration"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'code': self.code,
            'category': self.category,
            'sequence': self.sequence,
            'active': self.active,
            'is_public': self.is_public,
            'icon': self.icon,
            'color': self.color,
            'preview_image': self.preview_image,
            'widget_count': self.widget_count,
            'usage_count': self.usage_count,
        }
    
    def get_widgets(self):
        """Get widgets in this library"""
        return self.widget_ids.filtered(lambda w: w.active)
    
    def add_widget(self, widget_id):
        """Add widget to library"""
        widget = self.env['dashboard.widget'].browse([widget_id])
        if widget:
            widget.write({'library_id': self.id})
            self.write({'widget_count': self.widget_count + 1})
    
    def remove_widget(self, widget_id):
        """Remove widget from library"""
        widget = self.env['dashboard.widget'].browse([widget_id])
        if widget and widget.library_id.id == self.id:
            widget.write({'library_id': False})
            self.write({'widget_count': max(0, self.widget_count - 1)})
    
    def update_usage_count(self):
        """Update usage count based on widget usage"""
        total_usage = sum(widget.position_ids for widget in self.widget_ids)
        self.write({'usage_count': len(total_usage)})
    
    def get_popular_widgets(self, limit=10):
        """Get most popular widgets in library"""
        widgets = self.widget_ids.filtered(lambda w: w.active)
        # Sort by usage (number of positions)
        popular_widgets = sorted(widgets, key=lambda w: len(w.position_ids), reverse=True)
        return popular_widgets[:limit]
    
    def get_recent_widgets(self, limit=10):
        """Get most recent widgets in library"""
        widgets = self.widget_ids.filtered(lambda w: w.active)
        recent_widgets = sorted(widgets, key=lambda w: w.create_date, reverse=True)
        return recent_widgets[:limit]
    
    def get_widgets_by_type(self, widget_type):
        """Get widgets by type"""
        return self.widget_ids.filtered(lambda w: w.active and w.widget_type == widget_type)
    
    def create_widget_from_template(self, template_widget_id, name=None):
        """Create widget from template in library"""
        template_widget = self.env['dashboard.widget'].browse([template_widget_id])
        if not template_widget or not template_widget.is_template:
            raise ValueError("Template widget not found")
        
        widget_name = name or f"{template_widget.name} - {self.name}"
        
        new_widget = template_widget.duplicate_widget(widget_name)
        new_widget.write({
            'library_id': self.id,
            'is_template': False,
        })
        
        return new_widget