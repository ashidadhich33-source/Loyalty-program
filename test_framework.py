#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Framework Test
================================

Test script to verify the standalone ERP framework works.
"""

import sys
import os
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_imports():
    """Test that all core modules can be imported"""
    print("Testing imports...")
    
    try:
        from core_framework.config import Config
        print("✅ Config imported successfully")
    except Exception as e:
        print(f"❌ Config import failed: {e}")
        return False
    
    try:
        from core_framework.database import DatabaseManager
        print("✅ DatabaseManager imported successfully")
    except Exception as e:
        print(f"❌ DatabaseManager import failed: {e}")
        return False
    
    try:
        from core_framework.orm import BaseModel, CharField, IntegerField, BooleanField
        print("✅ ORM imported successfully")
    except Exception as e:
        print(f"❌ ORM import failed: {e}")
        return False
    
    try:
        from core_framework.addon_manager import AddonManager
        print("✅ AddonManager imported successfully")
    except Exception as e:
        print(f"❌ AddonManager import failed: {e}")
        return False
    
    try:
        from core_framework.web_interface import WebInterface
        print("✅ WebInterface imported successfully")
    except Exception as e:
        print(f"❌ WebInterface import failed: {e}")
        return False
    
    return True

def test_config():
    """Test configuration system"""
    print("\nTesting configuration...")
    
    try:
        from core_framework.config import Config
        config = Config()
        
        # Test basic config access
        db_host = config.get('database.host')
        print(f"✅ Database host: {db_host}")
        
        # Test config setting
        config.set('test.value', 'test_data')
        test_value = config.get('test.value')
        print(f"✅ Test value: {test_value}")
        
        return True
    except Exception as e:
        print(f"❌ Config test failed: {e}")
        return False

def test_orm():
    """Test ORM system"""
    print("\nTesting ORM...")
    
    try:
        from core_framework.orm import BaseModel, CharField, IntegerField, BooleanField
        
        # Create a test model
        class TestModel(BaseModel):
            _name = 'test.model'
            _description = 'Test Model'
            _table = 'test_model'
            
            name = CharField(string='Name', size=100)
            age = IntegerField(string='Age')
            active = BooleanField(string='Active', default=True)
        
        print("✅ Test model created successfully")
        
        # Test field definitions
        fields = TestModel._get_fields()
        print(f"✅ Model fields: {list(fields.keys())}")
        
        return True
    except Exception as e:
        print(f"❌ ORM test failed: {e}")
        return False

def test_addon_loading():
    """Test addon loading"""
    print("\nTesting addon loading...")
    
    try:
        from core_framework.config import Config
        from core_framework.addon_manager import AddonManager
        
        config = Config()
        addon_manager = AddonManager(config)
        
        # Test addon scanning
        addon_dirs = addon_manager._scan_addon_directories()
        print(f"✅ Found addon directories: {addon_dirs}")
        
        return True
    except Exception as e:
        print(f"❌ Addon loading test failed: {e}")
        return False

def test_core_base_models():
    """Test core_base models"""
    print("\nTesting core_base models...")
    
    try:
        # Import core_base models
        sys.path.insert(0, str(project_root / 'addons' / 'core_base' / 'models'))
        
        from res_config import ResConfigSettings
        from base_mixins import KidsClothingMixin, AgeGroupMixin
        from system_utils import SystemUtils
        
        print("✅ Core base models imported successfully")
        
        # Test model creation
        config_model = ResConfigSettings(None)
        print(f"✅ Config model created: {config_model._name}")
        
        # Test mixin
        mixin = KidsClothingMixin(None)
        print(f"✅ Mixin created: {mixin._name}")
        
        # Test system utils
        utils = SystemUtils(None)
        age_group = utils.get_age_group_from_months(24)
        print(f"✅ System utils working: age group for 24 months = {age_group}")
        
        return True
    except Exception as e:
        print(f"❌ Core base models test failed: {e}")
        return False

def main():
    """Main test function"""
    print("=" * 60)
    print("🧪 Kids Clothing ERP - Framework Test")
    print("=" * 60)
    
    tests = [
        test_imports,
        test_config,
        test_orm,
        test_addon_loading,
        test_core_base_models,
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
        print("🎉 All tests passed! Framework is working correctly.")
        return True
    else:
        print("❌ Some tests failed. Check the errors above.")
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)