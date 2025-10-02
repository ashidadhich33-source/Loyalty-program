# -*- coding: utf-8 -*-

from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError


class TestResPartner(TransactionCase):
    """Test cases for res.partner model with kids clothing specific fields"""

    def setUp(self):
        super().setUp()
        self.partner_model = self.env['res.partner']
        self.child_partner = self.partner_model.create({
            'name': 'Test Child',
            'is_child': True,
            'child_age': 5,
            'clothing_size': 'M',
            'loyalty_points': 100,
            'special_requirements': 'Allergic to wool',
        })
        self.parent_partner = self.partner_model.create({
            'name': 'Test Parent',
            'is_child': False,
            'loyalty_points': 50,
        })

    def test_child_partner_creation(self):
        """Test creation of child partner"""
        self.assertTrue(self.child_partner.is_child)
        self.assertEqual(self.child_partner.child_age, 5)
        self.assertEqual(self.child_partner.clothing_size, 'M')
        self.assertEqual(self.child_partner.loyalty_points, 100)
        self.assertEqual(self.child_partner.special_requirements, 'Allergic to wool')

    def test_parent_partner_creation(self):
        """Test creation of parent partner"""
        self.assertFalse(self.parent_partner.is_child)
        self.assertEqual(self.parent_partner.loyalty_points, 50)

    def test_child_age_validation(self):
        """Test child age validation"""
        with self.assertRaises(ValidationError):
            self.partner_model.create({
                'name': 'Invalid Child',
                'is_child': True,
                'child_age': -1,  # Negative age should raise error
            })

    def test_loyalty_points_usage(self):
        """Test loyalty points usage"""
        initial_points = self.child_partner.loyalty_points
        points_to_use = 20
        
        # Simulate using loyalty points
        self.child_partner.loyalty_points -= points_to_use
        self.assertEqual(self.child_partner.loyalty_points, initial_points - points_to_use)

    def test_loyalty_points_earned(self):
        """Test loyalty points earned"""
        initial_points = self.child_partner.loyalty_points
        points_earned = 30
        
        # Simulate earning loyalty points
        self.child_partner.loyalty_points += points_earned
        self.assertEqual(self.child_partner.loyalty_points, initial_points + points_earned)

    def test_child_parent_relationship(self):
        """Test child-parent relationship"""
        # Set parent for child
        self.child_partner.parent_id = self.parent_partner.id
        self.assertEqual(self.child_partner.parent_id, self.parent_partner)

    def test_special_requirements(self):
        """Test special requirements field"""
        requirements = "No synthetic materials, prefer organic cotton"
        self.child_partner.special_requirements = requirements
        self.assertEqual(self.child_partner.special_requirements, requirements)

    def test_clothing_size_update(self):
        """Test clothing size update"""
        new_size = 'L'
        self.child_partner.clothing_size = new_size
        self.assertEqual(self.child_partner.clothing_size, new_size)

    def test_loyalty_points_negative(self):
        """Test that loyalty points cannot go negative"""
        with self.assertRaises(ValidationError):
            self.child_partner.loyalty_points = -10

    def test_child_age_range(self):
        """Test child age range validation"""
        # Test valid ages
        valid_ages = [0, 1, 5, 10, 15, 18]
        for age in valid_ages:
            partner = self.partner_model.create({
                'name': f'Child {age}',
                'is_child': True,
                'child_age': age,
            })
            self.assertEqual(partner.child_age, age)

    def test_partner_type_consistency(self):
        """Test that child partners are always contacts, not companies"""
        self.assertEqual(self.child_partner.type, 'contact')
        self.assertFalse(self.child_partner.is_company)