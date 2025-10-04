# -*- coding: utf-8 -*-

from ocean.tests.common import TransactionCase
from ocean.exceptions import ValidationError, UserError


class TestAccountPayment(TransactionCase):
    
    def setUp(self):
        super(TestAccountPayment, self).setUp()
        self.payment_model = self.env['account.payment']
        self.partner_model = self.env['res.partner']
        
        # Create test partner
        self.test_partner = self.partner_model.create({
            'name': 'Test Customer',
            'is_company': True,
        })
    
    def test_payment_creation(self):
        """Test payment creation"""
        payment = self.payment_model.create({
            'partner_id': self.test_partner.id,
            'date': '2024-01-01',
            'amount': 100.0,
            'payment_type': 'inbound',
            'age_group': 'kids',
            'season': 'summer',
        })
        
        self.assertEqual(payment.partner_id, self.test_partner)
        self.assertEqual(payment.amount, 100.0)
        self.assertEqual(payment.age_group, 'kids')
        self.assertEqual(payment.season, 'summer')
        self.assertEqual(payment.state, 'draft')
    
    def test_payment_posting(self):
        """Test payment posting"""
        payment = self.payment_model.create({
            'partner_id': self.test_partner.id,
            'date': '2024-01-01',
            'amount': 100.0,
            'payment_type': 'inbound',
        })
        
        payment.action_post()
        
        self.assertEqual(payment.state, 'posted')
    
    def test_payment_cancellation(self):
        """Test payment cancellation"""
        payment = self.payment_model.create({
            'partner_id': self.test_partner.id,
            'date': '2024-01-01',
            'amount': 100.0,
            'payment_type': 'inbound',
        })
        
        payment.action_cancel()
        self.assertEqual(payment.state, 'cancelled')
    
    def test_payment_amount_validation(self):
        """Test payment amount validation"""
        with self.assertRaises(ValidationError):
            self.payment_model.create({
                'partner_id': self.test_partner.id,
                'date': '2024-01-01',
                'amount': 0.0,  # Invalid amount
                'payment_type': 'inbound',
            })