# -*- coding: utf-8 -*-
{
    'name': 'Company Management',
    'version': '1.0.0',
    'category': 'Core',
    'summary': 'Company setup, multi-company support, and GSTIN management for Kids Clothing ERP',
    'description': """
        Company Management Module
        ========================
        
        This module provides comprehensive company management functionality for the Kids Clothing ERP system:
        
        * Company setup and configuration
        * Multi-company support
        * GSTIN management and validation
        * Company-specific settings
        * Branch and location management
        * Company hierarchy
        * Financial year management
        * Company-specific user access
        * Company analytics and reporting
        * Company document management
        * Company communication settings
        
        This module handles all company-related functionality and multi-company operations.
    """,
    'author': 'Kids Clothing ERP Team',
    'website': 'https://www.kidsclothingerp.com',
    'license': 'LGPL-3',
    'depends': ['core_base', 'core_web', 'users'],
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'data/data.xml',
        'views/menu.xml',
        'views/company_views.xml',
        'views/branch_views.xml',
        'views/location_views.xml',
        'views/financial_year_views.xml',
        'views/company_settings_views.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'company/static/src/css/company_style.css',
            'company/static/src/js/company_script.js',
        ],
    },
    'installable': True,
    'application': False,
    'auto_install': True,
}