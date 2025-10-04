# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Purchase Addon
=================================

Purchase management for kids clothing retail.
"""

{
    'name': 'Purchase Management',
    'version': '1.0.0',
    'category': 'Purchase',
    'summary': 'Purchase orders, supplier management, and procurement',
    'description': """
        Purchase Management for Kids Clothing ERP
        ========================================
        
        This addon provides comprehensive purchase management functionality:
        
        * Supplier Management
        * Purchase Orders
        * Purchase Order Lines
        * Vendor Bills
        * Purchase Analytics
        * Kids Clothing Specific Features
        
        Features:
        - Supplier relationship management
        - Purchase order creation and management
        - Vendor bill processing
        - Purchase analytics and reporting
        - Kids clothing specific procurement
        - Age group and seasonal purchasing
        - Size range management
        - Special occasion procurement
    """,
    'author': 'Ocean ERP Team',
    'website': 'https://ocean-erp.com',
    'depends': [
        'base',
        'inventory',
        'products',
        'contacts',
        'company',
    ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/data.xml',
        'views/menu.xml',
        'views/purchase_order_views.xml',
        'views/purchase_order_line_views.xml',
        'views/vendor_bill_views.xml',
        'views/purchase_analytics_views.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'purchase/static/src/css/purchase_style.css',
            'purchase/static/src/js/purchase_script.js',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}