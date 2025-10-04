#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Studio Addon Manifest
========================================

Studio addon for low-code/no-code customization.
"""

{
    'name': 'Studio',
    'version': '1.0.0',
    'category': 'Customization',
    'summary': 'Low-code/no-code customization platform',
    'description': '''
        Studio Addon for Kids Clothing ERP
        
        Features:
        - Visual Model Builder
        - Drag & Drop Form Designer
        - Custom View Builder
        - Workflow Designer
        - Report Builder
        - Dashboard Designer
        - Custom Field Manager
        - Business Logic Builder
        - API Builder
        - Theme Customizer
        - Menu Customizer
        - Security Rule Builder
        - Data Migration Tools
        - Code Generator
        - Template Library
        - Version Control
        - Deployment Manager
    ''',
    'author': 'Kids Clothing ERP Team',
    'website': 'https://kidsclothingerp.com',
    'depends': [
        'core_base',
        'core_web',
        'users',
        'company',
        'reports',
        'dashboard',
        'analytics',
    ],
    'data': [
        'security/studio_security.xml',
        'data/studio_templates.xml',
        'data/studio_components.xml',
        'views/studio_views.xml',
        'views/model_builder_views.xml',
        'views/form_designer_views.xml',
        'views/workflow_designer_views.xml',
        'views/menu_views.xml',
    ],
    'demo': [
        'demo/studio_demo.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}