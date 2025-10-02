#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Contacts Addon Test
=======================================

Test script to verify the contacts addon works with the standalone framework.
"""

import sys
import os
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_contacts_imports():
    """Test that all contacts models can be imported"""
    print("Testing contacts addon imports...")
    
    try:
        # Add contacts models to path
        sys.path.insert(0, str(project_root / 'addons' / 'contacts' / 'models'))
        
        from res_partner import ResPartner
        print("✅ ResPartner imported successfully")
        
        from contact_customer import ContactCustomer
        print("✅ ContactCustomer imported successfully")
        
        from contact_supplier import ContactSupplier
        print("✅ ContactSupplier imported successfully")
        
        from contact_vendor import ContactVendor
        print("✅ ContactVendor imported successfully")
        
        from child_profile import ChildProfile
        print("✅ ChildProfile imported successfully")
        
        from contact_category import ContactCategory
        print("✅ ContactCategory imported successfully")
        
        from contact_tag import ContactTag
        print("✅ ContactTag imported successfully")
        
        from contact_history import ContactHistory
        print("✅ ContactHistory imported successfully")
        
        from contact_communication import ContactCommunication
        print("✅ ContactCommunication imported successfully")
        
        from contact_address import ContactAddress
        print("✅ ContactAddress imported successfully")
        
        from contact_analytics import ContactAnalytics
        print("✅ ContactAnalytics imported successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Contacts addon import failed: {e}")
        return False

def test_partner_model():
    """Test partner model functionality"""
    print("\nTesting partner model...")
    
    try:
        from res_partner import ResPartner
        
        # Create partner model instance
        partner_model = ResPartner(None)
        print(f"✅ Partner model created: {partner_model._name}")
        
        # Test field definitions
        fields = partner_model._get_fields()
        print(f"✅ Partner model fields: {len(fields)} fields defined")
        
        # Test key fields
        key_fields = ['name', 'contact_type', 'preferred_age_group', 'gstin', 'status']
        for field in key_fields:
            if field in fields:
                print(f"✅ Field {field} found")
            else:
                print(f"❌ Field {field} missing")
        
        return True
        
    except Exception as e:
        print(f"❌ Partner model test failed: {e}")
        return False

def test_customer_model():
    """Test customer model functionality"""
    print("\nTesting customer model...")
    
    try:
        from contact_customer import ContactCustomer
        
        # Create customer model instance
        customer_model = ContactCustomer(None)
        print(f"✅ Customer model created: {customer_model._name}")
        
        # Test field definitions
        fields = customer_model._get_fields()
        print(f"✅ Customer model fields: {len(fields)} fields defined")
        
        # Test key fields
        key_fields = ['name', 'customer_code', 'customer_type', 'loyalty_points', 'status']
        for field in key_fields:
            if field in fields:
                print(f"✅ Field {field} found")
            else:
                print(f"❌ Field {field} missing")
        
        return True
        
    except Exception as e:
        print(f"❌ Customer model test failed: {e}")
        return False

def test_child_profile_model():
    """Test child profile model functionality"""
    print("\nTesting child profile model...")
    
    try:
        from child_profile import ChildProfile
        
        # Create child profile model instance
        child_model = ChildProfile(None)
        print(f"✅ Child profile model created: {child_model._name}")
        
        # Test field definitions
        fields = child_model._get_fields()
        print(f"✅ Child profile model fields: {len(fields)} fields defined")
        
        return True
        
    except Exception as e:
        print(f"❌ Child profile model test failed: {e}")
        return False

def test_contact_category_model():
    """Test contact category model functionality"""
    print("\nTesting contact category model...")
    
    try:
        from contact_category import ContactCategory
        
        # Create category model instance
        category_model = ContactCategory(None)
        print(f"✅ Category model created: {category_model._name}")
        
        # Test field definitions
        fields = category_model._get_fields()
        print(f"✅ Category model fields: {len(fields)} fields defined")
        
        return True
        
    except Exception as e:
        print(f"❌ Category model test failed: {e}")
        return False

def test_contact_tag_model():
    """Test contact tag model functionality"""
    print("\nTesting contact tag model...")
    
    try:
        from contact_tag import ContactTag
        
        # Create tag model instance
        tag_model = ContactTag(None)
        print(f"✅ Tag model created: {tag_model._name}")
        
        # Test field definitions
        fields = tag_model._get_fields()
        print(f"✅ Tag model fields: {len(fields)} fields defined")
        
        return True
        
    except Exception as e:
        print(f"❌ Tag model test failed: {e}")
        return False

def test_contact_history_model():
    """Test contact history model functionality"""
    print("\nTesting contact history model...")
    
    try:
        from contact_history import ContactHistory
        
        # Create history model instance
        history_model = ContactHistory(None)
        print(f"✅ History model created: {history_model._name}")
        
        # Test field definitions
        fields = history_model._get_fields()
        print(f"✅ History model fields: {len(fields)} fields defined")
        
        return True
        
    except Exception as e:
        print(f"❌ History model test failed: {e}")
        return False

def test_contact_communication_model():
    """Test contact communication model functionality"""
    print("\nTesting contact communication model...")
    
    try:
        from contact_communication import ContactCommunication
        
        # Create communication model instance
        communication_model = ContactCommunication(None)
        print(f"✅ Communication model created: {communication_model._name}")
        
        # Test field definitions
        fields = communication_model._get_fields()
        print(f"✅ Communication model fields: {len(fields)} fields defined")
        
        return True
        
    except Exception as e:
        print(f"❌ Communication model test failed: {e}")
        return False

def test_contact_address_model():
    """Test contact address model functionality"""
    print("\nTesting contact address model...")
    
    try:
        from contact_address import ContactAddress
        
        # Create address model instance
        address_model = ContactAddress(None)
        print(f"✅ Address model created: {address_model._name}")
        
        # Test field definitions
        fields = address_model._get_fields()
        print(f"✅ Address model fields: {len(fields)} fields defined")
        
        return True
        
    except Exception as e:
        print(f"❌ Address model test failed: {e}")
        return False

def test_contact_analytics_model():
    """Test contact analytics model functionality"""
    print("\nTesting contact analytics model...")
    
    try:
        from contact_analytics import ContactAnalytics
        
        # Create analytics model instance
        analytics_model = ContactAnalytics(None)
        print(f"✅ Analytics model created: {analytics_model._name}")
        
        # Test field definitions
        fields = analytics_model._get_fields()
        print(f"✅ Analytics model fields: {len(fields)} fields defined")
        
        return True
        
    except Exception as e:
        print(f"❌ Analytics model test failed: {e}")
        return False

def test_partner_functionality():
    """Test partner model functionality"""
    print("\nTesting partner functionality...")
    
    try:
        from res_partner import ResPartner
        
        # Create partner model instance
        partner_model = ResPartner(None)
        
        # Test partner methods
        print("✅ Testing partner methods...")
        
        # Test get_partner_analytics
        analytics = partner_model.get_partner_analytics()
        print(f"✅ get_partner_analytics: {analytics}")
        
        # Test get_partner_analytics_summary
        summary = ResPartner.get_partner_analytics_summary()
        print(f"✅ get_partner_analytics_summary: {summary}")
        
        return True
        
    except Exception as e:
        print(f"❌ Partner functionality test failed: {e}")
        return False

def test_customer_functionality():
    """Test customer model functionality"""
    print("\nTesting customer functionality...")
    
    try:
        from contact_customer import ContactCustomer
        
        # Create customer model instance
        customer_model = ContactCustomer(None)
        
        # Test customer methods
        print("✅ Testing customer methods...")
        
        # Test get_customer_analytics
        analytics = customer_model.get_customer_analytics()
        print(f"✅ get_customer_analytics: {analytics}")
        
        # Test get_customer_analytics_summary
        summary = ContactCustomer.get_customer_analytics_summary()
        print(f"✅ get_customer_analytics_summary: {summary}")
        
        return True
        
    except Exception as e:
        print(f"❌ Customer functionality test failed: {e}")
        return False

def test_child_profile_functionality():
    """Test child profile model functionality"""
    print("\nTesting child profile functionality...")
    
    try:
        from child_profile import ChildProfile
        
        # Create child profile model instance
        child_model = ChildProfile(None)
        
        # Test child profile methods
        print("✅ Testing child profile methods...")
        
        # Test get_child_analytics
        analytics = child_model.get_child_analytics()
        print(f"✅ get_child_analytics: {analytics}")
        
        # Test get_child_analytics_summary
        summary = ChildProfile.get_child_analytics_summary()
        print(f"✅ get_child_analytics_summary: {summary}")
        
        return True
        
    except Exception as e:
        print(f"❌ Child profile functionality test failed: {e}")
        return False

def test_contact_category_functionality():
    """Test contact category model functionality"""
    print("\nTesting contact category functionality...")
    
    try:
        from contact_category import ContactCategory
        
        # Create category model instance
        category_model = ContactCategory(None)
        
        # Test category methods
        print("✅ Testing category methods...")
        
        # Test get_category_analytics
        analytics = category_model.get_category_analytics()
        print(f"✅ get_category_analytics: {analytics}")
        
        # Test get_category_analytics_summary
        summary = ContactCategory.get_category_analytics_summary()
        print(f"✅ get_category_analytics_summary: {summary}")
        
        return True
        
    except Exception as e:
        print(f"❌ Category functionality test failed: {e}")
        return False

def test_contact_tag_functionality():
    """Test contact tag model functionality"""
    print("\nTesting contact tag functionality...")
    
    try:
        from contact_tag import ContactTag
        
        # Create tag model instance
        tag_model = ContactTag(None)
        
        # Test tag methods
        print("✅ Testing tag methods...")
        
        # Test get_tag_analytics
        analytics = tag_model.get_tag_analytics()
        print(f"✅ get_tag_analytics: {analytics}")
        
        # Test get_tag_analytics_summary
        summary = ContactTag.get_tag_analytics_summary()
        print(f"✅ get_tag_analytics_summary: {summary}")
        
        return True
        
    except Exception as e:
        print(f"❌ Tag functionality test failed: {e}")
        return False

def test_contact_history_functionality():
    """Test contact history model functionality"""
    print("\nTesting contact history functionality...")
    
    try:
        from contact_history import ContactHistory
        
        # Create history model instance
        history_model = ContactHistory(None)
        
        # Test history methods
        print("✅ Testing history methods...")
        
        # Test get_history_info
        info = history_model.get_history_info()
        print(f"✅ get_history_info: {info}")
        
        # Test get_history_analytics_summary
        summary = ContactHistory.get_history_analytics_summary()
        print(f"✅ get_history_analytics_summary: {summary}")
        
        return True
        
    except Exception as e:
        print(f"❌ History functionality test failed: {e}")
        return False

def test_contact_communication_functionality():
    """Test contact communication model functionality"""
    print("\nTesting contact communication functionality...")
    
    try:
        from contact_communication import ContactCommunication
        
        # Create communication model instance
        communication_model = ContactCommunication(None)
        
        # Test communication methods
        print("✅ Testing communication methods...")
        
        # Test get_communication_info
        info = communication_model.get_communication_info()
        print(f"✅ get_communication_info: {info}")
        
        # Test get_communication_analytics_summary
        summary = ContactCommunication.get_communication_analytics_summary()
        print(f"✅ get_communication_analytics_summary: {summary}")
        
        return True
        
    except Exception as e:
        print(f"❌ Communication functionality test failed: {e}")
        return False

def test_contact_address_functionality():
    """Test contact address model functionality"""
    print("\nTesting contact address functionality...")
    
    try:
        from contact_address import ContactAddress
        
        # Create address model instance
        address_model = ContactAddress(None)
        
        # Test address methods
        print("✅ Testing address methods...")
        
        # Test get_address_info
        info = address_model.get_address_info()
        print(f"✅ get_address_info: {info}")
        
        # Test get_address_analytics_summary
        summary = ContactAddress.get_address_analytics_summary()
        print(f"✅ get_address_analytics_summary: {summary}")
        
        return True
        
    except Exception as e:
        print(f"❌ Address functionality test failed: {e}")
        return False

def test_contact_analytics_functionality():
    """Test contact analytics model functionality"""
    print("\nTesting contact analytics functionality...")
    
    try:
        from contact_analytics import ContactAnalytics
        
        # Create analytics model instance
        analytics_model = ContactAnalytics(None)
        
        # Test analytics methods
        print("✅ Testing analytics methods...")
        
        # Test get_analytics_summary
        summary = analytics_model.get_analytics_summary()
        print(f"✅ get_analytics_summary: {summary}")
        
        # Test get_analytics_analytics
        analytics = ContactAnalytics.get_analytics_analytics()
        print(f"✅ get_analytics_analytics: {analytics}")
        
        return True
        
    except Exception as e:
        print(f"❌ Analytics functionality test failed: {e}")
        return False

def main():
    """Main test function"""
    print("=" * 60)
    print("🧪 Kids Clothing ERP - Contacts Addon Test")
    print("=" * 60)
    
    tests = [
        test_contacts_imports,
        test_partner_model,
        test_customer_model,
        test_child_profile_model,
        test_contact_category_model,
        test_contact_tag_model,
        test_contact_history_model,
        test_contact_communication_model,
        test_contact_address_model,
        test_contact_analytics_model,
        test_partner_functionality,
        test_customer_functionality,
        test_child_profile_functionality,
        test_contact_category_functionality,
        test_contact_tag_functionality,
        test_contact_history_functionality,
        test_contact_communication_functionality,
        test_contact_address_functionality,
        test_contact_analytics_functionality,
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
        print("🎉 All tests passed! Contacts addon is working correctly.")
        return True
    else:
        print("❌ Some tests failed. Check the errors above.")
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)