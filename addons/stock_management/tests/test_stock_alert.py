# -*- coding: utf-8 -*-

from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError, UserError


class TestStockAlert(TransactionCase):
    
    def setUp(self):
        super(TestStockAlert, self).setUp()
        
        # Create test data
        self.product = self.env['product.product'].create({
            'name': 'Test Product',
            'type': 'product',
            'age_group': '0-2',
            'size': 's',
            'season': 'summer',
            'brand': 'Test Brand',
            'color': 'Blue',
        })
        
        self.warehouse = self.env['stock.warehouse'].create({
            'name': 'Test Warehouse',
            'code': 'TW',
        })
        
        self.location = self.env['stock.location'].create({
            'name': 'Test Location',
            'location_id': self.warehouse.lot_stock_id.id,
        })
    
    def test_create_stock_alert(self):
        """Test creating a stock alert"""
        alert = self.env['stock.alert'].create({
            'name': 'Test Alert',
            'product_id': self.product.id,
            'warehouse_id': self.warehouse.id,
            'location_id': self.location.id,
            'current_stock': 5,
            'minimum_stock': 10,
            'alert_type': 'low_stock',
            'priority': 'high',
            'age_group': '0-2',
            'size': 's',
            'season': 'summer',
            'brand': 'Test Brand',
            'color': 'Blue',
        })
        
        self.assertEqual(alert.name, 'Test Alert')
        self.assertEqual(alert.product_id, self.product)
        self.assertEqual(alert.warehouse_id, self.warehouse)
        self.assertEqual(alert.current_stock, 5)
        self.assertEqual(alert.minimum_stock, 10)
        self.assertEqual(alert.alert_type, 'low_stock')
        self.assertEqual(alert.priority, 'high')
        self.assertEqual(alert.status, 'active')
        self.assertEqual(alert.stock_variance, -5)
    
    def test_acknowledge_alert(self):
        """Test acknowledging a stock alert"""
        alert = self.env['stock.alert'].create({
            'name': 'Test Alert',
            'product_id': self.product.id,
            'warehouse_id': self.warehouse.id,
            'current_stock': 5,
            'minimum_stock': 10,
            'alert_type': 'low_stock',
            'priority': 'high',
        })
        
        self.assertEqual(alert.status, 'active')
        
        alert.action_acknowledge()
        
        self.assertEqual(alert.status, 'acknowledged')
        self.assertTrue(alert.acknowledge_date)
        self.assertEqual(alert.acknowledged_by, self.env.user)
    
    def test_resolve_alert(self):
        """Test resolving a stock alert"""
        alert = self.env['stock.alert'].create({
            'name': 'Test Alert',
            'product_id': self.product.id,
            'warehouse_id': self.warehouse.id,
            'current_stock': 5,
            'minimum_stock': 10,
            'alert_type': 'low_stock',
            'priority': 'high',
        })
        
        self.assertEqual(alert.status, 'active')
        
        alert.action_resolve()
        
        self.assertEqual(alert.status, 'resolved')
        self.assertTrue(alert.resolve_date)
        self.assertEqual(alert.resolved_by, self.env.user)
    
    def test_cancel_alert(self):
        """Test cancelling a stock alert"""
        alert = self.env['stock.alert'].create({
            'name': 'Test Alert',
            'product_id': self.product.id,
            'warehouse_id': self.warehouse.id,
            'current_stock': 5,
            'minimum_stock': 10,
            'alert_type': 'low_stock',
            'priority': 'high',
        })
        
        self.assertEqual(alert.status, 'active')
        
        alert.action_cancel()
        
        self.assertEqual(alert.status, 'cancelled')
    
    def test_generate_alert_message(self):
        """Test generating alert message"""
        alert = self.env['stock.alert'].create({
            'name': 'Test Alert',
            'product_id': self.product.id,
            'warehouse_id': self.warehouse.id,
            'current_stock': 5,
            'minimum_stock': 10,
            'alert_type': 'low_stock',
            'priority': 'high',
        })
        
        expected_message = f"Low stock alert for {self.product.name}. Current stock: 5, Minimum required: 10"
        self.assertEqual(alert.alert_message, expected_message)
    
    def test_days_since_created(self):
        """Test computing days since created"""
        alert = self.env['stock.alert'].create({
            'name': 'Test Alert',
            'product_id': self.product.id,
            'warehouse_id': self.warehouse.id,
            'current_stock': 5,
            'minimum_stock': 10,
            'alert_type': 'low_stock',
            'priority': 'high',
        })
        
        # The computed field should be calculated
        self.assertIsInstance(alert.days_since_created, int)
        self.assertGreaterEqual(alert.days_since_created, 0)
    
    def test_stock_variance(self):
        """Test computing stock variance"""
        alert = self.env['stock.alert'].create({
            'name': 'Test Alert',
            'product_id': self.product.id,
            'warehouse_id': self.warehouse.id,
            'current_stock': 5,
            'minimum_stock': 10,
            'alert_type': 'low_stock',
            'priority': 'high',
        })
        
        self.assertEqual(alert.stock_variance, -5)
        
        # Update current stock
        alert.current_stock = 15
        alert._compute_stock_variance()
        
        self.assertEqual(alert.stock_variance, 5)
    
    def test_kids_clothing_fields(self):
        """Test kids clothing specific fields"""
        alert = self.env['stock.alert'].create({
            'name': 'Test Alert',
            'product_id': self.product.id,
            'warehouse_id': self.warehouse.id,
            'current_stock': 5,
            'minimum_stock': 10,
            'alert_type': 'low_stock',
            'priority': 'high',
            'age_group': '0-2',
            'size': 's',
            'season': 'summer',
            'brand': 'Test Brand',
            'color': 'Blue',
        })
        
        self.assertEqual(alert.age_group, '0-2')
        self.assertEqual(alert.size, 's')
        self.assertEqual(alert.season, 'summer')
        self.assertEqual(alert.brand, 'Test Brand')
        self.assertEqual(alert.color, 'Blue')
    
    def test_alert_types(self):
        """Test different alert types"""
        alert_types = [
            'low_stock',
            'out_of_stock',
            'overstock',
            'expiry_warning',
            'seasonal_alert',
            'size_alert',
            'brand_alert',
            'color_alert',
        ]
        
        for alert_type in alert_types:
            alert = self.env['stock.alert'].create({
                'name': f'Test {alert_type} Alert',
                'product_id': self.product.id,
                'warehouse_id': self.warehouse.id,
                'current_stock': 5,
                'minimum_stock': 10,
                'alert_type': alert_type,
                'priority': 'medium',
            })
            
            self.assertEqual(alert.alert_type, alert_type)
    
    def test_priority_levels(self):
        """Test different priority levels"""
        priorities = ['low', 'medium', 'high', 'critical']
        
        for priority in priorities:
            alert = self.env['stock.alert'].create({
                'name': f'Test {priority} Priority Alert',
                'product_id': self.product.id,
                'warehouse_id': self.warehouse.id,
                'current_stock': 5,
                'minimum_stock': 10,
                'alert_type': 'low_stock',
                'priority': priority,
            })
            
            self.assertEqual(alert.priority, priority)
    
    def test_status_transitions(self):
        """Test status transitions"""
        alert = self.env['stock.alert'].create({
            'name': 'Test Alert',
            'product_id': self.product.id,
            'warehouse_id': self.warehouse.id,
            'current_stock': 5,
            'minimum_stock': 10,
            'alert_type': 'low_stock',
            'priority': 'high',
        })
        
        # Active -> Acknowledged
        self.assertEqual(alert.status, 'active')
        alert.action_acknowledge()
        self.assertEqual(alert.status, 'acknowledged')
        
        # Acknowledged -> Resolved
        alert.action_resolve()
        self.assertEqual(alert.status, 'resolved')
        
        # Cannot transition from resolved
        with self.assertRaises(Exception):
            alert.action_acknowledge()
    
    def test_notification_fields(self):
        """Test notification fields"""
        user = self.env['res.users'].create({
            'name': 'Test User',
            'login': 'testuser',
            'email': 'test@example.com',
        })
        
        alert = self.env['stock.alert'].create({
            'name': 'Test Alert',
            'product_id': self.product.id,
            'warehouse_id': self.warehouse.id,
            'current_stock': 5,
            'minimum_stock': 10,
            'alert_type': 'low_stock',
            'priority': 'high',
            'notify_users': [(6, 0, [user.id])],
        })
        
        self.assertIn(user, alert.notify_users)
        self.assertFalse(alert.email_sent)
        self.assertFalse(alert.sms_sent)