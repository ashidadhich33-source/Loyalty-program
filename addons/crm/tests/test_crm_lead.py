# -*- coding: utf-8 -*-

from core_framework.testing import TestCase


class TestCrmLead(TestCase):
    
    def setUp(self):
        super(TestCrmLead, self).setUp()
        self.lead = self.env['crm.lead']
    
    def test_create_lead(self):
        """Test creating a CRM lead"""
        lead = self.lead.create({
            'name': 'Test Lead',
            'partner_name': 'Test Partner',
            'email': 'test@example.com',
            'phone': '+1-555-0123',
            'type': 'lead',
            'priority': '1',
            'probability': 25,
            'expected_revenue': 1000.00,
            'child_count': 2,
            'child_ages': '3,5',
            'age_group_interest': 'toddler',
            'gender_preference': 'boys',
            'seasonal_interest': 'summer',
            'description': 'Test lead description',
        })
        
        self.assertEqual(lead.name, 'Test Lead')
        self.assertEqual(lead.partner_name, 'Test Partner')
        self.assertEqual(lead.email, 'test@example.com')
        self.assertEqual(lead.phone, '+1-555-0123')
        self.assertEqual(lead.type, 'lead')
        self.assertEqual(lead.priority, '1')
        self.assertEqual(lead.probability, 25)
        self.assertEqual(lead.expected_revenue, 1000.00)
        self.assertEqual(lead.child_count, 2)
        self.assertEqual(lead.child_ages, '3,5')
        self.assertEqual(lead.age_group_interest, 'toddler')
        self.assertEqual(lead.gender_preference, 'boys')
        self.assertEqual(lead.seasonal_interest, 'summer')
        self.assertEqual(lead.description, 'Test lead description')
        self.assertTrue(lead.is_active)
        self.assertFalse(lead.is_converted)
    
    def test_convert_lead_to_customer(self):
        """Test converting a lead to customer"""
        lead = self.lead.create({
            'name': 'Test Lead',
            'partner_name': 'Test Partner',
            'email': 'test@example.com',
            'phone': '+1-555-0123',
            'type': 'lead',
        })
        
        lead.action_convert_to_customer()
        
        self.assertTrue(lead.is_converted)
        self.assertEqual(lead.type, 'customer')
    
    def test_convert_lead_to_opportunity(self):
        """Test converting a lead to opportunity"""
        lead = self.lead.create({
            'name': 'Test Lead',
            'partner_name': 'Test Partner',
            'email': 'test@example.com',
            'phone': '+1-555-0123',
            'type': 'lead',
        })
        
        lead.action_convert_to_opportunity()
        
        self.assertTrue(lead.is_converted)
        self.assertEqual(lead.type, 'opportunity')