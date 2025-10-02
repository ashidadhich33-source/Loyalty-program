#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Company Addon Test
=====================================

Test script to verify the company addon works with the standalone framework.
"""

import sys
import os
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_company_imports():
    """Test that all company models can be imported"""
    print("Testing company addon imports...")
    
    try:
        # Add company models to path
        sys.path.insert(0, str(project_root / 'addons' / 'company' / 'models'))
        
        from res_company import ResCompany
        print("✅ ResCompany imported successfully")
        
        from company_branch import CompanyBranch
        print("✅ CompanyBranch imported successfully")
        
        from company_location import CompanyLocation
        print("✅ CompanyLocation imported successfully")
        
        from financial_year import FinancialYear
        print("✅ FinancialYear imported successfully")
        
        from company_settings import CompanySettings
        print("✅ CompanySettings imported successfully")
        
        from company_analytics import CompanyAnalytics
        print("✅ CompanyAnalytics imported successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Company addon import failed: {e}")
        return False

def test_company_model():
    """Test company model functionality"""
    print("\nTesting company model...")
    
    try:
        from res_company import ResCompany
        
        # Create company model instance
        company_model = ResCompany(None)
        print(f"✅ Company model created: {company_model._name}")
        
        # Test field definitions
        fields = company_model._get_fields()
        print(f"✅ Company model fields: {len(fields)} fields defined")
        
        # Test key fields
        key_fields = ['name', 'company_type', 'business_nature', 'gstin', 'is_active']
        for field in key_fields:
            if field in fields:
                print(f"✅ Field {field} found")
            else:
                print(f"❌ Field {field} missing")
        
        return True
        
    except Exception as e:
        print(f"❌ Company model test failed: {e}")
        return False

def test_company_branch_model():
    """Test company branch model functionality"""
    print("\nTesting company branch model...")
    
    try:
        from company_branch import CompanyBranch
        
        # Create branch model instance
        branch_model = CompanyBranch(None)
        print(f"✅ Branch model created: {branch_model._name}")
        
        # Test field definitions
        fields = branch_model._get_fields()
        print(f"✅ Branch model fields: {len(fields)} fields defined")
        
        # Test key fields
        key_fields = ['name', 'code', 'company_id', 'branch_type', 'is_active']
        for field in key_fields:
            if field in fields:
                print(f"✅ Field {field} found")
            else:
                print(f"❌ Field {field} missing")
        
        return True
        
    except Exception as e:
        print(f"❌ Company branch model test failed: {e}")
        return False

def test_company_location_model():
    """Test company location model functionality"""
    print("\nTesting company location model...")
    
    try:
        from company_location import CompanyLocation
        
        # Create location model instance
        location_model = CompanyLocation(None)
        print(f"✅ Location model created: {location_model._name}")
        
        # Test field definitions
        fields = location_model._get_fields()
        print(f"✅ Location model fields: {len(fields)} fields defined")
        
        return True
        
    except Exception as e:
        print(f"❌ Company location model test failed: {e}")
        return False

def test_financial_year_model():
    """Test financial year model functionality"""
    print("\nTesting financial year model...")
    
    try:
        from financial_year import FinancialYear
        
        # Create financial year model instance
        fy_model = FinancialYear(None)
        print(f"✅ Financial year model created: {fy_model._name}")
        
        # Test field definitions
        fields = fy_model._get_fields()
        print(f"✅ Financial year model fields: {len(fields)} fields defined")
        
        return True
        
    except Exception as e:
        print(f"❌ Financial year model test failed: {e}")
        return False

def test_company_settings_model():
    """Test company settings model functionality"""
    print("\nTesting company settings model...")
    
    try:
        from company_settings import CompanySettings
        
        # Create settings model instance
        settings_model = CompanySettings(None)
        print(f"✅ Settings model created: {settings_model._name}")
        
        # Test field definitions
        fields = settings_model._get_fields()
        print(f"✅ Settings model fields: {len(fields)} fields defined")
        
        return True
        
    except Exception as e:
        print(f"❌ Company settings model test failed: {e}")
        return False

def test_company_analytics_model():
    """Test company analytics model functionality"""
    print("\nTesting company analytics model...")
    
    try:
        from company_analytics import CompanyAnalytics
        
        # Create analytics model instance
        analytics_model = CompanyAnalytics(None)
        print(f"✅ Analytics model created: {analytics_model._name}")
        
        # Test field definitions
        fields = analytics_model._get_fields()
        print(f"✅ Analytics model fields: {len(fields)} fields defined")
        
        return True
        
    except Exception as e:
        print(f"❌ Company analytics model test failed: {e}")
        return False

def test_company_functionality():
    """Test company model functionality"""
    print("\nTesting company functionality...")
    
    try:
        from res_company import ResCompany
        
        # Create company model instance
        company_model = ResCompany(None)
        
        # Test company methods
        print("✅ Testing company methods...")
        
        # Test get_company_analytics
        analytics = company_model.get_company_analytics()
        print(f"✅ get_company_analytics: {analytics}")
        
        # Test get_company_analytics_summary
        summary = ResCompany.get_company_analytics_summary()
        print(f"✅ get_company_analytics_summary: {summary}")
        
        return True
        
    except Exception as e:
        print(f"❌ Company functionality test failed: {e}")
        return False

def test_company_branch_functionality():
    """Test company branch model functionality"""
    print("\nTesting company branch functionality...")
    
    try:
        from company_branch import CompanyBranch
        
        # Create branch model instance
        branch_model = CompanyBranch(None)
        
        # Test branch methods
        print("✅ Testing branch methods...")
        
        # Test get_branch_analytics
        analytics = branch_model.get_branch_analytics()
        print(f"✅ get_branch_analytics: {analytics}")
        
        # Test get_branch_analytics_summary
        summary = CompanyBranch.get_branch_analytics_summary()
        print(f"✅ get_branch_analytics_summary: {summary}")
        
        return True
        
    except Exception as e:
        print(f"❌ Company branch functionality test failed: {e}")
        return False

def test_company_location_functionality():
    """Test company location model functionality"""
    print("\nTesting company location functionality...")
    
    try:
        from company_location import CompanyLocation
        
        # Create location model instance
        location_model = CompanyLocation(None)
        
        # Test location methods
        print("✅ Testing location methods...")
        
        # Test get_location_analytics
        analytics = location_model.get_location_analytics()
        print(f"✅ get_location_analytics: {analytics}")
        
        # Test get_location_analytics_summary
        summary = CompanyLocation.get_location_analytics_summary()
        print(f"✅ get_location_analytics_summary: {summary}")
        
        return True
        
    except Exception as e:
        print(f"❌ Company location functionality test failed: {e}")
        return False

def test_financial_year_functionality():
    """Test financial year model functionality"""
    print("\nTesting financial year functionality...")
    
    try:
        from financial_year import FinancialYear
        
        # Create financial year model instance
        fy_model = FinancialYear(None)
        
        # Test financial year methods
        print("✅ Testing financial year methods...")
        
        # Test get_financial_year_analytics
        analytics = fy_model.get_financial_year_analytics()
        print(f"✅ get_financial_year_analytics: {analytics}")
        
        # Test get_financial_year_analytics_summary
        summary = FinancialYear.get_financial_year_analytics_summary()
        print(f"✅ get_financial_year_analytics_summary: {summary}")
        
        return True
        
    except Exception as e:
        print(f"❌ Financial year functionality test failed: {e}")
        return False

def test_company_settings_functionality():
    """Test company settings model functionality"""
    print("\nTesting company settings functionality...")
    
    try:
        from company_settings import CompanySettings
        
        # Create settings model instance
        settings_model = CompanySettings(None)
        
        # Test settings methods
        print("✅ Testing settings methods...")
        
        # Test get_setting_info
        info = settings_model.get_setting_info()
        print(f"✅ get_setting_info: {info}")
        
        # Test get_setting_analytics
        analytics = CompanySettings.get_setting_analytics()
        print(f"✅ get_setting_analytics: {analytics}")
        
        return True
        
    except Exception as e:
        print(f"❌ Company settings functionality test failed: {e}")
        return False

def test_company_analytics_functionality():
    """Test company analytics model functionality"""
    print("\nTesting company analytics functionality...")
    
    try:
        from company_analytics import CompanyAnalytics
        
        # Create analytics model instance
        analytics_model = CompanyAnalytics(None)
        
        # Test analytics methods
        print("✅ Testing analytics methods...")
        
        # Test get_analytics_summary
        summary = analytics_model.get_analytics_summary()
        print(f"✅ get_analytics_summary: {summary}")
        
        # Test get_analytics_analytics
        analytics = CompanyAnalytics.get_analytics_analytics()
        print(f"✅ get_analytics_analytics: {analytics}")
        
        return True
        
    except Exception as e:
        print(f"❌ Company analytics functionality test failed: {e}")
        return False

def main():
    """Main test function"""
    print("=" * 60)
    print("🧪 Kids Clothing ERP - Company Addon Test")
    print("=" * 60)
    
    tests = [
        test_company_imports,
        test_company_model,
        test_company_branch_model,
        test_company_location_model,
        test_financial_year_model,
        test_company_settings_model,
        test_company_analytics_model,
        test_company_functionality,
        test_company_branch_functionality,
        test_company_location_functionality,
        test_financial_year_functionality,
        test_company_settings_functionality,
        test_company_analytics_functionality,
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 60)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Company addon is working correctly.")
        return True
    else:
        print("❌ Some tests failed. Check the errors above.")
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)