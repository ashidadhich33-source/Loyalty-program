# -*- coding: utf-8 -*-
{
    'name': 'Human Resources',
    'version': '1.0.0',
    'category': 'Human Resources',
    'summary': 'Employee Management, Attendance, and Shift Management for Ocean ERP',
    'description': """
Human Resources Management for Ocean ERP
=======================================

This module provides comprehensive HR functionality for kids clothing retail business:

**Employee Management:**
- Employee records and profiles
- Employee hierarchy and reporting structure
- Employee documents and certificates
- Employee onboarding and offboarding
- Employee performance tracking

**Attendance Management:**
- Daily attendance tracking
- Check-in/check-out system
- Attendance reports and analytics
- Leave balance tracking
- Overtime calculation

**Shift Management:**
- Shift scheduling and planning
- Shift rotation management
- Shift coverage and replacement
- Shift performance tracking
- Shift-based payroll integration

**Kids Clothing Specific Features:**
- Age group based employee assignments
- Seasonal staffing requirements
- Brand-specific employee training
- Size-specific employee roles
- Special occasion staffing

**Indian Compliance:**
- PF (Provident Fund) management
- ESI (Employee State Insurance) tracking
- TDS (Tax Deducted at Source) calculation
- Gratuity calculation
- Indian labor law compliance

**Integration:**
- Payroll system integration
- Time tracking integration
- Performance management
- Training and development
- Reporting and analytics
    """,
    'author': 'Ocean ERP Team',
    'website': 'https://www.oceanerp.com',
    'depends': [
        'core_base',
        'core_web',
        'contacts',
        'users',
        'company',
        'l10n_in',
        'l10n_in_hr_payroll',
    ],
    'data': [
        'security/ocean.model.access.csv',
        'data/hr_employee_data.xml',
        'data/hr_department_data.xml',
        'data/hr_job_position_data.xml',
        'data/hr_shift_data.xml',
        'data/hr_attendance_data.xml',
        'views/hr_employee_views.xml',
        'views/hr_department_views.xml',
        'views/hr_job_position_views.xml',
        'views/hr_shift_views.xml',
        'views/hr_attendance_views.xml',
        'views/hr_leave_views.xml',
        'views/hr_performance_views.xml',
        'views/menu.xml',
    ],
    'demo': [
        'demo/hr_employee_demo.xml',
        'demo/hr_attendance_demo.xml',
        'demo/hr_shift_demo.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
    'license': 'LGPL-3',
}