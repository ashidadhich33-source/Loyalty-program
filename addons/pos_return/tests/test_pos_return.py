# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - POS Return Tests
====================================

Tests for POS return functionality.
"""

import unittest
from core_framework.testing import OceanTestCase

class TestPosReturn(OceanTestCase):
    """Test POS return functionality"""
    
    def setUp(self):
        super().setUp()
        self.pos_return = self.env['pos.return']
        self.pos_session = self.env['pos.session']
        self.pos_config = self.env['pos.config']
        self.pos_order = self.env['pos.order']
        self.company = self.env['res.company'].search([], limit=1)
        self.partner = self.env['res.partner'].search([], limit=1)
    
    def test_create_pos_return(self):
        """Test creating POS return"""
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
        
        # Create return
        return_vals = {
            'name': 'RET-001',
            'session_id': session.id,
            'partner_id': self.partner.id,
            'original_order_id': order.id,
            'return_type': 'full_return',
            'customer_age': 5,
            'within_return_period': True,
            'return_period_days': 7,
            'amount_returned': 100.0,
            'amount_refunded': 100.0,
            'refund_method': 'cash',
            'refund_percentage': 100.0
        }
        
        return_record = self.pos_return.create(return_vals)
        
        self.assertEqual(return_record.name, 'RET-001')
        self.assertEqual(return_record.session_id, session)
        self.assertEqual(return_record.partner_id, self.partner)
        self.assertEqual(return_record.original_order_id, order)
        self.assertEqual(return_record.return_type, 'full_return')
        self.assertEqual(return_record.customer_age, 5)
        self.assertTrue(return_record.within_return_period)
        self.assertEqual(return_record.amount_returned, 100.0)
        self.assertEqual(return_record.amount_refunded, 100.0)
        self.assertEqual(return_record.refund_method, 'cash')
        self.assertEqual(return_record.refund_percentage, 100.0)
    
    def test_confirm_return(self):
        """Test confirming POS return"""
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
        
        # Create return
        return_vals = {
            'name': 'RET-001',
            'session_id': session.id,
            'partner_id': self.partner.id,
            'original_order_id': order.id,
            'return_type': 'full_return',
            'customer_age': 5,
            'within_return_period': True,
            'return_period_days': 7,
            'amount_returned': 100.0,
            'amount_refunded': 100.0,
            'refund_method': 'cash',
            'refund_percentage': 100.0
        }
        return_record = self.pos_return.create(return_vals)
        
        # Confirm return
        return_record.action_confirm()
        
        self.assertEqual(return_record.state, 'confirmed')
        self.assertIsNotNone(return_record.return_receipt_number)
    
    def test_get_return_summary(self):
        """Test getting return summary"""
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
        
        # Create return
        return_vals = {
            'name': 'RET-001',
            'session_id': session.id,
            'partner_id': self.partner.id,
            'original_order_id': order.id,
            'return_type': 'full_return',
            'customer_age': 5,
            'within_return_period': True,
            'return_period_days': 7,
            'amount_returned': 100.0,
            'amount_refunded': 100.0,
            'refund_method': 'cash',
            'refund_percentage': 100.0
        }
        return_record = self.pos_return.create(return_vals)
        
        # Get summary
        summary = return_record.get_return_summary()
        
        self.assertIn('return_name', summary)
        self.assertIn('customer', summary)
        self.assertIn('cashier', summary)
        self.assertIn('return_date', summary)
        self.assertIn('state', summary)
        self.assertIn('return_type', summary)
        self.assertIn('amount_returned', summary)
        self.assertIn('amount_refunded', summary)
        self.assertIn('refund_method', summary)
        self.assertIn('original_order', summary)
        self.assertIn('store_credit_amount', summary)
    
    def tearDown(self):
        super().tearDown()