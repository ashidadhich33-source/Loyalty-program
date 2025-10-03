#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - POS Exchange Addon
=====================================

Exchange handling system for kids clothing retail.
"""

{
    'name': 'POS Exchange',
    'version': '1.0.0',
    'category': 'Sales',
    'summary': 'Exchange handling system for kids clothing retail',
    'description': """
        POS Exchange System for Kids Clothing ERP
        =========================================
        
        This addon provides comprehensive exchange functionality
        specifically designed for kids clothing retail business.
        
        Features:
        - Product exchange handling
        - Size exchange management
        - Color exchange management
        - Age group exchange tracking
        - Exchange approval workflow
        - Exchange analytics and reporting
        - Exchange policies and rules
        - Customer exchange history
    """,
    'author': 'Kids Clothing ERP Team',
    'website': 'https://www.kidsclothingerp.com',
    'license': 'LGPL-3',
    'depends': [
        'ocean_base',
        'ocean_web',
        'ocean_users',
        'ocean_company',
        'ocean_contacts',
        'ocean_products',
        'ocean_pos',
        'ocean_sales',
    ],
    'data': [
        'security/ocean.model.access.csv',
        'security/security.xml',
        'data/data.xml',
        'views/menu.xml',
        'views/exchange_request_views.xml',
        'views/exchange_approval_views.xml',
        'views/exchange_analytics_views.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
    'assets': {
        'ocean.assets_backend': [
            'pos_exchange/static/src/css/exchange_style.css',
            'pos_exchange/static/src/js/exchange_script.js',
        ],
    },
    'installable': True,
    'auto_install': False,
    'application': False,
}