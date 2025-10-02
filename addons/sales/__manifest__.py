# -*- coding: utf-8 -*-
{
    'name': 'Sales Management',
    'version': '1.0.0',
    'category': 'Sales',
    'summary': 'Sales orders, quotations, deliveries, and returns management',
    'description': """
        Sales Management Module for Kids Clothing ERP
        ============================================
        
        This module provides comprehensive sales management for the Kids Clothing ERP system:
        
        Features:
        ---------
        * Sales Orders: Create and manage sales orders with order lines
        * Sales Quotations: Send price quotes to customers
        * Sales Deliveries: Manage product deliveries to customers
        * Sales Returns: Handle product returns and refunds
        * Sales Teams: Organize and manage sales teams
        * Sales Territories: Define and assign sales territories
        * Sales Commissions: Calculate and manage sales commissions
        * Sales Analytics: Provide insights into sales performance
        
        Kids Clothing Specific Features:
        ---------------------------------
        * Age group-based sales tracking
        * Gender-specific sales analytics
        * Season-based sales management
        * Size and color variant support
        * Child profile integration
        * Kids clothing specific pricing
        
        Indian Localization:
        --------------------
        * GST compliance and reporting
        * Indian currency formatting
        * Multi-company support
        * Indian address format support
    """,
    'author': 'Kids Clothing ERP Development Team',
    'website': 'https://www.kidsclothingerp.com',
    'license': 'LGPL-3',
    'depends': [
        'core_base',
        'core_web',
        'users',
        'company',
        'contacts',
        'products',
        'categories',
        'bulk_import',
    ],
    'data': [
        # Security
        'security/security.xml',
        'security/erp.model.access.csv',
        
        # Data
        'data/data.xml',
        
        # Views
        'views/menu.xml',
        'views/sale_order_views.xml',
        'views/sale_quotation_views.xml',
        'views/sale_delivery_views.xml',
        'views/sale_return_views.xml',
        'views/sale_team_views.xml',
        'views/sale_territory_views.xml',
        'views/sale_commission_views.xml',
        'views/sale_analytics_views.xml',
        
        # Wizards
        'wizard/sale_commission_wizard.xml',
        'wizard/sale_analytics_wizard.xml',
        
        # Demo
        'demo/demo.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'sales/static/src/css/sales_style.css',
            'sales/static/src/js/sales_script.js',
        ],
    },
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}