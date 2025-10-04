# -*- coding: utf-8 -*-
{
    'name': 'Inventory Management',
    'version': '1.0.0',
    'category': 'Inventory',
    'summary': 'Inventory management for Kids Clothing retail',
    'description': """
        Inventory Management for Kids Clothing ERP
        =========================================
        
        This addon provides comprehensive inventory functionality:
        
        * Stock Inventory Management
        * Stock Location Management
        * Stock Move Tracking
        * Stock Picking Operations
        * Stock Quant Management
        * Kids Clothing Specific Features
        
        Features:
        - Complete inventory management
        - Location hierarchy management
        - Stock move tracking
        - Picking operations
        - Stock quantity management
        - Kids clothing specific inventory
        - Age group and size tracking
        - Seasonal inventory management
        - Brand and color tracking
        - Quality control
    """,
    'author': 'Kids Clothing ERP Team',
    'website': 'https://www.kidsclothingerp.com',
    'license': 'LGPL-3',
    'depends': [
        'core_base',
        'core_web',
        'users',
        'company',
        'products',
    ],
    'data': [
        'security/ocean.model.access.csv',
        'security/security.xml',
        'data/data.xml',
        'views/menu.xml',
        'views/stock_inventory_views.xml',
        'views/stock_location_views.xml',
        'views/stock_move_views.xml',
        'views/stock_picking_views.xml',
        'views/stock_quant_views.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'inventory/static/src/css/inventory_style.css',
        ],
    },
    'installable': True,
    'auto_install': False,
    'application': True,
}