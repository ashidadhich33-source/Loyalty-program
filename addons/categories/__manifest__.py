# -*- coding: utf-8 -*-
{
    'name': 'Categories',
    'version': '1.0.0',
    'category': 'Master Data',
    'summary': 'Product categories management for kids clothing retail',
    'description': """
        Categories Management for Kids Clothing Retail ERP
        
        This addon provides comprehensive product category management specifically designed for kids clothing retail:
        
        Key Features:
        - Product categories (babywear, toddler, teen)
        - Age group based categorization
        - Gender-based categorization
        - Season-based categorization
        - Brand-based categorization
        - Hierarchical category structure
        - Category attributes and properties
        - Category images and icons
        - Category analytics and reporting
        - Category performance tracking
        - Category-based pricing rules
        - Category-based discount rules
        - Category-based inventory rules
        - Category-based marketing rules
        
        Business Logic:
        - Age group categorization (0-2, 2-4, 4-6, 6-8, 8-10, 10-12, 12-14, 14-16)
        - Gender categorization (boys, girls, unisex)
        - Season categorization (summer, winter, monsoon, all-season)
        - Brand categorization (premium, mid-range, budget)
        - Category hierarchy management
        - Category performance analytics
        - Category-based business rules
        
        Technical Features:
        - Hierarchical category structure
        - Category attributes and values
        - Category images and icons
        - Category analytics
        - Category performance tracking
        - Category-based rules
        - Category import/export
        - Category bulk operations
    """,
    'author': 'Kids Clothing ERP Team',
    'website': 'https://kidsclothingerp.com',
    'license': 'LGPL-3',
    'depends': [
        'core_base',
        'core_web',
        'users',
        'company',
        'products',
    ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/data.xml',
        'views/category_views.xml',
        'views/category_analytics_views.xml',
        'views/menu.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'categories/static/src/js/category_script.js',
            'categories/static/src/css/category_style.css',
        ],
    },
    'installable': True,
    'auto_install': False,
    'application': False,
}