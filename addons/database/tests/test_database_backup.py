# -*- coding: utf-8 -*-

from odoo.tests.common import TransactionCase

class TestDatabaseBackup(TransactionCase):
    
    def setUp(self):
        super().setUp()
        self.model = self.env['database_backup']
    
    def test_create(self):
        """Test model creation"""
        record = self.model.create({'name': 'Test Record'})
        self.assertTrue(record)
