# -*- coding: utf-8 -*-
{
    'name': 'Indian Localization',
    'version': '1.0.0',
    'category': 'Localization/India',
    'summary': 'Indian localization for Ocean ERP - Chart of Accounts, States, Banks, Languages',
    'description': """
Indian Localization for Ocean ERP
=================================

This module provides Indian localization features including:

* Indian Chart of Accounts
* Indian States and Union Territories
* Indian Banks and Branches
* Indian Languages
* Indian Currency (INR)
* Indian Districts, Talukas, and Villages
* Indian Partner/Customer/Supplier formats

Features:
---------
* Complete Indian administrative divisions
* Bank branch management
* Multi-language support for Indian languages
* Indian-specific partner formats
* Integration with GST, EDI, and HR modules
    """,
    'author': 'Ocean ERP Team',
    'website': 'https://www.oceanerp.com',
    'depends': [
        'core_base',
        'company',
        'contacts',
    ],
    'data': [
        'data/res_country_state_data.xml',
        'data/res_bank_data.xml',
        'security/ir.model.access.csv',
        'views/res_country_state_views.xml',
        'views/res_bank_views.xml',
        'views/res_company_views.xml',
        'views/res_partner_views.xml',
        'views/res_currency_views.xml',
        'views/menu.xml',
    ],
    'demo': [
        'demo/res_company_demo.xml',
        'demo/res_partner_demo.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
    'license': 'LGPL-3',
}