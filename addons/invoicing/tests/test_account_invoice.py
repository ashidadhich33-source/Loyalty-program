# -*- coding: utf-8 -*-

from ocean.tests.common import TransactionCase
from ocean.exceptions import ValidationError, UserError


class TestAccountInvoice(TransactionCase):
    
    def setUp(self):
        super(TestAccountInvoice, self).setUp()
        self.invoice_model = self.env['account.invoice']
        self.partner_model = self.env['res.partner']
        self.product_model = self.env['product.product']
        
        # Create test partner
        self.test_partner = self.partner_model.create({
            'name': 'Test Customer',
            'is_company': True,
        })
        
        # Create test product
        self.test_product = self.product_model.create({
            'name': 'Test Product',
            'list_price': 100.0,
            'sale_ok': True,
        })
    
    def test_invoice_creation(self):
        """Test invoice creation"""
        invoice = self.invoice_model.create({
            'partner_id': self.test_partner.id,
            'date_invoice': '2024-01-01',
            'date_due': '2024-01-31',
            'age_group': 'kids',
            'season': 'summer',
        })
        
        self.assertEqual(invoice.partner_id, self.test_partner)
        self.assertEqual(invoice.age_group, 'kids')
        self.assertEqual(invoice.season, 'summer')
        self.assertEqual(invoice.state, 'draft')
    
    def test_invoice_posting(self):
        """Test invoice posting"""
        invoice = self.invoice_model.create({
            'partner_id': self.test_partner.id,
            'date_invoice': '2024-01-01',
            'date_due': '2024-01-31',
        })
        
        # Add invoice line
        self.env['account.invoice.line'].create({
            'invoice_id': invoice.id,
            'product_id': self.test_product.id,
            'name': 'Test Product',
            'quantity': 1,
            'price_unit': 100.0,
        })
        
        # Post invoice
        invoice.action_post()
        
        self.assertEqual(invoice.state, 'open')
        self.assertEqual(invoice.payment_state, 'not_paid')
    
    def test_invoice_cancellation(self):
        """Test invoice cancellation"""
        invoice = self.invoice_model.create({
            'partner_id': self.test_partner.id,
            'date_invoice': '2024-01-01',
            'date_due': '2024-01-31',
        })
        
        invoice.action_cancel()
        self.assertEqual(invoice.state, 'cancelled')
    
    def test_invoice_amount_computation(self):
        """Test invoice amount computation"""
        invoice = self.invoice_model.create({
            'partner_id': self.test_partner.id,
            'date_invoice': '2024-01-01',
            'date_due': '2024-01-31',
        })
        
        # Add invoice line
        line = self.env['account.invoice.line'].create({
            'invoice_id': invoice.id,
            'product_id': self.test_product.id,
            'name': 'Test Product',
            'quantity': 2,
            'price_unit': 100.0,
        })
        
        invoice._compute_amount()
        
        self.assertEqual(invoice.amount_untaxed, 200.0)
        self.assertEqual(invoice.amount_total, 200.0)  # No tax