# -*- coding: utf-8 -*-
"""
Ocean ERP - Indian Localization Bank Tests
==========================================

Tests for Indian localization bank models.
"""

from core_framework.testing import OceanTestCase
from addons.l10n_in.models.res_bank import ResBank, ResBankBranch
import logging

_logger = logging.getLogger(__name__)


class TestResBank(OceanTestCase):
    """Test cases for ResBank model"""
    
    def setUp(self):
        super(TestResBank, self).setUp()
        self.bank_model = self.env['res.bank']
    
    def test_create_bank(self):
        """Test creating a bank"""
        bank_vals = {
            'name': 'State Bank of India',
            'bank_type': 'public_sector',
            'ifsc_code': 'SBIN0001234',
            'micr_code': '400002123',
            'swift_code': 'SBININBB',
            'age_group': '4-6',
            'size': 'm',
            'season': 'all_season',
            'brand': 'Kids Brand',
            'color': 'Blue',
        }
        
        bank = self.bank_model.create(bank_vals)
        
        self.assertEqual(bank.name, 'State Bank of India')
        self.assertEqual(bank.bank_type, 'public_sector')
        self.assertEqual(bank.ifsc_code, 'SBIN0001234')
        self.assertEqual(bank.micr_code, '400002123')
        self.assertEqual(bank.swift_code, 'SBININBB')
        self.assertEqual(bank.age_group, '4-6')
        self.assertEqual(bank.size, 'm')
        self.assertEqual(bank.season, 'all_season')
        self.assertEqual(bank.brand, 'Kids Brand')
        self.assertEqual(bank.color, 'Blue')
        self.assertTrue(bank.active)
    
    def test_validate_ifsc_code(self):
        """Test IFSC code validation"""
        bank = self.bank_model.create({
            'name': 'Test Bank',
            'ifsc_code': 'SBIN0001234'
        })
        
        # Valid IFSC codes
        self.assertTrue(bank.validate_ifsc_code('SBIN0001234'))
        self.assertTrue(bank.validate_ifsc_code('HDFC0001234'))
        self.assertTrue(bank.validate_ifsc_code('ICIC0001234'))
        
        # Invalid IFSC codes
        self.assertFalse(bank.validate_ifsc_code('SBIN000123'))
        self.assertFalse(bank.validate_ifsc_code('SBIN00012345'))
        self.assertFalse(bank.validate_ifsc_code('1234567890'))
    
    def test_validate_micr_code(self):
        """Test MICR code validation"""
        bank = self.bank_model.create({
            'name': 'Test Bank',
            'micr_code': '400002123'
        })
        
        # Valid MICR codes
        self.assertTrue(bank.validate_micr_code('400002123'))
        self.assertTrue(bank.validate_micr_code('110002123'))
        self.assertTrue(bank.validate_micr_code('560002123'))
        
        # Invalid MICR codes
        self.assertFalse(bank.validate_micr_code('40000212'))
        self.assertFalse(bank.validate_micr_code('4000021234'))
        self.assertFalse(bank.validate_micr_code('ABCD12345'))
    
    def test_get_kids_clothing_banks(self):
        """Test filtering banks by kids clothing criteria"""
        # Create test banks
        bank1 = self.bank_model.create({
            'name': 'Baby Bank',
            'bank_type': 'public_sector',
            'age_group': '0-2',
            'size': 'xs',
            'season': 'summer',
            'brand': 'Baby Brand',
            'color': 'Pink'
        })
        
        bank2 = self.bank_model.create({
            'name': 'Toddler Bank',
            'bank_type': 'private_sector',
            'age_group': '2-4',
            'size': 's',
            'season': 'winter',
            'brand': 'Toddler Brand',
            'color': 'Blue'
        })
        
        bank3 = self.bank_model.create({
            'name': 'All Age Bank',
            'bank_type': 'cooperative',
            'age_group': 'all',
            'size': 'all',
            'season': 'all_season',
            'brand': 'All Brand',
            'color': 'Green'
        })
        
        # Test filtering by age group
        baby_banks = self.bank_model.get_kids_clothing_banks(age_group='0-2')
        self.assertIn(bank1, baby_banks)
        self.assertNotIn(bank2, baby_banks)
        self.assertIn(bank3, baby_banks)  # 'all' should match
        
        # Test filtering by size
        xs_banks = self.bank_model.get_kids_clothing_banks(size='xs')
        self.assertIn(bank1, xs_banks)
        self.assertNotIn(bank2, xs_banks)
        self.assertIn(bank3, xs_banks)  # 'all' should match
        
        # Test filtering by season
        summer_banks = self.bank_model.get_kids_clothing_banks(season='summer')
        self.assertIn(bank1, summer_banks)
        self.assertNotIn(bank2, summer_banks)
        self.assertIn(bank3, summer_banks)  # 'all_season' should match
        
        # Test filtering by brand
        baby_brand_banks = self.bank_model.get_kids_clothing_banks(brand='Baby Brand')
        self.assertIn(bank1, baby_brand_banks)
        self.assertNotIn(bank2, baby_brand_banks)
        self.assertNotIn(bank3, baby_brand_banks)
        
        # Test filtering by color
        pink_banks = self.bank_model.get_kids_clothing_banks(color='Pink')
        self.assertIn(bank1, pink_banks)
        self.assertNotIn(bank2, pink_banks)
        self.assertNotIn(bank3, pink_banks)
    
    def test_bank_types(self):
        """Test different bank types"""
        bank_types = [
            'public_sector',
            'private_sector',
            'foreign',
            'cooperative',
            'regional_rural',
            'small_finance',
            'payment',
            'other'
        ]
        
        for bank_type in bank_types:
            bank = self.bank_model.create({
                'name': f'Test {bank_type.title()} Bank',
                'bank_type': bank_type
            })
            self.assertEqual(bank.bank_type, bank_type)


