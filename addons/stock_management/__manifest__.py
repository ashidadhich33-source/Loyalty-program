# -*- coding: utf-8 -*-
{
    'name': 'Stock Management',
    'version': '1.0.0',
    'category': 'Inventory',
    'summary': 'Advanced stock management for Kids Clothing retail',
    'description': """
        Stock Management for Kids Clothing ERP
        =====================================
        
        This addon provides advanced stock management functionality:
        
        * Reorder Rules
        * Stock Adjustments
        * Stock Alerts
        * Stock Analysis
        * Kids Clothing Specific Features
        
        Features:
        - Automated reorder rules
        - Stock adjustment management
        - Stock alert system
        - Advanced stock analysis
        - Kids clothing specific stock management
        - Age group and seasonal analysis
        - Size and color tracking
        - Brand-specific management
        - Quality control alerts
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
        'inventory',
    ],
    'data': [
        'security/ocean.model.access.csv',
        'data/data.xml',
        'views/menu.xml',
        'views/reorder_rule_views.xml',
        'views/stock_adjustment_views.xml',
        'views/stock_alert_views.xml',
        'views/stock_analysis_views.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'stock_management/static/src/css/stock_management_style.css',
            'stock_management/static/src/js/stock_management_script.js',
        ],
    },
    'installable': True,
    'auto_install': False,
    'application': False,
}