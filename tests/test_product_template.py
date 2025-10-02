# -*- coding: utf-8 -*-

from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError


class TestProductTemplate(TransactionCase):
    """Test cases for product.template model with kids clothing specific fields"""

    def setUp(self):
        super().setUp()
        self.product_model = self.env['product.template']
        self.kids_product = self.product_model.create({
            'name': 'Kids T-Shirt',
            'is_kids_clothing': True,
            'age_range': '2-4 years',
            'gender': 'unisex',
            'season': 'summer',
            'clothing_type': 'shirt',
            'brand': 'KidsBrand',
            'material': '100% Cotton',
            'care_instructions': 'Machine wash cold, tumble dry low',
            'safety_certification': 'CPSC',
            'choking_hazard': False,
            'min_stock_level': 10.0,
            'reorder_qty': 50.0,
            'wholesale_price': 5.0,
            'retail_price': 15.0,
        })

    def test_kids_clothing_product_creation(self):
        """Test creation of kids clothing product"""
        self.assertTrue(self.kids_product.is_kids_clothing)
        self.assertEqual(self.kids_product.age_range, '2-4 years')
        self.assertEqual(self.kids_product.gender, 'unisex')
        self.assertEqual(self.kids_product.season, 'summer')
        self.assertEqual(self.kids_product.clothing_type, 'shirt')
        self.assertEqual(self.kids_product.brand, 'KidsBrand')
        self.assertEqual(self.kids_product.material, '100% Cotton')
        self.assertEqual(self.kids_product.care_instructions, 'Machine wash cold, tumble dry low')
        self.assertEqual(self.kids_product.safety_certification, 'CPSC')
        self.assertFalse(self.kids_product.choking_hazard)

    def test_product_defaults(self):
        """Test default values for kids clothing products"""
        self.assertEqual(self.kids_product.type, 'product')
        self.assertTrue(self.kids_product.sale_ok)
        self.assertTrue(self.kids_product.purchase_ok)

    def test_size_variants(self):
        """Test size variants creation"""
        size_variant = self.env['product.template.size.variant'].create({
            'product_tmpl_id': self.kids_product.id,
            'size': 'M',
            'age_range': '2-3 years',
            'chest_measurement': 20.0,
            'waist_measurement': 18.0,
            'length_measurement': 22.0,
        })
        
        self.assertEqual(size_variant.product_tmpl_id, self.kids_product)
        self.assertEqual(size_variant.size, 'M')
        self.assertEqual(size_variant.age_range, '2-3 years')
        self.assertEqual(size_variant.chest_measurement, 20.0)

    def test_color_variants(self):
        """Test color variants creation"""
        color_variant = self.env['product.template.color.variant'].create({
            'product_tmpl_id': self.kids_product.id,
            'color_name': 'Blue',
            'color_code': '#0000FF',
        })
        
        self.assertEqual(color_variant.product_tmpl_id, self.kids_product)
        self.assertEqual(color_variant.color_name, 'Blue')
        self.assertEqual(color_variant.color_code, '#0000FF')

    def test_product_attributes(self):
        """Test product attributes creation"""
        attribute = self.env['product.template.attribute'].create({
            'product_tmpl_id': self.kids_product.id,
            'attribute_name': 'Pattern',
            'attribute_value': 'Striped',
        })
        
        self.assertEqual(attribute.product_tmpl_id, self.kids_product)
        self.assertEqual(attribute.attribute_name, 'Pattern')
        self.assertEqual(attribute.attribute_value, 'Striped')

    def test_inventory_management(self):
        """Test inventory management fields"""
        self.assertEqual(self.kids_product.min_stock_level, 10.0)
        self.assertEqual(self.kids_product.reorder_qty, 50.0)

    def test_pricing(self):
        """Test pricing fields"""
        self.assertEqual(self.kids_product.wholesale_price, 5.0)
        self.assertEqual(self.kids_product.retail_price, 15.0)

    def test_safety_information(self):
        """Test safety information fields"""
        self.assertEqual(self.kids_product.safety_certification, 'CPSC')
        self.assertFalse(self.kids_product.choking_hazard)

    def test_gender_selection(self):
        """Test gender selection options"""
        valid_genders = ['unisex', 'boys', 'girls']
        for gender in valid_genders:
            product = self.product_model.create({
                'name': f'Test Product {gender}',
                'is_kids_clothing': True,
                'gender': gender,
            })
            self.assertEqual(product.gender, gender)

    def test_season_selection(self):
        """Test season selection options"""
        valid_seasons = ['spring', 'summer', 'fall', 'winter', 'all_season']
        for season in valid_seasons:
            product = self.product_model.create({
                'name': f'Test Product {season}',
                'is_kids_clothing': True,
                'season': season,
            })
            self.assertEqual(product.season, season)

    def test_clothing_type_selection(self):
        """Test clothing type selection options"""
        valid_types = ['shirt', 'pants', 'dress', 'shorts', 'jacket', 'sweater', 'shoes', 'accessories']
        for clothing_type in valid_types:
            product = self.product_model.create({
                'name': f'Test Product {clothing_type}',
                'is_kids_clothing': True,
                'clothing_type': clothing_type,
            })
            self.assertEqual(product.clothing_type, clothing_type)

    def test_stock_level_validation(self):
        """Test stock level validation"""
        with self.assertRaises(ValidationError):
            self.product_model.create({
                'name': 'Invalid Product',
                'is_kids_clothing': True,
                'min_stock_level': -1,  # Negative stock level should raise error
            })

    def test_reorder_quantity_validation(self):
        """Test reorder quantity validation"""
        with self.assertRaises(ValidationError):
            self.product_model.create({
                'name': 'Invalid Product',
                'is_kids_clothing': True,
                'reorder_qty': -1,  # Negative reorder quantity should raise error
            })

    def test_price_validation(self):
        """Test price validation"""
        with self.assertRaises(ValidationError):
            self.product_model.create({
                'name': 'Invalid Product',
                'is_kids_clothing': True,
                'wholesale_price': -1,  # Negative price should raise error
            })

    def test_action_view_stock(self):
        """Test action to view product stock levels"""
        action = self.kids_product.action_view_stock()
        self.assertEqual(action['res_model'], 'stock.quant')
        self.assertIn('product_tmpl_id', action['domain'][0])