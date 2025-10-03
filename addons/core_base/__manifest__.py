# -*- coding: utf-8 -*-
{
    'name': 'Core Base',
    'version': '1.0.0',
    'category': 'Core',
    'summary': 'Core base functionality for Kids Clothing ERP',
    'description': """
        Core Base Module
        ===============
        
        This module provides the core base functionality for the Kids Clothing ERP system:
        
        * System configuration and settings
        * Base utilities and helper functions
        * Translation management
        * System parameters and configuration
        * Base models and mixins
        * Common utilities for all modules
        
        This is the foundation module that all other modules depend on.
    """,
    'author': 'Kids Clothing ERP Team',
    'website': 'https://www.kidsclothingerp.com',
    'license': 'LGPL-3',
    'depends': [],
    'data': [
        'security/ocean.model.access.csv',
        'data/data.xml',
        'views/menu.xml',
        'views/res_config_views.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'core_base/static/src/css/style.css',
            'core_base/static/src/js/script.js',
        ],
    },
    'installable': True,
    'application': False,
    'auto_install': True,
}