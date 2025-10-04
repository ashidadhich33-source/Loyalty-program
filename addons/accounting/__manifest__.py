# -*- coding: utf-8 -*-
{
    'name': 'Accounting',
    'version': '1.0.0',
    'category': 'Accounting',
    'summary': 'Chart of accounts, journals, ledgers for kids clothing retail',
    'description': """
        Accounting System for Kids Clothing Retail ERP
        =============================================
        
        Comprehensive accounting system designed specifically for kids clothing retail:
        
        * Chart of Accounts Management
          - Complete chart of accounts structure
          - Account types (Assets, Liabilities, Equity, Income, Expenses)
          - Account codes and hierarchy
          - Kids clothing specific accounts (Inventory, Sales, Cost of Goods Sold)
          - Multi-currency support
          - Account reconciliation capabilities
          - Account analytics and reporting
        
        * Journal Management
          - Journal entries and posting
          - Journal types (Sales, Purchase, Cash, Bank, General)
          - Batch journal processing
          - Journal approval workflows
          - Recurring journal entries
          - Journal templates for common transactions
          - Kids clothing specific journal templates
          - Age-group and seasonal journal categorization
        
        * Ledger Management
          - General ledger with detailed transactions
          - Subsidiary ledgers (Customer, Supplier, Inventory)
          - Ledger reconciliation and balancing
          - Ledger reporting and analytics
          - Multi-period ledger analysis
          - Kids clothing specific ledger categories
          - Seasonal ledger tracking
        
        * Financial Reporting
          - Profit & Loss Statement
          - Balance Sheet
          - Cash Flow Statement
          - Trial Balance
          - Aged Receivables and Payables
          - Kids clothing specific reports (Inventory Valuation, Sales by Age Group)
          - Seasonal financial analysis
          - Brand-wise and size-wise profitability
        
        * Period Management
          - Financial year and period management
          - Period opening and closing
          - Period-based reporting
          - Multi-year financial analysis
          - Kids clothing seasonal periods
          - Age-group specific periods
        
        * Account Reconciliation
          - Bank reconciliation
          - Customer account reconciliation
          - Supplier account reconciliation
          - Inventory account reconciliation
          - Automated reconciliation rules
          - Reconciliation reporting
        
        * Kids Clothing Specific Features
          - Age-group specific accounting (baby, toddler, teen)
          - Seasonal accounting periods (summer, winter, monsoon)
          - Size-wise cost tracking (XS, S, M, L, XL, XXL, XXXL)
          - Brand-wise profitability analysis
          - Color-wise sales tracking
          - Special occasion accounting (festivals, back-to-school)
          - Growth-based accounting adjustments
          - Quality control cost tracking
          - Safety standards compliance costs
    """,
    'author': 'Kids Clothing ERP Team',
    'website': 'https://www.kidsclothing.com',
    'depends': [
        'base',
        'users',
        'company',
        'contacts',
        'products',
        'inventory',
        'sales',
        'purchase',
    ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/data.xml',
        'demo/demo.xml',
        'views/menu.xml',
        'views/account_account_views.xml',
        'views/account_journal_views.xml',
        'views/account_move_views.xml',
        'views/account_move_line_views.xml',
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
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}