# -*- coding: utf-8 -*-

from ocean.tests.common import TransactionCase
from ocean.exceptions import ValidationError


class TestAccountPaymentMethod(TransactionCase):
    
    def setUp(self):
        super(TestAccountPaymentMethod, self).setUp()
        self.payment_method_model = self.env['account.payment.method']
    
    def test_payment_method_creation(self):
        """Test payment method creation"""
        method = self.payment_method_model.create({
            'name': 'Test Payment Method',
            'code': 'test_method',
            'payment_type': 'inbound',
            'age_group': 'kids',
            'season': 'summer',
            'gst_treatment': 'regular',
        })
        
        self.assertEqual(method.name, 'Test Payment Method')
        self.assertEqual(method.code, 'test_method')
        self.assertEqual(method.payment_type, 'inbound')
        self.assertEqual(method.age_group, 'kids')
        self.assertEqual(method.season, 'summer')
        self.assertEqual(method.gst_treatment, 'regular')
        self.assertTrue(method.active)
    
    def test_payment_method_code_unique(self):
        """Test payment method code uniqueness"""
        self.payment_method_model.create({
            'name': 'Test Method 1',
            'code': 'test_code',
            'payment_type': 'inbound',
        })
        
        with self.assertRaises(ValidationError):
            self.payment_method_model.create({
                'name': 'Test Method 2',
                'code': 'test_code',  # Same code
                'payment_type': 'inbound',
            })
    
    def test_get_payment_method(self):
        """Test getting payment method by criteria"""
        # Create method
        method = self.payment_method_model.create({
            'name': 'Kids Summer Method',
            'code': 'kids_summer',
            'payment_type': 'inbound',
            'age_group': 'kids',
            'season': 'summer',
            'gst_treatment': 'regular',
        })
        
        # Get method
        retrieved_method = self.payment_method_model.get_payment_method(
            payment_type='inbound',
            age_group='kids',
            season='summer'
        )
        
        self.assertEqual(retrieved_method, method)