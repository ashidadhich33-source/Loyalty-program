# -*- coding: utf-8 -*-

from core_framework.testing import TestCase
from core_framework.exceptions import ValidationError


class TestDiscountProgram(TestCase):
    
    def setUp(self):
        super(TestDiscountProgram, self).setUp()
        self.discount_program = self.env['discount.program']
        self.discount_rule = self.env['discount.rule']
        self.discount_coupon = self.env['discount.coupon']
        self.discount_approval = self.env['discount.approval']
        self.discount_campaign = self.env['discount.campaign']
        self.discount_analytics = self.env['discount.analytics']
    
    def test_create_discount_program(self):
        """Test creating a discount program"""
        program = self.discount_program.create({
            'name': 'Test Discount Program',
            'type': 'percentage',
            'description': 'Test discount program',
            'discount_value': 10.0,
            'is_active': True,
        })
        
        self.assertEqual(program.name, 'Test Discount Program')
        self.assertEqual(program.type, 'percentage')
        self.assertEqual(program.discount_value, 10.0)
        self.assertTrue(program.is_active)
    
    def test_discount_program_validation(self):
        """Test discount program validation"""
        with self.assertRaises(ValidationError):
            self.discount_program.create({
                'name': 'Test Program',
                'type': 'percentage',
                'discount_value': -10.0,  # Negative discount value
            })
    
    def test_discount_program_activation(self):
        """Test discount program activation"""
        program = self.discount_program.create({
            'name': 'Test Program',
            'type': 'percentage',
            'discount_value': 10.0,
            'is_active': False,
        })
        
        program.action_activate()
        self.assertTrue(program.is_active)
    
    def test_discount_program_deactivation(self):
        """Test discount program deactivation"""
        program = self.discount_program.create({
            'name': 'Test Program',
            'type': 'percentage',
            'discount_value': 10.0,
            'is_active': True,
        })
        
        program.action_deactivate()
        self.assertFalse(program.is_active)
    
    def test_discount_program_analytics(self):
        """Test discount program analytics"""
        program = self.discount_program.create({
            'name': 'Test Program',
            'type': 'percentage',
            'discount_value': 10.0,
            'is_active': True,
        })
        
        analytics = program.get_analytics()
        self.assertIsInstance(analytics, dict)
        self.assertIn('total_usage', analytics)
        self.assertIn('total_customers', analytics)
        self.assertIn('total_orders', analytics)
        self.assertIn('total_discount_amount', analytics)
        self.assertIn('program_roi', analytics)
    
    def test_discount_program_coupon_generation(self):
        """Test discount program coupon generation"""
        program = self.discount_program.create({
            'name': 'Test Program',
            'type': 'percentage',
            'discount_value': 10.0,
            'is_active': True,
        })
        
        coupons = program.generate_coupons(count=10)
        self.assertEqual(len(coupons), 10)
        self.assertTrue(all(coupon.program_id == program for coupon in coupons))
    
    def test_discount_program_rule_association(self):
        """Test discount program rule association"""
        program = self.discount_program.create({
            'name': 'Test Program',
            'type': 'percentage',
            'discount_value': 10.0,
            'is_active': True,
        })
        
        rule = self.discount_rule.create({
            'name': 'Test Rule',
            'type': 'minimum_amount',
            'description': 'Test rule',
            'condition_value': 100.0,
            'program_id': program.id,
            'is_active': True,
        })
        
        self.assertEqual(rule.program_id, program)
        self.assertIn(rule, program.rule_ids)
    
    def test_discount_program_campaign_association(self):
        """Test discount program campaign association"""
        program = self.discount_program.create({
            'name': 'Test Program',
            'type': 'percentage',
            'discount_value': 10.0,
            'is_active': True,
        })
        
        campaign = self.discount_campaign.create({
            'name': 'Test Campaign',
            'type': 'seasonal',
            'description': 'Test campaign',
            'program_id': program.id,
            'is_active': True,
        })
        
        self.assertEqual(campaign.program_id, program)
        self.assertIn(campaign, program.campaign_ids)
    
    def test_discount_program_approval_workflow(self):
        """Test discount program approval workflow"""
        program = self.discount_program.create({
            'name': 'Test Program',
            'type': 'percentage',
            'discount_value': 10.0,
            'is_active': False,
            'requires_approval': True,
        })
        
        approval = self.discount_approval.create({
            'name': 'Test Approval',
            'type': 'manual',
            'description': 'Test approval',
            'program_id': program.id,
            'status': 'pending',
        })
        
        self.assertEqual(approval.program_id, program)
        self.assertEqual(approval.status, 'pending')
        
        approval.action_approve()
        self.assertEqual(approval.status, 'approved')
        
        program.action_activate()
        self.assertTrue(program.is_active)
    
    def test_discount_program_analytics_generation(self):
        """Test discount program analytics generation"""
        program = self.discount_program.create({
            'name': 'Test Program',
            'type': 'percentage',
            'discount_value': 10.0,
            'is_active': True,
        })
        
        analytics = self.discount_analytics.create({
            'name': 'Test Analytics',
            'program_id': program.id,
            'date': '2024-01-01',
            'period_type': 'daily',
        })
        
        self.assertEqual(analytics.program_id, program)
        self.assertEqual(analytics.period_type, 'daily')
    
    def test_discount_program_performance_metrics(self):
        """Test discount program performance metrics"""
        program = self.discount_program.create({
            'name': 'Test Program',
            'type': 'percentage',
            'discount_value': 10.0,
            'is_active': True,
        })
        
        metrics = program.get_performance_metrics()
        self.assertIsInstance(metrics, dict)
        self.assertIn('total_usage', metrics)
        self.assertIn('total_customers', metrics)
        self.assertIn('total_orders', metrics)
        self.assertIn('total_discount_amount', metrics)
        self.assertIn('program_roi', metrics)
        self.assertIn('cost_per_customer', metrics)
        self.assertIn('revenue_per_customer', metrics)
    
    def test_discount_program_kids_clothing_metrics(self):
        """Test discount program kids clothing specific metrics"""
        program = self.discount_program.create({
            'name': 'Test Program',
            'type': 'percentage',
            'discount_value': 10.0,
            'is_active': True,
        })
        
        metrics = program.get_kids_clothing_metrics()
        self.assertIsInstance(metrics, dict)
        self.assertIn('age_group_breakdown', metrics)
        self.assertIn('gender_breakdown', metrics)
        self.assertIn('seasonal_breakdown', metrics)
        self.assertIn('birthday_discounts', metrics)
        self.assertIn('referral_discounts', metrics)
        self.assertIn('loyalty_discounts', metrics)
        self.assertIn('seasonal_discounts', metrics)