class TestResBankBranch(OceanTestCase):
    """Test cases for ResBankBranch model"""
    
    def setUp(self):
        super(TestResBankBranch, self).setUp()
        self.bank_model = self.env['res.bank']
        self.branch_model = self.env['res.bank.branch']
    
    def test_create_bank_branch(self):
        """Test creating a bank branch"""
        # Create parent bank first
        bank = self.bank_model.create({
            'name': 'State Bank of India',
            'bank_type': 'public_sector',
            'ifsc_code': 'SBIN0001234'
        })
        
        branch_vals = {
            'name': 'Mumbai Main Branch',
            'bank_id': bank.id,
            'branch_type': 'main',
            'ifsc_code': 'SBIN0001234',
            'micr_code': '400002123',
            'age_group': '4-6',
            'size': 'm',
            'season': 'all_season',
            'brand': 'Kids Brand',
            'color': 'Blue',
        }
        
        branch = self.branch_model.create(branch_vals)
        
        self.assertEqual(branch.name, 'Mumbai Main Branch')
        self.assertEqual(branch.bank_id.id, bank.id)
        self.assertEqual(branch.branch_type, 'main')
        self.assertEqual(branch.ifsc_code, 'SBIN0001234')
        self.assertEqual(branch.micr_code, '400002123')
        self.assertEqual(branch.age_group, '4-6')
        self.assertEqual(branch.size, 'm')
        self.assertEqual(branch.season, 'all_season')
        self.assertEqual(branch.brand, 'Kids Brand')
        self.assertEqual(branch.color, 'Blue')
        self.assertTrue(branch.active)
    
    def test_validate_ifsc_code(self):
        """Test IFSC code validation"""
        bank = self.bank_model.create({
            'name': 'Test Bank',
            'bank_type': 'public_sector'
        })
        
        branch = self.branch_model.create({
            'name': 'Test Branch',
            'bank_id': bank.id,
            'ifsc_code': 'SBIN0001234'
        })
        
        # Valid IFSC codes
        self.assertTrue(branch.validate_ifsc_code('SBIN0001234'))
        self.assertTrue(branch.validate_ifsc_code('HDFC0001234'))
        self.assertTrue(branch.validate_ifsc_code('ICIC0001234'))
        
        # Invalid IFSC codes
        self.assertFalse(branch.validate_ifsc_code('SBIN000123'))
        self.assertFalse(branch.validate_ifsc_code('SBIN00012345'))
        self.assertFalse(branch.validate_ifsc_code('1234567890'))
    
    def test_validate_micr_code(self):
        """Test MICR code validation"""
        bank = self.bank_model.create({
            'name': 'Test Bank',
            'bank_type': 'public_sector'
        })
        
        branch = self.branch_model.create({
            'name': 'Test Branch',
            'bank_id': bank.id,
            'micr_code': '400002123'
        })
        
        # Valid MICR codes
        self.assertTrue(branch.validate_micr_code('400002123'))
        self.assertTrue(branch.validate_micr_code('110002123'))
        self.assertTrue(branch.validate_micr_code('560002123'))
        
        # Invalid MICR codes
        self.assertFalse(branch.validate_micr_code('40000212'))
        self.assertFalse(branch.validate_micr_code('4000021234'))
        self.assertFalse(branch.validate_micr_code('ABCD12345'))
    
    def test_get_kids_clothing_bank_branches(self):
        """Test filtering bank branches by kids clothing criteria"""
        # Create parent bank first
        bank = self.bank_model.create({
            'name': 'Test Bank',
            'bank_type': 'public_sector'
        })
        
        # Create test branches
        branch1 = self.branch_model.create({
            'name': 'Baby Branch',
            'bank_id': bank.id,
            'branch_type': 'main',
            'age_group': '0-2',
            'size': 'xs',
            'season': 'summer',
            'brand': 'Baby Brand',
            'color': 'Pink'
        })
        
        branch2 = self.branch_model.create({
            'name': 'Toddler Branch',
            'bank_id': bank.id,
            'branch_type': 'sub',
            'age_group': '2-4',
            'size': 's',
            'season': 'winter',
            'brand': 'Toddler Brand',
            'color': 'Blue'
        })
        
        branch3 = self.branch_model.create({
            'name': 'All Age Branch',
            'bank_id': bank.id,
            'branch_type': 'atm',
            'age_group': 'all',
            'size': 'all',
            'season': 'all_season',
            'brand': 'All Brand',
            'color': 'Green'
        })
        
        # Test filtering by age group
        baby_branches = self.branch_model.get_kids_clothing_bank_branches(age_group='0-2')
        self.assertIn(branch1, baby_branches)
        self.assertNotIn(branch2, baby_branches)
        self.assertIn(branch3, baby_branches)  # 'all' should match
        
        # Test filtering by size
        xs_branches = self.branch_model.get_kids_clothing_bank_branches(size='xs')
        self.assertIn(branch1, xs_branches)
        self.assertNotIn(branch2, xs_branches)
        self.assertIn(branch3, xs_branches)  # 'all' should match
        
        # Test filtering by season
        summer_branches = self.branch_model.get_kids_clothing_bank_branches(season='summer')
        self.assertIn(branch1, summer_branches)
        self.assertNotIn(branch2, summer_branches)
        self.assertIn(branch3, summer_branches)  # 'all_season' should match
        
        # Test filtering by brand
        baby_brand_branches = self.branch_model.get_kids_clothing_bank_branches(brand='Baby Brand')
        self.assertIn(branch1, baby_brand_branches)
        self.assertNotIn(branch2, baby_brand_branches)
        self.assertNotIn(branch3, baby_brand_branches)
        
        # Test filtering by color
        pink_branches = self.branch_model.get_kids_clothing_bank_branches(color='Pink')
        self.assertIn(branch1, pink_branches)
        self.assertNotIn(branch2, pink_branches)
        self.assertNotIn(branch3, pink_branches)
    
    def test_branch_types(self):
        """Test different branch types"""
        bank = self.bank_model.create({
            'name': 'Test Bank',
            'bank_type': 'public_sector'
        })
        
        branch_types = [
            'main',
            'sub',
            'atm',
            'extension',
            'other'
        ]
        
        for branch_type in branch_types:
            branch = self.branch_model.create({
                'name': f'Test {branch_type.title()} Branch',
                'bank_id': bank.id,
                'branch_type': branch_type
            })
            self.assertEqual(branch.branch_type, branch_type)