#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Dashboard Model
===================================

Dashboard management for customizable dashboards.
"""

from core_framework.orm import (
    BaseModel, CharField, TextField, SelectionField, Many2OneField,
    BooleanField, One2ManyField, IntegerField
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
    ], 'Layout', default='grid')
    
    theme = SelectionField([
        ('light', 'Light Theme'),
        ('dark', 'Dark Theme'),
        ('colorful', 'Colorful Theme'),
        ('minimal', 'Minimal Theme'),
    ], 'Theme', default='light')
    
    # Widgets Configuration
    widget_ids = One2ManyField('dashboard.widget.position', 'dashboard_id', 'Widgets')
    
    # Access Control
    is_public = BooleanField('Public Dashboard', default=False)
    group_ids = One2ManyField('users.group', 'dashboard_group_ids', 'Access Groups')
    shared_with_ids = One2ManyField('users.user', 'shared_dashboard_ids', 'Shared With')
    
    # Status
    active = BooleanField('Active', default=True)
    
    def get_dashboard_config(self):
        """Get dashboard configuration for frontend"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'layout': self.layout,
            'theme': self.theme,
            'widgets': [widget.get_widget_config() for widget in self.widget_ids],
            'is_public': self.is_public,
        }
    
    def add_widget(self, widget_id, x_position=0, y_position=0, width=4, height=300):
        """Add widget to dashboard"""
        self.env['dashboard.widget.position'].create({
            'dashboard_id': self.id,
            'widget_id': widget_id,
            'x_position': x_position,
            'y_position': y_position,
            'width': width,
            'height': height,
        })
    
    def remove_widget(self, widget_position_id):
        """Remove widget from dashboard"""
        widget_position = self.env['dashboard.widget.position'].browse([widget_position_id])
        if widget_position:
            widget_position.unlink()
    
    def duplicate_dashboard(self, new_name=None):
        """Duplicate dashboard"""
        new_name = new_name or f"{self.name} (Copy)"
        
        new_dashboard = self.create({
            'name': new_name,
            'description': self.description,
            'user_id': self.user_id.id,
            'layout': self.layout,
            'theme': self.theme,
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
    
    def get_widget_config(self):
        """Get widget position configuration"""
        return {
            'id': self.id,
            'widget_id': self.widget_id.id,
            'widget_name': self.widget_id.name,
            'widget_type': self.widget_id.widget_type,
            'x_position': self.x_position,
            'y_position': self.y_position,
            'width': self.width,
            'height': self.height,
            'sequence': self.sequence,
            'config': self.widget_id.get_widget_config(),
        }