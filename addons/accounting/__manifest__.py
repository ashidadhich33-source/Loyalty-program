# -*- coding: utf-8 -*-
{
    'name': 'Accounting',
    'version': '1.0.0',
    'category': 'Accounting',
    'summary': 'Accounting management for Kids Clothing ERP',
    'description': """
        Accounting Management for Kids Clothing ERP
        ==========================================
        
        This addon provides comprehensive accounting functionality:
        
        * Chart of Accounts
        * Journal Entries
        * Account Reconciliation
        * Financial Reports
        * Period Management
        * Journal Management
        * Kids Clothing Specific Accounting
        
        Features:
        - Complete chart of accounts
        - Journal entry management
        - Account reconciliation
        - Financial reporting
        - Period management
        - Journal configuration
        - Kids clothing specific accounting
        - Age group and seasonal accounting
        - Size-based cost accounting
        - Brand-specific accounting
    """,
    'author': 'Kids Clothing ERP Team',
    'website': 'https://www.kidsclothingerp.com',
    'license': 'LGPL-3',
    'depends': [
        'core_base',
        'core_web',
        'company',
        'contacts',
    ],
    'data': [
        'security/ocean.model.access.csv',
        'data/data.xml',
        'views/menu.xml',
        'views/account_account_views.xml',
        'views/account_journal_views.xml',
        'views/account_move_views.xml',
        'views/account_period_views.xml',
        'views/account_reconciliation_views.xml',
        'views/account_report_views.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'accounting/static/src/css/accounting_style.css',
            'accounting/static/src/js/accounting_script.js',
        ],
    },
    'installable': True,
    'auto_install': False,
    'application': True,
}