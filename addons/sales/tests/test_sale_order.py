# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Sales Addon - Sale Order Tests
=================================================

Standalone version of the sale order tests for kids clothing retail.
"""

import unittest
from datetime import datetime, date
from unittest.mock import Mock, patch

from core_framework.orm import BaseModel
from addons.sales.models.sale_order import SaleOrder, SaleOrderLine


class TestSaleOrder(unittest.TestCase):
    """Test cases for Sale Order model"""
    
    def setUp(self):
        """Set up test data"""
        self.sale_order_data = {
            'name': 'SO001',
            'partner_id': 1,
            'order_date': date.today().strftime('%Y-%m-%d'),
            'state': 'draft',
            'amount_total': 0.0,
            'currency_id': 1,
            'company_id': 1,
            'user_id': 1,
            'child_profile_id': 1,
        }
        
        self.sale_order_line_data = {
            'order_id': 1,
            'product_id': 1,
            'product_uom_qty': 2.0,
            'price_unit': 100.0,
            'price_subtotal': 200.0,
            'size_id': 1,
            'color_id': 1,
            'tax_id': 1,
        }
    
    def test_sale_order_creation(self):
        """Test sale order creation"""
        sale_order = SaleOrder(**self.sale_order_data)
        
        self.assertEqual(sale_order.name, 'SO001')
        self.assertEqual(sale_order.partner_id, 1)
        self.assertEqual(sale_order.state, 'draft')
        self.assertEqual(sale_order.child_profile_id, 1)
    
    def test_sale_order_line_creation(self):
        """Test sale order line creation"""
        sale_order_line = SaleOrderLine(**self.sale_order_line_data)
        
        self.assertEqual(sale_order_line.order_id, 1)
        self.assertEqual(sale_order_line.product_id, 1)
        self.assertEqual(sale_order_line.product_uom_qty, 2.0)
        self.assertEqual(sale_order_line.price_unit, 100.0)
        self.assertEqual(sale_order_line.price_subtotal, 200.0)
    
    def test_sale_order_state_transitions(self):
        """Test sale order state transitions"""
        sale_order = SaleOrder(**self.sale_order_data)
        
        # Test draft to sent
        sale_order.action_quotation_send()
        self.assertEqual(sale_order.state, 'sent')
        
        # Test sent to sale
        sale_order.action_confirm()
        self.assertEqual(sale_order.state, 'sale')
        
        # Test sale to done
        sale_order.action_done()
        self.assertEqual(sale_order.state, 'done')
    
    def test_sale_order_cancellation(self):
        """Test sale order cancellation"""
        sale_order = SaleOrder(**self.sale_order_data)
        
        sale_order.action_cancel()
        self.assertEqual(sale_order.state, 'cancel')
    
    def test_sale_order_kids_clothing_fields(self):
        """Test sale order kids clothing specific fields"""
        sale_order = SaleOrder(**self.sale_order_data)
        
        # Test child profile
        self.assertEqual(sale_order.child_profile_id, 1)
        
        # Test company
        self.assertEqual(sale_order.company_id, 1)
        
        # Test user
        self.assertEqual(sale_order.user_id, 1)


if __name__ == '__main__':
    unittest.main()