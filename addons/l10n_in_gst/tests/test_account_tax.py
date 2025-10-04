# -*- coding: utf-8 -*-
"""
Ocean ERP - Indian GST Tax Tests
=================================

Tests for Indian GST tax models.
"""

from core_framework.testing import OceanTestCase
from addons.l10n_in_gst.models.account_tax import AccountTax, AccountTaxGroup
import logging

_logger = logging.getLogger(__name__)


class TestAccountTax(OceanTestCase):
    """Test cases for AccountTax model"""
    
    def setUp(self):
        super(TestAccountTax, self).setUp()
        self.tax_model = self.env['account.tax']
        self.tax_group_model = self.env['account.tax.group']
    
    def test_create_gst_tax(self):
        """Test creating a GST tax"""
        tax_vals = {
            'name': 'GST 18%',
            'tax_type': 'gst',
            'gst_type': 'cgst',
            'amount': 18.0,
            'amount_type': 'percent',
            'gst_rate': 18.0,
            'hsn_code': '6203',
            'age_group': '4-6',
            'size': 'm',
            'season': 'all_season',
            'brand': 'Kids Brand',
            'color': 'Blue',
        }
        
        tax = self.tax_model.create(tax_vals)
        
        self.assertEqual(tax.name, 'GST 18%')
        self.assertEqual(tax.tax_type, 'gst')
        self.assertEqual(tax.gst_type, 'cgst')
        self.assertEqual(tax.amount, 18.0)
        self.assertEqual(tax.amount_type, 'percent')
        self.assertEqual(tax.gst_rate, 18.0)
        self.assertEqual(tax.hsn_code, '6203')
        self.assertEqual(tax.age_group, '4-6')
        self.assertEqual(tax.size, 'm')
        self.assertEqual(tax.season, 'all_season')
        self.assertEqual(tax.brand, 'Kids Brand')
        self.assertEqual(tax.color, 'Blue')
        self.assertTrue(tax.active)
    
    def test_validate_hsn_code(self):
        """Test HSN code validation"""
        tax = self.tax_model.create({
            'name': 'Test Tax',
            'tax_type': 'gst',
            'hsn_code': '6203'
        })
        
        # Valid HSN codes
        self.assertTrue(tax.validate_hsn_code('6203'))
        self.assertTrue(tax.validate_hsn_code('620342'))
        self.assertTrue(tax.validate_hsn_code('62034200'))
        
        # Invalid HSN codes
        self.assertFalse(tax.validate_hsn_code('620'))
        self.assertFalse(tax.validate_hsn_code('620342000'))
        self.assertFalse(tax.validate_hsn_code('6203A'))
        self.assertFalse(tax.validate_hsn_code('ABC123'))
    
    def test_validate_sac_code(self):
        """Test SAC code validation"""
        tax = self.tax_model.create({
            'name': 'Test Tax',
            'tax_type': 'gst',
            'sac_code': '998314'
        })
        
        # Valid SAC codes
        self.assertTrue(tax.validate_sac_code('998314'))
        self.assertTrue(tax.validate_sac_code('123456'))
        
        # Invalid SAC codes
        self.assertFalse(tax.validate_sac_code('99831'))
        self.assertFalse(tax.validate_sac_code('9983140'))
        self.assertFalse(tax.validate_sac_code('99831A'))
        self.assertFalse(tax.validate_sac_code('ABC123'))
    
    def test_compute_gst_amount(self):
        """Test GST amount computation"""
        tax = self.tax_model.create({
            'name': 'GST 18%',
            'tax_type': 'gst',
            'amount': 18.0,
            'amount_type': 'percent'
        })
        
        # Test percentage calculation
        base_amount = 1000.0
        gst_amount = tax.compute_gst_amount(base_amount)
        self.assertEqual(gst_amount, 180.0)
        
        # Test fixed amount
        tax_fixed = self.tax_model.create({
            'name': 'Fixed Tax',
            'tax_type': 'gst',
            'amount': 50.0,
            'amount_type': 'fixed'
        })
        
        gst_amount_fixed = tax_fixed.compute_gst_amount(base_amount)
        self.assertEqual(gst_amount_fixed, 50.0)
    
    def test_get_gst_breakdown(self):
        """Test GST breakdown calculation"""
        # Test IGST
        igst_tax = self.tax_model.create({
            'name': 'IGST 18%',
            'tax_type': 'gst',
            'gst_type': 'igst',
            'amount': 18.0,
            'amount_type': 'percent'
        })
        
        breakdown = igst_tax.get_gst_breakdown(1000.0)
        self.assertEqual(breakdown['igst'], 180.0)
        self.assertEqual(breakdown['cgst'], 0)
        self.assertEqual(breakdown['sgst'], 0)
        self.assertEqual(breakdown['cess'], 0)
        self.assertEqual(breakdown['total'], 1180.0)
        
        # Test CGST
        cgst_tax = self.tax_model.create({
            'name': 'CGST 18%',
            'tax_type': 'gst',
            'gst_type': 'cgst',
            'amount': 18.0,
            'amount_type': 'percent'
        })
        
        breakdown = cgst_tax.get_gst_breakdown(1000.0)
        self.assertEqual(breakdown['igst'], 0)
        self.assertEqual(breakdown['cgst'], 180.0)
        self.assertEqual(breakdown['sgst'], 180.0)
        self.assertEqual(breakdown['cess'], 0)
        self.assertEqual(breakdown['total'], 1360.0)
        
        # Test SGST
        sgst_tax = self.tax_model.create({
            'name': 'SGST 18%',
            'tax_type': 'gst',
            'gst_type': 'sgst',
            'amount': 18.0,
            'amount_type': 'percent'
        })
        
        breakdown = sgst_tax.get_gst_breakdown(1000.0)
        self.assertEqual(breakdown['igst'], 0)
        self.assertEqual(breakdown['cgst'], 180.0)
        self.assertEqual(breakdown['sgst'], 180.0)
        self.assertEqual(breakdown['cess'], 0)
        self.assertEqual(breakdown['total'], 1360.0)
        
        # Test CESS
        cess_tax = self.tax_model.create({
            'name': 'CESS 1%',
            'tax_type': 'gst',
            'gst_type': 'cess',
            'amount': 1.0,
            'amount_type': 'percent'
        })
        
        breakdown = cess_tax.get_gst_breakdown(1000.0)
        self.assertEqual(breakdown['igst'], 0)
        self.assertEqual(breakdown['cgst'], 0)
        self.assertEqual(breakdown['sgst'], 0)
        self.assertEqual(breakdown['cess'], 10.0)
        self.assertEqual(breakdown['total'], 1010.0)
    
    def test_get_kids_clothing_taxes(self):
        """Test filtering taxes by kids clothing criteria"""
        # Create test taxes
        tax1 = self.tax_model.create({
            'name': 'Baby Tax',
            'tax_type': 'gst',
            'age_group': '0-2',
            'size': 'xs',
            'season': 'summer',
            'brand': 'Baby Brand',
            'color': 'Pink'
        })
        
        tax2 = self.tax_model.create({
            'name': 'Toddler Tax',
            'tax_type': 'gst',
            'age_group': '2-4',
            'size': 's',
            'season': 'winter',
            'brand': 'Toddler Brand',
            'color': 'Blue'
        })
        
        tax3 = self.tax_model.create({
            'name': 'All Age Tax',
            'tax_type': 'gst',
            'age_group': 'all',
            'size': 'all',
            'season': 'all_season',
            'brand': 'All Brand',
            'color': 'Green'
        })
        
        # Test filtering by age group
        baby_taxes = self.tax_model.get_kids_clothing_taxes(age_group='0-2')
        self.assertIn(tax1, baby_taxes)
        self.assertNotIn(tax2, baby_taxes)
        self.assertIn(tax3, baby_taxes)  # 'all' should match
        
        # Test filtering by size
        xs_taxes = self.tax_model.get_kids_clothing_taxes(size='xs')
        self.assertIn(tax1, xs_taxes)
        self.assertNotIn(tax2, xs_taxes)
        self.assertIn(tax3, xs_taxes)  # 'all' should match
        
        # Test filtering by season
        summer_taxes = self.tax_model.get_kids_clothing_taxes(season='summer')
        self.assertIn(tax1, summer_taxes)
        self.assertNotIn(tax2, summer_taxes)
        self.assertIn(tax3, summer_taxes)  # 'all_season' should match
        
        # Test filtering by brand
        baby_brand_taxes = self.tax_model.get_kids_clothing_taxes(brand='Baby Brand')
        self.assertIn(tax1, baby_brand_taxes)
        self.assertNotIn(tax2, baby_brand_taxes)
        self.assertNotIn(tax3, baby_brand_taxes)
        
        # Test filtering by color
        pink_taxes = self.tax_model.get_kids_clothing_taxes(color='Pink')
        self.assertIn(tax1, pink_taxes)
        self.assertNotIn(tax2, pink_taxes)
        self.assertNotIn(tax3, pink_taxes)
    
    def test_tax_types(self):
        """Test different tax types"""
        tax_types = [
            'gst',
            'cgst',
            'sgst',
            'igst',
            'cess',
            'other'
        ]
        
        for tax_type in tax_types:
            tax = self.tax_model.create({
                'name': f'Test {tax_type.title()} Tax',
                'tax_type': tax_type
            })
            self.assertEqual(tax.tax_type, tax_type)
    
    def test_gst_types(self):
        """Test different GST types"""
        gst_types = [
            'cgst',
            'sgst',
            'igst',
            'cess'
        ]
        
        for gst_type in gst_types:
            tax = self.tax_model.create({
                'name': f'Test {gst_type.upper()} Tax',
                'tax_type': 'gst',
                'gst_type': gst_type
            })
            self.assertEqual(tax.gst_type, gst_type)
    
    def test_amount_types(self):
        """Test different amount types"""
        amount_types = [
            'percent',
            'fixed'
        ]
        
        for amount_type in amount_types:
            tax = self.tax_model.create({
                'name': f'Test {amount_type.title()} Tax',
                'tax_type': 'gst',
                'amount': 18.0,
                'amount_type': amount_type
            })
            self.assertEqual(tax.amount_type, amount_type)


