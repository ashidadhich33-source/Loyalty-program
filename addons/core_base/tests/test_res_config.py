# -*- coding: utf-8 -*-

from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError


class TestResConfigSettings(TransactionCase):
    """Test cases for res.config.settings model"""
    
    def setUp(self):
        super(TestResConfigSettings, self).setUp()
        self.config = self.env['res.config.settings']
        self.company = self.env['res.company'].create({
            'name': 'Test Company',
            'currency_id': self.env.ref('base.INR').id,
        })
    
    def test_config_creation(self):
        """Test configuration creation"""
        config = self.config.create({
            'company_id': self.company.id,
            'enable_child_profiles': True,
            'enable_loyalty_program': True,
        })
        
        self.assertTrue(config.enable_child_profiles)
        self.assertTrue(config.enable_loyalty_program)
        self.assertEqual(config.company_id, self.company)
    
    def test_get_values(self):
        """Test get_values method"""
        values = self.config.get_values()
        
        self.assertIn('enable_child_profiles', values)
        self.assertIn('enable_loyalty_program', values)
        self.assertIn('enable_gst', values)
    
    def test_set_values(self):
        """Test set_values method"""
        config = self.config.create({
            'company_id': self.company.id,
            'enable_child_profiles': False,
            'enable_loyalty_program': False,
        })
        
        config.set_values()
        
        # Check if parameters are set correctly
        params = self.env['ir.config_parameter'].sudo()
        self.assertEqual(params.get_param('core_base.enable_child_profiles'), 'False')
        self.assertEqual(params.get_param('core_base.enable_loyalty_program'), 'False')
    
    def test_get_system_info(self):
        """Test get_system_info method"""
        info = self.config.get_system_info()
        
        self.assertIn('version', info)
        self.assertIn('modules_installed', info)
        self.assertIn('users_count', info)
        self.assertIn('companies_count', info)
        
        self.assertEqual(info['version'], '1.0.0')
        self.assertGreaterEqual(info['users_count'], 1)
        self.assertGreaterEqual(info['companies_count'], 1)