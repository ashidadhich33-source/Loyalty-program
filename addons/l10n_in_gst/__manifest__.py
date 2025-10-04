# -*- coding: utf-8 -*-
{
    'name': 'Indian GST',
    'version': '1.0.0',
    'category': 'Localization/India',
    'summary': 'Indian GST compliance for Ocean ERP - CGST, SGST, IGST, UTGST, CESS',
    'description': """
Indian GST Compliance for Ocean ERP
===================================

This module provides comprehensive GST compliance features for Indian businesses:

* GST Tax Structure (CGST, SGST, IGST, UTGST, CESS)
* GST Return Filing (GSTR-1, GSTR-3B, GSTR-9)
* GST Reports and Analytics
* GST Invoice Formats
* HSN/SAC Code Management
* GST Registration Management
* Reverse Charge Mechanism
* Composition Scheme Support

Features:
---------
* Automatic GST calculation based on transaction type
* GST return preparation and filing
* Comprehensive GST reports
* Integration with EDI for e-invoicing
* GST compliance validation
* Multi-state GST handling
    """,
    'author': 'Ocean ERP Team',
    'website': 'https://www.oceanerp.com',
    'depends': [
        'core_base',
        'l10n_in',
        'accounting',
        'sales',
        'purchase',
        'products',
    ],
    'data': [
        'data/account_tax_data.xml',
        'security/ir.model.access.csv',
        'views/account_tax_views.xml',
        'views/account_fiscal_position_views.xml',
        'views/gst_return_views.xml',
        'views/gst_report_views.xml',
        'views/menu.xml',
    ],
    'demo': [
        'demo/account_tax_demo.xml',
        'demo/gst_return_demo.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
    'license': 'LGPL-3',
}