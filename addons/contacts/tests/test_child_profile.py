# -*- coding: utf-8 -*-

from odoo.tests.common import TransactionCase

class TestChildProfile(TransactionCase):
    
    def setUp(self):
        super().setUp()
        self.model = self.env['child_profile']
    
    def test_create(self):
        """Test model creation"""
        record = self.model.create({'name': 'Test Record'})
        self.assertTrue(record)
