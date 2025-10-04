# -*- coding: utf-8 -*-
{
    'name': 'Invoicing',
    'version': '1.0.0',
    'category': 'Accounting/Invoicing',
    'summary': 'Customer and Supplier Invoicing System for Ocean ERP',
    'description': """
Invoicing System for Ocean ERP
=============================

This module provides comprehensive invoicing functionality for kids clothing retail business:

**Customer Invoicing:**
- Sales invoices with GST compliance
- Credit notes for returns and adjustments
- Debit notes for additional charges
- Invoice templates and customization
- Bulk invoice generation

**Supplier Invoicing:**
- Vendor bills and purchase invoices
- Credit notes from suppliers
- Debit notes to suppliers
- Bill approval workflows
- Three-way matching (PO, Receipt, Invoice)

**Invoice Management:**
- Invoice numbering sequences
- Invoice validation and approval
- Payment terms and due dates
- Invoice aging reports
- Collection management

**Kids Clothing Specific Features:**
- Age group based pricing
- Seasonal discount applications
- Size-specific invoicing
- Brand-specific terms
- Special occasion billing

**Indian Compliance:**
- GST invoice formats
- E-invoice generation
- Tax calculations (CGST, SGST, IGST, UTGST, CESS)
- Invoice validation rules
- Statutory reporting

**Integration:**
- Sales order to invoice
- Purchase order to bill
- Payment processing
- Accounting entries
- Reporting integration
    """,
    'author': 'Ocean ERP Team',
    'website': 'https://www.oceanerp.com',
    'depends': [
        'core_base',
        'core_web',
        'accounting',
        'sales',
        'purchase',
        'contacts',
        'products',
        'l10n_in',
        'l10n_in_gst',
    ],
    'data': [
        'security/ocean.model.access.csv',
        'data/account_invoice_data.xml',
        'data/account_invoice_template_data.xml',
        'views/account_invoice_views.xml',
        'views/account_invoice_line_views.xml',
        'views/account_invoice_tax_views.xml',
        'views/account_payment_views.xml',
        'views/account_invoice_template_views.xml',
        'views/account_invoice_report_views.xml',
        'views/menu.xml',
    ],
    'demo': [
        'demo/account_invoice_demo.xml',
        'demo/account_payment_demo.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
    'license': 'LGPL-3',
}