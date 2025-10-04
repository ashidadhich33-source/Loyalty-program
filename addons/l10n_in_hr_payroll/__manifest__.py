# -*- coding: utf-8 -*-
{
    'name': 'Indian HR Payroll',
    'version': '1.0.0',
    'category': 'Localization/India',
    'summary': 'Indian HR Payroll for Ocean ERP - PF, ESI, TDS, Gratuity compliance',
    'description': """
Indian HR Payroll for Ocean ERP
===============================

This module provides comprehensive HR payroll features for Indian businesses:

* Provident Fund (PF) Management
* Employee State Insurance (ESI)
* Tax Deducted at Source (TDS)
* Gratuity Calculations
* Professional Tax
* Labor Welfare Fund
* Indian Payroll Reports
* Statutory Compliance

Features:
---------
* Automated PF and ESI calculations
* TDS computation and filing
* Gratuity calculation and management
* Professional tax handling
* Labor welfare fund management
* Statutory report generation
* Integration with accounting module
* Compliance with Indian labor laws
    """,
    'author': 'Ocean ERP Team',
    'website': 'https://www.oceanerp.com',
    'depends': [
        'core_base',
        'l10n_in',
        'hr',
        'accounting',
    ],
    'data': [
        'data/hr_contract_data.xml',
        'data/hr_employee_data.xml',
        'security/ir.model.access.csv',
        'views/hr_employee_views.xml',
        'views/hr_payslip_views.xml',
        'views/menu.xml',
    ],
    'demo': [
        'demo/hr_employee_demo.xml',
        'demo/hr_payslip_demo.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
    'license': 'LGPL-3',
}