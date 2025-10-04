# -*- coding: utf-8 -*-
{
    'name': 'Warehouse Management',
    'version': '1.0.0',
    'category': 'Inventory',
    'summary': 'Warehouse management, stock aging, and expiry tracking for kids clothing retail',
    'description': """
        Warehouse Management System
        ==========================
        
        Comprehensive warehouse management system designed specifically for kids clothing retail:
        
        * Warehouse Management
          - Multiple warehouse types (Main, Branch, Distribution, Retail, Online, Return, Seasonal)
          - Physical properties (area, capacity, temperature, humidity control)
          - Security levels and access control
          - Performance metrics (turnover rate, accuracy rate)
          - Address and contact information
        
        * Warehouse Location Management
          - Detailed location hierarchy (Zone → Aisle → Rack → Shelf → Bin)
          - Physical coordinates and dimensions
          - Capacity and weight management
          - Temperature and humidity control
          - Age-group specific locations
          - Security and access control
          - Performance tracking (pick frequency, last pick date)
        
        * Stock Aging Analysis
          - Complete aging categories (0-30, 31-60, 61-90, 91-180, 181-365, 365+ days)
          - Age group and seasonal filtering
          - Aging status determination (Fresh, Current, Aging, Stale, Obsolete)
          - Action recommendations (Promotion, Discount, Clearance, Return, Donate, Dispose)
          - Priority levels and risk assessment
          - Turnover rate and average age calculations
        
        * Stock Expiry Management
          - Expiry categories (Expired, 7 days, 15 days, 30 days, 60 days, 90 days, No expiry)
          - Expiry status determination (Critical, Urgent, Warning, Caution, Normal, No expiry)
          - Action recommendations (Immediate Sale, Clearance, Discount, Return, Donate, Dispose)
          - Expiry risk scoring (0-100)
          - Average days to expiry calculations
          - Alert system for expiring items
        
        * Warehouse Operations
          - Complete operation lifecycle (Draft → In Progress → Done)
          - Multiple operation types (Receiving, Putaway, Picking, Packing, Shipping, Inventory, Transfer, Adjustment, Quality Check, Maintenance)
          - Performance metrics (efficiency score, accuracy score)
          - Duration tracking and variance analysis
          - Quality control requirements
          - Customer age and product age group tracking
        
        * Kids Clothing Specific Features
          - Age-group specialized warehouses
          - Seasonal storage capabilities
          - Temperature-controlled storage for sensitive items
          - Special toddler section with restricted access
          - Age-group filtering in aging and expiry analysis
          - Seasonal category tracking
          - Quality control for children's clothing
    """,
    'author': 'Kids Clothing ERP Team',
    'website': 'https://www.kidsclothing.com',
    'depends': [
        'base',
        'inventory',
        'products',
        'contacts',
    ],
    'data': [
        'security/security.xml',
        'security/ocean.model.access.csv',
        'data/data.xml',
        'demo/demo.xml',
        'views/menu.xml',
        'views/warehouse_views.xml',
        'views/warehouse_location_views.xml',
        'views/stock_aging_views.xml',
        'views/stock_expiry_views.xml',
        'views/warehouse_operation_views.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'warehouse/static/src/css/warehouse_style.css',
            'warehouse/static/src/js/warehouse_script.js',
        ],
    },
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}