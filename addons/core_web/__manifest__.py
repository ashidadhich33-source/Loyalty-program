# -*- coding: utf-8 -*-
{
    'name': 'Core Web',
    'version': '1.0.0',
    'category': 'Core',
    'summary': 'Core web functionality for Kids Clothing ERP',
    'description': """
        Core Web Module
        ===============
        
        This module provides the core web functionality for the Kids Clothing ERP system:
        
        * Web client interface
        * UI assets and components
        * Menu structure and navigation
        * Notification system
        * Web utilities and helpers
        * Responsive design components
        * Kids-friendly UI themes
        
        This module handles all web-related functionality and user interface components.
    """,
    'author': 'Kids Clothing ERP Team',
    'website': 'https://www.kidsclothingerp.com',
    'license': 'LGPL-3',
    'depends': ['core_base'],
    'data': [
        'security/ir.model.access.csv',
        'data/data.xml',
        'views/menu.xml',
        'views/web_assets.xml',
        'views/notification_views.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'core_web/static/src/css/web_style.css',
            'core_web/static/src/js/web_script.js',
            'core_web/static/src/js/notification_system.js',
            'core_web/static/src/js/menu_enhancements.js',
        ],
        'web.assets_frontend': [
            'core_web/static/src/css/frontend_style.css',
            'core_web/static/src/js/frontend_script.js',
        ],
    },
    'installable': True,
    'application': False,
    'auto_install': True,
}