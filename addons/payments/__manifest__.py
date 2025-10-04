# -*- coding: utf-8 -*-
{
    'name': 'Payments',
    'version': '1.0.0',
    'category': 'Accounting/Payments',
    'summary': 'Payment Processing and Bank Integration System for Ocean ERP',
    'description': """
Payment Processing System for Ocean ERP
======================================

This module provides comprehensive payment processing functionality for kids clothing retail business:

**Payment Processing:**
- Customer payment collection
- Supplier payment processing
- Multi-payment method support
- Payment reconciliation
- Payment matching and allocation

**Payment Methods:**
- Cash payments
- Bank transfers
- Cheque processing
- UPI payments (PhonePe, Paytm, Google Pay)
- Credit/Debit card payments
- Digital wallet integration

**Bank Integration:**
- Bank statement import
- Automatic reconciliation
- Multi-bank support
- Bank account management
- Transaction matching

**Payment Workflows:**
- Payment approval workflows
- Payment authorization
- Payment validation
- Payment processing status tracking
- Payment failure handling

**Kids Clothing Specific Features:**
- Age group based payment tracking
- Seasonal payment analytics
- Brand-specific payment terms
- Size-based payment processing
- Special occasion payment handling

**Indian Compliance:**
- GST payment processing
- TDS payment handling
- Indian banking standards
- RBI compliance
- Digital payment regulations

**Integration:**
- Invoice payment matching
- Sales order payment processing
- Purchase order payment handling
- Accounting integration
- Reporting integration
    """,
    'author': 'Ocean ERP Team',
    'website': 'https://www.oceanerp.com',
    'depends': [
        'core_base',
        'core_web',
        'accounting',
        'invoicing',
        'contacts',
        'l10n_in',
        'l10n_in_gst',
    ],
    'data': [
        'security/ocean.model.access.csv',
        'data/account_payment_data.xml',
        'data/account_payment_method_data.xml',
        'data/bank_integration_data.xml',
        'views/account_payment_views.xml',
        'views/account_payment_method_views.xml',
        'views/account_payment_term_views.xml',
        'views/bank_account_views.xml',
        'views/bank_statement_views.xml',
        'views/payment_reconciliation_views.xml',
        'views/menu.xml',
    ],
    'demo': [
        'demo/account_payment_demo.xml',
        'demo/bank_statement_demo.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
    'license': 'LGPL-3',
}