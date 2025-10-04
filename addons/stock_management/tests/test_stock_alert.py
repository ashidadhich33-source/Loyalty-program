# -*- coding: utf-8 -*-
"""
Ocean ERP - Stock Alert Tests
============================

Tests for stock alert model in Ocean ERP.
"""

import unittest
from core_framework.testing import OceanTestCase
from core_framework.exceptions import ValidationError, UserError


class TestStockAlert(OceanTestCase):
    """Test Stock Alert Model"""
    
    def setUp(self):
        """Set up test data"""
        super().setUp()
        
        # Create test company
        self.company = self.env['res.company'].create({
            'name': 'Test Company',
            'currency_id': self.env.ref('base.INR').id,
        })
        
        # Create test product
        self.product = self.env['product.product'].create({
            'name': 'Test Product',
            'type': 'product',
            'company_id': self.company.id,
        })
        
        # Create test location
        self.location = self.env['stock.location'].create({
            'name': 'Test Location',
            'usage': 'internal',
            'company_id': self.company.id,
        })
        
        # Create test warehouse
        self.warehouse = self.env['stock.warehouse'].create({
            'name': 'Test Warehouse',
            'code': 'TEST',
            'company_id': self.company.id,
        })
    
    def test_create_stock_alert(self):
        """Test creating a stock alert"""
        alert = self.env['stock.alert'].create({
            'name': 'Test Alert',
            'product_id': self.product.id,
            'alert_type': 'low_stock',
            'priority': 'medium',
            'status': 'draft',
            'current_stock': 10.0,
            'minimum_stock': 20.0,
            'reorder_point': 15.0,
            'reorder_quantity': 50.0,
            'age_group': '0-2',
            'size': 's',
            'season': 'summer',
            'brand': 'Kids Brand',
            'color': 'Blue',
            'location_id': self.location.id,
            'warehouse_id': self.warehouse.id,
            'company_id': self.company.id,
        })
        
        self.assertEqual(alert.name, 'Test Alert')
        self.assertEqual(alert.product_id, self.product)
        self.assertEqual(alert.alert_type, 'low_stock')
        self.assertEqual(alert.priority, 'medium')
        self.assertEqual(alert.status, 'draft')
        self.assertEqual(alert.current_stock, 10.0)
        self.assertEqual(alert.minimum_stock, 20.0)
        self.assertEqual(alert.age_group, '0-2')
        self.assertEqual(alert.size, 's')
        self.assertEqual(alert.season, 'summer')
        self.assertEqual(alert.brand, 'Kids Brand')
        self.assertEqual(alert.color, 'Blue')
        self.assertTrue(alert.active)
    
    def test_alert_resolution(self):
        """Test alert resolution"""
        alert = self.env['stock.alert'].create({
            'name': 'Test Alert',
            'product_id': self.product.id,
            'alert_type': 'low_stock',
            'priority': 'medium',
            'status': 'active',
            'current_stock': 10.0,
            'minimum_stock': 20.0,
            'company_id': self.company.id,
        })
        
        # Resolve the alert
        alert.action_resolve()
        
        self.assertEqual(alert.status, 'resolved')
        self.assertIsNotNone(alert.resolved_date)
    
    def test_alert_cancellation(self):
        """Test alert cancellation"""
        alert = self.env['stock.alert'].create({
            'name': 'Test Alert',
            'product_id': self.product.id,
            'alert_type': 'low_stock',
            'priority': 'medium',
            'status': 'active',
            'current_stock': 10.0,
            'minimum_stock': 20.0,
            'company_id': self.company.id,
        })
        
        # Cancel the alert
        alert.action_cancel()
        
        self.assertEqual(alert.status, 'cancelled')
    
    def test_alert_reactivation(self):
        """Test alert reactivation"""
        alert = self.env['stock.alert'].create({
            'name': 'Test Alert',
            'product_id': self.product.id,
            'alert_type': 'low_stock',
            'priority': 'medium',
            'status': 'cancelled',
            'current_stock': 10.0,
            'minimum_stock': 20.0,
            'company_id': self.company.id,
        })
        
        # Reactivate the alert
        alert.action_reactivate()
        
        self.assertEqual(alert.status, 'active')
    
    def test_kids_clothing_alerts(self):
        """Test kids clothing specific alert filtering"""
        # Create alerts with different age groups
        baby_alert = self.env['stock.alert'].create({
            'name': 'Baby Alert',
            'product_id': self.product.id,
            'alert_type': 'low_stock',
            'priority': 'medium',
            'status': 'active',
            'current_stock': 10.0,
            'minimum_stock': 20.0,
            'age_group': '0-2',
            'company_id': self.company.id,
        })
        
        toddler_alert = self.env['stock.alert'].create({
            'name': 'Toddler Alert',
            'product_id': self.product.id,
            'alert_type': 'low_stock',
            'priority': 'medium',
            'status': 'active',
            'current_stock': 10.0,
            'minimum_stock': 20.0,
            'age_group': '2-4',
            'company_id': self.company.id,
        })
        
        all_age_alert = self.env['stock.alert'].create({
            'name': 'All Age Alert',
            'product_id': self.product.id,
            'alert_type': 'low_stock',
            'priority': 'medium',
            'status': 'active',
            'current_stock': 10.0,
            'minimum_stock': 20.0,
            'age_group': 'all',
            'company_id': self.company.id,
        })
        
        # Test filtering by age group
        baby_alerts = self.env['stock.alert'].get_kids_clothing_alerts(age_group='0-2')
        self.assertIn(baby_alert, baby_alerts)
        self.assertIn(all_age_alert, baby_alerts)
        self.assertNotIn(toddler_alert, baby_alerts)
    
    def test_reorder_rule_creation(self):
        """Test creating reorder rule from alert"""
        alert = self.env['stock.alert'].create({
            'name': 'Test Alert',
            'product_id': self.product.id,
            'alert_type': 'low_stock',
            'priority': 'medium',
            'status': 'active',
            'current_stock': 10.0,
            'minimum_stock': 20.0,
            'maximum_stock': 100.0,
            'reorder_point': 15.0,
            'reorder_quantity': 50.0,
            'age_group': '0-2',
            'size': 's',
            'season': 'summer',
            'brand': 'Kids Brand',
            'color': 'Blue',
            'company_id': self.company.id,
        })
        
        # Create reorder rule from alert
        reorder_rule = alert.create_reorder_rule()
        
        self.assertEqual(reorder_rule.product_id, self.product)
        self.assertEqual(reorder_rule.minimum_stock, 20.0)
        self.assertEqual(reorder_rule.maximum_stock, 100.0)
        self.assertEqual(reorder_rule.reorder_quantity, 50.0)
        self.assertEqual(reorder_rule.age_group, '0-2')
        self.assertEqual(reorder_rule.size, 's')
        self.assertEqual(reorder_rule.season, 'summer')
        self.assertEqual(reorder_rule.brand, 'Kids Brand')
        self.assertEqual(reorder_rule.color, 'Blue')
    
    def test_alert_priority_levels(self):
        """Test different alert priority levels"""
        priorities = ['low', 'medium', 'high', 'urgent']
        
        for priority in priorities:
            alert = self.env['stock.alert'].create({
                'name': f'Test Alert {priority}',
                'product_id': self.product.id,
                'alert_type': 'low_stock',
                'priority': priority,
                'status': 'active',
                'current_stock': 10.0,
                'minimum_stock': 20.0,
                'company_id': self.company.id,
            })
            
            self.assertEqual(alert.priority, priority)
    
    def test_alert_types(self):
        """Test different alert types"""
        alert_types = [
            'low_stock', 'out_of_stock', 'overstock', 'expiry',
            'seasonal', 'size', 'brand', 'color'
        ]
        
        for alert_type in alert_types:
            alert = self.env['stock.alert'].create({
                'name': f'Test Alert {alert_type}',
                'product_id': self.product.id,
                'alert_type': alert_type,
                'priority': 'medium',
                'status': 'active',
                'current_stock': 10.0,
                'minimum_stock': 20.0,
                'company_id': self.company.id,
            })
            
            self.assertEqual(alert.alert_type, alert_type)
    
    def test_alert_status_transitions(self):
        """Test alert status transitions"""
        alert = self.env['stock.alert'].create({
            'name': 'Test Alert',
            'product_id': self.product.id,
            'alert_type': 'low_stock',
            'priority': 'medium',
            'status': 'draft',
            'current_stock': 10.0,
            'minimum_stock': 20.0,
            'company_id': self.company.id,
        })
        
        # Draft -> Active
        alert.write({'status': 'active'})
        self.assertEqual(alert.status, 'active')
        
        # Active -> Resolved
        alert.action_resolve()
        self.assertEqual(alert.status, 'resolved')
        
        # Resolved -> Cancelled (should not be allowed)
        with self.assertRaises(ValidationError):
            alert.write({'status': 'cancelled'})
    
    def test_alert_assignment(self):
        """Test alert assignment to users"""
        user = self.env['res.users'].create({
            'name': 'Test User',
            'login': 'test_user',
            'email': 'test@example.com',
        })
        
        alert = self.env['stock.alert'].create({
            'name': 'Test Alert',
            'product_id': self.product.id,
            'alert_type': 'low_stock',
            'priority': 'medium',
            'status': 'active',
            'current_stock': 10.0,
            'minimum_stock': 20.0,
            'assigned_to': user.id,
            'company_id': self.company.id,
        })
        
        self.assertEqual(alert.assigned_to, user)


if __name__ == '__main__':
    unittest.main()