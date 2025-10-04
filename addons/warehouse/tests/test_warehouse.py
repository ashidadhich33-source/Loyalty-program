# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Warehouse Tests
===================================

Test cases for warehouse management functionality.
"""

import unittest
from datetime import datetime
from core_framework.orm import BaseModel
from core_framework.exceptions import ValidationError

class TestWarehouse(unittest.TestCase):
    """Test cases for Warehouse model"""
    
    def setUp(self):
        """Set up test data"""
        self.warehouse_data = {
            'name': 'Test Warehouse',
            'code': 'TEST_WH',
            'description': 'Test warehouse for unit testing',
            'warehouse_type': 'main',
            'is_active': True,
            'is_default': False,
            'street': '123 Test Street',
            'city': 'Test City',
            'zip': '12345',
            'phone': '+1-555-123-4567',
            'email': 'test@warehouse.com',
            'total_area': 5000.0,
            'storage_area': 4000.0,
            'office_area': 1000.0,
            'max_capacity': 10000.0,
            'current_capacity': 5000.0,
            'temperature_controlled': True,
            'min_temperature': 18.0,
            'max_temperature': 25.0,
            'humidity_controlled': True,
            'min_humidity': 40.0,
            'max_humidity': 60.0,
            'security_level': 'high',
            'requires_access_control': True,
            'age_group_specialization': 'mixed',
            'seasonal_storage': True,
            'operation_hours': '24/7',
            'timezone': 'UTC',
            'total_products': 100,
            'total_quantity': 2000.0,
            'total_value': 100000.0,
            'turnover_rate': 12.0,
            'accuracy_rate': 98.5
        }
    
    def tearDown(self):
        """Clean up test data"""
        pass
    
    def test_create_warehouse(self):
        """Test warehouse creation"""
        warehouse = self.env['warehouse'].create(self.warehouse_data)
        
        self.assertIsNotNone(warehouse)
        self.assertEqual(warehouse.name, 'Test Warehouse')
        self.assertEqual(warehouse.code, 'TEST_WH')
        self.assertEqual(warehouse.warehouse_type, 'main')
        self.assertTrue(warehouse.is_active)
        self.assertFalse(warehouse.is_default)
        self.assertEqual(warehouse.total_area, 5000.0)
        self.assertEqual(warehouse.storage_area, 4000.0)
        self.assertEqual(warehouse.office_area, 1000.0)
        self.assertEqual(warehouse.max_capacity, 10000.0)
        self.assertEqual(warehouse.current_capacity, 5000.0)
        self.assertTrue(warehouse.temperature_controlled)
        self.assertEqual(warehouse.min_temperature, 18.0)
        self.assertEqual(warehouse.max_temperature, 25.0)
        self.assertTrue(warehouse.humidity_controlled)
        self.assertEqual(warehouse.min_humidity, 40.0)
        self.assertEqual(warehouse.max_humidity, 60.0)
        self.assertEqual(warehouse.security_level, 'high')
        self.assertTrue(warehouse.requires_access_control)
        self.assertEqual(warehouse.age_group_specialization, 'mixed')
        self.assertTrue(warehouse.seasonal_storage)
        self.assertEqual(warehouse.operation_hours, '24/7')
        self.assertEqual(warehouse.timezone, 'UTC')
        self.assertEqual(warehouse.total_products, 100)
        self.assertEqual(warehouse.total_quantity, 2000.0)
        self.assertEqual(warehouse.total_value, 100000.0)
        self.assertEqual(warehouse.turnover_rate, 12.0)
        self.assertEqual(warehouse.accuracy_rate, 98.5)
    
    def test_warehouse_code_generation(self):
        """Test automatic warehouse code generation"""
        warehouse_data = self.warehouse_data.copy()
        del warehouse_data['code']
        warehouse_data['name'] = 'Auto Code Warehouse'
        
        warehouse = self.env['warehouse'].create(warehouse_data)
        
        self.assertEqual(warehouse.code, 'AUTO_CODE_WAREHOUSE')
    
    def test_warehouse_capacity_usage(self):
        """Test warehouse capacity usage calculation"""
        warehouse = self.env['warehouse'].create(self.warehouse_data)
        
        capacity_usage = warehouse._get_capacity_usage()
        expected_usage = (5000.0 / 10000.0) * 100
        
        self.assertEqual(capacity_usage, expected_usage)
    
    def test_warehouse_full_address(self):
        """Test warehouse full address generation"""
        warehouse = self.env['warehouse'].create(self.warehouse_data)
        
        full_address = warehouse._get_full_address()
        expected_address = '123 Test Street, Test City, 12345'
        
        self.assertEqual(full_address, expected_address)
    
    def test_warehouse_age_group_validation(self):
        """Test warehouse age group validation"""
        warehouse = self.env['warehouse'].create(self.warehouse_data)
        
        # Test toddler specialization
        warehouse.age_group_specialization = 'toddler'
        self.assertTrue(warehouse.validate_age_group('toddler'))
        self.assertFalse(warehouse.validate_age_group('child'))
        self.assertFalse(warehouse.validate_age_group('teen'))
        
        # Test child specialization
        warehouse.age_group_specialization = 'child'
        self.assertFalse(warehouse.validate_age_group('toddler'))
        self.assertTrue(warehouse.validate_age_group('child'))
        self.assertFalse(warehouse.validate_age_group('teen'))
        
        # Test teen specialization
        warehouse.age_group_specialization = 'teen'
        self.assertFalse(warehouse.validate_age_group('toddler'))
        self.assertFalse(warehouse.validate_age_group('child'))
        self.assertTrue(warehouse.validate_age_group('teen'))
        
        # Test mixed specialization
        warehouse.age_group_specialization = 'mixed'
        self.assertTrue(warehouse.validate_age_group('toddler'))
        self.assertTrue(warehouse.validate_age_group('child'))
        self.assertTrue(warehouse.validate_age_group('teen'))
    
    def test_warehouse_capacity_check(self):
        """Test warehouse capacity checking"""
        warehouse = self.env['warehouse'].create(self.warehouse_data)
        
        # Test within capacity
        capacity_ok, message = warehouse.check_capacity(1000.0)
        self.assertTrue(capacity_ok)
        self.assertEqual(message, "Capacity available")
        
        # Test exceeding capacity
        capacity_ok, message = warehouse.check_capacity(6000.0)
        self.assertFalse(capacity_ok)
        self.assertIn("Capacity exceeded", message)
    
    def test_warehouse_hierarchy(self):
        """Test warehouse hierarchy generation"""
        warehouse = self.env['warehouse'].create(self.warehouse_data)
        
        hierarchy = warehouse.get_warehouse_hierarchy()
        
        self.assertIsInstance(hierarchy, list)
        # Should contain at least the warehouse location
        self.assertGreaterEqual(len(hierarchy), 1)
    
    def test_warehouse_summary(self):
        """Test warehouse summary generation"""
        warehouse = self.env['warehouse'].create(self.warehouse_data)
        
        summary = warehouse.get_warehouse_summary()
        
        self.assertIsInstance(summary, dict)
        self.assertIn('warehouse_name', summary)
        self.assertIn('warehouse_code', summary)
        self.assertIn('warehouse_type', summary)
        self.assertIn('is_active', summary)
        self.assertIn('is_default', summary)
        self.assertIn('total_area', summary)
        self.assertIn('storage_area', summary)
        self.assertIn('office_area', summary)
        self.assertIn('max_capacity', summary)
        self.assertIn('current_capacity', summary)
        self.assertIn('capacity_usage', summary)
        self.assertIn('temperature_controlled', summary)
        self.assertIn('min_temperature', summary)
        self.assertIn('max_temperature', summary)
        self.assertIn('humidity_controlled', summary)
        self.assertIn('min_humidity', summary)
        self.assertIn('max_humidity', summary)
        self.assertIn('security_level', summary)
        self.assertIn('requires_access_control', summary)
        self.assertIn('age_group_specialization', summary)
        self.assertIn('seasonal_storage', summary)
        self.assertIn('operation_hours', summary)
        self.assertIn('timezone', summary)
        self.assertIn('total_products', summary)
        self.assertIn('total_quantity', summary)
        self.assertIn('total_value', summary)
        self.assertIn('turnover_rate', summary)
        self.assertIn('accuracy_rate', summary)
        
        self.assertEqual(summary['warehouse_name'], 'Test Warehouse')
        self.assertEqual(summary['warehouse_code'], 'TEST_WH')
        self.assertEqual(summary['warehouse_type'], 'main')
        self.assertTrue(summary['is_active'])
        self.assertFalse(summary['is_default'])
        self.assertEqual(summary['total_area'], 5000.0)
        self.assertEqual(summary['storage_area'], 4000.0)
        self.assertEqual(summary['office_area'], 1000.0)
        self.assertEqual(summary['max_capacity'], 10000.0)
        self.assertEqual(summary['current_capacity'], 5000.0)
        self.assertTrue(summary['temperature_controlled'])
        self.assertEqual(summary['min_temperature'], 18.0)
        self.assertEqual(summary['max_temperature'], 25.0)
        self.assertTrue(summary['humidity_controlled'])
        self.assertEqual(summary['min_humidity'], 40.0)
        self.assertEqual(summary['max_humidity'], 60.0)
        self.assertEqual(summary['security_level'], 'high')
        self.assertTrue(summary['requires_access_control'])
        self.assertEqual(summary['age_group_specialization'], 'mixed')
        self.assertTrue(summary['seasonal_storage'])
        self.assertEqual(summary['operation_hours'], '24/7')
        self.assertEqual(summary['timezone'], 'UTC')
        self.assertEqual(summary['total_products'], 100)
        self.assertEqual(summary['total_quantity'], 2000.0)
        self.assertEqual(summary['total_value'], 100000.0)
        self.assertEqual(summary['turnover_rate'], 12.0)
        self.assertEqual(summary['accuracy_rate'], 98.5)

if __name__ == '__main__':
    unittest.main()