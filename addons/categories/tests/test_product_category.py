# -*- coding: utf-8 -*-

from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)


class TestProductCategory(TransactionCase):
    """Test Product Category functionality"""
    
    def setUp(self):
        super(TestProductCategory, self).setUp()
        self.category_model = self.env['product.category']
        self.partner_model = self.env['res.partner']
        self.company_model = self.env['res.company']
        
        # Create test company
        self.test_company = self.company_model.create({
            'name': 'Test Company',
            'currency_id': self.env.ref('base.USD').id,
        })
        
        # Create test partner
        self.test_partner = self.partner_model.create({
            'name': 'Test Partner',
            'company_id': self.test_company.id,
        })
    
    def test_create_category(self):
        """Test creating a product category"""
        category = self.category_model.create({
            'name': 'Test Category',
            'age_group': '2-4',
            'gender': 'unisex',
            'season': 'all_season',
            'brand_type': 'all',
            'style_type': 'casual',
            'color_family': 'all',
            'size_range': 'all',
            'description': 'Test category description',
            'default_margin': 30.0,
            'min_margin': 20.0,
            'max_margin': 40.0,
            'company_id': self.test_company.id,
        })
        
        self.assertEqual(category.name, 'Test Category')
        self.assertEqual(category.age_group, '2-4')
        self.assertEqual(category.gender, 'unisex')
        self.assertEqual(category.season, 'all_season')
        self.assertEqual(category.brand_type, 'all')
        self.assertEqual(category.style_type, 'casual')
        self.assertEqual(category.color_family, 'all')
        self.assertEqual(category.size_range, 'all')
        self.assertEqual(category.description, 'Test category description')
        self.assertEqual(category.default_margin, 30.0)
        self.assertEqual(category.min_margin, 20.0)
        self.assertEqual(category.max_margin, 40.0)
        self.assertEqual(category.company_id, self.test_company)
    
    def test_category_hierarchy(self):
        """Test category hierarchy functionality"""
        # Create parent category
        parent_category = self.category_model.create({
            'name': 'Parent Category',
            'age_group': '0-2',
            'gender': 'unisex',
            'season': 'all_season',
            'brand_type': 'all',
            'style_type': 'all',
            'color_family': 'all',
            'size_range': 'all',
            'company_id': self.test_company.id,
        })
        
        # Create child category
        child_category = self.category_model.create({
            'name': 'Child Category',
            'parent_id': parent_category.id,
            'age_group': '0-2',
            'gender': 'boys',
            'season': 'all_season',
            'brand_type': 'all',
            'style_type': 'all',
            'color_family': 'all',
            'size_range': 'all',
            'company_id': self.test_company.id,
        })
        
        self.assertEqual(child_category.parent_id, parent_category)
        self.assertIn(child_category, parent_category.child_id)
        self.assertEqual(child_category.complete_name, 'Parent Category / Child Category')
    
    def test_category_validation(self):
        """Test category validation rules"""
        # Test age range validation
        with self.assertRaises(ValidationError):
            self.category_model.create({
                'name': 'Invalid Age Category',
                'min_age_months': 24,
                'max_age_months': 12,  # Invalid: min > max
                'age_group': '2-4',
                'gender': 'unisex',
                'season': 'all_season',
                'brand_type': 'all',
                'style_type': 'all',
                'color_family': 'all',
                'size_range': 'all',
                'company_id': self.test_company.id,
            })
        
        # Test height range validation
        with self.assertRaises(ValidationError):
            self.category_model.create({
                'name': 'Invalid Height Category',
                'min_height_cm': 100,
                'max_height_cm': 80,  # Invalid: min > max
                'age_group': '2-4',
                'gender': 'unisex',
                'season': 'all_season',
                'brand_type': 'all',
                'style_type': 'all',
                'color_family': 'all',
                'size_range': 'all',
                'company_id': self.test_company.id,
            })
        
        # Test weight range validation
        with self.assertRaises(ValidationError):
            self.category_model.create({
                'name': 'Invalid Weight Category',
                'min_weight_kg': 20,
                'max_weight_kg': 15,  # Invalid: min > max
                'age_group': '2-4',
                'gender': 'unisex',
                'season': 'all_season',
                'brand_type': 'all',
                'style_type': 'all',
                'color_family': 'all',
                'size_range': 'all',
                'company_id': self.test_company.id,
            })
        
        # Test margin range validation
        with self.assertRaises(ValidationError):
            self.category_model.create({
                'name': 'Invalid Margin Category',
                'min_margin': 40,
                'max_margin': 30,  # Invalid: min > max
                'age_group': '2-4',
                'gender': 'unisex',
                'season': 'all_season',
                'brand_type': 'all',
                'style_type': 'all',
                'color_family': 'all',
                'size_range': 'all',
                'company_id': self.test_company.id,
            })
    
    def test_category_methods(self):
        """Test category methods"""
        # Create test category
        category = self.category_model.create({
            'name': 'Test Category',
            'age_group': '2-4',
            'gender': 'unisex',
            'season': 'all_season',
            'brand_type': 'all',
            'style_type': 'all',
            'color_family': 'all',
            'size_range': 'all',
            'company_id': self.test_company.id,
        })
        
        # Test name_get
        name_get_result = category.name_get()
        self.assertEqual(name_get_result[0][1], 'Test Category')
        
        # Test name_search
        search_result = self.category_model.name_search('Test')
        self.assertGreater(len(search_result), 0)
        
        # Test get_category_path
        path = category.get_category_path()
        self.assertEqual(path, 'Test Category')
        
        # Test get_children_recursive
        children = category.get_children_recursive()
        self.assertEqual(len(children), 0)
        
        # Test get_parents
        parents = category.get_parents()
        self.assertEqual(len(parents), 0)
        
        # Test is_child_of
        is_child = category.is_child_of(category)
        self.assertFalse(is_child)
        
        # Test get_siblings
        siblings = category.get_siblings()
        self.assertEqual(len(siblings), 0)
    
    def test_category_archive_unarchive(self):
        """Test category archive/unarchive functionality"""
        category = self.category_model.create({
            'name': 'Test Category',
            'age_group': '2-4',
            'gender': 'unisex',
            'season': 'all_season',
            'brand_type': 'all',
            'style_type': 'all',
            'color_family': 'all',
            'size_range': 'all',
            'company_id': self.test_company.id,
        })
        
        # Test archive
        category.archive()
        self.assertFalse(category.active)
        
        # Test unarchive
        category.unarchive()
        self.assertTrue(category.active)
    
    def test_category_duplicate(self):
        """Test category duplication"""
        original_category = self.category_model.create({
            'name': 'Original Category',
            'age_group': '2-4',
            'gender': 'unisex',
            'season': 'all_season',
            'brand_type': 'all',
            'style_type': 'all',
            'color_family': 'all',
            'size_range': 'all',
            'description': 'Original description',
            'default_margin': 30.0,
            'min_margin': 20.0,
            'max_margin': 40.0,
            'company_id': self.test_company.id,
        })
        
        # Duplicate category
        duplicated_category = original_category.duplicate()
        
        self.assertEqual(duplicated_category.name, 'Original Category (Copy)')
        self.assertEqual(duplicated_category.age_group, '2-4')
        self.assertEqual(duplicated_category.gender, 'unisex')
        self.assertEqual(duplicated_category.season, 'all_season')
        self.assertEqual(duplicated_category.brand_type, 'all')
        self.assertEqual(duplicated_category.style_type, 'all')
        self.assertEqual(duplicated_category.color_family, 'all')
        self.assertEqual(duplicated_category.size_range, 'all')
        self.assertEqual(duplicated_category.description, 'Original description')
        self.assertEqual(duplicated_category.default_margin, 30.0)
        self.assertEqual(duplicated_category.min_margin, 20.0)
        self.assertEqual(duplicated_category.max_margin, 40.0)
        self.assertEqual(duplicated_category.company_id, self.test_company)
    
    def test_category_move_to_parent(self):
        """Test moving category to new parent"""
        # Create parent categories
        parent1 = self.category_model.create({
            'name': 'Parent 1',
            'age_group': '0-2',
            'gender': 'unisex',
            'season': 'all_season',
            'brand_type': 'all',
            'style_type': 'all',
            'color_family': 'all',
            'size_range': 'all',
            'company_id': self.test_company.id,
        })
        
        parent2 = self.category_model.create({
            'name': 'Parent 2',
            'age_group': '2-4',
            'gender': 'unisex',
            'season': 'all_season',
            'brand_type': 'all',
            'style_type': 'all',
            'color_family': 'all',
            'size_range': 'all',
            'company_id': self.test_company.id,
        })
        
        # Create child category
        child = self.category_model.create({
            'name': 'Child Category',
            'parent_id': parent1.id,
            'age_group': '0-2',
            'gender': 'unisex',
            'season': 'all_season',
            'brand_type': 'all',
            'style_type': 'all',
            'color_family': 'all',
            'size_range': 'all',
            'company_id': self.test_company.id,
        })
        
        # Move child to parent2
        child.move_to_parent(parent2)
        self.assertEqual(child.parent_id, parent2)
        self.assertIn(child, parent2.child_id)
        self.assertNotIn(child, parent1.child_id)
    
    def test_category_computed_fields(self):
        """Test category computed fields"""
        category = self.category_model.create({
            'name': 'Test Category',
            'age_group': '2-4',
            'gender': 'unisex',
            'season': 'all_season',
            'brand_type': 'all',
            'style_type': 'all',
            'color_family': 'all',
            'size_range': 'all',
            'company_id': self.test_company.id,
        })
        
        # Test complete_name computation
        self.assertEqual(category.complete_name, 'Test Category')
        
        # Test is_leaf_category computation
        self.assertTrue(category.is_leaf_category)
        
        # Test image computations
        self.assertFalse(category.image_medium)
        self.assertFalse(category.image_small)
        
        # Test product_count computation
        self.assertEqual(category.product_count, 0)
        
        # Test total_sales computation
        self.assertEqual(category.total_sales, 0.0)
        
        # Test avg_rating computation
        self.assertEqual(category.avg_rating, 0.0)
    
    def test_category_constraints(self):
        """Test category constraints"""
        # Test parent recursion constraint
        parent = self.category_model.create({
            'name': 'Parent',
            'age_group': '0-2',
            'gender': 'unisex',
            'season': 'all_season',
            'brand_type': 'all',
            'style_type': 'all',
            'color_family': 'all',
            'size_range': 'all',
            'company_id': self.test_company.id,
        })
        
        child = self.category_model.create({
            'name': 'Child',
            'parent_id': parent.id,
            'age_group': '0-2',
            'gender': 'unisex',
            'season': 'all_season',
            'brand_type': 'all',
            'style_type': 'all',
            'color_family': 'all',
            'size_range': 'all',
            'company_id': self.test_company.id,
        })
        
        # Test recursion constraint
        with self.assertRaises(ValidationError):
            parent.parent_id = child.id  # This should create recursion