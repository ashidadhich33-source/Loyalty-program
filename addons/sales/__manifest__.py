#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Sales Addon
===============================

Sales management for kids clothing retail including quotations, orders, and returns.
"""

{
    'name': 'Sales',
    'version': '1.0.0',
    'category': 'Sales',
    'summary': 'Sales management for kids clothing retail',
    'description': """
        Sales Management for Kids Clothing ERP
        =====================================
        
        This addon provides comprehensive sales management functionality
        specifically designed for kids clothing retail business.
        
        Features:
        - Sales quotations and orders
        - Delivery orders and returns
        - Customer-specific pricing
        - Age-based discounts
        - Seasonal promotions
        - Sales analytics and reporting
        - Multi-location sales support
        - Integration with inventory and accounting
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
    ],
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'data/data.xml',
        'views/menu.xml',
        'views/sale_order_views.xml',
        'views/sale_quotation_views.xml',
        'views/sale_delivery_views.xml',
        'views/sale_return_views.xml',
        'views/sale_analytics_views.xml',
        'wizard/sale_order_wizard_views.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
    'assets': {
        'ocean.assets_backend': [
            'sales/static/src/css/sales_style.css',
            'sales/static/src/js/sales_script.js',
        ],
    },
    'installable': True,
    'auto_install': False,
    'application': False,
}