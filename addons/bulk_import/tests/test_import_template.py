# -*- coding: utf-8 -*-

from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError


class TestImportTemplate(TransactionCase):
    
    def setUp(self):
        super().setUp()
        self.template_model = self.env['import.template']
        self.company = self.env['res.company'].browse(1)
        self.product_model = self.env['ir.model'].search([('model', '=', 'product.template')], limit=1)
    
    def test_create_template(self):
        """Test creating a basic import template"""
        template = self.template_model.create({
            'name': 'Test Template',
            'description': 'Test template description',
            'model_id': self.product_model.id,
            'template_type': 'excel',
            'is_kids_specific': True,
            'age_group_validation': True,
            'gender_validation': True,
            'company_id': self.company.id,
        })
        
        self.assertEqual(template.name, 'Test Template')
        self.assertEqual(template.template_type, 'excel')
        self.assertTrue(template.is_kids_specific)
        self.assertTrue(template.age_group_validation)
        self.assertTrue(template.gender_validation)
        self.assertTrue(template.is_active)
    
    def test_template_validation(self):
        """Test template validation rules"""
        # Test valid template
        template = self.template_model.create({
            'name': 'Valid Template',
            'model_id': self.product_model.id,
            'template_type': 'excel',
            'header_row': 1,
            'data_start_row': 2,
            'max_rows': 1000,
            'company_id': self.company.id,
        })
        
        self.assertEqual(template.header_row, 1)
        self.assertEqual(template.data_start_row, 2)
        self.assertEqual(template.max_rows, 1000)
        
        # Test invalid header row
        with self.assertRaises(ValidationError):
            self.template_model.create({
                'name': 'Invalid Template',
                'model_id': self.product_model.id,
                'template_type': 'excel',
                'header_row': 2,
                'data_start_row': 1,  # Less than header_row
                'company_id': self.company.id,
            })
        
        # Test invalid max rows
        with self.assertRaises(ValidationError):
            self.template_model.create({
                'name': 'Invalid Template',
                'model_id': self.product_model.id,
                'template_type': 'excel',
                'max_rows': 0,  # Must be greater than 0
                'company_id': self.company.id,
            })
    
    def test_default_template_constraint(self):
        """Test default template constraint"""
        # Create first default template
        template1 = self.template_model.create({
            'name': 'Default Template 1',
            'model_id': self.product_model.id,
            'template_type': 'excel',
            'is_default': True,
            'company_id': self.company.id,
        })
        
        self.assertTrue(template1.is_default)
        
        # Try to create second default template for same model
        with self.assertRaises(ValidationError):
            self.template_model.create({
                'name': 'Default Template 2',
                'model_id': self.product_model.id,
                'template_type': 'excel',
                'is_default': True,
                'company_id': self.company.id,
            })
    
    def test_template_actions(self):
        """Test template actions"""
        template = self.template_model.create({
            'name': 'Test Template',
            'model_id': self.product_model.id,
            'template_type': 'excel',
            'company_id': self.company.id,
        })
        
        # Test download template (should fail without file)
        with self.assertRaises(ValidationError):
            template.action_download_template()
        
        # Test preview template (should fail without file)
        with self.assertRaises(ValidationError):
            template.action_preview_template()
        
        # Test validate template (should fail without file)
        with self.assertRaises(ValidationError):
            template.action_validate_template()
    
    def test_template_duplicate(self):
        """Test template duplication"""
        template = self.template_model.create({
            'name': 'Original Template',
            'model_id': self.product_model.id,
            'template_type': 'excel',
            'usage_count': 5,
            'company_id': self.company.id,
        })
        
        new_template = template.action_duplicate_template()
        
        self.assertEqual(new_template.name, 'Original Template (Copy)')
        self.assertFalse(new_template.is_default)
        self.assertEqual(new_template.usage_count, 0)
        self.assertFalse(new_template.last_used)
    
    def test_template_export(self):
        """Test template export"""
        template = self.template_model.create({
            'name': 'Export Template',
            'model_id': self.product_model.id,
            'template_type': 'excel',
            'company_id': self.company.id,
        })
        
        # Test export template
        result = template.action_export_template()
        self.assertEqual(result['type'], 'ir.actions.act_url')
    
    def test_kids_clothing_validation(self):
        """Test kids clothing specific validation"""
        template = self.template_model.create({
            'name': 'Kids Template',
            'model_id': self.product_model.id,
            'template_type': 'excel',
            'is_kids_specific': True,
            'age_group_validation': True,
            'gender_validation': True,
            'size_validation': True,
            'company_id': self.company.id,
        })
        
        # Test valid kids clothing data
        valid_data = [
            {'name': 'Kids T-Shirt', 'age_group': '4-6', 'gender': 'unisex', 'size': 'M'},
            {'name': 'Baby Onesie', 'age_group': '0-2', 'gender': 'boys', 'size': 'S'},
        ]
        
        errors = template.validate_import_data(valid_data)
        self.assertEqual(len(errors), 0)
        
        # Test invalid kids clothing data
        invalid_data = [
            {'name': 'Invalid Product', 'age_group': 'invalid', 'gender': 'unknown', 'size': 'XXL'},
        ]
        
        errors = template.validate_import_data(invalid_data)
        self.assertGreater(len(errors), 0)
    
    def test_indian_localization_validation(self):
        """Test Indian localization validation"""
        template = self.template_model.create({
            'name': 'Indian Template',
            'model_id': self.product_model.id,
            'template_type': 'excel',
            'gstin_validation': True,
            'pan_validation': True,
            'mobile_validation': True,
            'company_id': self.company.id,
        })
        
        # Test valid Indian data
        valid_data = [
            {'name': 'Indian Product', 'gstin': '22AAAAA0000A1Z5', 'pan': 'AAAAA0000A', 'mobile': '9876543210'},
        ]
        
        errors = template.validate_import_data(valid_data)
        self.assertEqual(len(errors), 0)
        
        # Test invalid Indian data
        invalid_data = [
            {'name': 'Invalid Product', 'gstin': 'invalid', 'pan': 'invalid', 'mobile': 'invalid'},
        ]
        
        errors = template.validate_import_data(invalid_data)
        self.assertGreater(len(errors), 0)
    
    def test_template_company_isolation(self):
        """Test template company isolation"""
        company2 = self.env['res.company'].create({
            'name': 'Test Company 2',
        })
        
        template1 = self.template_model.create({
            'name': 'Template Company 1',
            'model_id': self.product_model.id,
            'template_type': 'excel',
            'company_id': self.company.id,
        })
        
        template2 = self.template_model.create({
            'name': 'Template Company 2',
            'model_id': self.product_model.id,
            'template_type': 'excel',
            'company_id': company2.id,
        })
        
        # Test company isolation
        templates_company1 = self.template_model.search([('company_id', '=', self.company.id)])
        templates_company2 = self.template_model.search([('company_id', '=', company2.id)])
        
        self.assertIn(template1, templates_company1)
        self.assertNotIn(template2, templates_company1)
        self.assertIn(template2, templates_company2)
        self.assertNotIn(template1, templates_company2)
    
    def test_template_sequence(self):
        """Test template sequence ordering"""
        template1 = self.template_model.create({
            'name': 'Template 1',
            'model_id': self.product_model.id,
            'template_type': 'excel',
            'sequence': 10,
            'company_id': self.company.id,
        })
        
        template2 = self.template_model.create({
            'name': 'Template 2',
            'model_id': self.product_model.id,
            'template_type': 'excel',
            'sequence': 5,
            'company_id': self.company.id,
        })
        
        template3 = self.template_model.create({
            'name': 'Template 3',
            'model_id': self.product_model.id,
            'template_type': 'excel',
            'sequence': 15,
            'company_id': self.company.id,
        })
        
        # Test ordering by sequence
        templates = self.template_model.search([], order='sequence')
        self.assertEqual(templates[0], template2)  # sequence 5
        self.assertEqual(templates[1], template1)   # sequence 10
        self.assertEqual(templates[2], template3)   # sequence 15