# -*- coding: utf-8 -*-

from core_framework.testing import TestCase

class TestDatabaseSecurity(TestCase):
    
    def setUp(self):
        super().setUp()
        self.model = self.env['database_security']
    
    def test_create(self):
        """Test model creation"""
        record = self.model.create({'name': 'Test Record'})
        self.assertTrue(record)
