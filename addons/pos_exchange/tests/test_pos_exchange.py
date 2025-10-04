# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - POS Exchange Tests
======================================

Tests for POS exchange functionality.
"""

import unittest
from core_framework.testing import OceanTestCase

class TestPosExchange(OceanTestCase):
    """Test POS exchange functionality"""
    
    def setUp(self):
        super().setUp()
        self.pos_exchange = self.env['pos.exchange']
        self.pos_session = self.env['pos.session']
        self.pos_config = self.env['pos.config']
        self.pos_order = self.env['pos.order']
        self.company = self.env['res.company'].search([], limit=1)
        self.partner = self.env['res.partner'].search([], limit=1)
    
    def test_create_pos_exchange(self):
        """Test creating POS exchange"""
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
            'state': 'done',
            'amount_total': 100.0
        }
        order = self.pos_order.create(order_vals)
        
        # Create exchange
        exchange_vals = {
            'name': 'EXC-001',
            'session_id': session.id,
            'partner_id': self.partner.id,
            'original_order_id': order.id,
            'exchange_type': 'size_change',
            'customer_age': 5,
            'within_exchange_period': True,
            'exchange_period_days': 7,
            'amount_returned': 50.0,
            'amount_charged': 55.0,
            'amount_difference': 5.0
        }
        
        exchange = self.pos_exchange.create(exchange_vals)
        
        self.assertEqual(exchange.name, 'EXC-001')
        self.assertEqual(exchange.session_id, session)
        self.assertEqual(exchange.partner_id, self.partner)
        self.assertEqual(exchange.original_order_id, order)
        self.assertEqual(exchange.exchange_type, 'size_change')
        self.assertEqual(exchange.customer_age, 5)
        self.assertTrue(exchange.within_exchange_period)
        self.assertEqual(exchange.amount_returned, 50.0)
        self.assertEqual(exchange.amount_charged, 55.0)
        self.assertEqual(exchange.amount_difference, 5.0)
    
    def test_confirm_exchange(self):
        """Test confirming POS exchange"""
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
            'state': 'done',
            'amount_total': 100.0
        }
        order = self.pos_order.create(order_vals)
        
        # Create exchange
        exchange_vals = {
            'name': 'EXC-001',
            'session_id': session.id,
            'partner_id': self.partner.id,
            'original_order_id': order.id,
            'exchange_type': 'size_change',
            'customer_age': 5,
            'within_exchange_period': True,
            'exchange_period_days': 7,
            'amount_returned': 50.0,
            'amount_charged': 55.0,
            'amount_difference': 5.0
        }
        exchange = self.pos_exchange.create(exchange_vals)
        
        # Confirm exchange
        exchange.action_confirm()
        
        self.assertEqual(exchange.state, 'confirmed')
        self.assertIsNotNone(exchange.exchange_receipt_number)
    
    def test_get_exchange_summary(self):
        """Test getting exchange summary"""
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
            'state': 'done',
            'amount_total': 100.0
        }
        order = self.pos_order.create(order_vals)
        
        # Create exchange
        exchange_vals = {
            'name': 'EXC-001',
            'session_id': session.id,
            'partner_id': self.partner.id,
            'original_order_id': order.id,
            'exchange_type': 'size_change',
            'customer_age': 5,
            'within_exchange_period': True,
            'exchange_period_days': 7,
            'amount_returned': 50.0,
            'amount_charged': 55.0,
            'amount_difference': 5.0
        }
        exchange = self.pos_exchange.create(exchange_vals)
        
        # Get summary
        summary = exchange.get_exchange_summary()
        
        self.assertIn('exchange_name', summary)
        self.assertIn('customer', summary)
        self.assertIn('cashier', summary)
        self.assertIn('exchange_date', summary)
        self.assertIn('state', summary)
        self.assertIn('exchange_type', summary)
        self.assertIn('amount_returned', summary)
        self.assertIn('amount_charged', summary)
        self.assertIn('amount_difference', summary)
        self.assertIn('original_order', summary)
    
    def tearDown(self):
        super().tearDown()