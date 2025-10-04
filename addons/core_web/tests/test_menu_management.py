# -*- coding: utf-8 -*-
"""
Test Menu Management
===================

Test cases for menu management functionality.
"""

import unittest
from ocean.tests.common import TransactionCase


class TestMenuManagement(TransactionCase):
    """Test menu management functionality."""
    
    def setUp(self):
        super().setUp()
        self.menu_model = self.env['menu.management']
    
    def test_menu_creation(self):
        """Test menu creation."""
        menu = self.menu_model.create({
            'name': 'Test Menu',
            'sequence': 10,
            'is_active': True,
        })
        self.assertTrue(menu.id)
        self.assertEqual(menu.name, 'Test Menu')
    
    def test_menu_sequence(self):
        """Test menu sequence ordering."""
        menu1 = self.menu_model.create({
            'name': 'Menu 1',
            'sequence': 10,
        })
        menu2 = self.menu_model.create({
            'name': 'Menu 2',
            'sequence': 20,
        })
        
        menus = self.menu_model.search([], order='sequence')
        self.assertEqual(menus[0], menu1)
        self.assertEqual(menus[1], menu2)