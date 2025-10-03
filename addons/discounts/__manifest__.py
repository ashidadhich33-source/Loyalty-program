#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Discounts Addon
===================================

Discount program management for kids clothing retail.
"""

{
    'name': 'Discount Programs',
    'version': '1.0.0',
    'category': 'Sales/Discounts',
    'summary': 'Comprehensive discount programs with approval flows and coupon codes',
    'description': """
Kids Clothing ERP - Discount Programs
====================================

This addon provides comprehensive discount program management for kids clothing retail:

* Discount program configuration
* Approval workflows for discounts
* Coupon code generation and management
* Seasonal discount campaigns
* Age group and gender specific discounts
* Bulk discount applications
* Discount analytics and reporting

Features:
---------
* Multiple discount types (percentage, fixed, buy X get Y)
* Approval workflows for discount applications
* Coupon code generation and validation
* Seasonal and promotional campaigns
* Age group and gender targeting
* Bulk discount operations
* Discount analytics and insights
* Integration with loyalty programs
* Discount expiry management
* Usage tracking and limits
""",
    'author': 'Kids Clothing ERP Team',
    'website': 'https://www.kidsclothingerp.com',
    'depends': [
        'core_base',
        'contacts',
        'sales',
        'products',
        'loyalty',
    ],
    'data': [
        'security/security.xml',
        'security/ocean.model.access.csv',
        'data/data.xml',
        'demo/demo.xml',
        'views/discount_program_views.xml',
        'views/discount_rule_views.xml',
        'views/discount_coupon_views.xml',
        'views/discount_approval_views.xml',
        'views/discount_campaign_views.xml',
        'views/discount_analytics_views.xml',
        'views/menu.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
    'assets': {
        'ocean.assets_backend': [
            'discounts/static/src/js/discounts_script.js',
            'discounts/static/src/css/discounts_style.css',
        ],
    },
    'installable': True,
    'auto_install': False,
    'application': False,
    'license': 'LGPL-3',
}