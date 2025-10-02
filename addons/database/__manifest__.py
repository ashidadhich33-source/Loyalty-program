# -*- coding: utf-8 -*-
{
    'name': 'Database Management',
    'version': '1.0.0',
    'category': 'Core',
    'summary': 'Multi-database management, database switching, and database operations for Kids Clothing ERP',
    'description': """
        Database Management Module
        =========================
        
        This module provides comprehensive database management functionality for the Kids Clothing ERP system:
        
        * Multi-database management
        * Database switching and selection
        * Database backup and restore
        * Database migration and versioning
        * Database monitoring and analytics
        * Database security and access control
        * Database performance optimization
        * Database maintenance and cleanup
        * Database replication and synchronization
        * Database configuration management
        * Database connection management
        * Database health monitoring
        * Database backup scheduling
        * Database recovery procedures
        * Database audit and logging
        
        This module handles all database-related operations and multi-database management.
    """,
    'author': 'Kids Clothing ERP Team',
    'website': 'https://www.kidsclothingerp.com',
    'license': 'LGPL-3',
    'depends': ['core_base', 'core_web', 'users', 'company'],
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'data/data.xml',
        'views/menu.xml',
        'views/database_views.xml',
        'views/database_connection_views.xml',
        'views/database_backup_views.xml',
        'views/database_migration_views.xml',
        'views/database_monitoring_views.xml',
        'views/database_analytics_views.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'database/static/src/css/database_style.css',
            'database/static/src/js/database_script.js',
        ],
    },
    'installable': True,
    'application': False,
    'auto_install': True,
}