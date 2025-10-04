# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Purchase Order Tests
========================================

Test cases for purchase order functionality.
"""

import unittest
from datetime import datetime
from core_framework.exceptions import ValidationError

class TestPurchaseOrder(unittest.TestCase):
    """Test cases for Purchase Order model"""
    
    def setUp(self):
        """Set up test data"""
        self.partner = self.env['res.partner'].create({
            'name': 'Test Supplier',
            'is_supplier': True,
        })
        
        self.product = self.env['product.template'].create({
            'name': 'Test Product',
            'type': 'product',
        })
    
    def tearDown(self):
        """Clean up test data"""
        pass
    
    def test_create_purchase_order(self):
        """Test creating a purchase order"""
        order = self.env['purchase.order'].create({
            'name': 'PO-TEST-001',
            'partner_id': self.partner.id,
            'date_order': datetime.now(),
            'age_group': 'child',
            'season': 'summer',
            'gender': 'unisex',
        })
        
        self.assertEqual(order.name, 'PO-TEST-001')
        self.assertEqual(order.partner_id.id, self.partner.id)
        self.assertEqual(order.state, 'draft')
        self.assertEqual(order.age_group, 'child')
        self.assertEqual(order.season, 'summer')
        self.assertEqual(order.gender, 'unisex')
    
    def test_purchase_order_workflow(self):
        """Test purchase order workflow"""
        order = self.env['purchase.order'].create({
            'name': 'PO-TEST-002',
            'partner_id': self.partner.id,
            'date_order': datetime.now(),
        })
        
        # Test sending RFQ
        order.action_send_rfq()
        self.assertEqual(order.state, 'sent')
        
        # Test approval
        order.action_approve()
        self.assertEqual(order.state, 'purchase')
        self.assertIsNotNone(order.approved_by)
        self.assertIsNotNone(order.approval_date)
        
        # Test completion
        order.action_done()
        self.assertEqual(order.state, 'done')
    
    def test_purchase_order_cancellation(self):
        """Test purchase order cancellation"""
        order = self.env['purchase.order'].create({
            'name': 'PO-TEST-003',
            'partner_id': self.partner.id,
            'date_order': datetime.now(),
        })
        
        # Test cancellation from draft
        order.action_cancel()
        self.assertEqual(order.state, 'cancel')
        
        # Test cancellation from sent
        order.state = 'sent'
        order.action_cancel()
        self.assertEqual(order.state, 'cancel')
        
        # Test cancellation from done (should fail)
        order.state = 'done'
        with self.assertRaises(ValidationError):
            order.action_cancel()
    
    def test_purchase_order_totals_calculation(self):
        """Test purchase order totals calculation"""
        order = self.env['purchase.order'].create({
            'name': 'PO-TEST-004',
            'partner_id': self.partner.id,
            'date_order': datetime.now(),
        })
        
        # Create order line
        line = self.env['purchase.order.line'].create({
            'order_id': order.id,
            'product_id': self.product.id,
            'product_qty': 10,
            'price_unit': 100.0,
        })
        
        # Calculate totals
        order._calculate_totals()
        
        self.assertEqual(order.amount_untaxed, 1000.0)
        self.assertEqual(order.amount_tax, 180.0)  # 18% GST
        self.assertEqual(order.amount_total, 1180.0)
    
    def test_purchase_order_validation(self):
        """Test purchase order validation"""
        order = self.env['purchase.order'].create({
            'name': 'PO-TEST-005',
            'partner_id': self.partner.id,
            'date_order': datetime.now(),
        })
        
        # Test validation without lines
        with self.assertRaises(ValidationError):
            order._validate_order()
        
        # Add order line
        self.env['purchase.order.line'].create({
            'order_id': order.id,
            'product_id': self.product.id,
            'product_qty': 10,
            'price_unit': 100.0,
        })
        
        # Should not raise error now
        order._validate_order()
    
    def test_purchase_order_summary(self):
        """Test purchase order summary"""
        order = self.env['purchase.order'].create({
            'name': 'PO-TEST-006',
            'partner_id': self.partner.id,
            'date_order': datetime.now(),
        })
        
        # Add order line
        self.env['purchase.order.line'].create({
            'order_id': order.id,
            'product_id': self.product.id,
            'product_qty': 5,
            'price_unit': 200.0,
        })
        
        summary = order.get_order_summary()
        
        self.assertEqual(summary['total_lines'], 1)
        self.assertEqual(summary['total_quantity'], 5)
        self.assertEqual(summary['total_amount'], 1180.0)  # 1000 + 180 tax
        self.assertEqual(summary['currency'], 'INR')
    
    def test_purchase_order_kids_clothing_fields(self):
        """Test kids clothing specific fields"""
        order = self.env['purchase.order'].create({
            'name': 'PO-TEST-007',
            'partner_id': self.partner.id,
            'date_order': datetime.now(),
            'age_group': 'toddler',
            'season': 'winter',
            'size_range': 'm',
            'gender': 'girls',
            'special_occasion': 'party_wear',
        })
        
        self.assertEqual(order.age_group, 'toddler')
        self.assertEqual(order.season, 'winter')
        self.assertEqual(order.size_range, 'm')
        self.assertEqual(order.gender, 'girls')
        self.assertEqual(order.special_occasion, 'party_wear')
    
    def test_purchase_order_reference_generation(self):
        """Test purchase order reference generation"""
        order = self.env['purchase.order'].create({
            'partner_id': self.partner.id,
            'date_order': datetime.now(),
        })
        
        # Check that reference was generated
        self.assertIsNotNone(order.name)
        self.assertTrue(order.name.startswith('PO'))
    
    def test_purchase_order_approval_workflow(self):
        """Test purchase order approval workflow"""
        order = self.env['purchase.order'].create({
            'name': 'PO-TEST-008',
            'partner_id': self.partner.id,
            'date_order': datetime.now(),
            'approval_required': True,
        })
        
        # Test approval from sent state
        order.state = 'sent'
        order.action_approve()
        self.assertEqual(order.state, 'purchase')
        self.assertIsNotNone(order.approved_by)
        self.assertIsNotNone(order.approval_date)
        
        # Test approval from to_approve state
        order.state = 'to_approve'
        order.action_approve()
        self.assertEqual(order.state, 'purchase')
    
    def test_purchase_order_company_defaults(self):
        """Test purchase order company defaults"""
        order = self.env['purchase.order'].create({
            'partner_id': self.partner.id,
            'date_order': datetime.now(),
        })
        
        # Check that company and currency were set
        self.assertIsNotNone(order.company_id)
        self.assertIsNotNone(order.currency_id)