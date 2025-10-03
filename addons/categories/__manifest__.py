# -*- coding: utf-8 -*-
{
    'name': 'Product Categories',
    'version': '1.0.0',
    'category': 'Master Data',
    'summary': 'Product categorization system for kids clothing retail',
    'description': """
        Product Categories Management for Kids Clothing Retail ERP
        
        This addon provides comprehensive product categorization specifically designed for kids clothing retail:
        
        Key Features:
        - Hierarchical category structure (babywear, toddler, teen)
        - Age group based categorization
        - Gender specific categories
        - Season based categorization
        - Brand specific categories
        - Style based categories
        - Color based categories
        - Size based categories
        - Category analytics and reporting
        - Category performance tracking
        - Category management tools
        - Bulk category operations
        - Category import/export
        - Category templates
        - Category rules and validation
        
        Business Logic:
        - Age group categorization (0-2, 2-4, 4-6, 6-8, 8-10, 10-12, 12-14, 14-16)
        - Gender categorization (boys, girls, unisex)
        - Season categorization (summer, winter, monsoon, all-season)
        - Brand categorization (premium, mid-range, budget)
        - Style categorization (casual, formal, party, sports, ethnic)
        - Color categorization (primary colors, pastels, neutrals)
        - Size categorization (XS, S, M, L, XL, XXL, XXXL)
        - Category hierarchy management
        - Category performance analytics
        - Category rules and validation
        
        Technical Features:
        - Hierarchical category structure
        - Category templates
        - Category attributes
        - Category rules
        - Category analytics
        - Category management
        - Bulk operations
        - Import/export functionality
        - Category validation
        - Category performance tracking
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