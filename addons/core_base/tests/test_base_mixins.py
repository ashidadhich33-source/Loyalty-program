# -*- coding: utf-8 -*-

from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError


class TestKidsClothingMixin(TransactionCase):
    """Test cases for kids.clothing.mixin model"""
    
    def setUp(self):
        super(TestKidsClothingMixin, self).setUp()
        self.user = self.env.user
        self.company = self.env['res.company'].create({
            'name': 'Test Company',
            'currency_id': self.env.ref('base.INR').id,
        })
    
    def test_mixin_creation(self):
        """Test mixin creation with default values"""
        # This test would require a concrete model that inherits from the mixin
        # For now, we'll test the mixin methods directly
        pass
    
    def test_created_by_default(self):
        """Test that created_by is set to current user by default"""
        # This would be tested with a concrete model
        pass
    
    def test_created_date_default(self):
        """Test that created_date is set to current datetime by default"""
        # This would be tested with a concrete model
        pass
    
    def test_updated_by_on_write(self):
        """Test that updated_by is set on write"""
        # This would be tested with a concrete model
        pass
    
    def test_updated_date_on_write(self):
        """Test that updated_date is set on write"""
        # This would be tested with a concrete model
        pass


class TestAgeGroupMixin(TransactionCase):
    """Test cases for age.group.mixin model"""
    
    def setUp(self):
        super(TestAgeGroupMixin, self).setUp()
        self.mixin = self.env['age.group.mixin']
    
    def test_age_group_selection(self):
        """Test age group selection options"""
        # Test that all age groups are available
        age_groups = [option[0] for option in self.mixin._fields['age_group'].selection]
        
        expected_groups = ['newborn', 'infant', 'toddler', 'preschool', 'school', 'teen']
        for group in expected_groups:
            self.assertIn(group, age_groups)
    
    def test_onchange_age_group(self):
        """Test age group onchange method"""
        # Test newborn
        self.mixin.age_group = 'newborn'
        self.mixin._onchange_age_group()
        self.assertEqual(self.mixin.min_age, 0)
        self.assertEqual(self.mixin.max_age, 6)
        
        # Test infant
        self.mixin.age_group = 'infant'
        self.mixin._onchange_age_group()
        self.assertEqual(self.mixin.min_age, 6)
        self.assertEqual(self.mixin.max_age, 12)
        
        # Test toddler
        self.mixin.age_group = 'toddler'
        self.mixin._onchange_age_group()
        self.assertEqual(self.mixin.min_age, 12)
        self.assertEqual(self.mixin.max_age, 36)
        
        # Test preschool
        self.mixin.age_group = 'preschool'
        self.mixin._onchange_age_group()
        self.assertEqual(self.mixin.min_age, 36)
        self.assertEqual(self.mixin.max_age, 60)
        
        # Test school
        self.mixin.age_group = 'school'
        self.mixin._onchange_age_group()
        self.assertEqual(self.mixin.min_age, 60)
        self.assertEqual(self.mixin.max_age, 144)
        
        # Test teen
        self.mixin.age_group = 'teen'
        self.mixin._onchange_age_group()
        self.assertEqual(self.mixin.min_age, 144)
        self.assertEqual(self.mixin.max_age, 216)
    
    def test_check_age_range_constraint(self):
        """Test age range constraint validation"""
        # Test valid range
        self.mixin.min_age = 12
        self.mixin.max_age = 36
        self.mixin._check_age_range()  # Should not raise exception
        
        # Test invalid range (min >= max)
        self.mixin.min_age = 36
        self.mixin.max_age = 12
        with self.assertRaises(ValidationError):
            self.mixin._check_age_range()


class TestGenderMixin(TransactionCase):
    """Test cases for gender.mixin model"""
    
    def setUp(self):
        super(TestGenderMixin, self).setUp()
        self.mixin = self.env['gender.mixin']
    
    def test_gender_selection(self):
        """Test gender selection options"""
        genders = [option[0] for option in self.mixin._fields['gender'].selection]
        
        expected_genders = ['unisex', 'boys', 'girls']
        for gender in expected_genders:
            self.assertIn(gender, genders)
    
    def test_gender_default(self):
        """Test gender default value"""
        self.assertEqual(self.mixin.gender, 'unisex')
    
    def test_check_gender_constraint(self):
        """Test gender constraint validation"""
        # Test valid gender
        self.mixin.gender = 'boys'
        self.mixin._check_gender()  # Should not raise exception
        
        # Test invalid gender (empty)
        self.mixin.gender = False
        with self.assertRaises(ValidationError):
            self.mixin._check_gender()


