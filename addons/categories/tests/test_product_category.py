# -*- coding: utf-8 -*-

from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError


class TestProductCategory(TransactionCase):
    
    def setUp(self):
        super().setUp()
        self.category_model = self.env['product.category']
        self.company = self.env['res.company'].browse(1)
    
    def test_create_category(self):
        """Test creating a basic category"""
        category = self.category_model.create({
            'name': 'Test Category',
            'age_group': '4-6',
            'gender': 'unisex',
            'season': 'all_season',
            'brand_type': 'all',
            'description': 'Test category description',
            'company_id': self.company.id,
        })
        
        self.assertEqual(category.name, 'Test Category')
        self.assertEqual(category.age_group, '4-6')
        self.assertEqual(category.gender, 'unisex')
        self.assertEqual(category.season, 'all_season')
        self.assertEqual(category.brand_type, 'all')
        self.assertTrue(category.is_active)
    
    def test_category_hierarchy(self):
        """Test category hierarchy"""
        parent_category = self.category_model.create({
            'name': 'Parent Category',
            'age_group': 'all',
            'gender': 'unisex',
            'season': 'all_season',
            'brand_type': 'all',
            'company_id': self.company.id,
        })
        
        child_category = self.category_model.create({
            'name': 'Child Category',
            'parent_id': parent_category.id,
            'age_group': '4-6',
            'gender': 'boys',
            'season': 'summer',
            'brand_type': 'premium',
            'company_id': self.company.id,
        })
        
        self.assertEqual(child_category.parent_id, parent_category)
        self.assertIn(child_category, parent_category.child_id)
        self.assertEqual(child_category.complete_name, 'Parent Category / Child Category')
    
    def test_category_complete_name(self):
        """Test category complete name computation"""
        grandparent = self.category_model.create({
            'name': 'Grandparent',
            'age_group': 'all',
            'gender': 'unisex',
            'season': 'all_season',
            'brand_type': 'all',
            'company_id': self.company.id,
        })
        
        parent = self.category_model.create({
            'name': 'Parent',
            'parent_id': grandparent.id,
            'age_group': 'all',
            'gender': 'unisex',
            'season': 'all_season',
            'brand_type': 'all',
            'company_id': self.company.id,
        })
        
        child = self.category_model.create({
            'name': 'Child',
            'parent_id': parent.id,
            'age_group': '4-6',
            'gender': 'boys',
            'season': 'summer',
            'brand_type': 'premium',
            'company_id': self.company.id,
        })
        
        self.assertEqual(grandparent.complete_name, 'Grandparent')
        self.assertEqual(parent.complete_name, 'Grandparent / Parent')
        self.assertEqual(child.complete_name, 'Grandparent / Parent / Child')
    
    def test_category_price_constraints(self):
        """Test category price constraints"""
        # Test valid price range
        category = self.category_model.create({
            'name': 'Test Category',
            'age_group': '4-6',
            'gender': 'unisex',
            'season': 'all_season',
            'brand_type': 'all',
            'min_price': 100.0,
            'max_price': 500.0,
            'company_id': self.company.id,
        })
        
        self.assertEqual(category.min_price, 100.0)
        self.assertEqual(category.max_price, 500.0)
        
        # Test invalid price range
        with self.assertRaises(ValidationError):
            self.category_model.create({
                'name': 'Invalid Category',
                'age_group': '4-6',
                'gender': 'unisex',
                'season': 'all_season',
                'brand_type': 'all',
                'min_price': 500.0,
                'max_price': 100.0,  # Less than min_price
                'company_id': self.company.id,
            })
    
    def test_category_analytics_computation(self):
        """Test category analytics computation"""
        category = self.category_model.create({
            'name': 'Analytics Category',
            'age_group': '4-6',
            'gender': 'unisex',
            'season': 'all_season',
            'brand_type': 'all',
            'company_id': self.company.id,
        })
        
        # Initially, analytics should be zero
        self.assertEqual(category.product_count, 0)
        self.assertEqual(category.total_sales, 0.0)
        self.assertEqual(category.avg_rating, 0.0)
    
    def test_category_name_search(self):
        """Test category name search"""
        category1 = self.category_model.create({
            'name': 'Boys Clothing',
            'age_group': '4-6',
            'gender': 'boys',
            'season': 'all_season',
            'brand_type': 'all',
            'company_id': self.company.id,
        })
        
        category2 = self.category_model.create({
            'name': 'Girls Clothing',
            'age_group': '4-6',
            'gender': 'girls',
            'season': 'all_season',
            'brand_type': 'all',
            'company_id': self.company.id,
        })
        
        # Test search by name
        results = self.category_model.name_search('Boys')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0][0], category1.id)
        
        # Test search by complete name
        results = self.category_model.name_search('Girls')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0][0], category2.id)
    
    def test_category_recursion_check(self):
        """Test category recursion check"""
        category1 = self.category_model.create({
            'name': 'Category 1',
            'age_group': '4-6',
            'gender': 'unisex',
            'season': 'all_season',
            'brand_type': 'all',
            'company_id': self.company.id,
        })
        
        category2 = self.category_model.create({
            'name': 'Category 2',
            'parent_id': category1.id,
            'age_group': '4-6',
            'gender': 'unisex',
            'season': 'all_season',
            'brand_type': 'all',
            'company_id': self.company.id,
        })
        
        # Test setting category1 as parent of category2 (should work)
        category2.parent_id = category1.id
        self.assertEqual(category2.parent_id, category1)
        
        # Test setting category2 as parent of category1 (should fail - recursion)
        with self.assertRaises(ValidationError):
            category1.parent_id = category2.id
    
    def test_category_sequence(self):
        """Test category sequence ordering"""
        category1 = self.category_model.create({
            'name': 'Category 1',
            'sequence': 10,
            'age_group': '4-6',
            'gender': 'unisex',
            'season': 'all_season',
            'brand_type': 'all',
            'company_id': self.company.id,
        })
        
        category2 = self.category_model.create({
            'name': 'Category 2',
            'sequence': 5,
            'age_group': '4-6',
            'gender': 'unisex',
            'season': 'all_season',
            'brand_type': 'all',
            'company_id': self.company.id,
        })
        
        category3 = self.category_model.create({
            'name': 'Category 3',
            'sequence': 15,
            'age_group': '4-6',
            'gender': 'unisex',
            'season': 'all_season',
            'brand_type': 'all',
            'company_id': self.company.id,
        })
        
        # Test ordering by sequence
        categories = self.category_model.search([], order='sequence')
        self.assertEqual(categories[0], category2)  # sequence 5
        self.assertEqual(categories[1], category1)   # sequence 10
        self.assertEqual(categories[2], category3)   # sequence 15
    
    def test_category_company_isolation(self):
        """Test category company isolation"""
        company2 = self.env['res.company'].create({
            'name': 'Test Company 2',
        })
        
        category1 = self.category_model.create({
            'name': 'Category Company 1',
            'age_group': '4-6',
            'gender': 'unisex',
            'season': 'all_season',
            'brand_type': 'all',
            'company_id': self.company.id,
        })
        
        category2 = self.category_model.create({
            'name': 'Category Company 2',
            'age_group': '4-6',
            'gender': 'unisex',
            'season': 'all_season',
            'brand_type': 'all',
            'company_id': company2.id,
        })
        
        # Test company isolation
        categories_company1 = self.category_model.search([('company_id', '=', self.company.id)])
        categories_company2 = self.category_model.search([('company_id', '=', company2.id)])
        
        self.assertIn(category1, categories_company1)
        self.assertNotIn(category2, categories_company1)
        self.assertIn(category2, categories_company2)
        self.assertNotIn(category1, categories_company2)