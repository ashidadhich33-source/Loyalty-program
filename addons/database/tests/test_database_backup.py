# -*- coding: utf-8 -*-

from core_framework.testing import TestCase

class TestDatabaseBackup(TestCase):
    
    def setUp(self):
        super().setUp()
        self.model = self.env['database_backup']
    
    def test_create(self):
        """Test model creation"""
        record = self.model.create({'name': 'Test Record'})
        self.assertTrue(record)
