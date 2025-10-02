# -*- coding: utf-8 -*-

from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError


class TestSaleOrder(TransactionCase):
    """Test cases for Sale Order model"""

    def setUp(self):
        super().setUp()
        self.partner = self.env['res.partner'].create({
            'name': 'Test Customer',
            'is_company': False,
        })
        self.product = self.env['product.product'].create({
            'name': 'Test Product',
            'type': 'product',
            'age_group': '4-6',
            'gender': 'boys',
            'season': 'summer',
        })
        self.sale_order = self.env['sale.order'].create({
            'partner_id': self.partner.id,
            'age_group': '4-6',
            'gender': 'boys',
            'season': 'summer',
        })

    def test_sale_order_creation(self):
        """Test sale order creation"""
        self.assertEqual(self.sale_order.partner_id, self.partner)
        self.assertEqual(self.sale_order.age_group, '4-6')
        self.assertEqual(self.sale_order.gender, 'boys')
        self.assertEqual(self.sale_order.season, 'summer')
        self.assertEqual(self.sale_order.state, 'draft')

    def test_sale_order_line_creation(self):
        """Test sale order line creation"""
        order_line = self.env['sale.order.line'].create({
            'order_id': self.sale_order.id,
            'product_id': self.product.id,
            'product_uom_qty': 2.0,
            'price_unit': 100.0,
        })
        self.assertEqual(order_line.order_id, self.sale_order)
        self.assertEqual(order_line.product_id, self.product)
        self.assertEqual(order_line.product_uom_qty, 2.0)
        self.assertEqual(order_line.price_unit, 100.0)

    def test_sale_order_amount_calculation(self):
        """Test sale order amount calculation"""
        self.env['sale.order.line'].create({
            'order_id': self.sale_order.id,
            'product_id': self.product.id,
            'product_uom_qty': 2.0,
            'price_unit': 100.0,
        })
        self.sale_order._compute_amount()
        self.assertEqual(self.sale_order.amount_untaxed, 200.0)

    def test_sale_order_kids_items_calculation(self):
        """Test sale order kids items calculation"""
        self.env['sale.order.line'].create({
            'order_id': self.sale_order.id,
            'product_id': self.product.id,
            'product_uom_qty': 2.0,
            'price_unit': 100.0,
        })
        self.sale_order._compute_kids_items()
        self.assertEqual(self.sale_order.total_kids_items, 2)

    def test_sale_order_age_group_distribution(self):
        """Test sale order age group distribution"""
        self.env['sale.order.line'].create({
            'order_id': self.sale_order.id,
            'product_id': self.product.id,
            'product_uom_qty': 2.0,
            'price_unit': 100.0,
        })
        self.sale_order._compute_age_group_distribution()
        self.assertIn('4-6', self.sale_order.age_group_distribution)

    def test_sale_order_gender_distribution(self):
        """Test sale order gender distribution"""
        self.env['sale.order.line'].create({
            'order_id': self.sale_order.id,
            'product_id': self.product.id,
            'product_uom_qty': 2.0,
            'price_unit': 100.0,
        })
        self.sale_order._compute_gender_distribution()
        self.assertIn('boys', self.sale_order.gender_distribution)

    def test_sale_order_season_distribution(self):
        """Test sale order season distribution"""
        self.env['sale.order.line'].create({
            'order_id': self.sale_order.id,
            'product_id': self.product.id,
            'product_uom_qty': 2.0,
            'price_unit': 100.0,
        })
        self.sale_order._compute_season_distribution()
        self.assertIn('summer', self.sale_order.season_distribution)

    def test_sale_order_quotation_send(self):
        """Test sale order quotation send"""
        self.sale_order.action_quotation_send()
        self.assertEqual(self.sale_order.state, 'sent')

    def test_sale_order_confirm(self):
        """Test sale order confirm"""
        self.sale_order.action_confirm()
        self.assertEqual(self.sale_order.state, 'sale')

    def test_sale_order_done(self):
        """Test sale order done"""
        self.sale_order.state = 'sale'
        self.sale_order.action_done()
        self.assertEqual(self.sale_order.state, 'done')

    def test_sale_order_cancel(self):
        """Test sale order cancel"""
        self.sale_order.action_cancel()
        self.assertEqual(self.sale_order.state, 'cancel')

    def test_sale_order_delivery_count(self):
        """Test sale order delivery count"""
        delivery = self.env['sale.delivery'].create({
            'order_id': self.sale_order.id,
            'date_delivery': '2024-01-01 10:00:00',
        })
        self.sale_order._compute_delivery_count()
        self.assertEqual(self.sale_order.delivery_count, 1)

    def test_sale_order_return_count(self):
        """Test sale order return count"""
        return_order = self.env['sale.return'].create({
            'order_id': self.sale_order.id,
            'date_return': '2024-01-01 10:00:00',
            'return_reason': 'defective',
        })
        self.sale_order._compute_return_count()
        self.assertEqual(self.sale_order.return_count, 1)

    def test_sale_order_sequence_generation(self):
        """Test sale order sequence generation"""
        order = self.env['sale.order'].create({
            'partner_id': self.partner.id,
        })
        self.assertTrue(order.name)
        self.assertNotEqual(order.name, 'New')

    def test_sale_order_multi_company(self):
        """Test sale order multi-company support"""
        company2 = self.env['res.company'].create({
            'name': 'Test Company 2',
        })
        order = self.env['sale.order'].create({
            'partner_id': self.partner.id,
            'company_id': company2.id,
        })
        self.assertEqual(order.company_id, company2)

    def test_sale_order_line_display_name(self):
        """Test sale order line display name"""
        order_line = self.env['sale.order.line'].create({
            'order_id': self.sale_order.id,
            'product_id': self.product.id,
            'product_uom_qty': 2.0,
        })
        order_line._compute_display_name()
        self.assertIn(self.product.name, order_line.display_name)
        self.assertIn('2.0', order_line.display_name)

    def test_sale_order_line_amount_calculation(self):
        """Test sale order line amount calculation"""
        order_line = self.env['sale.order.line'].create({
            'order_id': self.sale_order.id,
            'product_id': self.product.id,
            'product_uom_qty': 2.0,
            'price_unit': 100.0,
            'discount': 10.0,
        })
        order_line._compute_amount()
        self.assertEqual(order_line.price_subtotal, 180.0)

    def test_sale_order_line_kids_item(self):
        """Test sale order line kids item"""
        order_line = self.env['sale.order.line'].create({
            'order_id': self.sale_order.id,
            'product_id': self.product.id,
            'product_uom_qty': 2.0,
        })
        order_line._compute_is_kids_item()
        self.assertTrue(order_line.is_kids_item)

    def test_sale_order_line_product_onchange(self):
        """Test sale order line product onchange"""
        order_line = self.env['sale.order.line'].new({
            'order_id': self.sale_order.id,
            'product_id': self.product.id,
        })
        order_line._onchange_product_id()
        self.assertEqual(order_line.product_uom, self.product.uom_id)
        self.assertEqual(order_line.price_unit, self.product.list_price)