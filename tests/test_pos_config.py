# -*- coding: utf-8 -*-

from odoo.tests.common import TransactionCase


class TestPosConfig(TransactionCase):
    """Test cases for pos.config model with kids clothing specific fields"""

    def setUp(self):
        super().setUp()
        self.pos_config_model = self.env['pos.config']
        self.pos_config = self.pos_config_model.create({
            'name': 'Kids Clothing POS',
            'enable_loyalty_program': True,
            'loyalty_points_per_currency': 1.5,
            'enable_gift_wrapping': True,
            'gift_wrap_price': 5.0,
            'enable_exchange_return': True,
            'exchange_return_days': 30,
            'require_age_verification': False,
            'enable_size_recommendation': True,
            'enable_seasonal_promotions': True,
            'enable_multi_payment': True,
            'collect_child_info': True,
            'receipt_template': 'kids_friendly',
            'enable_barcode_scanning': True,
            'enable_product_recommendations': True,
        })

    def test_pos_config_creation(self):
        """Test creation of POS configuration"""
        self.assertEqual(self.pos_config.name, 'Kids Clothing POS')
        self.assertTrue(self.pos_config.enable_loyalty_program)
        self.assertEqual(self.pos_config.loyalty_points_per_currency, 1.5)
        self.assertTrue(self.pos_config.enable_gift_wrapping)
        self.assertEqual(self.pos_config.gift_wrap_price, 5.0)
        self.assertTrue(self.pos_config.enable_exchange_return)
        self.assertEqual(self.pos_config.exchange_return_days, 30)
        self.assertFalse(self.pos_config.require_age_verification)
        self.assertTrue(self.pos_config.enable_size_recommendation)
        self.assertTrue(self.pos_config.enable_seasonal_promotions)
        self.assertTrue(self.pos_config.enable_multi_payment)
        self.assertTrue(self.pos_config.collect_child_info)
        self.assertEqual(self.pos_config.receipt_template, 'kids_friendly')
        self.assertTrue(self.pos_config.enable_barcode_scanning)
        self.assertTrue(self.pos_config.enable_product_recommendations)

    def test_get_kids_clothing_config(self):
        """Test get_kids_clothing_config method"""
        config = self.pos_config.get_kids_clothing_config()
        
        expected_config = {
            'loyalty_program': True,
            'loyalty_points_rate': 1.5,
            'gift_wrapping': True,
            'gift_wrap_price': 5.0,
            'exchange_return': True,
            'exchange_return_days': 30,
            'age_verification': False,
            'size_recommendation': True,
            'seasonal_promotions': True,
            'multi_payment': True,
            'child_info': True,
            'receipt_template': 'kids_friendly',
            'barcode_scanning': True,
            'product_recommendations': True,
        }
        
        self.assertEqual(config, expected_config)

    def test_loyalty_program_configuration(self):
        """Test loyalty program configuration"""
        self.assertTrue(self.pos_config.enable_loyalty_program)
        self.assertEqual(self.pos_config.loyalty_points_per_currency, 1.5)

    def test_gift_wrapping_configuration(self):
        """Test gift wrapping configuration"""
        self.assertTrue(self.pos_config.enable_gift_wrapping)
        self.assertEqual(self.pos_config.gift_wrap_price, 5.0)

    def test_exchange_return_configuration(self):
        """Test exchange/return configuration"""
        self.assertTrue(self.pos_config.enable_exchange_return)
        self.assertEqual(self.pos_config.exchange_return_days, 30)

    def test_age_verification_configuration(self):
        """Test age verification configuration"""
        self.assertFalse(self.pos_config.require_age_verification)

    def test_size_recommendation_configuration(self):
        """Test size recommendation configuration"""
        self.assertTrue(self.pos_config.enable_size_recommendation)

    def test_seasonal_promotions_configuration(self):
        """Test seasonal promotions configuration"""
        self.assertTrue(self.pos_config.enable_seasonal_promotions)

    def test_multi_payment_configuration(self):
        """Test multi-payment configuration"""
        self.assertTrue(self.pos_config.enable_multi_payment)

    def test_child_info_collection_configuration(self):
        """Test child info collection configuration"""
        self.assertTrue(self.pos_config.collect_child_info)

    def test_receipt_template_configuration(self):
        """Test receipt template configuration"""
        self.assertEqual(self.pos_config.receipt_template, 'kids_friendly')

    def test_barcode_scanning_configuration(self):
        """Test barcode scanning configuration"""
        self.assertTrue(self.pos_config.enable_barcode_scanning)

    def test_product_recommendations_configuration(self):
        """Test product recommendations configuration"""
        self.assertTrue(self.pos_config.enable_product_recommendations)

    def test_receipt_template_options(self):
        """Test receipt template options"""
        valid_templates = ['standard', 'kids_friendly', 'gift_receipt']
        for template in valid_templates:
            config = self.pos_config_model.create({
                'name': f'Test POS {template}',
                'receipt_template': template,
            })
            self.assertEqual(config.receipt_template, template)

    def test_loyalty_points_per_currency_validation(self):
        """Test loyalty points per currency validation"""
        # Test positive values
        self.pos_config.loyalty_points_per_currency = 2.0
        self.assertEqual(self.pos_config.loyalty_points_per_currency, 2.0)
        
        # Test zero value
        self.pos_config.loyalty_points_per_currency = 0.0
        self.assertEqual(self.pos_config.loyalty_points_per_currency, 0.0)

    def test_gift_wrap_price_validation(self):
        """Test gift wrap price validation"""
        # Test positive values
        self.pos_config.gift_wrap_price = 10.0
        self.assertEqual(self.pos_config.gift_wrap_price, 10.0)
        
        # Test zero value
        self.pos_config.gift_wrap_price = 0.0
        self.assertEqual(self.pos_config.gift_wrap_price, 0.0)

    def test_exchange_return_days_validation(self):
        """Test exchange return days validation"""
        # Test positive values
        self.pos_config.exchange_return_days = 60
        self.assertEqual(self.pos_config.exchange_return_days, 60)
        
        # Test zero value
        self.pos_config.exchange_return_days = 0
        self.assertEqual(self.pos_config.exchange_return_days, 0)