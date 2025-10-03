#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Categories Addon
===================================

Product categories management for kids clothing retail.
Handles age-based categories, seasonal categories, and brand categories.
"""

{
    'name': 'Categories',
    'version': '1.0.0',
    'category': 'Sales',
    'summary': 'Product categories management for kids clothing',
    'description': """
        Categories Management for Kids Clothing ERP
        ==========================================
        
        This addon provides comprehensive product category management
        specifically designed for kids clothing retail business.
        
        Features:
        - Age-based categories (babywear, toddler, teen)
        - Seasonal categories (summer, winter, monsoon)
        - Brand categories and subcategories
        - Category hierarchy management
        - Category-based pricing rules
        - Category analytics and reporting
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
    ],
    'data': [
        'security/ocean.model.access.csv',
        'security/security.xml',
        'data/data.xml',
        'views/menu.xml',
        'views/category_views.xml',
        'views/category_hierarchy_views.xml',
        'views/category_analytics_views.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
    'assets': {
        'ocean.assets_backend': [
            'categories/static/src/css/category_style.css',
            'categories/static/src/js/category_script.js',
        ],
    },
    'installable': True,
    'auto_install': False,
    'application': False,
}