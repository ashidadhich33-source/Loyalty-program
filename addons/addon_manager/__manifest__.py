# -*- coding: utf-8 -*-
{
    'name': 'Addon Manager',
    'version': '1.0.0',
    'category': 'Administration',
    'summary': 'Addon management system for Ocean ERP',
    'description': """
        Addon Manager Module
        ===================
        
        This module provides comprehensive addon management functionality:
        
        * Browse available addons
        * Install/uninstall addons
        * Manage addon dependencies
        * Update addons
        * Addon marketplace integration
        * Addon development tools
        * Addon templates and scaffolding
        
        This module enables Ocean ERP to work like Odoo with full addon management.
    """,
    'author': 'Ocean ERP Team',
    'website': 'https://www.oceanerp.com',
    'license': 'LGPL-3',
    'depends': ['core_base', 'core_web', 'users'],
    'data': [
        'security/ocean.model.access.csv',
        'security/security.xml',
        'data/data.xml',
        'views/menu.xml',
        'views/addon_manager_views.xml',
        'views/addon_marketplace_views.xml',
        'views/addon_development_views.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'addon_manager/static/src/css/addon_manager.css',
            'addon_manager/static/src/js/addon_manager.js',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
}