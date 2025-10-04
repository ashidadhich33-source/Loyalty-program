# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - POS Session Tests
=====================================

Tests for POS session functionality.
"""

import unittest
from core_framework.testing import OceanTestCase

class TestPosSession(OceanTestCase):
    """Test POS session functionality"""
    
    def setUp(self):
        super().setUp()
        self.pos_session = self.env['pos.session']
        self.pos_config = self.env['pos.config']
        self.company = self.env['res.company'].search([], limit=1)
    
    def test_create_pos_session(self):
        """Test creating POS session"""
        # Create POS config first
        config_vals = {
            'name': 'Test POS',
            'code': 'TEST_POS',
            'company_id': self.company.id,
            'is_active': True
        }
        config = self.pos_config.create(config_vals)
        
        # Create session
        session_vals = {
            'name': 'Test Session',
            'config_id': config.id,
            'user_id': self.env.user.id,
            'state': 'opened',
            'start_cash': 1000.0
        }
        
        session = self.pos_session.create(session_vals)
        
        self.assertEqual(session.name, 'Test Session')
        self.assertEqual(session.config_id, config)
        self.assertEqual(session.user_id, self.env.user)
        self.assertEqual(session.state, 'opened')
        self.assertEqual(session.start_cash, 1000.0)
    
    def test_close_session(self):
        """Test closing POS session"""
        # Create POS config first
        config_vals = {
            'name': 'Test POS',
            'code': 'TEST_POS',
            'company_id': self.company.id,
            'is_active': True
        }
        config = self.pos_config.create(config_vals)
        
        # Create session
        session_vals = {
            'name': 'Test Session',
            'config_id': config.id,
            'user_id': self.env.user.id,
            'state': 'opened',
            'start_cash': 1000.0
        }
        session = self.pos_session.create(session_vals)
        
        # Close session
        session.action_close()
        
        self.assertEqual(session.state, 'closed')
        self.assertIsNotNone(session.stop_at)
    
    def test_get_session_summary(self):
        """Test getting session summary"""
        # Create POS config first
        config_vals = {
            'name': 'Test POS',
            'code': 'TEST_POS',
            'company_id': self.company.id,
            'is_active': True
        }
        config = self.pos_config.create(config_vals)
        
        # Create session
        session_vals = {
            'name': 'Test Session',
            'config_id': config.id,
            'user_id': self.env.user.id,
            'state': 'opened',
            'start_cash': 1000.0
        }
        session = self.pos_session.create(session_vals)
        
        # Get summary
        summary = session.get_session_summary()
        
        self.assertIn('session_name', summary)
        self.assertIn('cashier', summary)
        self.assertIn('start_time', summary)
        self.assertIn('order_count', summary)
        self.assertIn('total_sales', summary)
        self.assertIn('payment_summary', summary)
    
    def tearDown(self):
        super().tearDown()