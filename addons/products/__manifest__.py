# -*- coding: utf-8 -*-
{
    'name': 'Products',
    'version': '1.0.0',
    'category': 'Master Data',
    'summary': 'Product catalog management for kids clothing retail',
    'description': """
        Products Management for Kids Clothing Retail ERP
        
        This addon provides comprehensive product catalog management specifically designed for kids clothing retail:
        
        Key Features:
        - Product catalog with variants (size, color, age group)
        - Product categories (babywear, toddler, teen)
        - Product attributes (fabric, style, season)
        - Product variants and combinations
        - Product images and media
        - Product pricing and cost management
        - Product availability and stock tracking
        - Product tags and search
        - Kids clothing specific fields
        - Age group and size management
        - Brand and color preferences
        - Season-based categorization
        - Product bundles and sets
        - Bulk import/export functionality
        - Product analytics and reporting
        
        Business Logic:
        - Age group categorization (0-2, 2-4, 4-6, 6-8, 8-10, 10-12, 12-14, 14-16)
        - Size management (XS, S, M, L, XL, XXL, XXXL)
        - Color and brand preferences
        - Season-based product management
        - Product variant management
        - Pricing rules and cost management
        - Product availability tracking
        - Product performance analytics
        
        Technical Features:
        - Product template and variants
        - Product categories and subcategories
        - Product attributes and values
        - Product images and media
        - Product pricing and cost
        - Product availability
        - Product tags and search
        - Product analytics
        - Bulk operations
        - Import/export functionality
    """,
    'author': 'Kids Clothing ERP Team',
    'website': 'https://kidsclothingerp.com',
    'license': 'LGPL-3',
    'depends': [
        'core_base',
        'core_web',
        'users',
        'company',
        'contacts',
    ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/data.xml',
        'views/product_template_views.xml',
        'views/product_variant_views.xml',
        'views/product_category_views.xml',
        'views/product_attribute_views.xml',
        'views/product_tag_views.xml',
        'views/product_bundle_views.xml',
        'views/product_analytics_views.xml',
        'views/menu.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'products/static/src/js/product_script.js',
            'products/static/src/css/product_style.css',
        ],
    },
    'installable': True,
    'auto_install': False,
    'application': False,
}