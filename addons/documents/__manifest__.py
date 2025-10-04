#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Documents Addon Manifest
===========================================

Documents addon for document management system.
"""

{
    'name': 'Documents',
    'version': '1.0.0',
    'category': 'Utilities',
    'summary': 'Document management system',
    'description': '''
        Documents Addon for Kids Clothing ERP
        
        Features:
        - Document Storage
        - File Management
        - Document Versioning
        - Document Sharing
        - Document Collaboration
        - Document Search
        - Document Categories
        - Document Tags
        - Document Workflow
        - Document Approval
        - Document Templates
        - Document Conversion
        - Document Security
        - Document Analytics
        - Bulk Operations
    ''',
    'author': 'Kids Clothing ERP Team',
    'website': 'https://kidsclothingerp.com',
    'depends': [
        'core_base',
        'core_web',
        'users',
        'company',
        'workflows',
    ],
    'data': [
        'security/documents_security.xml',
        'data/document_templates.xml',
        'data/document_categories.xml',
        'views/document_views.xml',
        'views/document_folder_views.xml',
        'views/document_template_views.xml',
        'views/menu_views.xml',
    ],
    'demo': [
        'demo/documents_demo.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}