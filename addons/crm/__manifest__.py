#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - CRM Addon
============================

Customer relationship management for kids clothing retail including leads, opportunities, and activities.
"""

{
    'name': 'CRM',
    'version': '1.0.0',
    'category': 'Sales',
    'summary': 'Customer relationship management for kids clothing retail',
    'description': """
        CRM Management for Kids Clothing ERP
        =====================================
        
        This addon provides comprehensive customer relationship management
        specifically designed for kids clothing retail business.
        
        Features:
        - Lead management and conversion
        - Opportunity tracking and forecasting
        - Activity management and scheduling
        - Communication history tracking
        - Customer segmentation and targeting
        - Campaign management
        - Performance analytics and reporting
        - Integration with sales and marketing
    """,
    'author': 'Kids Clothing ERP Team',
    'website': 'https://www.kidsclothingerp.com',
    'license': 'LGPL-3',
    'depends': [
        'core_base',
        'core_web',
        'users',
        'company',
        'contacts',
        'sales',
    ],
    'data': [
        'security/ocean.model.access.csv',
        'security/security.xml',
        'data/data.xml',
        'views/menu.xml',
        'views/lead_views.xml',
        'views/opportunity_views.xml',
        'views/activity_views.xml',
        'views/communication_views.xml',
        'views/campaign_views.xml',
        'views/crm_analytics_views.xml',
        'wizard/crm_wizard_views.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
    'assets': {
        'ocean.assets_backend': [
            'crm/static/src/css/crm_style.css',
            'crm/static/src/js/crm_script.js',
        ],
    },
    'installable': True,
    'auto_install': False,
    'application': False,
}