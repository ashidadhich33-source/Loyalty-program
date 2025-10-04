#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Analytics Addon Manifest
==========================================

Analytics addon for advanced analytics and insights.
"""

{
    'name': 'Analytics',
    'version': '1.0.0',
    'category': 'Reporting',
    'summary': 'Advanced analytics and insights',
    'description': '''
        Analytics Addon for Kids Clothing ERP
        
        Features:
        - Advanced Data Analytics
        - Predictive Analytics
        - Business Intelligence
        - Data Mining
        - Statistical Analysis
        - Trend Analysis
        - Performance Analytics
        - Customer Analytics
        - Sales Analytics
        - Inventory Analytics
        - Financial Analytics
        - Real-time Analytics
        - Custom Analytics Models
        - Analytics Dashboards
        - Data Visualization
        - Analytics Reports
        - Machine Learning Integration
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
        'contacts',
        'products',
        'sales',
        'purchase',
        'inventory',
    ],
    'data': [
        'security/analytics_security.xml',
        'data/analytics_models.xml',
        'data/analytics_metrics.xml',
        'views/analytics_views.xml',
        'views/analytics_dashboard_views.xml',
        'views/menu_views.xml',
    ],
    'demo': [
        'demo/analytics_demo.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}