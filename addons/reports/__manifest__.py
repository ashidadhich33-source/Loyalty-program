#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Reports Addon Manifest
=========================================

Reports addon for financial reports, analytics, dashboards, and exports.
"""

{
    'name': 'Reports',
    'version': '1.0.0',
    'category': 'Reporting',
    'summary': 'Financial reports, analytics, dashboards, and exports',
    'description': '''
        Reports Addon for Kids Clothing ERP
        
        Features:
        - Financial Reports (P&L, Balance Sheet, Cash Flow)
        - Sales Reports (Revenue, Orders, Customers)
        - Inventory Reports (Stock, Valuation, Movement)
        - Purchase Reports (Vendor Analysis, Cost Analysis)
        - Custom Report Builder
        - Export to Excel, PDF, CSV
        - Scheduled Reports
        - Report Templates
        - Dashboard Widgets
    ''',
    'author': 'Kids Clothing ERP Team',
    'website': 'https://kidsclothingerp.com',
    'depends': [
        'core_base',
        'core_web',
        'users',
        'company',
        'contacts',
        'products',
        'sales',
        'purchase',
        'inventory',
        'accounting',
    ],
    'data': [
        'security/reports_security.xml',
        'data/report_templates.xml',
        'data/report_categories.xml',
        'views/report_views.xml',
        'views/dashboard_views.xml',
        'views/report_builder_views.xml',
        'views/menu_views.xml',
    ],
    'demo': [
        'demo/report_demo.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}