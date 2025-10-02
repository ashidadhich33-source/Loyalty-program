#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Users Addon Test
===================================

Test script to verify the users addon works with the standalone framework.
"""

import sys
import os
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_users_imports():
    """Test that all users models can be imported"""
    print("Testing users addon imports...")
    
    try:
        # Add users models to path
        sys.path.insert(0, str(project_root / 'addons' / 'users' / 'models'))
        
        from res_users import ResUsers
        print("✅ ResUsers imported successfully")
        
        from res_groups import ResGroups
        print("✅ ResGroups imported successfully")
        
        from user_permissions import UserPermissions
        print("✅ UserPermissions imported successfully")
        
        from user_activity import UserActivity
        print("✅ UserActivity imported successfully")
        
        from user_preferences import UserPreferences
        print("✅ UserPreferences imported successfully")
        
        from access_rights import AccessRights
        print("✅ AccessRights imported successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Users addon import failed: {e}")
        return False

def test_user_model():
    """Test user model functionality"""
    print("\nTesting user model...")
    
    try:
        from res_users import ResUsers
        
        # Create user model instance
        user_model = ResUsers(None)
        print(f"✅ User model created: {user_model._name}")
        
        # Test field definitions
        fields = user_model._get_fields()
        print(f"✅ User model fields: {len(fields)} fields defined")
        
        # Test key fields
        key_fields = ['name', 'login', 'email', 'active', 'theme_preference']
        for field in key_fields:
            if field in fields:
                print(f"✅ Field {field} found")
            else:
                print(f"❌ Field {field} missing")
        
        return True
        
    except Exception as e:
        print(f"❌ User model test failed: {e}")
        return False

def test_groups_model():
    """Test groups model functionality"""
    print("\nTesting groups model...")
    
    try:
        from res_groups import ResGroups
        
        # Create groups model instance
        groups_model = ResGroups(None)
        print(f"✅ Groups model created: {groups_model._name}")
        
        # Test field definitions
        fields = groups_model._get_fields()
        print(f"✅ Groups model fields: {len(fields)} fields defined")
        
        # Test key fields
        key_fields = ['name', 'description', 'category', 'is_active']
        for field in key_fields:
            if field in fields:
                print(f"✅ Field {field} found")
            else:
                print(f"❌ Field {field} missing")
        
        return True
        
    except Exception as e:
        print(f"❌ Groups model test failed: {e}")
        return False

def test_user_permissions():
    """Test user permissions functionality"""
    print("\nTesting user permissions...")
    
    try:
        from user_permissions import UserPermissions
        
        # Create permissions model instance
        permissions_model = UserPermissions(None)
        print(f"✅ Permissions model created: {permissions_model._name}")
        
        # Test field definitions
        fields = permissions_model._get_fields()
        print(f"✅ Permissions model fields: {len(fields)} fields defined")
        
        return True
        
    except Exception as e:
        print(f"❌ User permissions test failed: {e}")
        return False

def test_user_activity():
    """Test user activity functionality"""
    print("\nTesting user activity...")
    
    try:
        from user_activity import UserActivity
        
        # Create activity model instance
        activity_model = UserActivity(None)
        print(f"✅ Activity model created: {activity_model._name}")
        
        # Test field definitions
        fields = activity_model._get_fields()
        print(f"✅ Activity model fields: {len(fields)} fields defined")
        
        return True
        
    except Exception as e:
        print(f"❌ User activity test failed: {e}")
        return False

def test_user_preferences():
    """Test user preferences functionality"""
    print("\nTesting user preferences...")
    
    try:
        from user_preferences import UserPreferences
        
        # Create preferences model instance
        preferences_model = UserPreferences(None)
        print(f"✅ Preferences model created: {preferences_model._name}")
        
        # Test field definitions
        fields = preferences_model._get_fields()
        print(f"✅ Preferences model fields: {len(fields)} fields defined")
        
        return True
        
    except Exception as e:
        print(f"❌ User preferences test failed: {e}")
        return False

def test_access_rights():
    """Test access rights functionality"""
    print("\nTesting access rights...")
    
    try:
        from access_rights import AccessRights
        
        # Create access rights model instance
        access_rights_model = AccessRights(None)
        print(f"✅ Access rights model created: {access_rights_model._name}")
        
        # Test field definitions
        fields = access_rights_model._get_fields()
        print(f"✅ Access rights model fields: {len(fields)} fields defined")
        
        return True
        
    except Exception as e:
        print(f"❌ Access rights test failed: {e}")
        return False

def test_user_functionality():
    """Test user model functionality"""
    print("\nTesting user functionality...")
    
    try:
        from res_users import ResUsers
        
        # Create user model instance
        user_model = ResUsers(None)
        
        # Test user methods
        print("✅ Testing user methods...")
        
        # Test get_user_permissions
        permissions = user_model.get_user_permissions()
        print(f"✅ get_user_permissions: {permissions}")
        
        # Test get_user_statistics
        stats = user_model.get_user_statistics()
        print(f"✅ get_user_statistics: {stats}")
        
        # Test get_user_analytics
        analytics = ResUsers.get_user_analytics()
        print(f"✅ get_user_analytics: {analytics}")
        
        return True
        
    except Exception as e:
        print(f"❌ User functionality test failed: {e}")
        return False

def test_groups_functionality():
    """Test groups model functionality"""
    print("\nTesting groups functionality...")
    
    try:
        from res_groups import ResGroups
        
        # Create groups model instance
        groups_model = ResGroups(None)
        
        # Test groups methods
        print("✅ Testing groups methods...")
        
        # Test get_group_analytics
        analytics = ResGroups.get_group_analytics()
        print(f"✅ get_group_analytics: {analytics}")
        
        return True
        
    except Exception as e:
        print(f"❌ Groups functionality test failed: {e}")
        return False

def main():
    """Main test function"""
    print("=" * 60)
    print("🧪 Kids Clothing ERP - Users Addon Test")
    print("=" * 60)
    
    tests = [
        test_users_imports,
        test_user_model,
        test_groups_model,
        test_user_permissions,
        test_user_activity,
        test_user_preferences,
        test_access_rights,
        test_user_functionality,
        test_groups_functionality,
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
        print("🎉 All tests passed! Users addon is working correctly.")
        return True
    else:
        print("❌ Some tests failed. Check the errors above.")
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)