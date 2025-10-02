# -*- coding: utf-8 -*-
{
    'name': 'Bulk Import',
    'version': '1.0.0',
    'category': 'Master Data',
    'summary': 'Bulk import system for Excel/CSV files with templates',
    'description': """
        Bulk Import System for Kids Clothing Retail ERP
        
        This addon provides comprehensive bulk import functionality for Excel/CSV files with templates:
        
        Key Features:
        - Excel/CSV file import system
        - Pre-built templates for all modules
        - Data validation and error handling
        - Import mapping and field mapping
        - Batch processing and progress tracking
        - Import history and audit trail
        - Error reporting and correction
        - Template management
        - Import scheduling
        - Data transformation
        - Duplicate detection and handling
        - Import rollback functionality
        - Import statistics and reporting
        
        Supported Modules:
        - Products import with variants
        - Categories import with hierarchy
        - Contacts import (customers, suppliers, vendors)
        - Child profiles import
        - Company and branch import
        - User import
        - Inventory import
        - Sales orders import
        - Purchase orders import
        
        Business Logic:
        - Kids clothing specific validation
        - Age group validation
        - Gender validation
        - Size validation
        - Color and brand validation
        - Indian localization validation (GSTIN, PAN, mobile)
        - Data integrity checks
        - Business rule validation
        
        Technical Features:
        - Multiple file format support
        - Large file processing
        - Memory optimization
        - Progress tracking
        - Error handling
        - Data transformation
        - Field mapping
        - Validation rules
        - Import templates
        - Batch processing
        - Rollback functionality
    """,
    'author': 'Kids Clothing ERP Team',
    'website': 'https://kidsclothingerp.com',
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
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/data.xml',
        'views/import_template_views.xml',
        'views/import_job_views.xml',
        'views/import_mapping_views.xml',
        'views/import_history_views.xml',
        'views/import_statistics_views.xml',
        'views/menu.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'bulk_import/static/src/js/import_script.js',
            'bulk_import/static/src/css/import_style.css',
        ],
    },
    'installable': True,
    'auto_install': False,
    'application': False,
}