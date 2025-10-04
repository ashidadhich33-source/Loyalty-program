#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Notifications Addon Manifest
===============================================

Notifications addon for in-app, SMS, email alerts.
"""

{
    'name': 'Notifications',
    'version': '1.0.0',
    'category': 'Utilities',
    'summary': 'In-app, SMS, email alerts system',
    'description': '''
        Notifications Addon for Kids Clothing ERP
        
        Features:
        - In-app Notifications
        - Email Notifications
        - SMS Notifications
        - WhatsApp Notifications
        - Push Notifications
        - Notification Templates
        - Notification Rules
        - Notification Scheduling
        - Notification Preferences
        - Notification History
        - Notification Analytics
        - Bulk Notifications
        - Notification Channels
        - Notification Queuing
        - Delivery Tracking
    ''',
    'author': 'Kids Clothing ERP Team',
    'website': 'https://kidsclothingerp.com',
    'depends': [
        'core_base',
        'core_web',
        'users',
        'company',
    ],
    'data': [
        'security/notifications_security.xml',
        'data/notification_templates.xml',
        'data/notification_channels.xml',
        'views/notification_views.xml',
        'views/notification_template_views.xml',
        'views/notification_rule_views.xml',
        'views/menu_views.xml',
    ],
    'demo': [
        'demo/notifications_demo.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}