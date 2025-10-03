# -*- coding: utf-8 -*-
{
    'name': 'Contacts Management',
    'version': '1.0.0',
    'category': 'Contacts',
    'summary': 'Customer, Supplier, Vendor, and Child Profile Management',
    'description': """
Contact Management Module for Kids Clothing ERP
================================================

Features:
---------
* Customer Management
* Supplier Management
* Vendor Management
* Child Profile Management
* Contact Categories and Tags
* Contact History and Notes
* Multi-Address Support
* Contact Communication History
* Contact Rating and Feedback
* Contact Analytics and Reports
* Integration with Sales, Purchase, and POS
* Kids-Specific Features (Age Groups, Preferences)
* Indian Localization (GST, PAN validation)
    """,
    'author': 'Kids Clothing ERP Development Team',
    'website': 'https://www.kidsclothingerp.com',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'core_base',
        'core_web',
        'users',
        'company',
        'database',
    ],
    'data': [
        # Security
        'security/security.xml',
        'security/ocean.model.access.csv',
        
        # Data
        'data/data.xml',
        
        # Views
        'views/menu.xml',
        'views/contact_views.xml',
        'views/customer_views.xml',
        'views/supplier_views.xml',
        'views/vendor_views.xml',
        'views/child_profile_views.xml',
        'views/contact_category_views.xml',
        'views/contact_tag_views.xml',
        'views/contact_history_views.xml',
        'views/contact_communication_views.xml',
        'views/contact_address_views.xml',
        'views/contact_analytics_views.xml',
        
        # Wizards
        'wizard/contact_import_wizard.xml',
        'wizard/contact_export_wizard.xml',
        'wizard/contact_merge_wizard.xml',
        
        # Reports
        'report/contact_report.xml',
        
        # Demo
        'demo/demo.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'contacts/static/src/css/contact_style.css',
            'contacts/static/src/js/contact_script.js',
        ],
    },
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}