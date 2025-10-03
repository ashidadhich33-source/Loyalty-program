# -*- coding: utf-8 -*-

from core_framework.testing import TestCase
from core_framework.exceptions import ValidationError
from datetime import date, timedelta


class TestSystemUtils(TestCase):
    """Test cases for system.utils model"""
    
    def setUp(self):
        super(TestSystemUtils, self).setUp()
        self.utils = self.env['system.utils']
    
    def test_get_age_group_from_months(self):
        """Test age group calculation from months"""
        # Test newborn
        self.assertEqual(self.utils.get_age_group_from_months(3), 'newborn')
        self.assertEqual(self.utils.get_age_group_from_months(6), 'newborn')
        
        # Test infant
        self.assertEqual(self.utils.get_age_group_from_months(8), 'infant')
        self.assertEqual(self.utils.get_age_group_from_months(12), 'infant')
        
        # Test toddler
        self.assertEqual(self.utils.get_age_group_from_months(18), 'toddler')
        self.assertEqual(self.utils.get_age_group_from_months(36), 'toddler')
        
        # Test preschool
        self.assertEqual(self.utils.get_age_group_from_months(48), 'preschool')
        self.assertEqual(self.utils.get_age_group_from_months(60), 'preschool')
        
        # Test school
        self.assertEqual(self.utils.get_age_group_from_months(72), 'school')
        self.assertEqual(self.utils.get_age_group_from_months(144), 'school')
        
        # Test teen
        self.assertEqual(self.utils.get_age_group_from_months(150), 'teen')
        self.assertEqual(self.utils.get_age_group_from_months(216), 'teen')
    
    def test_get_age_group_from_birth_date(self):
        """Test age group calculation from birth date"""
        today = date.today()
        
        # Test newborn (3 months old)
        birth_date = today - timedelta(days=90)
        self.assertEqual(self.utils.get_age_group_from_birth_date(birth_date), 'newborn')
        
        # Test toddler (2 years old)
        birth_date = today - timedelta(days=730)
        self.assertEqual(self.utils.get_age_group_from_birth_date(birth_date), 'toddler')
        
        # Test school age (8 years old)
        birth_date = today - timedelta(days=2920)
        self.assertEqual(self.utils.get_age_group_from_birth_date(birth_date), 'school')
    
    def test_calculate_age_in_months(self):
        """Test age calculation in months"""
        today = date.today()
        
        # Test 6 months old
        birth_date = today - timedelta(days=180)
        age_months = self.utils.calculate_age_in_months(birth_date)
        self.assertGreaterEqual(age_months, 5)
        self.assertLessEqual(age_months, 7)
        
        # Test 2 years old
        birth_date = today - timedelta(days=730)
        age_months = self.utils.calculate_age_in_months(birth_date)
        self.assertGreaterEqual(age_months, 23)
        self.assertLessEqual(age_months, 25)
    
    def test_get_season_from_date(self):
        """Test season calculation from date"""
        # Test summer (April)
        summer_date = date(2024, 4, 15)
        self.assertEqual(self.utils.get_season_from_date(summer_date), 'summer')
        
        # Test monsoon (July)
        monsoon_date = date(2024, 7, 15)
        self.assertEqual(self.utils.get_season_from_date(monsoon_date), 'monsoon')
        
        # Test winter (December)
        winter_date = date(2024, 12, 15)
        self.assertEqual(self.utils.get_season_from_date(winter_date), 'winter')
    
    def test_get_size_recommendation(self):
        """Test size recommendation based on age and gender"""
        # Test newborn
        size = self.utils.get_size_recommendation(3, 'unisex')
        self.assertEqual(size, 'XS')
        
        # Test toddler
        size = self.utils.get_size_recommendation(24, 'boys')
        self.assertEqual(size, 'M')
        
        # Test school age
        size = self.utils.get_size_recommendation(96, 'girls')
        self.assertEqual(size, 'XL')
    
    def test_validate_gst_number(self):
        """Test GST number validation"""
        # Valid GST number
        valid_gst = "07AABCU9603R1ZX"
        self.assertTrue(self.utils.validate_gst_number(valid_gst))
        
        # Invalid GST number (wrong length)
        invalid_gst = "07AABCU9603R1Z"
        self.assertFalse(self.utils.validate_gst_number(invalid_gst))
        
        # Invalid GST number (wrong format)
        invalid_gst = "07AABCU9603R1Z1"
        self.assertFalse(self.utils.validate_gst_number(invalid_gst))
    
    def test_validate_pan_number(self):
        """Test PAN number validation"""
        # Valid PAN number
        valid_pan = "ABCDE1234F"
        self.assertTrue(self.utils.validate_pan_number(valid_pan))
        
        # Invalid PAN number (wrong length)
        invalid_pan = "ABCDE1234"
        self.assertFalse(self.utils.validate_pan_number(invalid_pan))
        
        # Invalid PAN number (wrong format)
        invalid_pan = "ABCD1234F"
        self.assertFalse(self.utils.validate_pan_number(invalid_pan))
    
    def test_validate_mobile_number(self):
        """Test mobile number validation"""
        # Valid mobile numbers
        valid_mobiles = ["9876543210", "8765432109", "7654321098", "6543210987"]
        for mobile in valid_mobiles:
            self.assertTrue(self.utils.validate_mobile_number(mobile))
        
        # Invalid mobile numbers
        invalid_mobiles = ["1234567890", "987654321", "98765432101", "987654321a"]
        for mobile in invalid_mobiles:
            self.assertFalse(self.utils.validate_mobile_number(mobile))
    
    def test_format_mobile_number(self):
        """Test mobile number formatting"""
        # Test 10 digit number
        formatted = self.utils.format_mobile_number("9876543210")
        self.assertEqual(formatted, "+919876543210")
        
        # Test already formatted number
        formatted = self.utils.format_mobile_number("+919876543210")
        self.assertEqual(formatted, "+919876543210")
        
        # Test number with 91 prefix
        formatted = self.utils.format_mobile_number("919876543210")
        self.assertEqual(formatted, "+919876543210")
    
    def test_get_currency_symbol(self):
        """Test currency symbol retrieval"""
        self.assertEqual(self.utils.get_currency_symbol('INR'), '₹')
        self.assertEqual(self.utils.get_currency_symbol('USD'), '$')
        self.assertEqual(self.utils.get_currency_symbol('EUR'), '€')
        self.assertEqual(self.utils.get_currency_symbol('GBP'), '£')
        self.assertEqual(self.utils.get_currency_symbol('JPY'), '¥')
        self.assertEqual(self.utils.get_currency_symbol('XYZ'), 'XYZ')
    
    def test_format_currency(self):
        """Test currency formatting"""
        formatted = self.utils.format_currency(1234.56, 'INR')
        self.assertEqual(formatted, '₹ 1,234.56')
        
        formatted = self.utils.format_currency(1234.56, 'USD')
        self.assertEqual(formatted, '$ 1,234.56')
    
    def test_calculate_discount(self):
        """Test discount calculation"""
        result = self.utils.calculate_discount(1000, 10)
        
        self.assertEqual(result['original_price'], 1000)
        self.assertEqual(result['discount_percent'], 10)
        self.assertEqual(result['discount_amount'], 100)
        self.assertEqual(result['final_price'], 900)
    
    def test_calculate_age_based_discount(self):
        """Test age-based discount calculation"""
        # Test newborn discount
        discount = self.utils.calculate_age_based_discount(3, 5)
        self.assertEqual(discount, 20)  # 5% base + 15% newborn = 20%
        
        # Test toddler discount
        discount = self.utils.calculate_age_based_discount(24, 5)
        self.assertEqual(discount, 10)  # 5% base + 5% toddler = 10%
        
        # Test school age (no additional discount)
        discount = self.utils.calculate_age_based_discount(96, 5)
        self.assertEqual(discount, 5)  # 5% base + 0% school = 5%
        
        # Test maximum discount limit
        discount = self.utils.calculate_age_based_discount(3, 40)
        self.assertEqual(discount, 50)  # Capped at 50%
    
    def test_generate_loyalty_points(self):
        """Test loyalty points generation"""
        points = self.utils.generate_loyalty_points(1000, 1)
        self.assertEqual(points, 1000)
        
        points = self.utils.generate_loyalty_points(1000, 2)
        self.assertEqual(points, 2000)
    
    def test_calculate_loyalty_discount(self):
        """Test loyalty discount calculation"""
        discount = self.utils.calculate_loyalty_discount(1000, 1)
        self.assertEqual(discount, 1000)
        
        discount = self.utils.calculate_loyalty_discount(1000, 2)
        self.assertEqual(discount, 500)
    
    def test_get_stock_status(self):
        """Test stock status calculation"""
        # Out of stock
        status = self.utils.get_stock_status(0)
        self.assertEqual(status, 'out_of_stock')
        
        # Low stock
        status = self.utils.get_stock_status(5, 10)
        self.assertEqual(status, 'low_stock')
        
        # In stock
        status = self.utils.get_stock_status(15, 10)
        self.assertEqual(status, 'in_stock')