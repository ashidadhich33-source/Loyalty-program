#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Bulk Import Addon
=====================================

Excel/CSV import system with templates for bulk data management.
"""

{
    'name': 'Bulk Import',
    'version': '1.0.0',
    'category': 'Tools',
    'summary': 'Excel/CSV import system with templates',
    'description': """
        Bulk Import System for Kids Clothing ERP
        ========================================
        
        This addon provides comprehensive bulk import functionality
        for Excel and CSV files with pre-built templates.
        
        Features:
        - Excel/CSV file import with validation
        - Pre-built templates for all modules
        - Data validation and error handling
        - Import history and rollback functionality
        - Custom field mapping
        - Batch processing with progress tracking
        - Import scheduling and automation
    """,
    'author': 'Kids Clothing ERP Team',
    'website': 'https://www.kidsclothingerp.com',
    'license': 'LGPL-3',
    'depends': [
        'core_base',
        'core_web',
        'users',
        'company',
        'contacts',
        'products',
        'categories',
    ],
    'data': [
        'security/ocean.model.access.csv',
        'security/security.xml',
        'data/data.xml',
        'views/menu.xml',
        'views/import_template_views.xml',
        'views/import_job_views.xml',
        'views/import_history_views.xml',
        'wizard/import_wizard_views.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
    'assets': {
        'ocean.assets_backend': [
            'bulk_import/static/src/css/import_style.css',
            'bulk_import/static/src/js/import_script.js',
        ],
    },
    'installable': True,
    'auto_install': False,
    'application': False,
}