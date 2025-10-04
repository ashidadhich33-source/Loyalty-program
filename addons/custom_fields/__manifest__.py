#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Custom Fields Addon Manifest
===============================================

Custom fields addon for dynamic field management.
"""

{
    'name': 'Custom Fields',
    'version': '1.0.0',
    'category': 'Customization',
    'summary': 'Dynamic field management system',
    'description': '''
        Custom Fields Addon for Kids Clothing ERP
        
        Features:
        - Dynamic Field Creation
        - Field Type Management
        - Field Validation Rules
        - Field Dependencies
        - Field Permissions
        - Field Migration
        - Field Templates
        - Bulk Field Operations
        - Field History Tracking
        - Field Usage Analytics
        - Custom Field Groups
        - Field Import/Export
        - Field Versioning
        - Field Testing
        - Field Documentation
    ''',
    'author': 'Kids Clothing ERP Team',
    'website': 'https://kidsclothingerp.com',
    'depends': [
        'core_base',
        'core_web',
        'users',
        'company',
        'studio',
    ],
    'data': [
        'security/custom_fields_security.xml',
        'data/field_types.xml',
        'data/field_templates.xml',
        'views/custom_fields_views.xml',
        'views/field_management_views.xml',
        'views/menu_views.xml',
    ],
    'demo': [
        'demo/custom_fields_demo.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}