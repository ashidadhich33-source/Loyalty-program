# -*- coding: utf-8 -*-

from core_framework.testing import TestCase

class TestDatabaseConnection(TestCase):
    
    def setUp(self):
        super(TestDatabaseConnection, self).setUp()
        self.DatabaseConnection = self.env['database.connection']
    
    def test_create_database_connection(self):
        """Test database connection creation"""
        connection = self.DatabaseConnection.create({
            'name': 'Test Connection',
            'host': 'localhost',
            'port': 5432,
            'username': 'test_user',
            'status': 'disconnected',
        })
        self.assertTrue(connection)
        self.assertEqual(connection.host, 'localhost')
        self.assertEqual(connection.port, 5432)
