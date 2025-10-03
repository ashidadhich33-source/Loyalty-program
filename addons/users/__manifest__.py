# -*- coding: utf-8 -*-
{
    'name': 'Users Management',
    'version': '1.0.0',
    'category': 'Core',
    'summary': 'User management, groups, permissions, and access rights for Kids Clothing ERP',
    'description': """
        Users Management Module
        ======================
        
        This module provides comprehensive user management functionality for the Kids Clothing ERP system:
        
        * User account management
        * Role-based access control
        * Permission management
        * Group management
        * Access rights configuration
        * User preferences and settings
        * Multi-company user access
        * User activity tracking
        * Password management
        * User authentication
        
        This module handles all user-related functionality and security management.
    """,
    'author': 'Kids Clothing ERP Team',
    'website': 'https://www.kidsclothingerp.com',
    'license': 'LGPL-3',
    'depends': ['core_base', 'core_web'],
    'data': [
        'security/ocean.model.access.csv',
        'security/security.xml',
        'data/data.xml',
        'views/menu.xml',
        'views/user_views.xml',
        'views/group_views.xml',
        'views/permission_views.xml',
        'views/access_rights_views.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'users/static/src/css/user_style.css',
            'users/static/src/js/user_script.js',
        ],
    },
    'installable': True,
    'application': False,
    'auto_install': True,
}