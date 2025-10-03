# -*- coding: utf-8 -*-

import unittest
from core_framework.orm import Model


class TestProductCategory(unittest.TestCase):
    """Test Product Category functionality"""
    
    def setUp(self):
        """Set up test environment"""
        self.category_model = Model('product.category')
        self.template_model = Model('product.category.template')
        self.rule_model = Model('product.category.rule')
        self.analytics_model = Model('product.category.analytics')
        self.tag_model = Model('product.category.tag')
    
    def test_create_category(self):
        """Test creating a product category"""
        category = self.category_model.create({
            'name': 'Test Category',
            'age_group': '2-4',
            'gender': 'unisex',
            'season': 'all_season',
            'brand_type': 'all',
            'style_type': 'all',
            'color_family': 'all',
            'size_range': 'all',
            'description': 'Test category description',
            'default_margin': 30.0,
            'min_margin': 20.0,
            'max_margin': 40.0,
        })
        
        self.assertEqual(category.name, 'Test Category')
        self.assertEqual(category.age_group, '2-4')
        self.assertEqual(category.gender, 'unisex')
        self.assertEqual(category.season, 'all_season')
        self.assertEqual(category.brand_type, 'all')
        self.assertEqual(category.style_type, 'all')
        self.assertEqual(category.color_family, 'all')
        self.assertEqual(category.size_range, 'all')
        self.assertEqual(category.description, 'Test category description')
        self.assertEqual(category.default_margin, 30.0)
        self.assertEqual(category.min_margin, 20.0)
        self.assertEqual(category.max_margin, 40.0)
    
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
        })
        
        self.assertEqual(child_category.parent_id, parent_category)
        self.assertIn(child_category, parent_category.child_id)
        self.assertEqual(child_category.complete_name, 'Parent Category / Child Category')
    
    def test_category_validation(self):
        """Test category validation rules"""
        # Test age range validation
        with self.assertRaises(ValueError):
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
        })
        
        # Test name_get
        name_get_result = category.name_get()
        self.assertEqual(name_get_result[0][1], 'Test Category')
        
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


if __name__ == '__main__':
    unittest.main()