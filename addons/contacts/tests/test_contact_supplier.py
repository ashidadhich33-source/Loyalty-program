# -*- coding: utf-8 -*-

from odoo.tests.common import TransactionCase

class TestContactSupplier(TransactionCase):
    
    def setUp(self):
        super().setUp()
        self.model = self.env['contact_supplier']
    
    def test_create(self):
        """Test model creation"""
        record = self.model.create({'name': 'Test Record'})
        self.assertTrue(record)
