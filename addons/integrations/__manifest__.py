#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Integrations Addon Manifest
==============================================

Integrations addon for API and 3rd party integrations.
"""

{
    'name': 'Integrations',
    'version': '1.0.0',
    'category': 'Utilities',
    'summary': 'API and 3rd party integrations',
    'description': '''
        Integrations Addon for Kids Clothing ERP
        
        Features:
        - REST API Management
        - Webhook Management
        - Third-party Integrations
        - Payment Gateway Integration
        - Shipping Integration
        - Accounting Integration
        - CRM Integration
        - E-commerce Integration
        - Social Media Integration
        - Email Service Integration
        - SMS Service Integration
        - Cloud Storage Integration
        - Integration Monitoring
        - Integration Testing
        - Integration Documentation
    ''',
    'author': 'Kids Clothing ERP Team',
    'website': 'https://kidsclothingerp.com',
    'depends': [
        'core_base',
        'core_web',
        'users',
        'company',
        'notifications',
    ],
    'data': [
        'security/integrations_security.xml',
        'data/integration_templates.xml',
        'data/api_endpoints.xml',
        'views/integration_views.xml',
        'views/api_management_views.xml',
        'views/webhook_views.xml',
        'views/menu_views.xml',
    ],
    'demo': [
        'demo/integrations_demo.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}