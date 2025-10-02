# -*- coding: utf-8 -*-
{
    'name': 'Kids Clothing Retail ERP',
    'version': '17.0.1.0.0',
    'category': 'Sales/CRM',
    'summary': 'Odoo-style ERP for Kids Clothing Retail Industry',
    'description': """
Kids Clothing Retail ERP System
==============================

A comprehensive ERP system designed specifically for the Kids' Clothing Retail Industry,
built as an Odoo clone with the same architecture and technology stack.

Key Features:
- Sales Management
- Point of Sale (POS)
- Inventory Management
- Purchase Management
- Accounting & Finance
- Customer Relationship Management (CRM)
- Human Resources
- Reporting & Analytics
- Multi-company Support
- Multi-language Support
- Customizable Dashboard
- Mobile Responsive Interface

Modules:
- Sales: Quotations, Sales Orders, Invoicing
- POS: Point of Sale for retail operations
- Inventory: Stock management, warehouse operations
- Purchase: Procurement, supplier management
- Accounting: Financial management, reporting
- CRM: Lead management, customer relationships
- HR: Employee management, payroll
- Reports: Custom reports, analytics
    """,
    'author': 'ERP Development Team',
    'website': 'https://www.erpcompany.com',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'web',
        'mail',
        'portal',
        'sale',
        'purchase',
        'stock',
        'account',
        'hr',
        'crm',
        'point_of_sale',
        'website',
        'website_sale',
    ],
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'data/data.xml',
        'views/menu.xml',
        'views/sale_views.xml',
        'views/pos_views.xml',
        'views/inventory_views.xml',
        'views/purchase_views.xml',
        'views/account_views.xml',
        'views/crm_views.xml',
        'views/hr_views.xml',
        'views/reports.xml',
        'wizard/wizard_views.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
    'qweb': [
        'static/src/xml/pos_templates.xml',
        'static/src/xml/reports.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'kids_clothing_erp/static/src/css/erp.css',
            'kids_clothing_erp/static/src/js/erp.js',
        ],
        'web.assets_frontend': [
            'kids_clothing_erp/static/src/css/website.css',
            'kids_clothing_erp/static/src/js/website.js',
        ],
        'point_of_sale.assets': [
            'kids_clothing_erp/static/src/css/pos.css',
            'kids_clothing_erp/static/src/js/pos.js',
        ],
    },
    'images': [
        'static/description/banner.png',
        'static/description/icon.png',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'sequence': 1,
}