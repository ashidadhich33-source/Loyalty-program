# -*- coding: utf-8 -*-
"""
Test Web Utils
==============

Test cases for web utilities functionality.
"""

import unittest
from ocean.tests.common import TransactionCase


class TestWebUtils(TransactionCase):
    """Test web utilities functionality."""
    
    def setUp(self):
        super().setUp()
        self.web_utils_model = self.env['web.utils']
    
    def test_web_utils_creation(self):
        """Test web utils creation."""
        web_util = self.web_utils_model.create({
            'name': 'Test Web Util',
            'utility_type': 'helper',
            'is_active': True,
        })
        self.assertTrue(web_util.id)
        self.assertEqual(web_util.name, 'Test Web Util')
    
    def test_web_utils_types(self):
        """Test different web utility types."""
        types = ['helper', 'component', 'service', 'widget']
        for util_type in types:
            web_util = self.web_utils_model.create({
                'name': f'Test {util_type}',
                'utility_type': util_type,
            })
            self.assertEqual(web_util.utility_type, util_type)