#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Product Category Tests
==========================================

Test cases for product category management.
"""

import unittest
from core_framework.testing import TestCase

class TestProductCategory(TestCase):
    """Test cases for ProductCategory model"""
    
    def setUp(self):
        """Set up test data"""
        super().setUp()
        self.category_model = self.env['product.category']
    
    def test_create_category(self):
        """Test creating a new category"""
        category_vals = {
            'name': 'Test Category',
            'code': 'TEST',
            'description': 'Test category description',
            'category_type': 'age_based',
            'age_group': 'toddler',
            'gender': 'all',
            'sequence': 10,
            'margin_percentage': 25.0,
            'is_active': True
        }
        
        category = self.category_model.create(category_vals)
        
        self.assertEqual(category.name, 'Test Category')
        self.assertEqual(category.code, 'TEST')
        self.assertEqual(category.category_type, 'age_based')
        self.assertEqual(category.age_group, 'toddler')
        self.assertEqual(category.margin_percentage, 25.0)
        self.assertTrue(category.is_active)
    
    def test_category_hierarchy(self):
        """Test category hierarchy functionality"""
        # Create parent category
        parent_vals = {
            'name': 'Parent Category',
            'code': 'PARENT',
            'category_type': 'age_based',
            'age_group': 'toddler'
        }
        parent = self.category_model.create(parent_vals)
        
        # Create child category
        child_vals = {
            'name': 'Child Category',
            'code': 'CHILD',
            'category_type': 'age_based',
            'age_group': 'toddler',
            'parent_id': parent.id
        }
        child = self.category_model.create(child_vals)
        
        # Test hierarchy
        self.assertEqual(child.parent_id, parent)
        self.assertIn(child, parent.child_ids)
        
        # Test hierarchy path
        hierarchy = child.get_category_hierarchy()
        self.assertIn('Parent Category', hierarchy)
        self.assertIn('Child Category', hierarchy)
    
    def test_category_validation(self):
        """Test category validation rules"""
        # Test circular reference
        parent_vals = {
            'name': 'Parent',
            'code': 'PARENT',
            'category_type': 'age_based'
        }
        parent = self.category_model.create(parent_vals)
        
        child_vals = {
            'name': 'Child',
            'code': 'CHILD',
            'category_type': 'age_based',
            'parent_id': parent.id
        }
        child = self.category_model.create(child_vals)
        
        # Try to create circular reference
        with self.assertRaises(Exception):
            parent.write({'parent_id': child.id})
    
    def test_category_analytics(self):
        """Test category analytics functionality"""
        category_vals = {
            'name': 'Analytics Category',
            'code': 'ANALYTICS',
            'category_type': 'age_based',
            'age_group': 'school'
        }
        category = self.category_model.create(category_vals)
        
        # Test analytics action
        analytics_action = category.action_analyze_category()
        self.assertIsInstance(analytics_action, dict)
        self.assertEqual(analytics_action['res_model'], 'category.analytics')
    
    def test_category_products_action(self):
        """Test view products action"""
        category_vals = {
            'name': 'Products Category',
            'code': 'PRODUCTS',
            'category_type': 'age_based',
            'age_group': 'preschool'
        }
        category = self.category_model.create(category_vals)
        
        # Test products action
        products_action = category.action_view_products()
        self.assertIsInstance(products_action, dict)
        self.assertEqual(products_action['res_model'], 'product.template')
    
    def test_category_defaults(self):
        """Test category default values"""
        category_vals = {
            'name': 'Default Category'
        }
        category = self.category_model.create(category_vals)
        
        # Test default code generation
        self.assertEqual(category.code, 'DEFAULT_CATEGORY')
        self.assertTrue(category.is_active)
        self.assertEqual(category.sequence, 10)
    
    def test_category_update_product_count(self):
        """Test product count update"""
        category_vals = {
            'name': 'Count Category',
            'code': 'COUNT'
        }
        category = self.category_model.create(category_vals)
        
        # Test product count update
        category._update_product_count()
        self.assertEqual(category.product_count, 0)
    
    def test_category_child_categories(self):
        """Test getting child categories"""
        parent_vals = {
            'name': 'Parent',
            'code': 'PARENT',
            'category_type': 'age_based'
        }
        parent = self.category_model.create(parent_vals)
        
        child1_vals = {
            'name': 'Child 1',
            'code': 'CHILD1',
            'category_type': 'age_based',
            'parent_id': parent.id
        }
        child1 = self.category_model.create(child1_vals)
        
        child2_vals = {
            'name': 'Child 2',
            'code': 'CHILD2',
            'category_type': 'age_based',
            'parent_id': parent.id
        }
        child2 = self.category_model.create(child2_vals)
        
        # Test getting child categories
        children = parent.get_child_categories()
        self.assertEqual(len(children), 2)
        self.assertIn(child1, children)
        self.assertIn(child2, children)