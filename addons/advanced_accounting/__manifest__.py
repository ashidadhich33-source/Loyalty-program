# -*- coding: utf-8 -*-
{
    'name': 'Advanced Accounting',
    'version': '1.0.0',
    'category': 'Accounting',
    'summary': 'Advanced accounting functionality for Ocean ERP',
    'description': """
Advanced Accounting Module
=========================

This module provides comprehensive accounting functionality including:

* Chart of Accounts Management
* Journal Entries and Posting
* Financial Reporting
* Account Reconciliation
* Budget Management
* Cost Centers and Profit Centers
* Multi-currency Support
* Indian Accounting Standards Compliance
* Kids Clothing Industry Specific Accounts

Features:
---------
* Complete Chart of Accounts
* Automated Journal Entry Posting
* Financial Statement Generation
* Account Reconciliation Tools
* Budget vs Actual Analysis
* Cost Center Reporting
* Multi-currency Transactions
* Indian GST Integration
* Kids Clothing Specific Accounts
* Automated Month-end Closing
* Financial Dashboard
* Audit Trail and Compliance
    """,
    'author': 'Ocean ERP',
    'website': 'https://www.oceanerp.com',
    'depends': [
        'core_framework',
        'l10n_in',
        'l10n_in_gst',
        'contacts',
        'invoicing',
        'payments',
    ],
    'data': [
        'security/ir.model.access.csv',
        'security/ocean.model.access.csv',
        'data/account_account_data.xml',
        'data/account_journal_data.xml',
        'data/account_fiscal_year_data.xml',
        'data/account_chart_template_data.xml',
        'views/account_account_views.xml',
        'views/account_journal_views.xml',
        'views/account_move_views.xml',
        'views/account_reconcile_views.xml',
        'views/account_budget_views.xml',
        'views/account_cost_center_views.xml',
        'views/account_financial_report_views.xml',
        'views/account_dashboard_views.xml',
        'views/menu.xml',
    ],
    'demo': [
        'demo/account_account_demo.xml',
        'demo/account_move_demo.xml',
        'demo/account_budget_demo.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'advanced_accounting/static/src/css/accounting.css',
            'advanced_accounting/static/src/js/accounting.js',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}