# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - POS Configuration Tests
===========================================

Tests for POS configuration functionality.
"""

import unittest
from core_framework.testing import OceanTestCase

class TestPosConfig(OceanTestCase):
    """Test POS configuration functionality"""
    
    def setUp(self):
        super().setUp()
        self.pos_config = self.env['pos.config']
        self.company = self.env['res.company'].search([], limit=1)
    
    def test_create_pos_config(self):
        """Test creating POS configuration"""
        config_vals = {
            'name': 'Test POS',
            'code': 'TEST_POS',
            'company_id': self.company.id,
            'is_active': True,
            'allow_discount': True,
            'max_discount_percentage': 20.0,
            'enable_loyalty': True,
            'loyalty_points_per_rupee': 1.0,
            'enable_age_discount': True,
            'age_discount_percentage': 10.0
        }
        
        config = self.pos_config.create(config_vals)
        
        self.assertEqual(config.name, 'Test POS')
        self.assertEqual(config.code, 'TEST_POS')
        self.assertEqual(config.company_id, self.company)
        self.assertTrue(config.is_active)
        self.assertTrue(config.allow_discount)
        self.assertEqual(config.max_discount_percentage, 20.0)
        self.assertTrue(config.enable_loyalty)
        self.assertEqual(config.loyalty_points_per_rupee, 1.0)
        self.assertTrue(config.enable_age_discount)
        self.assertEqual(config.age_discount_percentage, 10.0)
    
    def test_pos_config_validation(self):
        """Test POS configuration validation"""
        config_vals = {
            'name': 'Test POS',
            'code': 'TEST_POS',
            'company_id': self.company.id,
            'max_discount_percentage': 150.0  # Invalid: > 100
        }
        
        with self.assertRaises(Exception):
            self.pos_config.create(config_vals)
    
    def test_start_session(self):
        """Test starting POS session"""
        config_vals = {
            'name': 'Test POS',
            'code': 'TEST_POS',
            'company_id': self.company.id,
            'is_active': True
        }
        
        config = self.pos_config.create(config_vals)
        
        # Start session
        result = config.action_start_session()
        
        self.assertIsNotNone(result)
        self.assertEqual(result['res_model'], 'pos.session')
        
        # Check session was created
        session = self.env['pos.session'].search([
            ('config_id', '=', config.id),
            ('state', '=', 'opened')
        ])
        
        self.assertTrue(session)
        self.assertEqual(session.config_id, config)
        self.assertEqual(session.user_id, self.env.user)
    
    def test_close_session(self):
        """Test closing POS session"""
        config_vals = {
            'name': 'Test POS',
            'code': 'TEST_POS',
            'company_id': self.company.id,
            'is_active': True
        }
        
        config = self.pos_config.create(config_vals)
        
        # Start session
        config.action_start_session()
        
        # Close session
        result = config.action_close_session()
        
        self.assertTrue(result)
        
        # Check session was closed
        session = self.env['pos.session'].search([
            ('config_id', '=', config.id),
            ('state', '=', 'closed')
        ])
        
        self.assertTrue(session)
    
    def test_get_dashboard_data(self):
        """Test getting dashboard data"""
        config_vals = {
            'name': 'Test POS',
            'code': 'TEST_POS',
            'company_id': self.company.id,
            'is_active': True
        }
        
        config = self.pos_config.create(config_vals)
        
        # Get dashboard data
        data = config.get_pos_dashboard_data()
        
        self.assertIn('today_sales', data)
        self.assertIn('today_revenue', data)
        self.assertIn('session_info', data)
        self.assertIsInstance(data['today_sales'], int)
        self.assertIsInstance(data['today_revenue'], (int, float))
        self.assertIsInstance(data['session_info'], dict)
    
    def test_validate_pos_config(self):
        """Test POS configuration validation"""
        config_vals = {
            'name': 'Test POS',
            'code': 'TEST_POS',
            'company_id': self.company.id,
            'is_active': True,
            'enable_loyalty': True,
            'loyalty_points_per_rupee': 0.0  # Invalid: <= 0
        }
        
        config = self.pos_config.create(config_vals)
        
        with self.assertRaises(Exception):
            config.validate_pos_config()
    
    def tearDown(self):
        super().tearDown()