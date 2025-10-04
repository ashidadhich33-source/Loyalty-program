# -*- coding: utf-8 -*-
{
    'name': 'Indian EDI',
    'version': '1.0.0',
    'category': 'Localization/India',
    'summary': 'Indian EDI compliance for Ocean ERP - E-invoice, E-way bill integration',
    'description': """
Indian EDI Compliance for Ocean ERP
===================================

This module provides EDI (Electronic Data Interchange) compliance for Indian businesses:

* E-invoice Generation and Transmission
* E-way Bill Generation
* EDI Document Management
* EDI Message Processing
* EDI Transmission and Acknowledgment
* EDI Error Handling and Validation
* Integration with GST Portal

Features:
---------
* Automated e-invoice generation
* E-way bill creation and management
* EDI document validation
* Real-time transmission to government portals
* Acknowledgment tracking
* Error handling and retry mechanisms
* Integration with GST and accounting modules
    """,
    'author': 'Ocean ERP Team',
    'website': 'https://www.oceanerp.com',
    'depends': [
        'core_base',
        'l10n_in',
        'l10n_in_gst',
        'accounting',
        'sales',
        'purchase',
    ],
    'data': [
        'data/edi_document_data.xml',
        'security/ir.model.access.csv',
        'views/edi_document_views.xml',
        'views/edi_transaction_views.xml',
        'views/edi_envelope_views.xml',
        'views/edi_message_views.xml',
        'views/edi_transmission_views.xml',
        'views/edi_validation_views.xml',
        'views/edi_acknowledgment_views.xml',
        'views/edi_error_views.xml',
        'views/edi_configuration_views.xml',
        'views/menu.xml',
    ],
    'demo': [
        'demo/edi_document_demo.xml',
        'demo/edi_transmission_demo.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
    'license': 'LGPL-3',
}