# -*- coding: utf-8 -*-
{
    'name': 'Website',
    'version': '1.0.0',
    'category': 'Website',
    'summary': 'Website functionality for Ocean ERP',
    'description': """
Website Module
==============

This module provides comprehensive website functionality including:

* Website Builder and Management
* Page Templates and Layouts
* Content Management System (CMS)
* SEO Optimization
* Multi-language Support
* Responsive Design
* Kids Clothing Specific Templates
* Indian Localization
* E-commerce Integration
* Blog and News Management
* Contact Forms and Lead Generation
* Analytics and Tracking

Features:
---------
* Drag-and-drop Website Builder
* Pre-built Kids Clothing Templates
* Mobile-responsive Design
* SEO-friendly URLs and Meta Tags
* Multi-language Content
* Image and Media Management
* Form Builder and Lead Capture
* Social Media Integration
* Google Analytics Integration
* Indian Payment Gateway Integration
* Kids Clothing Product Showcase
* Age Group Specific Pages
* Seasonal Campaign Pages
* Brand Showcase Pages
* Customer Reviews and Testimonials
* Newsletter Subscription
* Contact and Support Pages
    """,
    'author': 'Ocean ERP',
    'website': 'https://www.oceanerp.com',
    'depends': [
        'core_framework',
        'l10n_in',
        'contacts',
        'products',
        'invoicing',
        'payments',
    ],
    'data': [
        'security/ir.model.access.csv',
        'security/ocean.model.access.csv',
        'data/website_data.xml',
        'data/page_template_data.xml',
        'data/menu_data.xml',
        'views/website_views.xml',
        'views/page_views.xml',
        'views/template_views.xml',
        'views/content_views.xml',
        'views/form_views.xml',
        'views/analytics_views.xml',
        'views/menu.xml',
    ],
    'demo': [
        'demo/website_demo.xml',
        'demo/page_demo.xml',
        'demo/content_demo.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'website/static/src/css/website.css',
            'website/static/src/js/website.js',
        ],
        'web.assets_frontend': [
            'website/static/src/css/frontend.css',
            'website/static/src/js/frontend.js',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}