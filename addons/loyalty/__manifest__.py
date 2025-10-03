#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Loyalty Addon
================================

Loyalty program management for kids clothing retail.
"""

{
    'name': 'Loyalty Program',
    'version': '1.0.0',
    'category': 'Sales/Loyalty',
    'summary': 'Customer loyalty program with points, rewards, and special offers',
    'description': """
Kids Clothing ERP - Loyalty Program
===================================

This addon provides comprehensive loyalty program management for kids clothing retail:

* Customer loyalty points system
* Reward catalog management
* Voucher and coupon system
* Birthday and special occasion offers
* Loyalty tier management
* Points redemption tracking
* Loyalty analytics and reporting

Features:
---------
* Points earning and redemption
* Reward catalog with kids clothing items
* Voucher generation and management
* Birthday offer automation
* Loyalty tier progression
* Points expiry management
* Loyalty program analytics
* Customer loyalty insights
* Special promotion campaigns
* Referral program support
""",
    'author': 'Kids Clothing ERP Team',
    'website': 'https://www.kidsclothingerp.com',
    'depends': [
        'core_base',
        'contacts',
        'sales',
        'products',
    ],
    'data': [
        'security/security.xml',
        'security/ocean.model.access.csv',
        'data/data.xml',
        'demo/demo.xml',
        'views/loyalty_program_views.xml',
        'views/loyalty_points_views.xml',
        'views/loyalty_rewards_views.xml',
        'views/loyalty_vouchers_views.xml',
        'views/loyalty_offers_views.xml',
        'views/loyalty_tiers_views.xml',
        'views/loyalty_analytics_views.xml',
        'views/menu.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
    'assets': {
        'ocean.assets_backend': [
            'loyalty/static/src/js/loyalty_script.js',
            'loyalty/static/src/css/loyalty_style.css',
        ],
    },
    'installable': True,
    'auto_install': False,
    'application': False,
    'license': 'LGPL-3',
}