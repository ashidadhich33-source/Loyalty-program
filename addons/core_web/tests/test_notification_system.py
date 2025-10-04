# -*- coding: utf-8 -*-
"""
Test Notification System
========================

Test cases for notification system functionality.
"""

import unittest
from ocean.tests.common import TransactionCase


class TestNotificationSystem(TransactionCase):
    """Test notification system functionality."""
    
    def setUp(self):
        super().setUp()
        self.notification_model = self.env['notification.system']
    
    def test_notification_creation(self):
        """Test notification creation."""
        notification = self.notification_model.create({
            'name': 'Test Notification',
            'message': 'This is a test notification',
            'notification_type': 'info',
            'is_active': True,
        })
        self.assertTrue(notification.id)
        self.assertEqual(notification.name, 'Test Notification')
    
    def test_notification_types(self):
        """Test different notification types."""
        types = ['info', 'warning', 'error', 'success']
        for notif_type in types:
            notification = self.notification_model.create({
                'name': f'Test {notif_type}',
                'message': f'This is a {notif_type} notification',
                'notification_type': notif_type,
            })
            self.assertEqual(notification.notification_type, notif_type)