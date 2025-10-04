# -*- coding: utf-8 -*-
"""
Ocean ERP - Indian Company Tests
================================

Tests for Indian company model.
"""

from core_framework.testing import OceanTestCase
from addons.l10n_in.models.res_company import ResCompany
import logging

_logger = logging.getLogger(__name__)


class TestResCompany(OceanTestCase):
    """Test cases for ResCompany model"""
    
    def setUp(self):
        super(TestResCompany, self).setUp()
        self.company_model = self.env['res.company']
    
    def test_create_company(self):
        """Test creating a company"""
        company_vals = {
            'name': 'Test Kids Clothing Company',
            'company_type': 'private_limited',
            'pan': 'ABCDE1234F',
            'gstin': '12ABCDE1234F1Z5',
            'cin': 'A12345BC6789DEF012345',
            'business_nature': 'retail',
            'industry_type': 'kids_clothing',
            'age_group': '4-6',
            'size': 'm',
            'season': 'all_season',
            'brand': 'Kids Brand',
            'color': 'Blue',
        }
        
        company = self.company_model.create(company_vals)
        
        self.assertEqual(company.name, 'Test Kids Clothing Company')
        self.assertEqual(company.company_type, 'private_limited')
        self.assertEqual(company.pan, 'ABCDE1234F')
        self.assertEqual(company.gstin, '12ABCDE1234F1Z5')
        self.assertEqual(company.cin, 'A12345BC6789DEF012345')
        self.assertEqual(company.business_nature, 'retail')
        self.assertEqual(company.industry_type, 'kids_clothing')
        self.assertEqual(company.age_group, '4-6')
        self.assertEqual(company.size, 'm')
        self.assertEqual(company.season, 'all_season')
        self.assertEqual(company.brand, 'Kids Brand')
        self.assertEqual(company.color, 'Blue')
        self.assertTrue(company.active)
    
    def test_validate_pan(self):
        """Test PAN validation"""
        company = self.company_model.create({
            'name': 'Test Company',
            'pan': 'ABCDE1234F'
        })
        
        # Valid PAN
        self.assertTrue(company.validate_pan('ABCDE1234F'))
        
        # Invalid PAN
        self.assertFalse(company.validate_pan('ABCDE123'))
        self.assertFalse(company.validate_pan('ABCDE1234G'))
        self.assertFalse(company.validate_pan('1234567890'))
    
    def test_validate_gstin(self):
        """Test GSTIN validation"""
        company = self.company_model.create({
            'name': 'Test Company',
            'gstin': '12ABCDE1234F1Z5'
        })
        
        # Valid GSTIN
        self.assertTrue(company.validate_gstin('12ABCDE1234F1Z5'))
        
        # Invalid GSTIN
        self.assertFalse(company.validate_gstin('12ABCDE1234F1Z'))
        self.assertFalse(company.validate_gstin('ABCDE1234F1Z5'))
        self.assertFalse(company.validate_gstin('12ABCDE1234F1Z6'))
    
    def test_validate_cin(self):
        """Test CIN validation"""
        company = self.company_model.create({
            'name': 'Test Company',
            'cin': 'A12345BC6789DEF012345'
        })
        
        # Valid CIN
        self.assertTrue(company.validate_cin('A12345BC6789DEF012345'))
        
        # Invalid CIN
        self.assertFalse(company.validate_cin('A12345BC6789DEF01234'))
        self.assertFalse(company.validate_cin('12345BC6789DEF012345'))
        self.assertFalse(company.validate_cin('A12345BC6789DEF0123456'))
    
    def test_get_kids_clothing_companies(self):
        """Test filtering companies by kids clothing criteria"""
        # Create test companies
        company1 = self.company_model.create({
            'name': 'Baby Company',
            'age_group': '0-2',
            'size': 'xs',
            'season': 'summer',
            'brand': 'Baby Brand',
            'color': 'Pink'
        })
        
        company2 = self.company_model.create({
            'name': 'Toddler Company',
            'age_group': '2-4',
            'size': 's',
            'season': 'winter',
            'brand': 'Toddler Brand',
            'color': 'Blue'
        })
        
        company3 = self.company_model.create({
            'name': 'All Age Company',
            'age_group': 'all',
            'size': 'all',
            'season': 'all_season',
            'brand': 'All Brand',
            'color': 'Green'
        })
        
        # Test filtering by age group
        baby_companies = self.company_model.get_kids_clothing_companies(age_group='0-2')
        self.assertIn(company1, baby_companies)
        self.assertNotIn(company2, baby_companies)
        self.assertIn(company3, baby_companies)  # 'all' should match
        
        # Test filtering by size
        xs_companies = self.company_model.get_kids_clothing_companies(size='xs')
        self.assertIn(company1, xs_companies)
        self.assertNotIn(company2, xs_companies)
        self.assertIn(company3, xs_companies)  # 'all' should match
        
        # Test filtering by season
        summer_companies = self.company_model.get_kids_clothing_companies(season='summer')
        self.assertIn(company1, summer_companies)
        self.assertNotIn(company2, summer_companies)
        self.assertIn(company3, summer_companies)  # 'all_season' should match
        
        # Test filtering by brand
        baby_brand_companies = self.company_model.get_kids_clothing_companies(brand='Baby Brand')
        self.assertIn(company1, baby_brand_companies)
        self.assertNotIn(company2, baby_brand_companies)
        self.assertNotIn(company3, baby_brand_companies)
        
        # Test filtering by color
        pink_companies = self.company_model.get_kids_clothing_companies(color='Pink')
        self.assertIn(company1, pink_companies)
        self.assertNotIn(company2, pink_companies)
        self.assertNotIn(company3, pink_companies)
    
    def test_default_values(self):
        """Test default values are set correctly"""
        company = self.company_model.create({
            'name': 'Test Company'
        })
        
        # Check default country is India
        self.assertEqual(company.country_id.code, 'IN')
        
        # Check default currency is INR
        self.assertEqual(company.currency_id.name, 'INR')
        
        # Check default fiscal year settings
        self.assertEqual(company.fiscalyear_last_day, 31)
        self.assertEqual(company.fiscalyear_last_month, '3')
    
    def test_company_types(self):
        """Test different company types"""
        company_types = [
            'private_limited',
            'public_limited',
            'partnership',
            'sole_proprietorship',
            'llp',
            'trust',
            'society',
            'ngo'
        ]
        
        for company_type in company_types:
            company = self.company_model.create({
                'name': f'Test {company_type.title()} Company',
                'company_type': company_type
            })
            self.assertEqual(company.company_type, company_type)
    
    def test_business_natures(self):
        """Test different business natures"""
        business_natures = [
            'manufacturing',
            'trading',
            'service',
            'retail',
            'wholesale',
            'ecommerce',
            'franchise'
        ]
        
        for business_nature in business_natures:
            company = self.company_model.create({
                'name': f'Test {business_nature.title()} Company',
                'business_nature': business_nature
            })
            self.assertEqual(company.business_nature, business_nature)
    
    def test_industry_types(self):
        """Test different industry types"""
        industry_types = [
            'textiles',
            'garments',
            'kids_clothing',
            'fashion',
            'retail',
            'wholesale',
            'ecommerce',
            'other'
        ]
        
        for industry_type in industry_types:
            company = self.company_model.create({
                'name': f'Test {industry_type.title()} Company',
                'industry_type': industry_type
            })
            self.assertEqual(company.industry_type, industry_type)