# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - POS Order Tests
===================================

Tests for POS order functionality.
"""

import unittest
from core_framework.testing import OceanTestCase

class TestPosOrder(OceanTestCase):
    """Test POS order functionality"""
    
    def setUp(self):
        super().setUp()
        self.pos_order = self.env['pos.order']
        self.pos_session = self.env['pos.session']
        self.pos_config = self.env['pos.config']
        self.company = self.env['res.company'].search([], limit=1)
    
    def test_create_pos_order(self):
        """Test creating POS order"""
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
            'state': 'opened'
        }
        session = self.pos_session.create(session_vals)
        
        # Create order
        order_vals = {
            'name': 'POS-001',
            'session_id': session.id,
            'user_id': self.env.user.id,
            'state': 'draft',
            'amount_total': 100.0
        }
        
        order = self.pos_order.create(order_vals)
        
        self.assertEqual(order.name, 'POS-001')
        self.assertEqual(order.session_id, session)
        self.assertEqual(order.user_id, self.env.user)
        self.assertEqual(order.state, 'draft')
        self.assertEqual(order.amount_total, 100.0)
    
    def test_confirm_order(self):
        """Test confirming POS order"""
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
            'state': 'opened'
        }
        session = self.pos_session.create(session_vals)
        
        # Create order
        order_vals = {
            'name': 'POS-001',
            'session_id': session.id,
            'user_id': self.env.user.id,
            'state': 'draft',
            'amount_total': 100.0
        }
        order = self.pos_order.create(order_vals)
        
        # Confirm order
        order.action_confirm()
        
        self.assertEqual(order.state, 'paid')
        self.assertIsNotNone(order.receipt_number)
    
    def test_get_order_summary(self):
        """Test getting order summary"""
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
            'state': 'opened'
        }
        session = self.pos_session.create(session_vals)
        
        # Create order
        order_vals = {
            'name': 'POS-001',
            'session_id': session.id,
            'user_id': self.env.user.id,
            'state': 'draft',
            'amount_total': 100.0
        }
        order = self.pos_order.create(order_vals)
        
        # Get summary
        summary = order.get_order_summary()
        
        self.assertIn('order_name', summary)
        self.assertIn('customer', summary)
        self.assertIn('cashier', summary)
        self.assertIn('date', summary)
        self.assertIn('state', summary)
        self.assertIn('amount_total', summary)
        self.assertIn('payment_summary', summary)
    
    def tearDown(self):
        super().tearDown()