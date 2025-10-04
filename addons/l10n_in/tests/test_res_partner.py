# -*- coding: utf-8 -*-
"""
Ocean ERP - Indian Localization Partner Tests
=============================================

Tests for Indian localization partner models.
"""

from core_framework.testing import OceanTestCase
from addons.l10n_in.models.res_partner import ResPartner
import logging

_logger = logging.getLogger(__name__)


class TestResPartner(OceanTestCase):
    """Test cases for ResPartner model"""
    
    def setUp(self):
        super(TestResPartner, self).setUp()
        self.partner_model = self.env['res.partner']
    
    def test_create_partner(self):
        """Test creating a partner"""
        partner_vals = {
            'name': 'Test Partner',
            'partner_type': 'customer',
            'pan': 'ABCDE1234F',
            'gstin': '27ABCDE1234F1Z5',
            'aadhar': '123456789012',
            'business_nature': 'retail',
            'industry_type': 'kids_clothing',
            'age_group': '4-6',
            'size': 'm',
            'season': 'all_season',
            'brand': 'Kids Brand',
            'color': 'Blue',
        }
        
        partner = self.partner_model.create(partner_vals)
        
        self.assertEqual(partner.name, 'Test Partner')
        self.assertEqual(partner.partner_type, 'customer')
        self.assertEqual(partner.pan, 'ABCDE1234F')
        self.assertEqual(partner.gstin, '27ABCDE1234F1Z5')
        self.assertEqual(partner.aadhar, '123456789012')
        self.assertEqual(partner.business_nature, 'retail')
        self.assertEqual(partner.industry_type, 'kids_clothing')
        self.assertEqual(partner.age_group, '4-6')
        self.assertEqual(partner.size, 'm')
        self.assertEqual(partner.season, 'all_season')
        self.assertEqual(partner.brand, 'Kids Brand')
        self.assertEqual(partner.color, 'Blue')
        self.assertTrue(partner.active)
    
    def test_validate_pan(self):
        """Test PAN validation"""
        partner = self.partner_model.create({
            'name': 'Test Partner',
            'pan': 'ABCDE1234F'
        })
        
        # Valid PAN
        self.assertTrue(partner.validate_pan('ABCDE1234F'))
        
        # Invalid PAN
        self.assertFalse(partner.validate_pan('ABCDE123'))
        self.assertFalse(partner.validate_pan('ABCDE1234G'))
        self.assertFalse(partner.validate_pan('1234567890'))
    
    def test_validate_gstin(self):
        """Test GSTIN validation"""
        partner = self.partner_model.create({
            'name': 'Test Partner',
            'gstin': '27ABCDE1234F1Z5'
        })
        
        # Valid GSTIN
        self.assertTrue(partner.validate_gstin('27ABCDE1234F1Z5'))
        
        # Invalid GSTIN
        self.assertFalse(partner.validate_gstin('27ABCDE1234F1Z'))
        self.assertFalse(partner.validate_gstin('27ABCDE1234F1Z6'))
        self.assertFalse(partner.validate_gstin('ABCDE1234F1Z5'))
    
    def test_validate_aadhar(self):
        """Test Aadhar validation"""
        partner = self.partner_model.create({
            'name': 'Test Partner',
            'aadhar': '123456789012'
        })
        
        # Valid Aadhar
        self.assertTrue(partner.validate_aadhar('123456789012'))
        
        # Invalid Aadhar
        self.assertFalse(partner.validate_aadhar('12345678901'))
        self.assertFalse(partner.validate_aadhar('1234567890123'))
        self.assertFalse(partner.validate_aadhar('ABCD123456789'))
    
    def test_get_kids_clothing_partners(self):
        """Test filtering partners by kids clothing criteria"""
        # Create test partners
        partner1 = self.partner_model.create({
            'name': 'Baby Partner',
            'partner_type': 'customer',
            'age_group': '0-2',
            'size': 'xs',
            'season': 'summer',
            'brand': 'Baby Brand',
            'color': 'Pink'
        })
        
        partner2 = self.partner_model.create({
            'name': 'Toddler Partner',
            'partner_type': 'supplier',
            'age_group': '2-4',
            'size': 's',
            'season': 'winter',
            'brand': 'Toddler Brand',
            'color': 'Blue'
        })
        
        partner3 = self.partner_model.create({
            'name': 'All Age Partner',
            'partner_type': 'both',
            'age_group': 'all',
            'size': 'all',
            'season': 'all_season',
            'brand': 'All Brand',
            'color': 'Green'
        })
        
        # Test filtering by age group
        baby_partners = self.partner_model.get_kids_clothing_partners(age_group='0-2')
        self.assertIn(partner1, baby_partners)
        self.assertNotIn(partner2, baby_partners)
        self.assertIn(partner3, baby_partners)  # 'all' should match
        
        # Test filtering by size
        xs_partners = self.partner_model.get_kids_clothing_partners(size='xs')
        self.assertIn(partner1, xs_partners)
        self.assertNotIn(partner2, xs_partners)
        self.assertIn(partner3, xs_partners)  # 'all' should match
        
        # Test filtering by season
        summer_partners = self.partner_model.get_kids_clothing_partners(season='summer')
        self.assertIn(partner1, summer_partners)
        self.assertNotIn(partner2, summer_partners)
        self.assertIn(partner3, summer_partners)  # 'all_season' should match
        
        # Test filtering by brand
        baby_brand_partners = self.partner_model.get_kids_clothing_partners(brand='Baby Brand')
        self.assertIn(partner1, baby_brand_partners)
        self.assertNotIn(partner2, baby_brand_partners)
        self.assertNotIn(partner3, baby_brand_partners)
        
        # Test filtering by color
        pink_partners = self.partner_model.get_kids_clothing_partners(color='Pink')
        self.assertIn(partner1, pink_partners)
        self.assertNotIn(partner2, pink_partners)
        self.assertNotIn(partner3, pink_partners)
    
    def test_partner_types(self):
        """Test different partner types"""
        partner_types = [
            'customer',
            'supplier',
            'both'
        ]
        
        for partner_type in partner_types:
            partner = self.partner_model.create({
                'name': f'Test {partner_type.title()} Partner',
                'partner_type': partner_type
            })
            self.assertEqual(partner.partner_type, partner_type)
    
    def test_business_nature_types(self):
        """Test different business nature types"""
        business_natures = [
            'retail',
            'wholesale',
            'manufacturing',
            'service',
            'other'
        ]
        
        for business_nature in business_natures:
            partner = self.partner_model.create({
                'name': f'Test {business_nature.title()} Partner',
                'partner_type': 'customer',
                'business_nature': business_nature
            })
            self.assertEqual(partner.business_nature, business_nature)
    
    def test_industry_type_types(self):
        """Test different industry type types"""
        industry_types = [
            'kids_clothing',
            'textiles',
            'retail',
            'manufacturing',
            'other'
        ]
        
        for industry_type in industry_types:
            partner = self.partner_model.create({
                'name': f'Test {industry_type.title()} Partner',
                'partner_type': 'customer',
                'industry_type': industry_type
            })
            self.assertEqual(partner.industry_type, industry_type)