class TestSeasonMixin(TransactionCase):
    """Test cases for season.mixin model"""
    
    def setUp(self):
        super(TestSeasonMixin, self).setUp()
        self.mixin = self.env['season.mixin']
    
    def test_season_selection(self):
        """Test season selection options"""
        seasons = [option[0] for option in self.mixin._fields['season'].selection]
        
        expected_seasons = ['summer', 'winter', 'monsoon', 'all_season']
        for season in expected_seasons:
            self.assertIn(season, seasons)
    
    def test_season_default(self):
        """Test season default value"""
        self.assertEqual(self.mixin.season, 'all_season')
    
    def test_check_season_constraint(self):
        """Test season constraint validation"""
        # Test valid season
        self.mixin.season = 'summer'
        self.mixin._check_season()  # Should not raise exception
        
        # Test invalid season (empty)
        self.mixin.season = False
        with self.assertRaises(ValidationError):
            self.mixin._check_season()


class TestSizeMixin(TransactionCase):
    """Test cases for size.mixin model"""
    
    def setUp(self):
        super(TestSizeMixin, self).setUp()
        self.mixin = self.env['size.mixin']
    
    def test_size_selection(self):
        """Test size selection options"""
        sizes = [option[0] for option in self.mixin._fields['size'].selection]
        
        expected_sizes = ['xs', 's', 'm', 'l', 'xl', 'xxl', 'xxxl']
        for size in expected_sizes:
            self.assertIn(size, sizes)
    
    def test_size_type_selection(self):
        """Test size type selection options"""
        size_types = [option[0] for option in self.mixin._fields['size_type'].selection]
        
        expected_types = ['age', 'standard', 'custom']
        for size_type in expected_types:
            self.assertIn(size_type, size_types)
    
    def test_size_type_default(self):
        """Test size type default value"""
        self.assertEqual(self.mixin.size_type, 'age')
    
    def test_check_size_constraint(self):
        """Test size constraint validation"""
        # Test valid size for standard type
        self.mixin.size_type = 'standard'
        self.mixin.size = 'm'
        self.mixin._check_size()  # Should not raise exception
        
        # Test invalid size for standard type (empty)
        self.mixin.size_type = 'standard'
        self.mixin.size = False
        with self.assertRaises(ValidationError):
            self.mixin._check_size()


class TestColorMixin(TransactionCase):
    """Test cases for color.mixin model"""
    
    def setUp(self):
        super(TestColorMixin, self).setUp()
        self.mixin = self.env['color.mixin']
    
    def test_check_color_code_constraint(self):
        """Test color code constraint validation"""
        # Test valid color code
        self.mixin.color_code = '#FF0000'
        self.mixin._check_color_code()  # Should not raise exception
        
        # Test invalid color code (no # prefix)
        self.mixin.color_code = 'FF0000'
        with self.assertRaises(ValidationError):
            self.mixin._check_color_code()


class TestPriceMixin(TransactionCase):
    """Test cases for price.mixin model"""
    
    def setUp(self):
        super(TestPriceMixin, self).setUp()
        self.mixin = self.env['price.mixin']
    
    def test_compute_margin(self):
        """Test margin computation"""
        # Test with valid prices
        self.mixin.list_price = 1000
        self.mixin.cost_price = 800
        self.mixin._compute_margin()
        self.assertEqual(self.mixin.margin, 20.0)  # (1000-800)/1000 * 100 = 20%
        
        # Test with zero prices
        self.mixin.list_price = 0
        self.mixin.cost_price = 0
        self.mixin._compute_margin()
        self.assertEqual(self.mixin.margin, 0.0)
    
    def test_check_prices_constraint(self):
        """Test price constraint validation"""
        # Test valid prices
        self.mixin.list_price = 1000
        self.mixin.cost_price = 800
        self.mixin._check_prices()  # Should not raise exception
        
        # Test negative list price
        self.mixin.list_price = -100
        self.mixin.cost_price = 800
        with self.assertRaises(ValidationError):
            self.mixin._check_prices()
        
        # Test negative cost price
        self.mixin.list_price = 1000
        self.mixin.cost_price = -800
        with self.assertRaises(ValidationError):
            self.mixin._check_prices()
        
        # Test cost price higher than list price
        self.mixin.list_price = 800
        self.mixin.cost_price = 1000
        with self.assertRaises(ValidationError):
            self.mixin._check_prices()