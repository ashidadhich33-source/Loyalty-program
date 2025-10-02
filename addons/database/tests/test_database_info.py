# -*- coding: utf-8 -*-

from odoo.tests.common import TransactionCase

class TestDatabaseInfo(TransactionCase):
    
    def setUp(self):
        super(TestDatabaseInfo, self).setUp()
        self.DatabaseInfo = self.env['database.info']
    
    def test_create_database_info(self):
        """Test database info creation"""
        database = self.DatabaseInfo.create({
            'name': 'Test Database',
            'database_type': 'postgresql',
            'version': '14.0',
            'status': 'active',
        })
        self.assertTrue(database)
        self.assertEqual(database.name, 'Test Database')
        self.assertEqual(database.database_type, 'postgresql')
    
    def test_database_info_status(self):
        """Test database info status"""
        database = self.DatabaseInfo.create({
            'name': 'Test Database',
            'database_type': 'postgresql',
            'status': 'active',
        })
        self.assertEqual(database.status, 'active')
        database.status = 'inactive'
        self.assertEqual(database.status, 'inactive')