class TestAccountTaxGroup(OceanTestCase):
    """Test cases for AccountTaxGroup model"""
    
    def setUp(self):
        super(TestAccountTaxGroup, self).setUp()
        self.tax_group_model = self.env['account.tax.group']
    
    def test_create_gst_tax_group(self):
        """Test creating a GST tax group"""
        tax_group_vals = {
            'name': 'GST 18% Group',
            'gst_group_type': 'gst_18',
            'age_group': '4-6',
            'size': 'm',
            'season': 'all_season',
            'brand': 'Kids Brand',
            'color': 'Blue',
        }
        
        tax_group = self.tax_group_model.create(tax_group_vals)
        
        self.assertEqual(tax_group.name, 'GST 18% Group')
        self.assertEqual(tax_group.gst_group_type, 'gst_18')
        self.assertEqual(tax_group.age_group, '4-6')
        self.assertEqual(tax_group.size, 'm')
        self.assertEqual(tax_group.season, 'all_season')
        self.assertEqual(tax_group.brand, 'Kids Brand')
        self.assertEqual(tax_group.color, 'Blue')
        self.assertTrue(tax_group.active)
    
    def test_get_kids_clothing_tax_groups(self):
        """Test filtering tax groups by kids clothing criteria"""
        # Create test tax groups
        group1 = self.tax_group_model.create({
            'name': 'Baby Group',
            'gst_group_type': 'gst_5',
            'age_group': '0-2',
            'size': 'xs',
            'season': 'summer',
            'brand': 'Baby Brand',
            'color': 'Pink'
        })
        
        group2 = self.tax_group_model.create({
            'name': 'Toddler Group',
            'gst_group_type': 'gst_12',
            'age_group': '2-4',
            'size': 's',
            'season': 'winter',
            'brand': 'Toddler Brand',
            'color': 'Blue'
        })
        
        group3 = self.tax_group_model.create({
            'name': 'All Age Group',
            'gst_group_type': 'gst_18',
            'age_group': 'all',
            'size': 'all',
            'season': 'all_season',
            'brand': 'All Brand',
            'color': 'Green'
        })
        
        # Test filtering by age group
        baby_groups = self.tax_group_model.get_kids_clothing_tax_groups(age_group='0-2')
        self.assertIn(group1, baby_groups)
        self.assertNotIn(group2, baby_groups)
        self.assertIn(group3, baby_groups)  # 'all' should match
        
        # Test filtering by size
        xs_groups = self.tax_group_model.get_kids_clothing_tax_groups(size='xs')
        self.assertIn(group1, xs_groups)
        self.assertNotIn(group2, xs_groups)
        self.assertIn(group3, xs_groups)  # 'all' should match
        
        # Test filtering by season
        summer_groups = self.tax_group_model.get_kids_clothing_tax_groups(season='summer')
        self.assertIn(group1, summer_groups)
        self.assertNotIn(group2, summer_groups)
        self.assertIn(group3, summer_groups)  # 'all_season' should match
        
        # Test filtering by brand
        baby_brand_groups = self.tax_group_model.get_kids_clothing_tax_groups(brand='Baby Brand')
        self.assertIn(group1, baby_brand_groups)
        self.assertNotIn(group2, baby_brand_groups)
        self.assertNotIn(group3, baby_brand_groups)
        
        # Test filtering by color
        pink_groups = self.tax_group_model.get_kids_clothing_tax_groups(color='Pink')
        self.assertIn(group1, pink_groups)
        self.assertNotIn(group2, pink_groups)
        self.assertNotIn(group3, pink_groups)
    
    def test_gst_group_types(self):
        """Test different GST group types"""
        gst_group_types = [
            'gst_0',
            'gst_5',
            'gst_12',
            'gst_18',
            'gst_28',
            'exempt',
            'nil_rated',
            'non_gst'
        ]
        
        for gst_group_type in gst_group_types:
            tax_group = self.tax_group_model.create({
                'name': f'Test {gst_group_type.title()} Group',
                'gst_group_type': gst_group_type
            })
            self.assertEqual(tax_group.gst_group_type, gst_group_type)