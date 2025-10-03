#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - POS Addon
=============================

Point of Sale system for kids clothing retail.
"""

{
    'name': 'POS',
    'version': '1.0.0',
    'category': 'Sales',
    'summary': 'Point of Sale system for kids clothing retail',
    'description': """
        Point of Sale System for Kids Clothing ERP
        ==========================================
        
        This addon provides comprehensive POS functionality
        specifically designed for kids clothing retail business.
        
        Features:
        - Product scanning and barcode support
        - Fast checkout with touchscreen UI
        - Multi-payment integration (UPI, Paytm, PhonePe, Cash, Card)
        - Customer management and loyalty integration
        - Receipt printing and customization
        - Inventory integration
        - Sales analytics and reporting
        - Multi-location support
        - Offline mode support
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
        'ocean_categories',
        'ocean_sales',
        'ocean_loyalty',
        'ocean_discounts',
    ],
    'data': [
        'security/ocean.model.access.csv',
        'security/security.xml',
        'data/data.xml',
        'views/menu.xml',
        'views/pos_order_views.xml',
        'views/pos_session_views.xml',
        'views/pos_config_views.xml',
        'views/pos_receipt_views.xml',
        'views/pos_analytics_views.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
    'assets': {
        'ocean.assets_backend': [
            'pos/static/src/css/pos_style.css',
            'pos/static/src/js/pos_script.js',
        ],
    },
    'installable': True,
    'auto_install': False,
    'application': False,
}