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
            'total_amount': 0.0,
            'currency_id': 1,
            'company_id': 1,
            'user_id': 1,
            'child_profile_id': 1,
            'age_group': 'toddler',
            'gst_treatment': 'consumer',
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
        self.assertEqual(sale_order.age_group, 'toddler')
        self.assertEqual(sale_order.gst_treatment, 'consumer')
    
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
        sale_order.state = 'sent'
        self.assertEqual(sale_order.state, 'sent')
        
        # Test sent to sale
        sale_order.state = 'sale'
        self.assertEqual(sale_order.state, 'sale')
        
        # Test sale to done
        sale_order.state = 'done'
        self.assertEqual(sale_order.state, 'done')
    
    def test_sale_order_cancellation(self):
        """Test sale order cancellation"""
        sale_order = SaleOrder(**self.sale_order_data)
        
        sale_order.state = 'cancel'
        self.assertEqual(sale_order.state, 'cancel')
    
    def test_sale_order_total_calculation(self):
        """Test sale order total calculation"""
        sale_order = SaleOrder(**self.sale_order_data)
        
        # Mock order lines
        line1 = Mock()
        line1.price_subtotal = 100.0
        
        line2 = Mock()
        line2.price_subtotal = 150.0
        
        sale_order.order_line_ids = [line1, line2]
        
        # Calculate total
        sale_order._compute_total_amount()
        
        self.assertEqual(sale_order.total_amount, 250.0)
    
    def test_sale_order_line_subtotal_calculation(self):
        """Test sale order line subtotal calculation"""
        sale_order_line = SaleOrderLine(**self.sale_order_line_data)
        
        # Calculate subtotal
        sale_order_line._compute_price_subtotal()
        
        expected_subtotal = sale_order_line.product_uom_qty * sale_order_line.price_unit
        self.assertEqual(sale_order_line.price_subtotal, expected_subtotal)
    
    def test_sale_order_kids_clothing_fields(self):
        """Test sale order kids clothing specific fields"""
        sale_order = SaleOrder(**self.sale_order_data)
        
        # Test age group
        self.assertIn(sale_order.age_group, ['infant', 'toddler', 'preschool', 'child', 'teen'])
        
        # Test GST treatment
        self.assertIn(sale_order.gst_treatment, ['consumer', 'registered', 'unregistered'])
        
        # Test child profile
        self.assertEqual(sale_order.child_profile_id, 1)
    
    def test_sale_order_validation(self):
        """Test sale order validation"""
        # Test required fields
        with self.assertRaises(ValueError):
            SaleOrder()  # Missing required fields
        
        # Test valid order
        sale_order = SaleOrder(**self.sale_order_data)
        self.assertIsNotNone(sale_order)
    
    def test_sale_order_line_validation(self):
        """Test sale order line validation"""
        # Test required fields
        with self.assertRaises(ValueError):
            SaleOrderLine()  # Missing required fields
        
        # Test valid line
        sale_order_line = SaleOrderLine(**self.sale_order_line_data)
        self.assertIsNotNone(sale_order_line)
    
    def test_sale_order_multi_company(self):
        """Test sale order multi-company support"""
        sale_order = SaleOrder(**self.sale_order_data)
        
        # Test company assignment
        self.assertEqual(sale_order.company_id, 1)
        
        # Test company change
        sale_order.company_id = 2
        self.assertEqual(sale_order.company_id, 2)
    
    def test_sale_order_currency_support(self):
        """Test sale order currency support"""
        sale_order = SaleOrder(**self.sale_order_data)
        
        # Test currency assignment
        self.assertEqual(sale_order.currency_id, 1)
        
        # Test currency change
        sale_order.currency_id = 2
        self.assertEqual(sale_order.currency_id, 2)
    
    def test_sale_order_salesperson_assignment(self):
        """Test sale order salesperson assignment"""
        sale_order = SaleOrder(**self.sale_order_data)
        
        # Test salesperson assignment
        self.assertEqual(sale_order.user_id, 1)
        
        # Test salesperson change
        sale_order.user_id = 2
        self.assertEqual(sale_order.user_id, 2)
    
    def test_sale_order_quotation_reference(self):
        """Test sale order quotation reference"""
        sale_order = SaleOrder(**self.sale_order_data)
        
        # Test quotation reference
        sale_order.quotation_id = 1
        self.assertEqual(sale_order.quotation_id, 1)
    
    def test_sale_order_date_handling(self):
        """Test sale order date handling"""
        sale_order = SaleOrder(**self.sale_order_data)
        
        # Test order date
        self.assertEqual(sale_order.order_date, date.today().strftime('%Y-%m-%d'))
        
        # Test date change
        new_date = '2024-12-31'
        sale_order.order_date = new_date
        self.assertEqual(sale_order.order_date, new_date)
    
    def test_sale_order_line_product_variants(self):
        """Test sale order line product variants"""
        sale_order_line = SaleOrderLine(**self.sale_order_line_data)
        
        # Test size and color
        self.assertEqual(sale_order_line.size_id, 1)
        self.assertEqual(sale_order_line.color_id, 1)
        
        # Test variant changes
        sale_order_line.size_id = 2
        sale_order_line.color_id = 2
        self.assertEqual(sale_order_line.size_id, 2)
        self.assertEqual(sale_order_line.color_id, 2)
    
    def test_sale_order_line_tax_handling(self):
        """Test sale order line tax handling"""
        sale_order_line = SaleOrderLine(**self.sale_order_line_data)
        
        # Test tax assignment
        self.assertEqual(sale_order_line.tax_id, 1)
        
        # Test tax change
        sale_order_line.tax_id = 2
        self.assertEqual(sale_order_line.tax_id, 2)
    
    def test_sale_order_line_quantity_validation(self):
        """Test sale order line quantity validation"""
        sale_order_line = SaleOrderLine(**self.sale_order_line_data)
        
        # Test positive quantity
        self.assertGreater(sale_order_line.product_uom_qty, 0)
        
        # Test quantity change
        sale_order_line.product_uom_qty = 5.0
        self.assertEqual(sale_order_line.product_uom_qty, 5.0)
    
    def test_sale_order_line_price_validation(self):
        """Test sale order line price validation"""
        sale_order_line = SaleOrderLine(**self.sale_order_line_data)
        
        # Test positive price
        self.assertGreaterEqual(sale_order_line.price_unit, 0)
        
        # Test price change
        sale_order_line.price_unit = 150.0
        self.assertEqual(sale_order_line.price_unit, 150.0)
    
    def test_sale_order_line_subtotal_recalculation(self):
        """Test sale order line subtotal recalculation"""
        sale_order_line = SaleOrderLine(**self.sale_order_line_data)
        
        # Change quantity and price
        sale_order_line.product_uom_qty = 3.0
        sale_order_line.price_unit = 120.0
        
        # Recalculate subtotal
        sale_order_line._compute_price_subtotal()
        
        expected_subtotal = 3.0 * 120.0
        self.assertEqual(sale_order_line.price_subtotal, expected_subtotal)
    
    def test_sale_order_total_recalculation(self):
        """Test sale order total recalculation"""
        sale_order = SaleOrder(**self.sale_order_data)
        
        # Mock order lines with different subtotals
        line1 = Mock()
        line1.price_subtotal = 100.0
        
        line2 = Mock()
        line2.price_subtotal = 200.0
        
        line3 = Mock()
        line3.price_subtotal = 300.0
        
        sale_order.order_line_ids = [line1, line2, line3]
        
        # Recalculate total
        sale_order._compute_total_amount()
        
        expected_total = 100.0 + 200.0 + 300.0
        self.assertEqual(sale_order.total_amount, expected_total)
    
    def test_sale_order_empty_lines(self):
        """Test sale order with empty lines"""
        sale_order = SaleOrder(**self.sale_order_data)
        
        # Test with no lines
        sale_order.order_line_ids = []
        sale_order._compute_total_amount()
        
        self.assertEqual(sale_order.total_amount, 0.0)
    
    def test_sale_order_line_zero_quantity(self):
        """Test sale order line with zero quantity"""
        sale_order_line = SaleOrderLine(**self.sale_order_line_data)
        
        # Set quantity to zero
        sale_order_line.product_uom_qty = 0.0
        sale_order_line._compute_price_subtotal()
        
        self.assertEqual(sale_order_line.price_subtotal, 0.0)
    
    def test_sale_order_line_zero_price(self):
        """Test sale order line with zero price"""
        sale_order_line = SaleOrderLine(**self.sale_order_line_data)
        
        # Set price to zero
        sale_order_line.price_unit = 0.0
        sale_order_line._compute_price_subtotal()
        
        self.assertEqual(sale_order_line.price_subtotal, 0.0)
    
    def test_sale_order_line_negative_quantity(self):
        """Test sale order line with negative quantity"""
        sale_order_line = SaleOrderLine(**self.sale_order_line_data)
        
        # Set negative quantity
        sale_order_line.product_uom_qty = -1.0
        sale_order_line._compute_price_subtotal()
        
        # Should handle negative quantity gracefully
        self.assertEqual(sale_order_line.price_subtotal, -100.0)
    
    def test_sale_order_line_negative_price(self):
        """Test sale order line with negative price"""
        sale_order_line = SaleOrderLine(**self.sale_order_line_data)
        
        # Set negative price
        sale_order_line.price_unit = -50.0
        sale_order_line._compute_price_subtotal()
        
        # Should handle negative price gracefully
        self.assertEqual(sale_order_line.price_subtotal, -100.0)
    
    def test_sale_order_line_large_numbers(self):
        """Test sale order line with large numbers"""
        sale_order_line = SaleOrderLine(**self.sale_order_line_data)
        
        # Set large quantity and price
        sale_order_line.product_uom_qty = 1000.0
        sale_order_line.price_unit = 1000.0
        sale_order_line._compute_price_subtotal()
        
        expected_subtotal = 1000.0 * 1000.0
        self.assertEqual(sale_order_line.price_subtotal, expected_subtotal)
    
    def test_sale_order_line_decimal_precision(self):
        """Test sale order line decimal precision"""
        sale_order_line = SaleOrderLine(**self.sale_order_line_data)
        
        # Set decimal quantity and price
        sale_order_line.product_uom_qty = 2.5
        sale_order_line.price_unit = 99.99
        sale_order_line._compute_price_subtotal()
        
        expected_subtotal = 2.5 * 99.99
        self.assertAlmostEqual(sale_order_line.price_subtotal, expected_subtotal, places=2)
    
    def test_sale_order_line_unicode_support(self):
        """Test sale order line unicode support"""
        sale_order_line = SaleOrderLine(**self.sale_order_line_data)
        
        # Test unicode in product name (if applicable)
        # This would be tested in the actual implementation
        pass
    
    def test_sale_order_line_special_characters(self):
        """Test sale order line special characters"""
        sale_order_line = SaleOrderLine(**self.sale_order_line_data)
        
        # Test special characters in product description (if applicable)
        # This would be tested in the actual implementation
        pass
    
    def test_sale_order_line_encoding(self):
        """Test sale order line encoding"""
        sale_order_line = SaleOrderLine(**self.sale_order_line_data)
        
        # Test different encodings (if applicable)
        # This would be tested in the actual implementation
        pass


if __name__ == '__main__':
    unittest.main()