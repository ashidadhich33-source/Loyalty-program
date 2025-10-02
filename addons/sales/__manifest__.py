# -*- coding: utf-8 -*-
{
    'name': 'Sales',
    'version': '1.0.0',
    'category': 'Sales & CRM',
    'summary': 'Sales management for kids clothing retail',
    'description': """
        Sales Management for Kids Clothing Retail ERP
        
        This addon provides comprehensive sales management specifically designed for kids clothing retail:
        
        Key Features:
        - Sales quotations and orders
        - Delivery orders and returns
        - Customer management and segmentation
        - Kids clothing specific sales features
        - Age group and gender-based sales
        - Season-based sales management
        - Brand and size-based sales
        - Sales analytics and reporting
        - Customer loyalty integration
        - Discount and promotion management
        - Multi-payment support
        - Indian localization (GST, tax compliance)
        - Sales team management
        - Territory management
        - Sales forecasting
        - Commission management
        
        Business Logic:
        - Kids clothing specific sales processes
        - Age group-based product recommendations
        - Gender-based sales strategies
        - Season-based sales campaigns
        - Size-based inventory management
        - Brand preference tracking
        - Customer lifecycle management
        - Sales performance analytics
        - Territory-based sales management
        - Commission calculation and tracking
        
        Technical Features:
        - Sales order management
        - Quotation management
        - Delivery order processing
        - Return and exchange handling
        - Customer segmentation
        - Sales analytics
        - Performance tracking
        - Commission management
        - Territory management
        - Sales forecasting
        - Multi-company support
        - Indian tax compliance
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
        'products',
        'categories',
    ],
    'data': [
        'security/security.xml',
        'security/erp.model.access.csv',
        'data/data.xml',
        'views/sale_order_views.xml',
        'views/sale_quotation_views.xml',
        'views/sale_delivery_views.xml',
        'views/sale_return_views.xml',
        'views/sale_team_views.xml',
        'views/sale_territory_views.xml',
        'views/sale_commission_views.xml',
        'views/sale_analytics_views.xml',
        'views/menu.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'sales/static/src/js/sales_script.js',
            'sales/static/src/css/sales_style.css',
        ],
    },
    'installable': True,
    'auto_install': False,
    'application': False,
}