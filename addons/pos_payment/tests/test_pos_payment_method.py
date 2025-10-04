# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - POS Payment Method Tests
============================================

Tests for POS payment method functionality.
"""

import unittest
from core_framework.testing import OceanTestCase

class TestPosPaymentMethod(OceanTestCase):
    """Test POS payment method functionality"""
    
    def setUp(self):
        super().setUp()
        self.pos_payment_method = self.env['pos.payment.method']
        self.pos_config = self.env['pos.config']
        self.company = self.env['res.company'].search([], limit=1)
    
    def test_create_payment_method(self):
        """Test creating payment method"""
        # Create POS config first
        config_vals = {
            'name': 'Test POS',
            'code': 'TEST_POS',
            'company_id': self.company.id,
            'is_active': True
        }
        config = self.pos_config.create(config_vals)
        
        # Create payment method
        method_vals = {
            'name': 'Test Payment Method',
            'code': 'TEST_PAYMENT',
            'description': 'Test payment method',
            'payment_type': 'cash',
            'is_active': True,
            'is_default': False,
            'requires_confirmation': False,
            'payment_provider': 'manual',
            'has_fees': False,
            'min_amount': 0.0,
            'max_amount': 0.0,
            'daily_limit': 0.0,
            'age_group_restriction': 'none',
            'requires_adult_supervision': False,
            'requires_pin': False,
            'requires_signature': False,
            'icon': 'fas fa-money-bill-wave',
            'color': '#28a745',
            'sequence': 10
        }
        
        method = self.pos_payment_method.create(method_vals)
        
        self.assertEqual(method.name, 'Test Payment Method')
        self.assertEqual(method.code, 'TEST_PAYMENT')
        self.assertEqual(method.payment_type, 'cash')
        self.assertTrue(method.is_active)
        self.assertFalse(method.is_default)
        self.assertFalse(method.requires_confirmation)
        self.assertEqual(method.payment_provider, 'manual')
        self.assertFalse(method.has_fees)
        self.assertEqual(method.min_amount, 0.0)
        self.assertEqual(method.max_amount, 0.0)
        self.assertEqual(method.daily_limit, 0.0)
        self.assertEqual(method.age_group_restriction, 'none')
        self.assertFalse(method.requires_adult_supervision)
        self.assertFalse(method.requires_pin)
        self.assertFalse(method.requires_signature)
        self.assertEqual(method.icon, 'fas fa-money-bill-wave')
        self.assertEqual(method.color, '#28a745')
        self.assertEqual(method.sequence, 10)
    
    def test_validate_age_group(self):
        """Test age group validation"""
        # Create payment method
        method_vals = {
            'name': 'Test Payment Method',
            'code': 'TEST_PAYMENT',
            'payment_type': 'card',
            'age_group_restriction': 'child_teen'
        }
        method = self.pos_payment_method.create(method_vals)
        
        # Test age group validation
        self.assertTrue(method.validate_age_group(5))  # Child
        self.assertTrue(method.validate_age_group(15))  # Teen
        self.assertFalse(method.validate_age_group(2))  # Toddler
    
    def test_validate_amount(self):
        """Test amount validation"""
        # Create payment method
        method_vals = {
            'name': 'Test Payment Method',
            'code': 'TEST_PAYMENT',
            'payment_type': 'card',
            'min_amount': 10.0,
            'max_amount': 1000.0
        }
        method = self.pos_payment_method.create(method_vals)
        
        # Test amount validation
        is_valid, message = method.validate_amount(50.0)
        self.assertTrue(is_valid)
        
        is_valid, message = method.validate_amount(5.0)
        self.assertFalse(is_valid)
        self.assertIn('Amount must be at least', message)
        
        is_valid, message = method.validate_amount(1500.0)
        self.assertFalse(is_valid)
        self.assertIn('Amount cannot exceed', message)
    
    def test_calculate_fee(self):
        """Test fee calculation"""
        # Create payment method with percentage fee
        method_vals = {
            'name': 'Test Payment Method',
            'code': 'TEST_PAYMENT',
            'payment_type': 'card',
            'has_fees': True,
            'fee_type': 'percentage',
            'fee_percentage': 2.5
        }
        method = self.pos_payment_method.create(method_vals)
        
        # Test fee calculation
        fee = method.calculate_fee(100.0)
        self.assertEqual(fee, 2.5)
        
        # Create payment method with fixed fee
        method_vals = {
            'name': 'Test Payment Method 2',
            'code': 'TEST_PAYMENT_2',
            'payment_type': 'card',
            'has_fees': True,
            'fee_type': 'fixed',
            'fee_amount': 5.0
        }
        method2 = self.pos_payment_method.create(method_vals)
        
        # Test fixed fee calculation
        fee = method2.calculate_fee(100.0)
        self.assertEqual(fee, 5.0)
    
    def test_process_payment(self):
        """Test payment processing"""
        # Create payment method
        method_vals = {
            'name': 'Test Payment Method',
            'code': 'TEST_PAYMENT',
            'payment_type': 'cash',
            'payment_provider': 'manual',
            'has_fees': False
        }
        method = self.pos_payment_method.create(method_vals)
        
        # Test payment processing
        result = method.process_payment(100.0)
        
        self.assertEqual(result['status'], 'success')
        self.assertIn('transaction_id', result)
        self.assertEqual(result['amount'], 100.0)
        self.assertEqual(result['fee'], 0.0)
        self.assertEqual(result['net_amount'], 100.0)
    
    def test_get_payment_method_summary(self):
        """Test getting payment method summary"""
        # Create payment method
        method_vals = {
            'name': 'Test Payment Method',
            'code': 'TEST_PAYMENT',
            'payment_type': 'card',
            'is_active': True,
            'is_default': False,
            'requires_confirmation': True,
            'payment_provider': 'manual',
            'has_fees': True,
            'fee_type': 'percentage',
            'fee_percentage': 2.5,
            'min_amount': 10.0,
            'max_amount': 1000.0,
            'daily_limit': 5000.0,
            'age_group_restriction': 'none',
            'requires_adult_supervision': True,
            'requires_pin': True,
            'requires_signature': False,
            'usage_count': 10,
            'total_amount': 5000.0
        }
        method = self.pos_payment_method.create(method_vals)
        
        # Get summary
        summary = method.get_payment_method_summary()
        
        self.assertIn('payment_method_name', summary)
        self.assertIn('payment_method_code', summary)
        self.assertIn('payment_type', summary)
        self.assertIn('is_active', summary)
        self.assertIn('is_default', summary)
        self.assertIn('requires_confirmation', summary)
        self.assertIn('payment_provider', summary)
        self.assertIn('has_fees', summary)
        self.assertIn('fee_type', summary)
        self.assertIn('fee_amount', summary)
        self.assertIn('fee_percentage', summary)
        self.assertIn('min_amount', summary)
        self.assertIn('max_amount', summary)
        self.assertIn('daily_limit', summary)
        self.assertIn('age_group_restriction', summary)
        self.assertIn('requires_adult_supervision', summary)
        self.assertIn('requires_pin', summary)
        self.assertIn('requires_signature', summary)
        self.assertIn('usage_count', summary)
        self.assertIn('total_amount', summary)
        self.assertIn('last_used', summary)
    
    def tearDown(self):
        super().tearDown()