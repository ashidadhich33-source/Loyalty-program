#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Dashboard Addon Manifest
===========================================

Dashboard addon for customizable dashboards and widgets.
"""

{
    'name': 'Dashboard',
    'version': '1.0.0',
    'category': 'Reporting',
    'summary': 'Customizable dashboards and widgets',
    'description': '''
        Dashboard Addon for Kids Clothing ERP
        
        Features:
        - Customizable Dashboards
        - Drag & Drop Widgets
        - Real-time Data Updates
        - Multiple Dashboard Themes
        - Widget Library
        - Dashboard Sharing
        - Mobile Responsive Design
        - Export Dashboard as PDF/Image
        - Dashboard Templates
        - Widget Configuration
    ''',
    'author': 'Kids Clothing ERP Team',
    'website': 'https://kidsclothingerp.com',
    'depends': [
        'core_base',
        'core_web',
        'users',
        'company',
        'reports',
    ],
    'data': [
        'security/dashboard_security.xml',
        'data/dashboard_templates.xml',
        'data/widget_templates.xml',
        'views/dashboard_views.xml',
        'views/widget_views.xml',
        'views/menu_views.xml',
    ],
    'demo': [
        'demo/dashboard_demo.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}