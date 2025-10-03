# -*- coding: utf-8 -*-
{
    'name': 'Kids Clothing ERP System',
    'version': '1.0.0',
    'category': 'ERP',
    'summary': 'Complete ERP system for kids clothing retail industry',
    'description': """
        Kids Clothing ERP System
        =======================
        
        A comprehensive ERP system designed specifically for kids clothing retail businesses.
        Features include:
        
        * Core Framework - System configuration, users, company management
        * Master Data - Products, categories, contacts with kids-specific fields
        * Sales & CRM - Quotations, orders, loyalty programs, customer segmentation
        * Point of Sale - Fast checkout, exchange/return handling, multi-payment
        * Inventory - Multi-location warehouse, stock management, procurement
        * Accounting - Chart of accounts, invoicing, payments, GST compliance
        * Indian Localization - GST, E-invoice, E-way bill, statutory compliance
        * HR & Payroll - Employee management, attendance, payroll processing
        * E-commerce - Online storefront, customer portal, order tracking
        * Reporting - Pre-built reports, custom dashboards, analytics
        * Customization - Studio, custom fields, workflows, automated actions
        
        Designed for Indian retail businesses with GST compliance and local features.
    """,
    'author': 'Kids Clothing ERP Team',
    'website': 'https://www.kidsclothingerp.com',
    'license': 'LGPL-3',
    'depends': [],
    'data': [
        'security/ocean.model.access.csv',
        'data/data.xml',
        'views/menu.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'kids_clothing_erp/static/src/css/style.css',
            'kids_clothing_erp/static/src/js/script.js',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
}