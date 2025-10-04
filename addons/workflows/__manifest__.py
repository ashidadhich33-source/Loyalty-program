#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Workflows Addon Manifest
===========================================

Workflows addon for user-defined business processes.
"""

{
    'name': 'Workflows',
    'version': '1.0.0',
    'category': 'Customization',
    'summary': 'User-defined business processes',
    'description': '''
        Workflows Addon for Kids Clothing ERP
        
        Features:
        - Visual Workflow Designer
        - Process Automation
        - Approval Workflows
        - Task Management
        - Workflow Templates
        - Conditional Logic
        - Parallel Processing
        - Workflow Monitoring
        - Performance Analytics
        - Workflow Versioning
        - Integration Points
        - Custom Actions
        - Workflow Scheduling
        - Error Handling
        - Workflow Testing
    ''',
    'author': 'Kids Clothing ERP Team',
    'website': 'https://kidsclothingerp.com',
    'depends': [
        'core_base',
        'core_web',
        'users',
        'company',
        'studio',
        'custom_fields',
    ],
    'data': [
        'security/workflows_security.xml',
        'data/workflow_templates.xml',
        'data/workflow_actions.xml',
        'views/workflow_views.xml',
        'views/workflow_designer_views.xml',
        'views/workflow_execution_views.xml',
        'views/menu_views.xml',
    ],
    'demo': [
        'demo/workflows_demo.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}