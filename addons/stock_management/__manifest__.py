# -*- coding: utf-8 -*-
{
    'name': 'Stock Management',
    'version': '1.0.0',
    'category': 'Inventory',
    'summary': 'Stock alerts, reorder rules, and adjustments for kids clothing retail',
    'description': """
        Stock Management System
        ======================
        
        Comprehensive stock management system designed specifically for kids clothing retail:
        
        * Stock Alerts Management
          - Low stock alerts with customizable thresholds
          - Age-group specific alert rules (babywear, toddler, teen)
          - Seasonal alert management (summer, winter, monsoon)
          - Size-specific alerts (XS, S, M, L, XL, XXL, XXXL)
          - Brand and color-specific alerts
          - Critical stock alerts with priority levels
          - Alert notification system (email, SMS, in-app)
          - Alert escalation and approval workflows
        
        * Reorder Rules Management
          - Automatic reorder point calculation
          - Age-group specific reorder rules
          - Seasonal reorder planning
          - Size-based reorder quantities
          - Brand and supplier-specific rules
          - Lead time consideration
          - Safety stock calculations
          - Economic order quantity (EOQ) optimization
          - Reorder approval workflows
          - Purchase order auto-generation
        
        * Stock Adjustments Management
          - Physical inventory adjustments
          - Cycle counting and variance analysis
          - Age-group specific adjustments
          - Seasonal stock adjustments
          - Size and color adjustments
          - Brand-specific adjustments
          - Adjustment approval workflows
          - Reason codes and documentation
          - Impact analysis and reporting
          - Integration with accounting
        
        * Stock Analysis and Reporting
          - Stock turnover analysis by age group
          - Seasonal stock performance
          - Size-wise stock analysis
          - Brand performance tracking
          - Color trend analysis
          - Stock aging reports
          - Reorder efficiency reports
          - Adjustment history and trends
          - Predictive analytics for stock planning
        
        * Kids Clothing Specific Features
          - Age-group specialized stock management
          - Seasonal stock planning and alerts
          - Size-specific reorder rules
          - Brand and color trend analysis
          - Special occasion stock management (festivals, back-to-school)
          - Growth-based size progression tracking
          - Quality control integration
          - Safety standards compliance
    """,
    'author': 'Kids Clothing ERP Team',
    'website': 'https://www.kidsclothing.com',
    'depends': [
        'base',
        'inventory',
        'warehouse',
        'products',
        'contacts',
        'purchase',
    ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/data.xml',
        'demo/demo.xml',
        'views/menu.xml',
        'views/stock_alert_views.xml',
        'views/reorder_rule_views.xml',
        'views/stock_adjustment_views.xml',
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
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}