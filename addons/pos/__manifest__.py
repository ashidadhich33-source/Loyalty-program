# -*- coding: utf-8 -*-
{
    'name': 'Point of Sale',
    'version': '1.0.0',
    'category': 'Sales',
    'summary': 'Point of Sale management for Kids Clothing retail',
    'description': """
        Point of Sale Management for Kids Clothing ERP
        ============================================
        
        This addon provides comprehensive POS functionality:
        
        * POS Configuration
        * POS Orders and Order Lines
        * POS Payments
        * POS Receipts
        * POS Sessions
        * POS Analytics
        * Kids Clothing Specific Features
        
        Features:
        - Complete POS configuration
        - Order management and processing
        - Payment processing
        - Receipt generation
        - Session management
        - POS analytics and reporting
        - Kids clothing specific POS features
        - Age group and size management
        - Seasonal promotions
        - Customer-specific pricing
    """,
    'author': 'Kids Clothing ERP Team',
    'website': 'https://www.kidsclothingerp.com',
    'license': 'LGPL-3',
    'depends': [
        'core_base',
        'core_web',
        'users',
        'company',
        'contacts',
        'products',
        'inventory',
    ],
    'data': [
        'security/ocean.model.access.csv',
        'security/security.xml',
        'data/data.xml',
        'views/menu.xml',
        'views/pos_config_views.xml',
        'views/pos_order_views.xml',
        'views/pos_payment_views.xml',
        'views/pos_receipt_views.xml',
        'views/pos_session_views.xml',
        'views/pos_analytics_views.xml',
        'views/pos_customer_wizard_views.xml',
        'views/pos_loyalty_wizard_views.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'pos/static/src/css/pos_style.css',
            'pos/static/src/js/pos_script.js',
        ],
    },
    'installable': True,
    'auto_install': False,
    'application': True,
}